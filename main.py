from PIL import Image
import os
from tkinter import *
from tkinter import filedialog


root = Tk()

frames = []

for filename in sorted(os.listdir("frames")):
    if filename.endswith(".png"):
        frames.append(
            Image.open(f"frames/{filename}")
        )

print("Frames loaded:", len(frames))

frames[0].save(
    "animation.gif",
    save_all = True,
    append_images = frames[1:],
    duration=100,
    loop=0
)






