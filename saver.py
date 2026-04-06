import json
import os
from typing import List, Dict, Any

from config import OUTPUT_FILE


def save_to_json(data: List[Dict[str, Any]], filename: str = OUTPUT_FILE) -> bool:
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
        print(f"📁 Создана папка: {directory}")

    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        print(f"✅ Данные сохранены в {filename}")
        print(f"   Записей: {len(data)}")
        return True

    except Exception as e:
        print(f"❌ Ошибка при сохранении {filename}: {type(e).__name__} - {str(e)}")
        return False


def append_to_json(new_data: List[Dict[str, Any]], filename: str = OUTPUT_FILE) -> bool:
    existing_data = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        except Exception as e:
            print(f"⚠️ Не удалось прочитать {filename}: {e}")

    combined_data = existing_data + new_data
    return save_to_json(combined_data, filename)
