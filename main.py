import requests

# Ссылки на фильтры
urls = [
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_27.txt",
    "https://adguardteam.github.io/AdGuardSDNSFilter/Filters/filter.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_49.txt"
]

# Итоговый файл
output_file = "combined_filter.txt"

# Уникальные правила
unique_rules = set()

for url in urls:
    try:
        # Скачиваем файл
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки
        print(f"Загружен: {url}")

        # Обрабатываем строки
        for line in response.text.splitlines():
            stripped_line = line.strip()
            if stripped_line and not stripped_line.startswith("!"):  # Убираем пустые строки и комментарии
                unique_rules.add(stripped_line)

    except requests.RequestException as e:
        print(f"Ошибка при скачивании {url}: {e}")

# Сохранение итогового файла
with open(output_file, "w", encoding="utf-8") as output:
    output.write("\n".join(sorted(unique_rules)))

print(f"Объединённый фильтр сохранён в {output_file}")