# 🎙️ Mic Monitor Toggle

A lightweight desktop utility written in Python for monitoring your own microphone with minimal latency. It allows you to toggle voice monitoring on and off using a global hotkey while running in the background.

Perfect for gamers, streamers, and anyone using closed-back headphones who wants to hear their own voice without alt-tabbing from a game. The application is compatible with **Equalizer APO** (uses Shared Mode).

## ✨ Features

* **Global Hotkey:** Toggle the audio on/off with a single key press (default is `F9`) from any window.
* **Minimal Latency:** Uses the `sounddevice` library (built on PortAudio/WASAPI) for fast audio routing.
* **Background Operation:** The audio capture process runs in a separate thread and does not freeze the UI.
* **Modern UI:** Out-of-the-box dark mode interface built with `customtkinter`.
* **Plugin Support:** Correctly captures audio that has already been processed by system equalizers and plugins (e.g., RNNoise, LoudMax via Equalizer APO).

## 🚀 Installation and Usage

### Requirements
* Python 3.8 or higher.
* Windows OS.

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git](https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git)
cd YOUR_REPOSITORY
