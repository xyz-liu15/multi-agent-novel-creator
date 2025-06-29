[English Version](README.md)

# 多智能体网络小说创作系统

这是一个创新的多智能体网络小说创作系统，旨在通过模拟人类创作团队的协作方式，自动化生成高质量的小说内容。系统从一个简单的用户提示开始，通过智能体之间的分工与协作，逐步完成小说大纲的构建、章节内容的撰写，并支持创作过程的持久化。

## ✨ 主要特性

*   **自动化内容创作**：将复杂的小说创作过程分解为可管理的任务，并由不同的AI智能体协同完成。
*   **提升创作效率**：显著减少人工创作的时间和精力投入，实现快速原型创作和内容迭代。
*   **模块化与可扩展性**：采用清晰的模块化架构，便于引入新的智能体、集成不同的LLM服务或扩展新的创作阶段。
*   **状态管理与恢复**：确保创作过程的连续性，允许用户随时保存、加载和恢复创作进度。

## 🚀 快速开始

### 🛠️ 环境搭建与依赖管理 (使用 `uv`)

本项目推荐使用 `uv` 进行虚拟环境管理和依赖安装，以确保环境的隔离和高效性。

1.  **克隆仓库** (如果你还没有克隆):
    ```bash
    git clone https://github.com/xyz-liu15/multi-agent-novel-creator.git
    cd multi-agent-novel-creator
    ```

2.  **创建并激活虚拟环境** (使用 `uv`)：
    ```bash
    uv venv
    source .venv/bin/activate  # macOS/Linux
    # .venv\\Scripts\\activate   # Windows
    ```

3.  **安装依赖** (使用 `uv add`)：
    本项目核心依赖包括 `typer` 和 `rich`。智能体内部可能还会依赖其他库，例如用于LLM交互的库。
    ```bash
    uv add typer rich
    # 如果你的LLM提供商需要特定的Python库，例如 DeepSeek，你可能还需要安装：
    # uv add deepseek-python # 假设DeepSeek提供了官方Python SDK
    ```
    **注意**：请根据实际使用的LLM提供商和其SDK要求，安装相应的Python包。

### 🔑 API 配置 (以 DeepSeek 为例)

本项目通过环境变量和 `.taskmaster/config.json` 文件来管理LLM的API密钥和模型设置。

1.  **设置 DeepSeek API 密钥环境变量**：
    你需要将你的 DeepSeek API 密钥设置为名为 `DEEPSEEK_API_KEY` 的环境变量。
    *   **Linux/macOS**:
        ```bash
        export DEEPSEEK_API_KEY="你的DeepSeekAPI密钥"
        ```
        为了持久化，请将其添加到你的 shell 配置文件（如 `~/.bashrc`, `~/.zshrc`）中。
    *   **Windows**: 
        通过系统环境变量设置，或在命令行中临时设置。

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

## 📖 使用方法

所有命令都在项目的根目录下执行，并**务必使用虚拟环境中的 Python 解释器**。

1.  **启动小说创作**：
    使用 `start` 命令并提供一个初始提示来开始创作。
    ```bash
    /home/athanx/multi-agent-novel-creator/.venv/bin/python -m src.main start "一个关于赛博朋克侦探的故事，他发现自己被困在一个虚拟现实中。"
    ```
    这将启动多智能体工作流，包括大纲生成和章节创作。创作过程可能需要一些时间，具体取决于提示的复杂度和LLM的响应速度。

2.  **查看创作状态**：
    使用 `status` 命令可以查看当前小说的创作进度和概览。
    ```bash
    /home/athanx/multi-agent-novel-creator/.venv/bin/python -m src.main status
    ```
    这将显示已生成的大纲、已创作章节数、总章节数以及当前状态等信息。

3.  **保存当前创作状态**：
    在创作过程中，你可以随时手动保存当前状态。
    ```bash
    /home/athanx/multi-agent-novel-creator/.venv/bin/python -m src.main save
    ```
    这会将当前的小说状态持久化到 `./data` 目录。

