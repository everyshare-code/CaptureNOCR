import os
from datetime import datetime
import pyperclip
import tkinter as tk
from PIL import ImageGrab,Image,ImageFilter
import io

class ScreenCaptureTool(tk.Tk):
    def __init__(self):
        super().__init__()

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas = tk.Canvas(self, cursor="cross", bg="white")
        self.canvas.pack(fill="both", expand=True)


        # 창 설정
        self.attributes("-alpha", 0.2)  # 투명도 조절
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()+100}')
        self.attributes("-fullscreen", True)

        # 마우스 이벤트 바인딩
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.canvas.focus_set()
        self.canvas.bind("<Escape>", self.on_esc_keypress)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

        if not self.rect:
            self.rect = self.canvas.create_rectangle(
                self.start_x,
                self.start_y,
                self.start_x,
                self.start_y,
                outline="red",
                width=2)

    def on_drag(self, event):
        self.canvas.coords(
            self.rect,
            self.start_x,
            self.start_y,
            event.x,
            event.y)

    def on_release(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        self.capture_screen(x1, y1, x2, y2)
        self.destroy()

    def on_esc_keypress(self, event):
        self.destroy()
    def capture_screen(self, x1, y1, x2, y2):
        bbox = (
            self.winfo_rootx() + x1,
            self.winfo_rooty() + y1,
            self.winfo_rootx() + x2,
            self.winfo_rooty() + y2
        )
        # bbox = (x1, y1, x2, y2)
        screenshot = ImageGrab.grab(bbox)
        if screenshot.mode == 'RGBA':
            screenshot = screenshot.convert('RGB')
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        capture_path = os.path.join('capture')
        if not os.path.exists(capture_path):
            os.makedirs(capture_path)
        filepath = os.path.join(capture_path, f'{timestamp}.jpg')
        screenshot.save(filepath)
        self.detect_text(filepath)
        # screenshot.save("capture.png")  # 저장할 파일명

    def detect_text(self,path):
        """Detects text in the file."""

        from google.cloud import vision

        client = vision.ImageAnnotatorClient()



        content = Image.open(path)
        if content.mode == 'RGBA':
            content = content.convert('RGB')
        sharpened = content.filter(ImageFilter.SHARPEN)
        byte_stream = io.BytesIO()
        sharpened.save(byte_stream, format='JPEG')
        byte_stream.seek(0)

        image = vision.Image(content=byte_stream.read())

        try:
            response = client.text_detection(image=image)
            if response.full_text_annotation:
                full_text = response.full_text_annotation.text
                print("Full text:", full_text)
                sentences = full_text.split('\n')
                pyperclip.copy('\n'.join(sentences))
                os.remove(path)
        except Exception as e:
            print("Error detecting text:", e)

