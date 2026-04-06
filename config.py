import os

DEFAULT_TIMEOUT = 10
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:149.0) Gecko/20100101 Firefox/149.0"
HEADERS = {"User-Agent": USER_AGENT}

REQUEST_DELAY = 1.0
MAX_RETRIES = 3
RETRY_BACKOFF = 2.0

TARGET_URLS = [
    "https://httpbin.org/html",
    "https://example.com",
    "https://edition.cnn.com/"
]

DATA_DIR = "data"
LOGS_DIR = "logs"
OUTPUT_FILE = f"{DATA_DIR}/parsed_data.json"
ERROR_LOG = f"{LOGS_DIR}/error.log"

LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"


def validate_config():
    if not TARGET_URLS:
        print("ОШИБКА: Список TARGET_URLS пуст!")
        return False

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print(f"Поскольку папка не была создана, осуществилось создание папки: {DATA_DIR}")

    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)
        print(f"Поскольку папка не была создана, осуществилось создание папки: {LOGS_DIR}")

    print(f"Конфигурация загружена:")
    print(f" - Таймаут {DEFAULT_TIMEOUT} сек")
    print(f" - Задержка {REQUEST_DELAY} сек")
    print(f" - URL для парсинга {len(TARGET_URLS)} шт")

    return True
