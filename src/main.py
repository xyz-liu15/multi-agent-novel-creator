# main.py

import typer
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table

import json
import os
import logging

from src.workflow import CreativeWorkflow
from src.persistence import FileStorage

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Placeholder for LLM. In a real scenario, this would be a proper LLM client.
from src.llm_client import LLMClientFactory

llm_config = load_llm_config()
llm = LLMClientFactory(llm_config)

app = typer.Typer()
console = Console()
storage = FileStorage(base_path="./data")

@app.command()
def start(prompt: str = typer.Argument(..., help="小说的初始创作提示，例如：'一个关于赛博朋克侦探的故事'")):
    """启动多智能体网络小说创作流程。"""
    logging.info("🚀 启动多智能体网络小说创作流程")
    logging.info(f"初始提示: {prompt}")

    workflow = CreativeWorkflow(prompt, storage, llm)
    workflow.start_workflow()

    logging.info("✅ 小说创作流程完成！")

@app.command()
def status():
    """显示当前小说创作的进度和状态。"""
    logging.info("📊 当前小说创作状态")

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

    logging.info(console.export_text(table))

    # 打印故事元素（简化版）
    story_elements = current_state.get("story_elements", {})
    if story_elements.get("world"):
        logging.info(f"世界观: {story_elements["world"]["name"]} - {story_elements["world"]["description"]}")
    if story_elements.get("characters"):
        char_names = ", ".join(story_elements["characters"].keys())
        logging.info(f"主要角色: {char_names}")

@app.command()
def save():
    """手动保存当前小说创作状态。"""
    logging.info("💾 正在保存当前创作状态...")
    # 临时创建 workflow 实例以访问 story_state_manager
    workflow = CreativeWorkflow("", storage, llm) # prompt 可以为空，因为我们只保存状态
    workflow.story_state_manager.save_state()
    logging.info("✅ 创作状态已保存！")

@app.command()
def load():
    """加载之前保存的小说创作状态。"""
    logging.info("📂 正在加载之前保存的创作状态...")
    # 临时创建 workflow 实例以访问 story_state_manager
    workflow = CreativeWorkflow("", storage, llm) # prompt 可以为空，因为我们只加载状态
    workflow.story_state_manager.load_state()
    logging.info("✅ 创作状态已加载！")

@app.command()
def export(output_filename: str = typer.Argument("novel_output.txt", help="导出小说的文件名，例如：'my_novel.txt'")):
    """将已创作的小说章节导出为单个文本文件。"""
    logging.info("📤 正在导出小说章节...")

    # 临时创建 workflow 实例以访问 story_state_manager
    workflow = CreativeWorkflow("", storage, llm) # prompt 可以为空，因为我们只加载状态
    workflow.story_state_manager.load_state()
    current_state = workflow.story_state_manager.get_current_state()

    chapters_content = current_state.get("chapters_content", {})

    if not chapters_content:
        logging.warning("⚠️ 没有找到已创作的章节内容，无法导出。")
        return

    # 按章节索引排序
    sorted_chapters = sorted(chapters_content.items(), key=lambda item: int(item[0]))

    output_path = os.path.join(storage.base_path, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        for chapter_index, content in sorted_chapters:
            f.write(f"\n\n--- Chapter {chapter_index} ---\n\n")
            f.write(content)

    logging.info(f"✅ 小说已成功导出到: {output_path}")

if __name__ == "__main__":
    app()
