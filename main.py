import os
import threading
import subprocess
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock

# Папка для скачивания (в Android это папка Download)
DOWNLOAD_DIR = '/storage/emulated/0/Download'

class MusicApp(App):
    def build(self):
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        title = Label(text="Мой Плейлист", size_hint=(1, 0.1), font_size='20sp', color=(1, 1, 1, 1))
        layout.add_widget(title)

        self.status_label = Label(text="Готов к работе", size_hint=(1, 0.15), font_size='13sp', color=(0.8, 0.8, 0.8, 1))
        layout.add_widget(self.status_label)

        self.scroll = ScrollView(size_hint=(1, 0.45))
        self.song_list = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.song_list.bind(minimum_height=self.song_list.setter('height'))
        self.scroll.add_widget(self.song_list)
        layout.add_widget(self.scroll)

        btn_load = Button(text="Загрузить TXT", size_hint=(1, 0.15), background_color=(0.2, 0.6, 1, 1))
        btn_load.bind(on_press=self.load_file)
        layout.add_widget(btn_load)
        
        self.btn_more = Button(text="Загрузить еще", size_hint=(1, 0.15), background_color=(0.2, 0.8, 0.2, 1), disabled=True)
        self.btn_more.bind(on_press=self.load_more)
        layout.add_widget(self.btn_more)
        
        self.all_lines = []
        self.current_index = 0
        self.chunk_size = 50
        return layout

    def load_file(self, instance):
        # Ищем файл в папке Загрузки
        file_path = '/storage/emulated/0/Download/playlist.txt'
        self.song_list.clear_widgets()
        self.current_index = 0
        self.all_lines = []
        
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    self.all_lines = [line.strip() for line in f.readlines() if line.strip()]
                
                if len(self.all_lines) > 0:
                    self.load_more(None)
                    self.btn_more.disabled = False
                    self.status_label.text = "Список загружен"
            else:
                self.song_list.add_widget(Label(text="Файл playlist.txt не найден в Download", color=(1, 0, 0, 1)))
        except Exception as e:
            self.song_list.add_widget(Label(text=f"ОШИБКА: {str(e)}", color=(1, 0, 0, 1)))

    def load_more(self, instance):
        next_chunk = self.all_lines[self.current_index : self.current_index + self.chunk_size]
        
        for song in next_chunk:
            btn = Button(text=song, size_hint_y=None, height=50, background_color=(0.3, 0.3, 0.3, 1), font_size='14sp')
            btn.bind(on_press=lambda instance, s=song: self.play_song(s))
            self.song_list.add_widget(btn)
            
        self.current_index += len(next_chunk)
        if self.current_index >= len(self.all_lines):
            self.btn_more.disabled = True
            self.btn_more.text = "Это все песни"

    def play_song(self, song_name):
        self.status_label.text = f"Ищу: {song_name}..."
        
        # 1. Ищем локально в папке Download
        found_file = None
        if os.path.exists(DOWNLOAD_DIR):
            for filename in os.listdir(DOWNLOAD_DIR):
                if filename.lower().endswith(('.mp3', '.m4a')) and song_name.lower() in filename.lower():
                    found_file = os.path.join(DOWNLOAD_DIR, filename)
                    break

        if found_file:
            self.play_local_file(found_file)
        else:
            self.status_label.text = f"Скачивание: {song_name}..."
            # 2. Если нет локально — качаем в фоне
            threading.Thread(target=self.download_song, args=(song_name,)).start()

    def play_local_file(self, file_path):
        try:
            # В Android запускаем системный плеер
            subprocess.run(['am', 'start', '-a', 'android.intent.action.VIEW', '-d', f'file://{file_path}', '-t', 'audio/mp3'], check=True)
            self.status_label.text = f"Играет: {os.path.basename(file_path)}"
        except Exception as e:
            self.status_label.text = f"Ошибка плеера: {e}"

    def download_song(self, song_name):
        try:
            import yt_dlp
            
            safe_name = "".join(c for c in song_name if c.isalnum() or c in ' ._-').strip()
            output_template = os.path.join(DOWNLOAD_DIR, f"{safe_name}.%(ext)s")
            
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': output_template,
                'quiet': True,
                'no_warnings': True,
                'noplaylist': True,
                'nocheckcertificate': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.extract_info(f"ytsearch1:{song_name} audio", download=True)
                
                for f in os.listdir(DOWNLOAD_DIR):
                    if f.startswith(safe_name) and f.endswith('.mp3'):
                        file_path = os.path.join(DOWNLOAD_DIR, f)
                        Clock.schedule_once(lambda dt: self.play_local_file(file_path), 0)
                        return
                        
        except Exception as e:
            err_text = str(e)[:100].replace('\n', ' ')
            Clock.schedule_once(lambda dt: setattr(self.status_label, 'text', f"Ошибка: {err_text}"), 0)

if __name__ == '__main__':
    MusicApp().run()
