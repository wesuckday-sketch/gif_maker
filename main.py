import os
import sys
from PIL import Image
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

class GifMakerApp(QWidget):
    #User Interface Setup
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wesuckday's GIF Maker")
        self.setGeometry(100, 100, 400, 200)
        self.folder_path = ""

        self.frame_list = QListWidget()
        self.frame_list.setViewMode(QListWidget.ListMode)
        self.frame_list.setIconSize(QSize(72, 72))
        self.frame_list.setResizeMode(QListWidget.Adjust)
        self.frame_list.setMovement(QListWidget.Free)
        self.frame_list.setDragDropMode(QListWidget.InternalMove)
        self.frame_list.setSpacing(4)
        self.frame_list.setSelectionMode(QListWidget.SingleSelection)
        self.frame_list.model().rowsMoved.connect(self.refresh_frame_labels)

        layout = QVBoxLayout()

        self.folder_button = QPushButton("Choose Frames Folder")
        self.folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_button)

        self.folder_label = QLabel("No folder selected")
        layout.addWidget(self.folder_label)

        self.frame_hint = QLabel("Load a folder to preview frames. Drag items to reorder the numbered stack before generating.")
        self.frame_hint.setWordWrap(True)
        layout.addWidget(self.frame_hint)

        layout.addWidget(self.frame_list)

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

    #Folder Selection and GIF Generation Logic
    def select_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Frames Folder")
        if folder_path:
            self.folder_path = folder_path
            self.folder_label.setText(folder_path)
            self.status_label.setText("Folder selected")
            self.load_frames_from_folder(folder_path)
            print("Folder selected:", folder_path)

    #Loads frames from the selected folder and populates the list widget with thumbnails and filenames. 
    #It also updates the status label to indicate how many frames were loaded or if no image files were found.
    def load_frames_from_folder(self, folder_path):
        self.frame_list.clear()
        allowed_extensions = (".png", ".jpg", ".jpeg", ".bmp", ".gif")

        for filename in sorted(os.listdir(folder_path)):
            if filename.lower().endswith(allowed_extensions):
                path = os.path.join(folder_path, filename)
                self.add_frame(path)

        self.refresh_frame_labels()

        if self.frame_list.count() == 0:
            self.status_label.setText("No image files in folder")
        else:
            self.status_label.setText(f"Loaded {self.frame_list.count()} frames")

    #Adds a single frame to the list widget with its thumbnail, filename, and tooltip. The frame's file path is stored in the item's user data for later retrieval during GIF generation.
    def add_frame(self, frame_path):
        item = QListWidgetItem()
        item.setIcon(QIcon(frame_path))
        item.setData(Qt.UserRole, frame_path)
        item.setToolTip(frame_path)
        item.setSizeHint(QSize(240, 80))
        self.frame_list.addItem(item)

    #Refreshes the labels of the frames in the list widget to reflect their current order after any drag-and-drop reordering.
    def refresh_frame_labels(self):
        for index in range(self.frame_list.count()):
            item = self.frame_list.item(index)
            frame_name = os.path.basename(item.data(Qt.UserRole))
            item.setText(f"{index + 1:02d}. {frame_name}")

    #GIF Generation Logic
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
            frame_paths = []

            if self.frame_list.count() > 0:
                for index in range(self.frame_list.count()):
                    item = self.frame_list.item(index)
                    frame_paths.append(item.data(Qt.UserRole))
            else:
                for filename in sorted(os.listdir(self.folder_path)):
                    if filename.lower().endswith((".png", ".jpg", ".jpeg", ".bmp", ".gif")):
                        frame_paths.append(os.path.join(self.folder_path, filename))

            for path in frame_paths:
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









