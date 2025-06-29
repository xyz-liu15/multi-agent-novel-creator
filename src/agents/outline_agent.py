# src/agents/outline_agent.py

import json
from .base_agent import BaseAgent

class OutlineAgent(BaseAgent):
    def __init__(self, llm, name="OutlineAgent"):
        super().__init__(name, llm)

    def execute_task(self, task: dict) -> dict:
        print(f"{self.name} is executing task: {task['description']}")
        prompt = task.get("description", "")

        outline_generation_prompt = f"""
        You are a professional novelist and outline creator. Based on the following prompt, generate a detailed novel outline.
        The outline should include:
        - A compelling title for the novel.
        - A concise logline (1-2 sentences).
        - A list of 3-5 chapters, where each chapter has:
            - A chapter title.
            - A brief summary of the chapter's content.

        Ensure the outline is coherent, engaging, and sets up a compelling narrative arc.

        Prompt: {prompt}

        Generate the outline in JSON format, like this:
        {{
            "title": "Novel Title",
            "logline": "A concise logline.",
            "chapters": [
                {{"title": "Chapter 1 Title", "summary": "Chapter 1 Summary."}},
                {{"title": "Chapter 2 Title", "summary": "Chapter 2 Summary."}}
            ]
        }}
        """

        print(f"{self.name}: Generating outline for: {prompt[:50]}...")
        response = self.llm.generate_text(outline_generation_prompt)

        try:
            # Remove markdown code block if present
            if response.startswith('```json') and response.endswith('```'):
                response = response[len('```json'):-len('```')].strip()
            outline = json.loads(response)
            print(f"{self.name} generated outline: {outline.get('title', 'N/A')}")
            return {"status": "completed", "result": outline}
        except json.JSONDecodeError:
            print(f"{self.name}: Failed to decode JSON response for outline: {response}")
            return {"status": "failed", "message": "Failed to generate valid JSON outline."}

    def communicate(self, message: dict) -> dict:
        print(f"{self.name} received message: {message['content']}")
        return {"status": "acknowledged", "response": "收到大纲请求。"}
