# src/story/story_elements.py

from typing import List, Dict, Any

class World:
    def __init__(self, name: str, description: str, rules: List[str]):
        self.name = name
        self.description = description
        self.rules = rules

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "rules": self.rules
        }

class Character:
    def __init__(self, name: str, description: str, personality: List[str], backstory: str):
        self.name = name
        self.description = description
        self.personality = personality
        self.backstory = backstory

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "personality": self.personality,
            "backstory": self.backstory
        }

class Plotline:
    def __init__(self, name: str, summary: str, key_events: List[str]):
        self.name = name
        self.summary = summary
        self.key_events = key_events

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "summary": self.summary,
            "key_events": self.key_events
        }

class StoryElements:
    def __init__(self):
        self.world: World = None
        self.characters: Dict[str, Character] = {}
        self.plotlines: Dict[str, Plotline] = {}

    def add_world(self, world: World):
        self.world = world

    def add_character(self, character: Character):
        self.characters[character.name] = character

    def add_plotline(self, plotline: Plotline):
        self.plotlines[plotline.name] = plotline

    def to_dict(self) -> Dict[str, Any]:
        return {
            "world": self.world.to_dict() if self.world else None,
            "characters": {name: char.to_dict() for name, char in self.characters.items()},
            "plotlines": {name: plot.to_dict() for name, plot in self.plotlines.items()}
        }
