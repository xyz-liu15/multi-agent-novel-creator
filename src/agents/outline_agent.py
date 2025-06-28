# src/agents/outline_agent.py

from .base_agent import BaseAgent

class OutlineAgent(BaseAgent):
    def __init__(self, name="OutlineAgent"):
        super().__init__(name)

    def execute_task(self, task: dict) -> dict:
        print(f"{self.name} is executing task: {task['description']}")
        # 模拟生成小说大纲的逻辑
        outline = {
            "title": "赛博朋克侦探",
            "logline": "在一个反乌托邦的未来，一名侦探揭露了一场涉及人工智能和企业阴谋的巨大阴谋。",
            "chapters": [
                {"title": "第一章：霓虹之影", "summary": "介绍主角和赛博朋克世界。"},
                {"title": "第二章：数据迷宫", "summary": "侦探开始调查案件。"},
                {"title": "第三章：真相边缘", "summary": "揭露部分阴谋。"}
            ]
        }
        print(f"{self.name} generated outline: {outline['title']}")
        return {"status": "completed", "result": outline}

    def communicate(self, message: dict) -> dict:
        print(f"{self.name} received message: {message['content']}")
        return {"status": "acknowledged", "response": "收到大纲请求。"}
