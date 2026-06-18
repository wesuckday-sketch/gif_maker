import os
from tkinter import *
from tkinter import filedialog

#Functions
selected_folder = ""

def choose_folder():
    global selected_folder
    selected_folder = filedialog.askdirectory()
    
    if selected_folder:
        folder_label.config(text=selected_folder)
        status_label.config(text="Folder selected")
        print("Folder selected:", selected_folder)

def generate_gif():
    try:
        from PIL import Image as PILImage
    except ImportError:
        status_label.config(text="Pillow is not installed")
        return

    folder_path = selected_folder or "frames"
    output_name = output_entry.get().strip() or "animation.gif"

    try:
        fps = int(fps_entry.get().strip())
    except ValueError:
        status_label.config(text="FPS must be a number")
        return

    frames = []
    for filename in sorted(os.listdir(folder_path)):
        if filename.endswith(".png"):
            frames.append(
                PILImage.open(os.path.join(folder_path, filename))
            )   

    if not frames:
        status_label.config(text="No PNG frames found")
        return

    frames[0].save(
    output_name,
    save_all=True,
    append_images=frames[1:],
    duration=max(1, int(1000 / fps)),
    loop=0
    )
    status_label.config(text=f"Saved {output_name}")


#User Interface
root = Tk()
root.title("Wesuckday's GIF Maker")
root.geometry("400x250")

folder_label = Label(root, text="No folder selected")
folder_label.pack()

output_label = Label(root, text="Output Name")
output_label.pack()

output_entry = Entry(root)
output_entry.insert(0, "animation.gif")
output_entry.pack()

fps_label = Label(root, text="FPS")
fps_label.pack()

fps_entry = Entry(root)
fps_entry.insert(0,"12")
fps_entry.pack()

generate_button = Button(root, text="Generate GIF", command=generate_gif)
generate_button.pack(pady=10)

Button(root, text="Select Frames Folder", command=choose_folder).pack()

status_label = Label(root, text="Ready")
status_label.pack()

root.mainloop()










