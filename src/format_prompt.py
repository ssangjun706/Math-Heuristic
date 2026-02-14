from pathlib import Path
from typing import Optional


class PromptFormatter:
    def __init__(self, model_name: Optional[str] = None) -> None:
        self.model_name = model_name
        self.system_prompt_dir = Path(__file__).parent.parent / "system_prompt"

    def _load_system_prompt(self, filename: str) -> Optional[str]:
        file_path = self.system_prompt_dir / filename
        if file_path.exists():
            return file_path.read_text(encoding="utf-8").strip()
        return None

    @staticmethod
    def format_deepseek(problem: str) -> list[dict]:
        content = problem
        content = f"{problem}\n"
        content += (
            "Please reason step by step, and put your final answer within \boxed{}."
        )
        return [{"role": "user", "content": content}]

    @staticmethod
    def format_qwen(problem: str) -> list[dict]:
        content = f"{problem}\n"
        content += (
            "Please reason step by step, and put your final answer within \boxed{}."
        )
        return [{"role": "user", "content": content}]

    def format_olmo(
        self,
        problem: str,
        has_chat_template: Optional[bool],
    ) -> list[dict]:
        system_prompt = self._load_system_prompt("OLMO_3")
        content = f"{problem}\n"
        content += (
            "Please reason step by step, and put your final answer within \boxed{}."
        )

        if not has_chat_template:
            return content

        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]

    def format_claude(self, problem: str) -> list[dict]:
        # system_prompt = self._load_system_prompt("CLAUDE_SONNET_4.5")
        content = f"{problem}\n"
        content += (
            "Please reason step by step, and put your final answer within \boxed{}."
        )
        return [
            # {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]

    def format_nemotron(self, problem: str) -> list[dict]:
        system_prompt = self._load_system_prompt("NEMOTRON_CASCADE")
        content = f"{problem}\n"
        content += (
            "Please reason step by step, and put your final answer within \boxed{}."
        )
        content += " /think"
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]

    def format_prompt(
        self,
        problem: str,
        has_chat_template: Optional[bool] = True,
    ) -> list[dict]:
        model_name = self.model_name.lower()

        if "deepseek" in model_name:
            return self.format_deepseek(problem)
        elif "qwen" in model_name:
            return self.format_qwen(problem)
        elif "olmo" in model_name:
            return self.format_olmo(problem, has_chat_template=has_chat_template)
        elif "claude" in model_name or "anthropic" in model_name:
            return self.format_claude(problem)
        elif "nemotron" in model_name or "nvidia" in model_name:
            return self.format_nemotron(problem)
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")
