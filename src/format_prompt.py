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
    def format_deepseek(question: str) -> list[dict]:
        content = question
        return [{"role": "user", "content": content}]

    @staticmethod
    def format_qwen(question: str) -> list[dict]:
        content = f"{question}\n"
        content += (
            "Please reason step by step, and put your final answer within \boxed{}."
        )
        return [{"role": "user", "content": content}]

    def format_olmo(self, question: str) -> list[dict]:
        system_prompt = self._load_system_prompt("OLMO_3")
        content = question
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]

    def format_claude(self, question: str) -> list[dict]:
        # system_prompt = self._load_system_prompt("OLMO_3")
        content = question
        return [
            # {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]

    def format_nemotron(self, question: str) -> list[dict]:
        system_prompt = self._load_system_prompt("NEMOTRON_CASCADE")
        content = question + " /think"
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content},
        ]

    def format_prompt(self, question: str) -> list[dict]:
        model_name = self.model_name.lower()

        if "deepseek" in model_name:
            return self.format_deepseek(question)
        elif "qwen" in model_name:
            return self.format_qwen(question)
        elif "olmo" in model_name:
            return self.format_olmo(question)
        elif "claude" in model_name or "anthropic" in model_name:
            return self.format_claude(question)
        elif "nemotron" in model_name or "nvidia" in model_name:
            return self.format_nemotron(question)
        else:
            raise ValueError(f"Unsupported model: {self.model_name}")