4.  **加载之前保存的状态**：
    如果你中断了创作，或者想从之前的某个检查点继续，可以使用 `load` 命令。
    ```bash
    /home/athanx/multi-agent-novel-creator/.venv/bin/python -m src.main load
    ```
    这将从 `./data` 目录加载最新保存的状态。

## 🏗️ 项目架构

本项目采用分层和模块化的设计，主要由以下核心组件构成：

### 1. **核心工作流 (`src/workflow/creative_workflow.py`)**
这是整个系统的“大脑”，负责编排和驱动小说创作的各个阶段。
*   **`CreativeWorkflow` 类**：
    *   接收初始创作提示。
    *   协调 `OutlineAgent` 和 `ChapterAgent` 的工作。
    *   管理 `StoryStateManager` 以跟踪和更新小说创作的整体进度和内容。
    *   定义了清晰的创作步骤（例如：大纲生成 -> 章节生成）。
    *   在工作流结束时自动保存当前状态。

### 2. **智能体管理 (`src/agent_manager.py`)**
负责智能体的注册、查找和任务分派。
*   **`AgentManager` 类**：
    *   维护一个智能体实例的字典（目前包括 `OutlineAgent` 和 `ChapterAgent`）。
    *   提供 `get_agent` 方法，允许工作流根据名称获取特定的智能体实例。
    *   提供 `dispatch_task` 方法，将具体的任务（如生成大纲、创作章节）委派给相应的智能体执行。

### 3. **智能体 (`src/agents/`)**
每个智能体都扮演着小说创作过程中的特定角色，专注于完成其职责范围内的任务。
*   **`base_agent.py` (`BaseAgent`)**：定义了所有智能体的基类，提供了通用的接口和方法，如 `execute_task` 和 `communicate`。
*   **`outline_agent.py` (`OutlineAgent`)**：
    *   **职责**：根据初始提示生成小说的整体大纲，包括标题、梗概和章节列表（每个章节包含标题和摘要）。
    *   **协作**：将生成的大纲传递给 `CreativeWorkflow`，供后续章节创作使用。
*   **`chapter_agent.py` (`ChapterAgent`)**：
    *   **职责**：根据大纲中每个章节的标题和摘要，创作具体的章节内容。
    *   **协作**：将创作完成的章节内容返回给 `CreativeWorkflow`，由其添加到小说的整体内容中。

### 4. **持久化层 (`src/persistence/file_storage.py`)**
负责系统状态和生成内容的存储与加载。
*   **`FileStorage` 类**：
    *   提供 `save_data` 和 `load_data` 方法，用于将Python对象（如小说状态、大纲、章节内容）序列化为JSON格式并保存到文件系统，或从文件系统加载。
    *   默认将数据存储在项目根目录下的 `./data` 文件夹中。

### 5. **故事状态管理 (`src/story/story_state_manager.py`)**
集中管理小说的所有相关数据和创作进度。
*   **`StoryStateManager` 类**：
    *   存储小说的核心元素（世界观、角色、情节线）。
    *   存储已创作的章节内容。
    *   跟踪整体创作进度（如大纲是否生成、已完成章节数、总章节数）。
    *   通过 `FileStorage` 实现状态的保存和加载。

### 6. **命令行接口 (`src/main.py`)**
用户与系统交互的入口。
*   使用 `typer` 库构建，提供友好的命令行界面。
*   定义了 `start`、`status`、`save`、`load` 等命令，方便用户启动创作、查询进度、管理状态。

### 7. **配置 (`.taskmaster/config.json`)**
包含系统运行时的全局配置，特别是LLM模型的选择和参数。
*   允许用户配置 `main`、`research`、`fallback` 等不同用途的LLM模型，包括提供商、模型ID、最大Token数和温度等。

## 🤝 贡献

欢迎对本项目进行贡献！如果你有任何建议、bug 报告或功能请求，请通过 [Issue](https://github.com/xyz-liu15/multi-agent-novel-creator/issues) 提交。

## 📄 许可证

本项目采用 [MIT License](LICENSE) 许可.