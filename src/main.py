# main.py

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

from src.workflow import CreativeWorkflow
from src.persistence import FileStorage

app = typer.Typer()
console = Console()
storage = FileStorage(base_path="./data")

@app.command()
def start(prompt: str = typer.Argument(..., help="小说的初始创作提示，例如：'一个关于赛博朋克侦探的故事'")):
    """启动多智能体网络小说创作流程。"""
    console.print(Panel(Text("🚀 启动多智能体网络小说创作流程", justify="center", style="bold green"), border_style="green"))
    console.print(f"[bold blue]初始提示:[/bold blue] {prompt}\n")

    workflow = CreativeWorkflow(prompt, storage)
    workflow.start_workflow()

    console.print(Panel(Text("✅ 小说创作流程完成！", justify="center", style="bold green"), border_style="green"))

@app.command()
def status():
    """显示当前小说创作的进度和状态。"""
    console.print(Panel(Text("📊 当前小说创作状态", justify="center", style="bold cyan"), border_style="cyan"))

    # 尝试加载状态以显示最新进度
    story_state_manager = CreativeWorkflow("", storage).story_state_manager # 临时创建，只为获取状态
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
    workflow = CreativeWorkflow("", storage) # prompt 可以为空，因为我们只保存状态
    workflow.story_state_manager.save_state()
    console.print(Panel(Text("✅ 创作状态已保存！", justify="center", style="bold blue"), border_style="blue"))

@app.command()
def load():
    """加载之前保存的小说创作状态。"""
    console.print(Panel(Text("📂 正在加载之前保存的创作状态...", justify="center", style="bold purple"), border_style="purple"))
    # 临时创建 workflow 实例以访问 story_state_manager
    workflow = CreativeWorkflow("", storage) # prompt 可以为空，因为我们只加载状态
    workflow.story_state_manager.load_state()
    console.print(Panel(Text("✅ 创作状态已加载！", justify="center", style="bold purple"), border_style="purple"))

if __name__ == "__main__":
    app()
