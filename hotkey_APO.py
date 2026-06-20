import shutil
import os
import time
import keyboard


CONFIG_DIR = r"E:\Eqalizer APO\config"
ACTIVE_FILE = os.path.join(CONFIG_DIR, "config.txt")
FLAT_FILE = os.path.join(CONFIG_DIR, "flat.txt")


current_effect = None


def activate_effect(preset_name):
    global current_effect

    try:

        if current_effect == preset_name:
            if not os.path.exists(FLAT_FILE):
                print(f"Ошибка: Чистый файл {FLAT_FILE} не найден!")
                return
            shutil.copyfile(FLAT_FILE, ACTIVE_FILE)
            current_effect = None
            print("--- ALL Eff OFF  ---")
            return


        effect_path = os.path.join(CONFIG_DIR, preset_name)
        if not os.path.exists(effect_path):
            print(f"Ошибка: Файл пресета {preset_name} не найден!")
            return

        shutil.copyfile(effect_path, ACTIVE_FILE)
        current_effect = preset_name
        print(f"+++ Eff ON: {preset_name} +++")

    except PermissionError:
        print("Ошибка доступа! Запустите скрипт от имени Администратора.")
    except Exception as e:
        print(f"Что-то пошло не так: {e}")


def main():
    print("Мульти-переключатель запущен!")
    print("Alt+1 -> ON/OFF 123.txt")
    print("Alt+2 -> ON/OFF 213.txt")
    print("Alt+2 -> ON/OFF 3333.txt")
    print("Alt+2 -> ON/OFF 4444.txt")
    print("Alt+3 -> ON/OFF autotune.txt")
    print("Alt+0 -> ALL OFF")


    keyboard.add_hotkey("alt+1", activate_effect, args=["123.txt"])
    keyboard.add_hotkey("alt+2", activate_effect, args=["213.txt"])
    keyboard.add_hotkey("alt+3", activate_effect, args=["avtotun.txt"])
    keyboard.add_hotkey("alt+4", activate_effect, args=["3333.txt"])
    keyboard.add_hotkey("alt+5", activate_effect, args=["4444.txt"])


    keyboard.add_hotkey("alt+0", activate_effect, args=["flat.txt"])

    while True:
        time.sleep(1)


if __name__ == "__main__":
    main()
