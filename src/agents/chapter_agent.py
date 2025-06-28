# src/agents/chapter_agent.py

from .base_agent import BaseAgent

class ChapterAgent(BaseAgent):
    def __init__(self, name="ChapterAgent"):
        super().__init__(name)

    def execute_task(self, task: dict) -> dict:
        print(f"{self.name} is executing task: {task['description']}")
        chapter_info = task.get("chapter_info", {})
        # 模拟生成章节内容的逻辑
        chapter_content = f"这是关于 {chapter_info.get('title', '未知章节')} 的内容。\n\n{chapter_info.get('summary', '')}"
        print(f"{self.name} generated chapter: {chapter_info.get('title', '未知章节')}")
        return {"status": "completed", "result": chapter_content}

    def communicate(self, message: dict) -> dict:
        print(f"{self.name} received message: {message['content']}")
        return {"status": "acknowledged", "response": "收到章节创作请求。"}

