import os
from datetime import datetime
import pyperclip
import tkinter as tk
from PIL import ImageGrab,Image,ImageFilter
import io
import time

class ScreenCaptureTool(tk.Tk):
    def __init__(self):
        super().__init__()

        # 더블 클릭 방지를 위한 마지막 클릭 시간 기록
        self.last_click_time = 0
        # 더블 클릭 시간 간격
        self.double_click_threshold = 0.3


        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas = tk.Canvas(self, cursor="cross", bg="white")
        self.canvas.pack(fill="both", expand=True)


        # 창 설정
        self.attributes("-alpha", 0.1)  # 투명도 조절
        self.attributes("-topmost", True)
        # self.overrideredirect(True) 윈도우 매니저 우회하여 창 만들기
        # 창 사이즈 현재 기기의 스크린 사이즈로 설정
        self.geometry(f'{self.winfo_screenwidth()}x{self.winfo_screenheight()+200}')
        # self.attributes("-fullscreen", True)

        # 이벤트 바인딩
        self.canvas.bind("<ButtonPress-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.on_key_press)

    def on_click(self, event):
        # 현재 클릭 시간
        current_click_time = time.time()
        # 현재 클릭 시간과 마지막 클릭한 시간이 더블 클릭 시간 간격보다 클 경우에만 동작
        if (current_click_time - self.last_click_time) > self.double_click_threshold:

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
        self.last_click_time = current_click_time
    def on_drag(self, event):
        self.canvas.coords(
            self.rect,
            self.start_x,
            self.start_y,
            event.x,
            event.y)
    def on_release(self, event):
        # 드래그 방향에 따라 사각형이 만들어지는 위치가 다르기 때문에 min, max 함수 사용
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)
        self.capture_screen(x1, y1, x2, y2)
        self.destroy()
    def on_key_press(self,event):
        print(event.keysym)
        if event.keysym == 'Escape':
            self.destroy()
    def on_esc_keypress(self,event):
        self.destroy()
    def capture_screen(self, x1, y1, x2, y2):
        # 바운딩 박스 좌표
        bbox = (
            self.winfo_rootx() + x1,
            self.winfo_rooty() + y1,
            self.winfo_rootx() + x2,
            self.winfo_rooty() + y2
        )
        # 바운딩 박스 위치의 이미지 자르기
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

    def detect_text(self, path):
        """Detects text in the file."""
        # Google Cloud Vision 사용
        from google.cloud import vision
        client = vision.ImageAnnotatorClient()

        content = Image.open(path)
        if content.mode == 'RGBA':
            content = content.convert('RGB')
        # 이미지 선명도 조정
        sharpened = content.filter(ImageFilter.SHARPEN)
        byte_stream = io.BytesIO()
        sharpened.save(byte_stream, format='JPEG')
        byte_stream.seek(0)

        # google vision에 맞는 이미지 객체 생성
        image = vision.Image(content=byte_stream.read())

        try:
            # 해당 이미지에서 텍스트 추출
            response = client.text_detection(image=image)
            if response.full_text_annotation:
                # 감지된 전체 텍스트
                full_text = response.full_text_annotation.text
                # 클립보드에 복사
                pyperclip.copy(full_text)
                # 캡처된 이미지 삭제
                os.remove(path)
        except Exception as e:
            print("Error detecting text:", e)


        # import easyocr
        # reader = easyocr.Reader(['ko','en'], gpu=False)
        # generated_text = reader.readtext(path)
        # print(generated_text)
