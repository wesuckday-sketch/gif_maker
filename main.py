import os
from PIL import Image
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QLineEdit, QFileDialog
import sys

class GifMakerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wesuckday's GIF Maker")
        self.setGeometry(100, 100, 400, 200)
        self.folder_path = ""

        layout = QVBoxLayout()

        self.folder_button = QPushButton("Choose Frames Folder")
        self.folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_button)

        self.folder_label = QLabel("No folder selected")
        layout.addWidget(self.folder_label)

        self.output_entry = QLineEdit()
        self.output_entry.setPlaceholderText("Output GIF name (default: animation.gif)")
        layout.addWidget(self.output_entry)

        self.fps_entry = QLineEdit()
        self.fps_entry.setPlaceholderText("Frames per second (default: 10)")
        layout.addWidget(self.fps_entry)

        self.generate_button = QPushButton("Generate GIF")
        self.generate_button.clicked.connect(self.generate_gif)
        layout.addWidget(self.generate_button)

        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Frames Folder")
        if folder_path:
            self.folder_path = folder_path
            self.folder_label.setText(folder_path)
            self.status_label.setText("Folder selected")
            print("Folder selected:", folder_path)

    def generate_gif(self):
        output_name = self.output_entry.text() or "animation.gif"
        fps_text = self.fps_entry.text()
        try:
            fps = int(fps_text) if fps_text else 10
        except ValueError:
            self.status_label.setText("FPS must be a number")
            return

        if not self.folder_path:
            self.status_label.setText("Select a folder first")
            return

        self.status_label.setText("Generating GIF...")
        try:
            frames = []
            for filename in sorted(os.listdir(self.folder_path)):
                if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                    path = os.path.join(self.folder_path, filename)
                    frames.append(Image.open(path).convert("RGBA"))

            if not frames:
                self.status_label.setText("No image files in folder")
                return

            frames[0].save(
                output_name,
                save_all=True,
                append_images=frames[1:],
                duration=int(1000 / fps),
                loop=0
            )

            self.status_label.setText(f"GIF generated: {output_name}")
            print("Output:", output_name)
            print("FPS:", fps)
        except Exception as e:
            self.status_label.setText(f"Error: {e}")
            print("Error generating GIF:", e)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GifMakerApp()
    window.show()
    sys.exit(app.exec())









