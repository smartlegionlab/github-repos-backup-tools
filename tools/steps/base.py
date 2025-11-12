from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseStep(ABC):
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
        self.success = False
        self.result = None

    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> bool:
        pass

    def get_status_icon(self) -> str:
        return "✅" if self.success else "❌"
