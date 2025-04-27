import re
import requests

# Ссылки на фильтры
urls = [
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_1.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_59.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_49.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_27.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_3.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_33.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_24.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_53.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_4.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_34.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_48.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_51.txt",
    "https://adguardteam.github.io/HostlistsRegistry/assets/filter_5.txt"
]

output_file = "combined_filter.txt"

# Множество нормализованных правил
unique_rules = set()

# Регулярки для разбора
HOSTS_RE = re.compile(r'^(?:0\.0\.0\.0|127\.0\.0\.1)\s+([^\s#]+)')
ADGUARD_RE = re.compile(r'^\|{1,2}([^\/\^*]+)')  # поймает ||domain или |domain
PLAIN_DOMAIN_RE = re.compile(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

def normalize_rule(line: str) -> str | None:
    """
    Приводит правило к виду ||domain^
    Возвращает None, если правило не является фильтрующим домен.
    """
    # 1) hosts-style: "0.0.0.0 domain"
    m = HOSTS_RE.match(line)
    if m:
        domain = m.group(1).lower()
        return f'||{domain}^'

    # 2) AdGuard-style с || или |
    m = ADGUARD_RE.match(line)
    if m:
        domain = m.group(1).lower()
        return f'||{domain}^'

    # 3) просто домен без префикса
    stripped = line.lower()
    if PLAIN_DOMAIN_RE.match(stripped):
        return f'||{stripped}^'

    # 4) всё остальное — не обрабатываем, возвращаем исходник, чтобы сохранить особые правила
    return line

for url in urls:
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        print(f"Загружен: {url}")
    except requests.RequestException as e:
        print(f"Ошибка при скачивании {url}: {e}")
        continue

    for raw in resp.text.splitlines():
        line = raw.strip()
        # пропускаем пустые и комментарии
        if not line or line.startswith('!') or line.startswith('#'):
            continue

        norm = normalize_rule(line)
        if norm:
            unique_rules.add(norm)

# Сохраняем результат
with open(output_file, 'w', encoding='utf-8') as fw:
    for rule in sorted(unique_rules):
        fw.write(rule + '\n')

print(f"Объединённый и нормализованный фильтр сохранён в {output_file}")
