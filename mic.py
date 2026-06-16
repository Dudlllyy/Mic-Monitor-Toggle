import sounddevice as sd
import keyboard
import customtkinter as ctk
import sys

# --- НАСТРОЙКИ ---
INPUT_DEVICE = 9
OUTPUT_DEVICE = 8
BLOCKSIZE = 128
SAMPLE_RATE = 48000
HOTKEY = '0'

is_listening = False


def audio_callback(indata, outdata, frames, time, status):
    # Убрал print(status), чтобы ошибки буфера не забивали память и не вешали программу
    if is_listening:
        outdata[:] = indata
    else:
        outdata.fill(0)


class MicMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Mic Monitor")
        self.geometry("300x150")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")

        self.status_label = ctk.CTkLabel(self, text="Звук ВЫКЛЮЧЕН", font=("Arial", 16, "bold"), text_color="gray")
        self.status_label.pack(pady=(20, 10))

        self.toggle_btn = ctk.CTkButton(self, text=f"Включить (или {HOTKEY.upper()})",
                                        command=self.toggle_state,
                                        fg_color="#1f538d", hover_color="#14375e")
        self.toggle_btn.pack(pady=10)

        # Переменные для защиты от сбоев
        self.hotkey_pressed_before = False
        self.stream = None

        # Запускаем звук
        self.start_stream()

        # Запускаем безопасные циклы проверки (вместо опасных глобальных хуков)
        self.check_hotkey()
        self.check_audio_watchdog()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_stream(self):
        """Безопасный запуск или перезапуск аудиопотока"""
        try:
            if self.stream is not None:
                self.stream.close()

            self.stream = sd.Stream(device=(INPUT_DEVICE, OUTPUT_DEVICE),
                                    channels=1,
                                    samplerate=SAMPLE_RATE,
                                    blocksize=BLOCKSIZE,
                                    latency='low',
                                    callback=audio_callback)
            self.stream.start()
        except Exception as e:
            print(f"Ошибка потока: {e}")

    def toggle_state(self):
        global is_listening
        is_listening = not is_listening

        if is_listening:
            self.status_label.configure(text="Звук ВКЛЮЧЕН", text_color="#2ecc71")
            self.toggle_btn.configure(text=f"Выключить (или {HOTKEY.upper()})", fg_color="#c0392b",
                                      hover_color="#922b21")
        else:
            self.status_label.configure(text="Звук ВЫКЛЮЧЕН", text_color="gray")
            self.toggle_btn.configure(text=f"Включить (или {HOTKEY.upper()})", fg_color="#1f538d",
                                      hover_color="#14375e")

    def check_hotkey(self):
        """Безопасный опрос клавиатуры каждые 50 миллисекунд"""
        try:
            is_pressed = keyboard.is_pressed(HOTKEY)

            # Если кнопка нажата СЕЙЧАС, но не была нажата 50мс назад (защита от залипания)
            if is_pressed and not self.hotkey_pressed_before:
                self.toggle_state()
                self.hotkey_pressed_before = True
            # Если кнопку отпустили
            elif not is_pressed:
                self.hotkey_pressed_before = False
        except:
            pass  # Игнорируем случайные системные ошибки клавиатуры

        # Запускаем эту же функцию снова через 50 мс
        self.after(50, self.check_hotkey)

    def check_audio_watchdog(self):
        """Сторожевой пес: проверяет жив ли звук, каждые 2 секунды"""
        if self.stream is None or not self.stream.active:
            print("Обнаружено падение аудиопотока. Перезапуск...")
            self.start_stream()

        self.after(2000, self.check_audio_watchdog)

    def on_closing(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
        self.destroy()
        sys.exit()


if __name__ == "__main__":
    app = MicMonitorApp()
    app.mainloop()
