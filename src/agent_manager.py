# src/agent_manager.py

from src.agents import BaseAgent, OutlineAgent, ChapterAgent, CharacterAgent

class AgentManager:
    def __init__(self, llm):
        self.agents = {
            "outline_agent": OutlineAgent(llm=llm),
            "chapter_agent": ChapterAgent(llm=llm),
            "character_agent": CharacterAgent(llm=llm)
        }

    def get_agent(self, agent_name: str) -> BaseAgent:
        return self.agents.get(agent_name)

    def dispatch_task(self, agent_name: str, task: dict) -> dict:
        agent = self.get_agent(agent_name)
        if agent:
            return agent.execute_task(task)
        else:
            return {"status": "error", "message": f"Agent {agent_name} not found."}

    def send_message(self, agent_name: str, message: dict) -> dict:
        agent = self.get_agent(agent_name)
        if agent:
            return agent.communicate(message)
        else:
            return {"status": "error", "message": f"Agent {agent_name} not found."}
