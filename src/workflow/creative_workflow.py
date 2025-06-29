# src/workflow/creative_workflow.py

from src.agent_manager import AgentManager
from src.story import StoryStateManager, CollaborationProtocol
from src.workflow.task_queue import TaskQueue
from src.persistence import FileStorage
from typing import Dict, Any

class CreativeWorkflow:
    def __init__(self, initial_prompt: str, storage: FileStorage, llm):
        self.agent_manager = AgentManager(llm)
        self.story_state_manager = StoryStateManager(storage)
        self.collaboration_protocol = CollaborationProtocol()
        self.task_queue = TaskQueue()
        self.initial_prompt = initial_prompt
        self.storage = storage

    def start_workflow(self):
        print(f"\n--- Starting Creative Workflow with prompt: '{self.initial_prompt}' ---")

        # Step 1: Outline Generation
        print("\n[Workflow] Step 1: Outline Generation")
        outline_task = {"name": "Generate Novel Outline", "description": f"根据提示 '{self.initial_prompt}' 生成小说大纲"}
        self.task_queue.add_task({"agent": "outline_agent", "task": outline_task})

        while not self.task_queue.is_empty():
            current_job = self.task_queue.get_next_task()
            if not current_job: continue

            agent_name = current_job["agent"]
            task_details = current_job["task"]

            agent = self.agent_manager.get_agent(agent_name)
            if agent:
                result = agent.execute_task(task_details)
                if result["status"] == "completed":
                    if agent_name == "outline_agent":
                        outline = result["result"]
                        self.story_state_manager.update_progress("outline_generated", True)
                        self.story_state_manager.set_total_chapters(len(outline["chapters"]))
                        self.collaboration_protocol.share_information("OutlineAgent", "novel_outline", outline)
                        print("[Workflow] Outline generated.")

                        # Step 2: Character Generation
                        print("\n[Workflow] Step 2: Character Generation")
                        character_task = {"name": "Generate Novel Characters", "prompt": self.initial_prompt, "outline": outline}
                        self.task_queue.add_task({"agent": "character_agent", "task": character_task})

                        print("[Workflow] Proceeding to Character Generation.")

                        # Step 3: Chapter Generation (add tasks to queue)
                        print("\n[Workflow] Step 3: Chapter Generation")
                        for i, chapter_info in enumerate(outline["chapters"]):
                            chapter_task = {"name": f"Write Chapter {i+1}", "description": f"创作章节: {chapter_info['title']}", "chapter_info": chapter_info}
                            self.task_queue.add_task({"agent": "chapter_agent", "task": chapter_task})

                    elif agent_name == "character_agent":
                        characters = result["result"]
                        self.story_state_manager.update_elements({"characters": characters})
                        print(f"[Workflow] Generated {len(characters)} characters. Proceeding to Chapter Generation.")

                        # Now, re-add chapter generation tasks, potentially with character context
                        outline = self.collaboration_protocol.get_information("novel_outline")
                        if outline:
                            print("\n[Workflow] Resuming Chapter Generation with Character Context")
                            for i, chapter_info in enumerate(outline["chapters"]):
                                chapter_task = {"name": f"Write Chapter {i+1}", "description": f"创作章节: {chapter_info['title']}", "chapter_info": chapter_info, "characters": characters}
                                self.task_queue.add_task({"agent": "chapter_agent", "task": chapter_task})
                        else:
                            print("[Workflow] Error: Outline not found for chapter generation after character generation.")

                    elif agent_name == "chapter_agent":
                        chapter_content = result["result"]
                        chapter_info = task_details["chapter_info"]
                        chapter_index = self.story_state_manager.overall_progress["chapters_written"] + 1 # Simple increment
                        self.story_state_manager.add_chapter_content(chapter_index, chapter_content)
                        print(f"[Workflow] Chapter '{chapter_info['title']}' written.")

                else:
                    print(f"[Workflow] Task failed for {agent_name}: {result['message']}")
            else:
                print(f"[Workflow] Agent {agent_name} not found.")

        print("\n--- Creative Workflow Completed ---")
        print("Final Story State:", self.story_state_manager.get_current_state())
        self.story_state_manager.save_state() # Save state at the end of workflow