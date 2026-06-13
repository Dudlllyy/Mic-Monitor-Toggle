import sounddevice as sd
import keyboard
import customtkinter as ctk
import sys

# --- НАСТРОЙКИ ---
INPUT_DEVICE = 9  # Твой Fifine Microphone
OUTPUT_DEVICE = 8  # Твои Динамики
BLOCKSIZE = 128
SAMPLE_RATE = 48000
HOTKEY = '0'

# Глобальная переменная состояния
is_listening = False


def audio_callback(indata, outdata, frames, time, status):
    if is_listening:
        outdata[:] = indata
    else:
        outdata.fill(0)


class MicMonitorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройки окна
        self.title("Mic Monitor")
        self.geometry("300x150")
        self.resizable(False, False)
        ctk.set_appearance_mode("dark")  # Темная тема

        # Текст со статусом
        self.status_label = ctk.CTkLabel(self, text="Звук ВЫКЛЮЧЕН", font=("Arial", 16, "bold"), text_color="gray")
        self.status_label.pack(pady=(20, 10))

        # Кнопка включения/выключения
        self.toggle_btn = ctk.CTkButton(self, text=f"Включить (или {HOTKEY.upper()})",
                                        command=self.toggle_state,
                                        fg_color="#1f538d", hover_color="#14375e")
        self.toggle_btn.pack(pady=10)

        # Привязка горячей клавиши (lambda вызывает смену состояния)
        keyboard.add_hotkey(HOTKEY, lambda: self.after(0, self.toggle_state))

        # Запуск аудиопотока в фоновом режиме
        self.stream = sd.Stream(device=(INPUT_DEVICE, OUTPUT_DEVICE),
                                channels=1,
                                samplerate=SAMPLE_RATE,
                                blocksize=BLOCKSIZE,
                                latency='low',
                                callback=audio_callback)
        self.stream.start()

        # Правильное закрытие программы
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def toggle_state(self):
        global is_listening
        is_listening = not is_listening

        # Обновляем интерфейс
        if is_listening:
            self.status_label.configure(text="Звук ВКЛЮЧЕН", text_color="#2ecc71")
            self.toggle_btn.configure(text=f"Выключить (или {HOTKEY.upper()})", fg_color="#c0392b",
                                      hover_color="#922b21")
        else:
            self.status_label.configure(text="Звук ВЫКЛЮЧЕН", text_color="gray")
            self.toggle_btn.configure(text=f"Включить (или {HOTKEY.upper()})", fg_color="#1f538d",
                                      hover_color="#14375e")

    def on_closing(self):
        # Останавливаем звук и закрываем окно
        self.stream.stop()
        self.stream.close()
        self.destroy()
        sys.exit()


if __name__ == "__main__":
    app = MicMonitorApp()
    app.mainloop()