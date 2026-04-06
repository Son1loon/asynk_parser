import time
from typing import List, Dict, Any

from config import TARGET_URLS, OUTPUT_FILE
from fetcher import fetch_url
from parser import parse_title
from saver import save_to_json


def main():
    """
    Главная функция парсера.
    Координирует загрузку, парсинг и сохранение данных.
    """
    print("=" * 60)
    print("🚀 АСИНХРОННЫЙ ПАРСЕР (Синхронный прототип)")
    print("=" * 60)
    print(f"📋 Всего URL для обработки: {len(TARGET_URLS)}")
    print(f"💾 Результат будет сохранён в: {OUTPUT_FILE}")
    print("-" * 60)

    # Результаты парсинга
    results: List[Dict[str, Any]] = []

    # Счётчики
    success_count = 0
    error_count = 0

    # Засекаем время начала
    start_time = time.time()

    # Обрабатываем каждый URL
    for i, url in enumerate(TARGET_URLS, 1):
        print(f"\n[{i}/{len(TARGET_URLS)}] Обработка: {url}")

        # Шаг 1: Загружаем HTML
        html = fetch_url(url)

        # Шаг 2: Извлекаем заголовок
        if html:
            title = parse_title(html)
            success_count += 1
            # Обрезаем длинный заголовок для красивого вывода
            display_title = title[:80] + "..." if len(title) > 80 else title
            print(f"   📝 Заголовок: {display_title}")
        else:
            title = "Error: failed to fetch"
            error_count += 1
            print(f"   ❌ Ошибка загрузки")

        # Шаг 3: Сохраняем результат
        results.append({
            "url": url,
            "title": title,
            "status": "success" if html else "error"
        })

    # Подсчитываем время выполнения
    elapsed_time = time.time() - start_time

    print("\n" + "=" * 60)
    print("📊 СТАТИСТИКА")
    print("=" * 60)
    print(f"✅ Успешно загружено: {success_count}")
    print(f"❌ Ошибок загрузки: {error_count}")
    print(f"📦 Всего обработано: {len(results)}")
    print(f"⏱️ Время выполнения: {elapsed_time:.2f} секунд")

    # Сохраняем результаты
    print("\n💾 Сохранение результатов...")
    if save_to_json(results, OUTPUT_FILE):
        print("🎉 Парсинг завершён успешно!")
    else:
        print("⚠️ Парсинг завершён, но НЕ УДАЛОСЬ сохранить результаты!")

    print("=" * 60)


if __name__ == "__main__":
    main()
