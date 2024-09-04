# 프로젝트 명:
ScreenCaptureTool

# 프로젝트 설명:
이 프로젝트는 그래픽 사용자 인터페이스(GUI)에서 마우스 이벤트를 처리하고 선택한 영역의 스크린샷을 캡처하는 기능을 제공하는 `ScreenCaptureTool` 애플리케이션을 구현합니다. 사용자는 마우스를 통해 원하는 영역을 선택하고, 선택이 완료되면 해당 영역의 스크린샷을 손쉽게 캡처할 수 있습니다. 이 애플리케이션은 텍스트 감지 기능도 포함하고 있어, 캡처된 이미지에서 텍스트를 자동으로 인식하고 출력합니다.

## 기능
1. **마우스 이벤트 처리**:
   - `on_click`: 마우스 클릭 시 시작 좌표(`start_x`, `start_y`)를 초기화합니다. 사각형이 이미 존재하지 않으면 캔버스에 사각형을 생성합니다.
   - `on_drag`: 마우스를 드래그할 때 사각형의 좌표를 업데이트하여 크기를 조정합니다.
   - `on_release`: 마우스 버튼을 놓을 때 사각형의 크기를 확정하고, 경계 상자 좌표를 계산한 후 `capture_screen` 메서드를 호출하여 선택한 영역의 스크린샷을 캡처합니다.
   - `on_key_press` 및 `on_esc_keypress`: 'Escape' 키 입력을 감지하여 애플리케이션을 종료합니다.

2. **스크린샷 캡처**:
   - `capture_screen`: 지정된 경계 상자 영역의 스크린샷을 캡처합니다. 필요 시 이미지를 RGB 형식으로 변환하고, 타임스탬프가 포함된 파일 이름으로 'capture' 디렉토리에 저장한 후, 캡처된 이미지에서 텍스트를 감지하는 메서드를 호출합니다.

3. **텍스트 감지**:
   - `detect_text`: 이미지 파일에서 텍스트를 감지하는 메서드입니다. 초기에는 Google Cloud Vision을 사용하도록 되어 있었으나 주석 처리되어 있으며, 대신 `easyocr` 라이브러리를 사용하여 한국어와 영어 텍스트를 읽습니다. 감지된 텍스트는 콘솔에 출력됩니다.

4. **GUI 설정**:
   - `ScreenCaptureTool` 클래스는 `tk.Tk`를 상속받아 GUI 애플리케이션을 생성합니다. 투명성과 항상 위에 표시되는 속성을 설정하며, 더블 클릭 방지를 위한 클릭 시간 기록 및 더블 클릭 감지를 위한 임계값을 정의합니다.

5. **캔버스 설정**: 사용자 상호작용을 위한 캔버스를 생성하며, 흰색 배경 위에 교차 커서를 사용하여 드로잉 또는 선택을 가능하게 합니다.

6. **이벤트 바인딩**: 캔버스는 마우스 및 키보드 이벤트를 메서드에 바인딩하여 클릭, 드래그 및 마우스 버튼 해제를 처리합니다.

# 설치 방법
1. 이 저장소를 클론합니다:
   ```bash
   git clone https://github.com/yourusername/ScreenCaptureTool.git
   cd ScreenCaptureTool
   ```

2. 필요한 라이브러리를 설치합니다:
   ```bash
   pip install easyocr pillow pyperclip
   ```

# 사용법
1. 애플리케이션을 실행합니다:
   ```bash
   python main.py
   ```

2. 마우스를 사용하여 캔버스에서 선택 영역을 드래그합니다. 선택이 완료되면 마우스 버튼을 놓아 스크린샷을 캡처합니다.

3. 'Escape' 키를 눌러 애플리케이션을 종료합니다.

# 예시
사용자가 캔버스에서 드래그하여 선택한 영역의 스크린샷을 캡처하고, 해당 이미지에서 텍스트를 감지하여 콘솔에 출력하는 과정을 보여주는 예시입니다.

# 프로젝트 파일 구조
```
ScreenCaptureTool/
├── main.py               # 애플리케이션의 메인 실행 파일
├── capture/              # 캡처된 스크린샷을 저장하는 디렉토리
├── requirements.txt      # 프로젝트 의존성 목록
└── README.md             # 프로젝트 설명서
```

# 기여
기여를 원하시는 분은 다음 단계를 따라 주세요:
1. 이 저장소를 포크합니다.
2. 새로운 기능이나 버그 수정을 위한 브랜치를 생성합니다:
   ```bash
   git checkout -b feature/YourFeature
   ```
3. 변경 사항을 커밋합니다:
   ```bash
   git commit -m "Add some feature"
   ```
4. 브랜치에 푸시합니다:
   ```bash
   git push origin feature/YourFeature
   ```
5. Pull Request를 생성합니다.

# 라이센스
이 프로젝트는 MIT 라이센스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

# 프로젝트 문의
추가 질문이나 피드백이 있으시면 언제든지 문의해 주세요! 프로젝트 팀 또는 유지보수자에게 연락하기 위해 [park20542040@gmail.com]를 사용하시거나 GitHub 이슈를 통해 문의하실 수 있습니다.