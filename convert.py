import re
import requests

# Ссылки на блоклист и allowlist
adguard_blocklist_url = "https://raw.githubusercontent.com/JustRomacH/adguard_blocklist/refs/heads/main/combined_filter.txt"
adguard_allowlist_url = "https://raw.githubusercontent.com/JustRomacH/adguard_blocklist/refs/heads/main/combined_whitelist.txt"

# Пути для сохранения файлов
blocklist_output_file = "./lean-blocklist.txt"
allowlist_output_file = "./lean-allowlist.txt"

def download_list(url):
    """Загрузка списка (блоклист или allowlist)"""
    response = requests.get(url)
    return response.text

def parse_adguard_list(adguard_list, is_allowlist=False):
    """Парсинг списка AdGuard и преобразование в формат adblock-lean"""
    # Регулярное выражение для поиска доменов в блоклисте
    domain_pattern = re.compile(r'^\|\|?([a-z0-9\-\.]+\.[a-z]{2,})(?:\^|$)', re.IGNORECASE)

    # Регулярное выражение для allowlist (с учетом @@| и подстановочных символов)
    allowlist_pattern = re.compile(r'^\@\@?\|([a-z0-9\*\-\.\_]+\.[a-z]{2,})(?:\^|$)', re.IGNORECASE)

    # Множество для уникальных доменов
    domains = set()

    for line in adguard_list.splitlines():
        if is_allowlist:
            # Если это allowlist, ищем строку с префиксом @@|
            match = allowlist_pattern.match(line)
        else:
            # Для блоклиста ищем строки с префиксом ||
            match = domain_pattern.match(line)

        if match:
            domain = match.group(1)
            domains.add(domain)

    return domains

def save_to_file(domains, output_path):
    """Сохранение списка доменов в файл"""
    with open(output_path, "w") as f:
        for domain in domains:
            f.write(domain + "\n")
    print(f"Список сохранён в {output_path}")

# Основной процесс
if __name__ == "__main__":
    # Загружаем блоклист и allowlist
    blocklist = download_list(adguard_blocklist_url)
    allowlist = download_list(adguard_allowlist_url)

    # Парсим и извлекаем домены для блоклиста
    blocklist_domains = parse_adguard_list(blocklist)
    save_to_file(blocklist_domains, blocklist_output_file)

    # Парсим и извлекаем домены для allowlist (с учетом префикса @@|)
    allowlist_domains = parse_adguard_list(allowlist, is_allowlist=True)
    save_to_file(allowlist_domains, allowlist_output_file)
