import json
import os
from datetime import datetime
from typing import Dict, Any

class Storage:
    def __init__(self, file_path: str = "pet_data.json"):
        self.file_path = file_path

    def save(self, data: Dict[str, Any]) -> None:
        """保存数据到文件"""
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load(self) -> Dict[str, Any]:
        """从文件加载数据"""
        if not os.path.exists(self.file_path):
            return {}
        with open(self.file_path, 'r', encoding='utf-8') as f:
            return json.load(f) 