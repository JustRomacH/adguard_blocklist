import requests

# Ссылки на фильтры
urls = [
    "https://raw.githubusercontent.com/hl2guide/AdGuard-Home-Whitelist/main/whitelist.txt",
    "https://raw.githubusercontent.com/anudeepND/whitelist/master/domains/whitelist.txt"# Simple DNS Filtering Whitelist
]


# Итоговый файл
output_file = "combined_whitelist.txt"

# Уникальные правила
unique_rules = set()

for url in urls:
    try:
        # Скачиваем файл
        response = requests.get(url)  # Проверка на ошибки
        if response.status_code != 200: continue
        print(f"Загружен: {url}")

        # Обрабатываем строки
        for line in response.text.splitlines():
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith("!") and not stripped_line.startswith("#"):  # Убираем пустые строки и комментарии
                unique_rules.add(stripped_line)

    except requests.RequestException as e:
        print(f"Ошибка при скачивании {url}: {e}")

# Сохранение итогового файла
with open(output_file, "w", encoding="utf-8") as output:
    output.write("\n".join(sorted(unique_rules)))

print(f"Объединённый фильтр сохранён в {output_file}")