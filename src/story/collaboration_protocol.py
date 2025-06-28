# src/story/collaboration_protocol.py

from typing import Dict, Any

class CollaborationProtocol:
    def __init__(self):
        self.shared_context: Dict[str, Any] = {}
        self.conflict_resolution_log: list = []

    def share_information(self, agent_name: str, info_type: str, data: Any):
        """智能体共享信息。"""
        self.shared_context[info_type] = data
        print(f"[Collaboration] {agent_name} shared {info_type}.")

    def get_context(self, info_type: str) -> Any:
        """智能体获取共享上下文。"""
        return self.shared_context.get(info_type)

    def propose_change(self, agent_name: str, change_details: Dict[str, Any]) -> bool:
        """智能体提出修改建议。"""
        print(f"[Collaboration] {agent_name} proposed change: {change_details}")
        # 简单的冲突解决机制：先到先得，或者更复杂的投票/协商机制
        # For now, just log and accept
        self.conflict_resolution_log.append({"agent": agent_name, "change": change_details, "status": "accepted"})
        return True

    def resolve_conflict(self, conflict_details: Dict[str, Any]) -> Dict[str, Any]:
        """解决智能体之间的创作冲突。"""
        print(f"[Collaboration] Resolving conflict: {conflict_details}")
        # 复杂的冲突解决逻辑，例如：
        # 1. 优先级：某些智能体（如大纲智能体）的提议优先级更高。
        # 2. 投票：多个智能体对某个提议进行投票。
        # 3. 协商：智能体之间进行多轮沟通，直到达成一致。
        # For now, a simple placeholder
        self.conflict_resolution_log.append({"conflict": conflict_details, "status": "resolved"})
        return {"resolution": "accepted_one_proposal", "details": conflict_details}
