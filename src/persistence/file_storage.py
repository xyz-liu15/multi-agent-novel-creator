# src/persistence/file_storage.py

import os
import json
import logging
from typing import Dict, Any

class FileStorage:
    def __init__(self, base_path: str = "./data"):
        self.base_path = base_path
        # 确保数据存储目录存在
        os.makedirs(self.base_path, exist_ok=True)

    def save_data(self, filename: str, data: Dict[str, Any]):
        """将数据保存为JSON文件。"""
        filepath = os.path.join(self.base_path, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        logging.info(f"[Persistence] Data saved to {filepath}")

    def load_data(self, filename: str) -> Dict[str, Any] or None:
        """从JSON文件加载数据。"""
        filepath = os.path.join(self.base_path, filename)
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            logging.info(f"[Persistence] Data loaded from {filepath}")
            return data
        logging.warning(f"[Persistence] File not found: {filepath}")
        return None
