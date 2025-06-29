[中文版本](README_zh.md)

# Multi-Agent Web Novel Creation System

This is an innovative multi-agent web novel creation system designed to automate the generation of high-quality novel content by simulating the collaborative approach of a human creative team. The system starts with a simple user prompt, and through the division of labor and collaboration among agents, it gradually completes the construction of the novel outline, the writing of chapter content, and supports the persistence of the creative process.

## ✨ Features

*   **Automated Content Creation**: Decompose the complex novel creation process into manageable tasks, which are then collaboratively completed by different AI agents, resulting in plot-coherent, engaging, and character-driven novel chapters.
*   **Improved Creation Efficiency**: Significantly reduce the time and effort required for manual creation, enabling rapid prototyping and content iteration.
*   **Modular and Extensible Architecture**: Adopt a clear modular design, facilitating the introduction of new agents, integration of different LLM services, or expansion of new creative stages.
*   **State Management and Recovery**: Ensure the continuity of the creative process, allowing users to save, load, and resume creative progress at any time.

## 🚀 Getting Started

### 🛠️ Environment Setup and Dependency Management (Using `uv`)

This project recommends using `uv` for virtual environment management and dependency installation to ensure environment isolation and efficiency.

1.  **Clone the Repository** (if you haven't already):
    ```bash
    git clone https://github.com/xyz-liu15/multi-agent-novel-creator.git
    cd multi-agent-novel-creator
    ```

2.  **Create and Activate Virtual Environment** (using `uv`):
    ```bash
    uv venv
    source .venv/bin/activate  # macOS/Linux
    # .venv\\Scripts\\activate   # Windows
    ```

3.  **Install Dependencies** (using `uv add`):
    The core dependencies of this project include `typer` and `rich`. Agents may also depend on other libraries, such as those for LLM interaction.
    ```bash
    uv add typer rich
    # If your LLM provider requires specific Python libraries, e.g., DeepSeek, you might also need to install:
    # uv add deepseek-python # Assuming DeepSeek provides an official Python SDK
    ```
    **Note**: Please install the appropriate Python packages based on the LLM provider you are using and its SDK requirements.

### 🔑 API Configuration (Example: DeepSeek)

This project manages LLM API keys and model settings through environment variables and the `.taskmaster/config.json` file.

1.  **Set DeepSeek API Key Environment Variable**:
    You need to set your DeepSeek API key as an environment variable named `DEEPSEEK_API_KEY`.
    *   **Linux/macOS**:
        ```bash
        export DEEPSEEK_API_KEY="YourDeepSeekAPIKey"
        ```
        To persist it, add it to your shell configuration file (e.g., `~/.bashrc`, `~/.zshrc`).
    *   **Windows**:
        Set via system environment variables, or temporarily in the command line.

2.  **Modify `.taskmaster/config.json` File**:
    Open the `.taskmaster/config.json` file in the project root. You need to modify the `provider` and `modelId` in the `models.main` section to the corresponding DeepSeek configuration.

    Find the following section:
    ```json
    "main": {
      "provider": "anthropic",
      "modelId": "claude-3-7-sonnet-20250219",
      "maxTokens": 120000,
      "temperature": 0.2
    }
    ```
    Modify it to (please adjust according to DeepSeek's actual model name, `deepseek-chat` is a common example):
    ```json
    "main": {
      "provider": "deepseek",
      "modelId": "deepseek-chat",
      "maxTokens": 120000,
      "temperature": 0.2
    }
    ```
    Parameters like `maxTokens` and `temperature` can be adjusted according to DeepSeek model characteristics and your needs.

## 📖 Usage

All commands are executed from the project root directory, and **it is crucial to use the Python interpreter from the virtual environment**.

1.  **Start Novel Creation**:
    Use the `start` command and provide an initial prompt to begin creation.
    ```bash
    /home/athanx/multi-agent-novel-creator/.venv/bin/python -m src.main start "A story about a cyberpunk detective who finds himself trapped in a virtual reality."
    ```
    This will initiate the multi-agent workflow, including outline generation and chapter creation. The creation process may take some time, depending on the complexity of the prompt and the LLM's response speed.

2.  **View Creation Status**:
    Use the `status` command to view the current novel's creation progress and overview.
    ```bash
    /home/athanx/multi-agent-novel-creator/.venv/bin/python -m src.main status
    ```
    This will display information such as the generated outline, number of chapters created, total chapters, and current status.

3.  **Save Current Creation State**:
    You can manually save the current state at any time during the creation process.
    ```bash
    /home/athanx/multi-agent-novel-creator/.venv/bin/python -m src.main save
    ```
    This will persist the current novel state to the `./data` directory.

4.  **Load Previously Saved State**:
    If you interrupted creation, or want to continue from a previous checkpoint, you can use the `load` command.
    ```bash
    /home/athanx/multi-agent-novel-creator/.venv/bin/python -m src.main load
    ```
    This will load the latest saved state from the `./data` directory.

5.  **Export Novel to a File**:
    After chapters are generated, you can export the complete novel content to a single text file.
    ```bash
    /home/athanx/multi-agent-novel-creator/.venv/bin/python -m src.main export [output_filename.txt]
    ```
    The `output_filename.txt` is optional; if not provided, it defaults to `novel_output.txt`. The file will be saved in the `./data` directory.

## 🏗️ Project Architecture

This project adopts a layered and modular design, mainly composed of the following core components:

### 1. **Core Workflow (`src/workflow/creative_workflow.py`)**
This is the "brain" of the entire system, responsible for orchestrating and driving various stages of novel creation.
*   **`CreativeWorkflow` Class**:
    *   Receives initial creative prompts.
    *   Coordinates the work of `OutlineAgent` and `ChapterAgent`.
    *   Manages `StoryStateManager` to track and update the overall progress and content of novel creation.
    *   Defines clear creative steps (e.g., Outline Generation -> Chapter Generation).
    *   Automatically saves the current state at the end of the workflow.

### 2. **Agent Management (`src/agent_manager.py`)**
Responsible for agent registration, lookup, and task dispatch.
*   **`AgentManager` Class**:
    *   Maintains a dictionary of agent instances (currently including `OutlineAgent` and `ChapterAgent`).
    *   Provides a `get_agent` method, allowing the workflow to retrieve specific agent instances by name.
    *   Provides a `dispatch_task` method to delegate specific tasks (e.g., generating outlines, writing chapters) to the corresponding agents for execution.

### 3. **Agents (`src/agents/`)**
Each agent plays a specific role in the novel creation process, focusing on completing tasks within its scope of responsibility.
*   **`base_agent.py` (`BaseAgent`)**: Defines the base class for all agents, providing common interfaces and methods, such as `execute_task` and `communicate`.
*   **`outline_agent.py` (`OutlineAgent`)**:
    *   **Responsibilities**: Generates the overall outline of the novel based on the initial prompt, including title, synopsis, and a list of chapters (each chapter containing a title and summary).
    *   **Collaboration**: Passes the generated outline to `CreativeWorkflow`, for subsequent chapter creation.
*   **`character_agent.py` (`CharacterAgent`)**:
    *   **Responsibilities**: Generates detailed character profiles (name, personality, background, role, unique traits) based on the story prompt and outline.
    *   **Collaboration**: Provides character data to `CreativeWorkflow` and `StoryStateManager` for consistency across chapters.
*   **`chapter_agent.py` (`ChapterAgent`)**:
    *   **Responsibilities**: Writes specific chapter content based on the title and summary of each chapter in the outline, now also leveraging generated character information.
    *   **Collaboration**: Returns the completed chapter content to `CreativeWorkflow`, which adds it to the overall content of the novel.

### 4. **Persistence Layer (`src/persistence/file_storage.py`)**
Responsible for storing and loading system state and generated content.
*   **`FileStorage` Class**:
    *   Provides `save_data` and `load_data` methods for serializing Python objects (e.g., novel state, outline, chapter content) into JSON format and saving them to the file system, or loading them from the file system.
    *   By default, data is stored in the `./data` folder at the project root.

### 5. **Story State Management (`src/story/story_state_manager.py`)**
Centralizes the management of all novel-related data and creative progress.
*   **`StoryStateManager` Class**:
    *   Stores core elements of the novel (worldview, characters, plotlines).
    *   Stores created chapter content.
    *   Tracks overall creative progress (e.g., whether the outline is generated, number of chapters completed, total chapters).
    *   Implements state saving and loading via `FileStorage`.

### 6. **Command Line Interface (`src/main.py`)**
The entry point for user interaction with the system.
*   Built using the `typer` library, providing a user-friendly command-line interface.
*   Defines commands suchs as `start`, `status`, `save`, `load`, making it convenient for users to initiate creation, query progress, and manage state.

### 7. **Configuration (`.taskmaster/config.json`)**
Contains global configurations for system runtime, especially LLM model selection and parameters.
*   Allows users to configure different LLM models for `main`, `research`, `fallback`, etc., including provider, model ID, max tokens, and temperature.

## 🤝 Contributing

Contributions to this project are welcome! If you have any suggestions, bug reports, or feature requests, please submit them via [Issues](https://github.com/xyz-liu15/multi-agent-novel-creator/issues).

## 📄 License

This project is licensed under the [MIT License](LICENSE).