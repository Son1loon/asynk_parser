import time

import requests
from requests.exceptions import (Timeout, ConnectionError, HTTPError, TooManyRedirects)

from config import (DEFAULT_TIMEOUT, HEADERS, MAX_RETRIES, RETRY_BACKOFF)


def is_retryable_status(status_code):
    if status_code in [500, 502, 503, 504]:
        return True
    if status_code == 429:
        return True
    return False


def fetch_url(url, retry_count=MAX_RETRIES):
    try:
        print(f"[INFO] Загружаем: {url} (осталось попыток: {retry_count})")

        response = requests.get(
            url,
            timeout=DEFAULT_TIMEOUT,
            headers=HEADERS
        )

        response.raise_for_status()

        print(f"[OK] Успешно загружена: {url}")
        return response.text

    except Timeout:
        print(f"[TIMEOUT] Сайт {url} не отвечает. Попыток осталось: {retry_count - 1}")

        if retry_count > 1:
            delay = RETRY_BACKOFF * (MAX_RETRIES - retry_count + 1)
            print(f"[RETRY] Повтор через {delay} секунд...")
            time.sleep(delay)
            return fetch_url(url, retry_count - 1)
        else:
            print(f"[FAIL] Не удалось загрузить {url} после всех попыток (Timeout)")
            return None

    except ConnectionError:
        print(f"[CONNECTION ERROR] Не могу подключиться к {url}")

        if retry_count > 1:
            delay = RETRY_BACKOFF * (MAX_RETRIES - retry_count + 1)
            print(f"[RETRY] Повтор через {delay} секунд...")
            time.sleep(delay)
            return fetch_url(url, retry_count - 1)
        else:
            print(f"[FAIL] Не удалось загрузить {url} после всех попыток (ConnectionError)")
            return None

    except TooManyRedirects:
        print(f"[REDIRECT ERROR] Слишком много редиректов на {url}")
        print(f"[FAIL] Пропускаем этот URL (повторять бесполезно)")
        return None

    except HTTPError as e:
        status_code = e.response.status_code
        print(f"[HTTP ERROR] {url} вернул статус {status_code}")

        if is_retryable_status(status_code) and retry_count > 1:
            delay = RETRY_BACKOFF * (MAX_RETRIES - retry_count + 1)
            print(f"[RETRY] Ошибка сервера, повтор через {delay} секунд...")
            time.sleep(delay)
            return fetch_url(url, retry_count - 1)
        else:
            if not is_retryable_status(status_code):
                print(f"[FAIL] Ошибка клиента (статус {status_code}), повторять бессмысленно")
            else:
                print(f"[FAIL] Не удалось загрузить {url} после всех попыток")
            return None

    except Exception as e:
        print(f"[UNEXPECTED ERROR] {url}: {type(e).__name__} - {str(e)}")
        print(f"[FAIL] Неизвестная ошибка, пропускаем")
        return None


if __name__ == "__main__":
    print("=" * 50)
    print("Тестирование fetcher.py")
    print("=" * 50)

    test_url = "https://httpbin.org/html"
    print(f"\n[TEST 1] Загрузка: {test_url}")
    result = fetch_url(test_url)

    if result:
        print(f"УСПЕХ! Длина HTML: {len(result)} символов")
        print(f"Первые 200 символов:\n{result[:200]}")
    else:
        print("ПРОВАЛ")

    bad_url = "https://this-site-definitely-does-not-exist-12345.com"
    print(f"\n[TEST 2] Загрузка: {bad_url}")
    result = fetch_url(bad_url)

    if result:
        print("НЕОЖИДАННЫЙ УСПЕХ (должен быть None)")
    else:
        print("ОЖИДАЕМЫЙ ПРОВАЛ (вернул None)")

    print("\n" + "=" * 50)
    print("Тестирование завершено")
