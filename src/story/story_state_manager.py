# src/story/story_state_manager.py

from typing import Dict, Any
from .story_elements import StoryElements
from src.persistence import FileStorage

class StoryStateManager:
    def __init__(self, storage: FileStorage):
        self.current_story_elements = StoryElements()
        self.chapters_content: Dict[int, str] = {}
        self.current_chapter_index = 0
        self.overall_progress: Dict[str, Any] = {
            "outline_generated": False,
            "chapters_written": 0,
            "total_chapters": 0,
            "status": "initialized"
        }
        self.storage = storage

    def update_elements(self, new_elements: Dict[str, Any]):
        # This method would parse and update story elements based on agent output
        # For now, a simple placeholder
        if "world" in new_elements:
            # Assuming new_elements['world'] is a dict that can be used to create a World object
            pass # Implement actual parsing and updating
        if "characters" in new_elements:
            pass # Implement actual parsing and updating
        if "plotlines" in new_elements:
            pass # Implement actual parsing and updating

    def add_chapter_content(self, chapter_index: int, content: str):
        self.chapters_content[chapter_index] = content
        self.overall_progress["chapters_written"] = len(self.chapters_content)

    def set_total_chapters(self, count: int):
        self.overall_progress["total_chapters"] = count

    def update_progress(self, key: str, value: Any):
        self.overall_progress[key] = value

    def get_current_state(self) -> Dict[str, Any]:
        return {
            "story_elements": self.current_story_elements.to_dict(),
            "chapters_content": self.chapters_content,
            "current_chapter_index": self.current_chapter_index,
            "overall_progress": self.overall_progress
        }

    def save_state(self, filename: str = "story_state.json"):
        state_to_save = self.get_current_state()
        self.storage.save_data(filename, state_to_save)

    def load_state(self, filename: str = "story_state.json"):
        loaded_state = self.storage.load_data(filename)
        if loaded_state:
            # Reconstruct state from loaded data
            self.current_story_elements = StoryElements() # Needs proper reconstruction from dict
            # For simplicity, directly assign for now
            if loaded_state.get("story_elements") and loaded_state["story_elements"].get("world"):
                world_data = loaded_state["story_elements"]["world"]
                self.current_story_elements.add_world(World(world_data["name"], world_data["description"], world_data["rules"]))
            # ... similarly for characters and plotlines

            self.chapters_content = loaded_state.get("chapters_content", {})
            self.current_chapter_index = loaded_state.get("current_chapter_index", 0)
            self.overall_progress = loaded_state.get("overall_progress", {})
            print("[Persistence] Story state loaded.")
        else:
            print("[Persistence] No saved state found to load.")