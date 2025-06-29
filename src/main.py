# main.py

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

import json
import os
from src.workflow import CreativeWorkflow
from src.persistence import FileStorage

# Placeholder for LLM. In a real scenario, this would be a proper LLM client.
from openai import OpenAI

class DeepSeekLLM:
    def __init__(self, api_key: str, model: str):
        self.client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com/v1")
        self.model = model

    def generate_text(self, prompt: str) -> str:
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                stream=False
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating text with DeepSeek LLM: {e}")
            return ""

def load_llm_config():
    config_path = os.path.join(os.path.dirname(__file__), '..', '.taskmaster', 'config.json')
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        main_model_config = config.get('models', {}).get('main', {})
        # In a real application, you'd use the provider and modelId to instantiate the correct LLM client
        # For now, we'll just return the config for demonstration
        return main_model_config
    except FileNotFoundError:
        print(f"Error: config.json not found at {config_path}")
        return {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode config.json at {config_path}")
        return {}

llm_config = load_llm_config()
# Here, you would instantiate your actual LLM client based on llm_config
# For now, we'll use a MockLLM
llm = DeepSeekLLM(api_key=os.environ.get("DEEPSEEK_API_KEY"), model=llm_config.get("modelId"))

app = typer.Typer()
console = Console()
storage = FileStorage(base_path="./data")

@app.command()
def start(prompt: str = typer.Argument(..., help="小说的初始创作提示，例如：'一个关于赛博朋克侦探的故事'")):
    """启动多智能体网络小说创作流程。"""
    console.print(Panel(Text("🚀 启动多智能体网络小说创作流程", justify="center", style="bold green"), border_style="green"))
    console.print(f"[bold blue]初始提示:[/bold blue] {prompt}\n")

    workflow = CreativeWorkflow(prompt, storage, llm)
    workflow.start_workflow()

    console.print(Panel(Text("✅ 小说创作流程完成！", justify="center", style="bold green"), border_style="green"))

@app.command()
def status():
    """显示当前小说创作的进度和状态。"""
    console.print(Panel(Text("📊 当前小说创作状态", justify="center", style="bold cyan"), border_style="cyan"))

    # 尝试加载状态以显示最新进度
    story_state_manager = CreativeWorkflow("", storage, llm).story_state_manager # 临时创建，只为获取状态
    story_state_manager.load_state() # 加载最新状态
    current_state = story_state_manager.get_current_state()

    table = Table(title="创作进度概览", style="bold magenta")
    table.add_column("指标", style="cyan", no_wrap=True)
    table.add_column("状态", style="green")

    overall_progress = current_state.get("overall_progress", {})
    table.add_row("大纲已生成", "是" if overall_progress.get("outline_generated") else "否")
    table.add_row("已创作章节数", str(overall_progress.get("chapters_written", 0)))
    table.add_row("总章节数", str(overall_progress.get("total_chapters", 0)))
    table.add_row("当前状态", overall_progress.get("status", "未知"))

    console.print(table)

    # 打印故事元素（简化版）
    story_elements = current_state.get("story_elements", {})
    if story_elements.get("world"):
        console.print(Panel(f"[bold yellow]世界观:[/bold yellow] {story_elements["world"]["name"]} - {story_elements["world"]["description"]}", border_style="yellow"))
    if story_elements.get("characters"):
        char_names = ", ".join(story_elements["characters"].keys())
        console.print(Panel(f"[bold yellow]主要角色:[/bold yellow] {char_names}", border_style="yellow"))

@app.command()
def save():
    """手动保存当前小说创作状态。"""
    console.print(Panel(Text("💾 正在保存当前创作状态...", justify="center", style="bold blue"), border_style="blue"))
    # 临时创建 workflow 实例以访问 story_state_manager
    workflow = CreativeWorkflow("", storage, llm) # prompt 可以为空，因为我们只保存状态
    workflow.story_state_manager.save_state()
    console.print(Panel(Text("✅ 创作状态已保存！", justify="center", style="bold blue"), border_style="blue"))

@app.command()
def load():
    """加载之前保存的小说创作状态。"""
    console.print(Panel(Text("📂 正在加载之前保存的创作状态...", justify="center", style="bold purple"), border_style="purple"))
    # 临时创建 workflow 实例以访问 story_state_manager
    workflow = CreativeWorkflow("", storage, llm) # prompt 可以为空，因为我们只加载状态
    workflow.story_state_manager.load_state()
    console.print(Panel(Text("✅ 创作状态已加载！", justify="center", style="bold purple"), border_style="purple"))

@app.command()
def export(output_filename: str = typer.Argument("novel_output.txt", help="导出小说的文件名，例如：'my_novel.txt'")):
    """将已创作的小说章节导出为单个文本文件。"""
    console.print(Panel(Text("📤 正在导出小说章节...", justify="center", style="bold green"), border_style="green"))

    # 临时创建 workflow 实例以访问 story_state_manager
    workflow = CreativeWorkflow("", storage, llm) # prompt 可以为空，因为我们只加载状态
    workflow.story_state_manager.load_state()
    current_state = workflow.story_state_manager.get_current_state()

    chapters_content = current_state.get("chapters_content", {})

    if not chapters_content:
        console.print(Panel(Text("⚠️ 没有找到已创作的章节内容，无法导出。", justify="center", style="bold yellow"), border_style="yellow"))
        return

    # 按章节索引排序
    sorted_chapters = sorted(chapters_content.items(), key=lambda item: int(item[0]))

    output_path = os.path.join(storage.base_path, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        for chapter_index, content in sorted_chapters:
            f.write(f"\n\n--- Chapter {chapter_index} ---\n\n")
            f.write(content)

    console.print(Panel(Text(f"✅ 小说已成功导出到: [bold blue]{output_path}[/bold blue]", justify="center", style="bold green"), border_style="green"))

if __name__ == "__main__":
    app()
