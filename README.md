# 多智能体网络小说创作项目

这是一个基于多智能体协作的命令行工具，旨在自动化网络小说的创作过程。通过定义不同的智能体角色（如大纲智能体、章节智能体），项目能够从一个简单的提示开始，逐步生成完整的小说内容。

## 🚀 特性

*   **智能大纲生成**：根据初始提示自动生成小说大纲。
*   **章节内容创作**：基于大纲逐章生成详细的小说内容。
*   **进度跟踪**：实时查看小说创作的进度和状态。
*   **状态保存与加载**：支持保存和加载创作过程中的状态，方便中断和恢复。
*   **可配置的LLM后端**：支持通过配置文件切换不同的LLM服务提供商（如DeepSeek, Anthropic等）。

## 🏗️ 项目架构

项目采用模块化设计，主要组件包括：

*   **`src/main.py`**：
    *   项目的命令行接口（CLI）入口。
    *   使用 `typer` 库处理命令行参数和命令。
    *   负责启动 `CreativeWorkflow`，并提供 `start`、`status`、`save`、`load` 等核心命令。

*   **`src/agent_manager.py`**：
    *   智能体管理器，负责注册和管理项目中使用的各种智能体。
    *   提供 `get_agent` 方法来获取特定智能体实例。
    *   负责将任务分派给相应的智能体执行。

*   **`src/agents/`**：
    *   存放不同智能体角色的定义。
    *   `base_agent.py`：定义了所有智能体的基类，包含通用的方法和属性。
    *   `outline_agent.py`：负责生成小说的大纲。
    *   `chapter_agent.py`：负责根据大纲创作小说的具体章节内容。

*   **`src/workflow/`**：
    *   定义了小说的创作流程。
    *   `creative_workflow.py`：核心工作流类，编排智能体之间的协作，驱动小说从大纲到章节的生成。
    *   `task_queue.py`：可能用于管理和调度智能体任务的队列（如果项目有实现）。

*   **`src/persistence/`**：
    *   处理项目数据的持久化。
    *   `file_storage.py`：负责将小说状态、大纲、章节等数据保存到本地文件系统，并从文件系统加载数据。

*   **`src/story/`**：
    *   定义了小说的核心元素和状态管理。
    *   `story_elements.py`：定义了小说中的各种元素，如世界观、角色、情节等。
    *   `story_state_manager.py`：管理小说的整体创作状态，包括当前进度、已完成章节、待办任务等。

*   **`.taskmaster/`**：
    *   项目配置和任务管理目录。
    *   `config.json`：包含LLM模型配置、日志级别等全局设置。
    *   `tasks/tasks.json`：可能用于存储任务管理相关的数据。

## 🛠️ 环境搭建

在运行项目之前，请确保你的系统已安装 Python 3.9 或更高版本。

1.  **克隆仓库** (如果你还没有克隆):
    ```bash
    git clone <你的仓库地址>
    cd multi-agent-novel-creator
    ```

2.  **创建并激活虚拟环境** (推荐):
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # macOS/Linux
    # .venv\Scripts\activate   # Windows
    ```

3.  **安装依赖**：
    ```bash
    pip install -r requirements.txt # 假设存在requirements.txt，如果不存在，请根据src/main.py和src/agent_manager.py中的import手动安装typer, rich等
    ```
    **注意**：如果 `requirements.txt` 文件不存在，你需要根据 `src/main.py` 和 `src/agent_manager.py` 中的 `import` 语句手动安装所需的库，例如：
    ```bash
    pip install typer rich
    ```
    项目内部的智能体可能还会依赖其他库，例如用于LLM交互的库（如 `anthropic`, `deepseek-python` 等）。请检查 `src/agents/` 目录下的文件，确保所有必要的依赖都已安装。

## 🔑 API 配置 (使用 DeepSeek API)

本项目通过配置文件和环境变量来管理LLM的API密钥和模型设置。

1.  **设置 DeepSeek API 密钥环境变量**：
    你需要将你的 DeepSeek API 密钥设置为名为 `DEEPSEEK_API_KEY` 的环境变量。

    *   **Linux/macOS**:
        在终端中运行（仅对当前会话有效）：
        ```bash
        export DEEPSEEK_API_KEY="你的DeepSeekAPI密钥"
        ```
        为了持久化，你可以将这行添加到你的 `~/.bashrc`, `~/.zshrc` 或 `~/.profile` 文件中，然后运行 `source ~/.bashrc` (或对应文件) 使其生效。

    *   **Windows (Command Prompt)**:
        ```cmd
        set DEEPSEEK_API_KEY="你的DeepSeekAPI密钥"
        ```
        为了持久化，你可以通过系统环境变量设置。

    *   **Windows (PowerShell)**:
        ```powershell
        $env:DEEPSEEK_API_KEY="你的DeepSeekAPI密钥"
        ```
        为了持久化，你可以通过系统环境变量设置。

2.  **修改 `.taskmaster/config.json` 文件**：
    打开项目根目录下的 `.taskmaster/config.json` 文件。你需要将 `models.main` 部分的 `provider` 和 `modelId` 修改为 DeepSeek 的相应配置。

    找到以下部分：
    ```json
    "main": {
      "provider": "anthropic",
      "modelId": "claude-3-7-sonnet-20250219",
      "maxTokens": 120000,
      "temperature": 0.2
    }
    ```
    将其修改为（请根据DeepSeek的实际模型名称进行调整，`deepseek-chat` 是一个常见示例）：
    ```json
    "main": {
      "provider": "deepseek",
      "modelId": "deepseek-chat",
      "maxTokens": 120000,
      "temperature": 0.2
    }
    ```
    `maxTokens` 和 `temperature` 等参数可以根据 DeepSeek 模型的特性和你的需求进行调整。

## 🚀 使用方法

所有命令都在项目的根目录下执行。

1.  **启动小说创作**：
    使用 `start` 命令并提供一个初始提示来开始创作。
    ```bash
    python src/main.py start "一个关于赛博朋克侦探的故事，他发现自己被困在一个虚拟现实中。"
    ```
    这将启动多智能体工作流，包括大纲生成和章节创作。创作过程可能需要一些时间，具体取决于提示的复杂度和LLM的响应速度。

2.  **查看创作状态**：
    使用 `status` 命令可以查看当前小说的创作进度和概览。
    ```bash
    python src/main.py status
    ```
    这将显示已生成的大纲、已创作章节数、总章节数以及当前状态等信息。

3.  **保存当前创作状态**：
    在创作过程中，你可以随时手动保存当前状态。
    ```bash
    python src/main.py save
    ```
    这会将当前的小说状态持久化到 `./data` 目录（由 `FileStorage` 配置）。

4.  **加载之前保存的状态**：
    如果你中断了创作，或者想从之前的某个检查点继续，可以使用 `load` 命令。
    ```bash
    python src/main.py load
    ```
    这将从 `./data` 目录加载最新保存的状态。

## 🤝 贡献

欢迎对本项目进行贡献！如果你有任何建议、bug 报告或功能请求，请通过 Issue 提交。

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可。
