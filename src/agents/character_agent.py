from src.agents.base_agent import BaseAgent
from src.story.story_elements import Character
from typing import List, Dict, Any
import json

class CharacterAgent(BaseAgent):
    def __init__(self, llm):
        super().__init__("CharacterAgent", llm)

    def execute_task(self, task: Dict[str, Any]) -> List[Character]:
        prompt = task.get("prompt", "")
        outline = task.get("outline", {})

        chapters_list = [f'- Chapter {i+1}: {c.get("title", "N/A")} - {c.get("summary", "N/A")}' for i, c in enumerate(outline.get('chapters', []))]
        chapters_str = '\n'.join(chapters_list)

        # Construct a detailed prompt for character generation
        character_generation_prompt = f"""
        Based on the following story prompt and outline, generate a list of detailed character profiles.
        For each character, include:
        - name
        - personality traits (3-5 adjectives)
        - brief background story (2-3 sentences)
        - key role in the story
        - any unique physical traits or quirks

        Story Prompt: {prompt}

        Story Outline:
        Title: {outline.get('title', 'N/A')}
        Synopsis: {outline.get('synopsis', 'N/A')}
        Chapters:
        {chapters_str}

        Generate characters in a JSON array format, like this:
        [
            {{
                "name": "Character Name 1",
                "personality": ["trait1", "trait2"],
                "background": "Background story.",
                "role": "Key role.",
                "unique_traits": "Unique traits."
            }},
            {{
                "name": "Character Name 2",
                "personality": ["trait1", "trait2"],
                "background": "Background story.",
                "role": "Key role.",
                "unique_traits": "Unique traits."
            }}
        ]
        """

        print(f"CharacterAgent: Generating characters for prompt: {prompt[:50]}...")
        response = self.llm.generate_text(character_generation_prompt)
        
        try:
            characters_data = json.loads(response)
            characters = [Character(**data) for data in characters_data]
            print(f"CharacterAgent: Generated {len(characters)} characters.")
            return {"status": "completed", "result": characters}
        except json.JSONDecodeError:
            print(f"CharacterAgent: Failed to decode JSON response for characters: {response}")
            return {"status": "failed", "message": f"Failed to decode JSON response for characters: {response}"}
        except TypeError as e:
            print(f"CharacterAgent: Type error when creating Character objects: {e} - Response: {response}")
            return {"status": "failed", "message": f"Type error when creating Character objects: {e} - Response: {response}"}

    def communicate(self, message: dict) -> dict:
        print(f"{self.name} received message: {message['content']}")
        return {"status": "acknowledged", "response": "收到角色信息。"}