"""vLLM server management utilities."""

import atexit
import subprocess
import time
from urllib.parse import urlparse

import requests


def check_server_health(url: str, timeout: int = 300) -> bool:
    """Check if the vLLM server is ready."""
    parsed_url = urlparse(url)
    base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
    health_url = f"{base_url}/health"

    print(f"Waiting for server at {base_url} to be ready...")
    start_time = time.time()

    while time.time() - start_time < timeout:
        try:
            response = requests.get(health_url, timeout=2)
            if response.status_code == 200:
                print(f"Server is ready!")
                return True
        except requests.exceptions.RequestException:
            pass
        time.sleep(2)

    print(f"Server did not become ready within {timeout} seconds.")
    return False


def start_vllm_server(
    model_name: str,
    host: str = "0.0.0.0",
    port: int = 65001,
    vllm_args: dict = None,
) -> subprocess.Popen:
    """Start a vLLM server in the background."""
    cmd = [
        "vllm",
        "serve",
        model_name,
        "--host",
        host,
        "--port",
        str(port),
    ]

    if vllm_args:
        for key, value in vllm_args.items():
            cmd.append(f"--{key}")
            if value is not None and value is not True:
                cmd.append(str(value))

    print(f"Starting vLLM server: {' '.join(cmd)}")
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )

    return process


def setup_local_vllm(
    model_name: str, api_base_url: str, vllm_args: dict = None
) -> subprocess.Popen:
    """Setup and start a local vLLM server with health check and cleanup."""
    parsed_url = urlparse(api_base_url)
    host = parsed_url.hostname or "0.0.0.0"
    port = parsed_url.port or 65001

    vllm_process = start_vllm_server(
        model_name=model_name,
        host=host,
        port=port,
        vllm_args=vllm_args,
    )

    # Register cleanup function
    def cleanup():
        if vllm_process and vllm_process.poll() is None:
            print("\nShutting down vLLM server...")
            vllm_process.terminate()
            try:
                vllm_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                vllm_process.kill()

    atexit.register(cleanup)

    # Wait for server to be ready
    if not check_server_health(api_base_url):
        cleanup()
        raise RuntimeError("Failed to start vLLM server")

    return vllm_process
