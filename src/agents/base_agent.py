# src/agents/base_agent.py

from abc import ABC, abstractmethod

class BaseAgent(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def execute_task(self, task: dict) -> dict:
        """执行特定任务的抽象方法。"""
        pass

    @abstractmethod
    def communicate(self, message: dict) -> dict:
        """与其他智能体通信的抽象方法。"""
        pass
