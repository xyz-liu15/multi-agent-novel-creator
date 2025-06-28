# Multi-Agent Novel Creator

## Project Overview

The Multi-Agent Novel Creator is an innovative project designed to leverage the power of multiple AI agents to collaboratively generate and write novels. This system orchestrates various specialized agents, each contributing to different aspects of the storytelling process, from outlining and character development to chapter generation and plot progression.

## Main Purpose

The primary goal of this project is to automate and enhance the creative writing process by:
-   **Collaborative Storytelling:** Enabling different AI agents to work together, simulating a team of writers.
-   **Structured Novel Generation:** Providing a framework for generating novels chapter by chapter, ensuring coherence and continuity.
-   **Modular Design:** Allowing for easy integration of new agent types and workflow enhancements.
-   **State Management:** Persisting the novel's progress and state, allowing for iterative development and recovery.

## Features

*   **Modular Agent System:** Specialized agents for different creative tasks (e.g., outlining, chapter writing).
*   **Collaborative Protocol:** Agents communicate and collaborate to build the story.
*   **Persistent Story State:** The novel's progress is saved and managed, allowing for seamless continuation.
*   **Configurable Workflow:** Define and manage the creative process through a structured workflow.
*   **Extensible Architecture:** Easily add new agents, story elements, or workflow steps.

## Project Architecture

The project is structured to promote modularity and clear separation of concerns:

```
multi-agent-novel-creator/
├───.taskmaster/             # Task management and project configuration
├───data/                    # Stores persistent data, e.g., story_state.json
├───src/
│   ├───agent_manager.py     # Manages the lifecycle and interaction of AI agents
│   ├───main.py              # Main entry point for the application
│   ├───agents/              # Contains definitions for various AI agents
│   │   ├───base_agent.py    # Base class for all agents
│   │   ├───chapter_agent.py # Agent responsible for writing chapters
│   │   └───outline_agent.py # Agent responsible for generating story outlines
│   ├───persistence/         # Handles data storage and retrieval
│   │   └───file_storage.py  # Manages reading from and writing to files
│   ├───story/               # Core logic for story creation and management
│   │   ├───collaboration_protocol.py # Defines how agents interact and share information
│   │   ├───story_elements.py         # Defines data structures for story components (characters, plot points, etc.)
│   │   └───story_state_manager.py    # Manages the overall state and progression of the novel
│   └───workflow/            # Defines the creative process and task execution
│       ├───creative_workflow.py      # Orchestrates the sequence of creative tasks
│       └───task_queue.py             # Manages tasks for agents to process
└───pyproject.toml           # Project dependencies and metadata (managed by uv)
```

## Getting Started

### Prerequisites

*   Python 3.9+
*   **`uv`**: A fast Python package installer and resolver. It is highly recommended for managing this project's dependencies due to its speed and efficiency. You can install it via `pip install uv`.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/multi-agent-novel-creator.git
    cd multi-agent-novel-creator
    ```

2.  **Install dependencies using `uv`:**
    ```bash
    uv sync
    ```
    This command will create a virtual environment and install all necessary dependencies as defined in `pyproject.toml`.

### Usage

To start generating a novel, run the main application script using `uv`:

```bash
uv run python src/main.py
```

This command ensures that the project is run within the virtual environment managed by `uv`. The application will then guide you through the novel creation process, leveraging the configured AI agents. The novel's progress, including generated outlines, characters, and chapter content, is persistently saved in `data/story_state.json`. This file is updated throughout the process to reflect the ongoing progress of the novel. You can inspect the current state of the novel at any time by viewing this JSON file, or by running the `uv run python src/main.py status` command for a summarized overview.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

[Specify your license here, e.g., MIT, Apache 2.0, etc.]