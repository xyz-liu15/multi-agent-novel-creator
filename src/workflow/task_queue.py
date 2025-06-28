# src/workflow/task_queue.py

from collections import deque
from typing import Dict, Any

class TaskQueue:
    def __init__(self):
        self.queue = deque()

    def add_task(self, task: Dict[str, Any]):
        """添加一个任务到队列。"""
        self.queue.append(task)
        print(f"[TaskQueue] Added task: {task.get('name', 'Unnamed Task')}")

    def get_next_task(self) -> Dict[str, Any] or None:
        """获取并移除队列中的下一个任务。"""
        if self.queue:
            task = self.queue.popleft()
            print(f"[TaskQueue] Retrieved task: {task.get('name', 'Unnamed Task')}")
            return task
        return None

    def is_empty(self) -> bool:
        """检查任务队列是否为空。"""
        return len(self.queue) == 0

    def size(self) -> int:
        """返回任务队列中的任务数量。"""
        return len(self.queue)
