import urllib.request
import urllib.parse
import re
import time
import threading
import random
from datetime import datetime

# Словарь городов (английские названия для wttr.in)
CITIES_WTTR = {
    "1. Москва": "Moscow",
    "2. Санкт-Петербург": "Saint+Petersburg",
    "3. Новосибирск": "Novosibirsk",
    "4. Екатеринбург": "Yekaterinburg",
    "5. Казань": "Kazan",
    "6. Нижний Новгород": "Nizhny+Novgorod",
    "7. Челябинск": "Chelyabinsk",
    "8. Омск": "Omsk",
    "9. Самара": "Samara",
    "10. Ростов-на-Дону": "Rostov-na-Donu",
    "11. Уфа": "Ufa",
    "12. Красноярск": "Krasnoyarsk",
    "13. Пермь": "Perm",
    "14. Воронеж": "Voronezh",
    "15. Волгоград": "Volgograd",
}

stop_program = False

def random_user_agent():
    return f"Mozilla/5.0 (Windows NT {random.choice(['10.0', '11.0'])}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.randint(100, 123)}.0.0.0 Safari/537.36"

def get_weather_wttr(city_en):
    """Получение погоды через wttr.in (текстовый формат)"""
    url = f"https://wttr.in/{city_en}?format=%t+%w+%C"
    headers = {'User-Agent': random_user_agent()}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read().decode('utf-8').strip()
        # Пример ответа: "+10°C 5 km/h Clear"
        parts = data.split(maxsplit=2)
        if len(parts) >= 3:
            temp = parts[0].replace('°C', '')
            wind = parts[1]
            desc = parts[2]
            return temp, desc, wind
        else:
            return "?", "?", "?"
    except Exception as e:
        print(f"Ошибка: {e}")
        return "?", "?", "?"

def check_space():
    global stop_program
    try:
        import msvcrt
        while not stop_program:
            if msvcrt.kbhit() and msvcrt.getch() == b' ':
                stop_program = True
                print("\n␣ Программа остановлена")
                break
            time.sleep(0.1)
    except ImportError:
        try:
            import keyboard
            keyboard.wait('space')
            stop_program = True
            print("\n␣ Программа остановлена")
        except ImportError:
            print("Не удалось отследить пробел. Используйте Ctrl+C.")
            input("Нажмите Enter для выхода...")
            stop_program = True

def choose_city():
    print("\nВыберите город:")
    for key in CITIES_WTTR:
        print(f"  {key}")
    while True:
        choice = input("Введите номер (1-15): ").strip()
        for key, city_en in CITIES_WTTR.items():
            if choice == key[0]:
                return key, city_en
        print("Неверный ввод.")

threading.Thread(target=check_space, daemon=True).start()

city_name, city_en = choose_city()
print(f"\n🌤️  ПОГОДА В ГОРОДЕ: {city_name[3:].upper()}")
print("Источник: wttr.in (консольный сервис)")
print("Обновление: каждые 10 секунд")
print("Нажмите ПРОБЕЛ для остановки\n")

try:
    while not stop_program:
        temp, desc, wind = get_weather_wttr(city_en)
        now = datetime.now().strftime('%H:%M:%S')
        if temp != "?":
            print(f"[{now}] 🌡️ {temp}°C | {desc} | 💨 Ветер {wind}")
        else:
            print(f"[{now}] ❌ Не удалось получить данные")
        for _ in range(10):
            if stop_program:
                break
            time.sleep(1)
except KeyboardInterrupt:
    print("\n✅ Остановлено")