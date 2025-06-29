# src/agents/chapter_agent.py

import logging
from .base_agent import BaseAgent

class ChapterAgent(BaseAgent):
    def __init__(self, llm, name="ChapterAgent"):
        super().__init__(name, llm)

    def execute_task(self, task: dict) -> dict:
        logging.info(f"{self.name} is executing task: {task['description']}")
        chapter_info = task.get("chapter_info", {})
        characters = task.get("characters", [])

        chapter_title = chapter_info.get("title", "")
        chapter_summary = chapter_info.get("summary", "")

        character_details = "\n".join([
            f"- Name: {c.name}, Personality: {', '.join(c.personality)}, Background: {c.background}, Role: {c.role}, Unique Traits: {c.unique_traits}"
            for c in characters
        ])

        prompt = f"""
        You are a professional novelist. Write an engaging and coherent chapter based on the following information.

        Chapter Title: {chapter_title}
        Chapter Summary: {chapter_summary}

        Characters involved in the story:
        {character_details}

        Ensure the chapter:
        - Follows the given title and summary.
        - Integrates the provided characters naturally, reflecting their personalities and roles.
        - Advances the plot in an interesting way.
        - Is well-written, with vivid descriptions and compelling dialogue.
        - Is approximately 800-1200 words long.

        Begin writing the chapter now.
        """

        logging.info(f"{self.name}: Generating content for chapter: {chapter_title}")
        chapter_content = self.llm.generate_text(prompt)

        if chapter_content:
            logging.info(f"{self.name} generated chapter: {chapter_title}")
            return {"status": "completed", "result": chapter_content}
        else:
            logging.error(f"{self.name} failed to generate content for chapter: {chapter_title}")
            return {"status": "failed", "message": "Failed to generate chapter content."}

    def communicate(self, message: dict) -> dict:
        logging.info(f"{self.name} received message: {message['content']}")
        return {"status": "acknowledged", "response": "收到章节创作请求。"}

