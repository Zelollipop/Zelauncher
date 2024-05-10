import shutil
import json
import os
import sys
import tkinter as tk  
from tkinter.filedialog import askdirectory

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def get_save_path(bin):
    directory = bin
    save_file_path = os.path.join(directory, "SAVE.BIN")
    return resource_path(save_file_path)

def setup_saves():
    save_dir = os.path.join(os.path.expanduser('~/Documents'), 'Zelauncher/game_saves')
    game_saves = resource_path("data/game_saves")
    if not os.path.exists(save_dir):
        shutil.copytree(game_saves, save_dir)
    return save_dir

def get_config_path():
    game_dir = os.path.join(os.path.expanduser('~/Documents'), 'Zelauncher')
    if not os.path.exists(game_dir):
        os.makedirs(game_dir)
    return os.path.join(game_dir, 'config.json')

def load_directories():
    config_path = get_config_path()
    if os.path.exists(config_path):
        with open(config_path, "r") as file:
            return json.load(file)
    else:
        return False
        
def save_directories(directory):
    if load_directories():
        directories = load_directories()
    else: directories = {}
    config_path = get_config_path()
    for key, value in directory.items():
        if value:
            directories[key] = value
    with open(config_path, "w") as file:
        json.dump(directories, file)

def ask_directory(description = "Select a directory"):
    directory = askdirectory(title=description)
    if directory:
        return directory

def input_dir(key):
    key = key.replace("_", " ")
    message = f"Please select the directory for the {key}."
    tk.messagebox.showinfo("Directory Selection", message)
    directory_path = ask_directory(f"Please select the directory for {key}")
    if directory_path:
        return directory_path
    else:
        print(f"No directory selected for {key}.")

def add_second_account():
    directories = load_directories()

    message = "Please select the directory for the 2nd account save file."
    tk.messagebox.showinfo("Directory Selection", message)
    directory_path = ask_directory("Please select the directory for the second account")
    if directory_path:
        directories["second_account"] = directory_path
        save_directories(directories)
    else:
        print(f"No directory selected.")

def show_frame(frame):
    frame.tkraise()

def update_frame2(tiers, button_info):
    if button_info == "Red":
        icon = "rtier"
    else:
        icon = "wtier"

    button_info = [{"image_path": f"data/{icon+tier[5]}.png", "button_text": tier, "file_path": f"/tier_{tier[5]}"} for tier in tiers]
    add_buttons_with_images(frame_tier, button_info, "Please select your robe tier:")

def update_save_path(key):
    directories = load_directories()
    directories[key] = input_dir(key)
    save_directories(directories)

def path_settings(frame, keys):
    show_frame(frame)
    for widget in frame.winfo_children():
        widget.destroy()
    prompt_label = tk.Label(frame, text="Select the directory path you'd like to change :", font=("Helvetica", 15))
    prompt_label.pack(side="top", pady=50)

    button_frame = tk.Frame(frame)
    button_frame.pack(side="top", fill="x")

    for key in keys:
        buttons = tk.Button(button_frame, text=key.replace("_", " "), command=lambda keys = key: update_save_path(keys))
        buttons.pack(side="left", pady=(20,10), expand=True )
    
    save_path = tk.Button(button_frame, text="bin saves", command=lambda: update_save_path("bin_path"))
    save_path.pack(side="left", pady=(20,10), expand=True)

    back_button = tk.Button(frame, text="Back", command=lambda: go_back(frame))
    back_button.pack(side="bottom", pady=30)
    
def handle_choice(frame, button_info, path):
    global binpath
    history.append((frame, binpath))
    binpath += path
    if frame == frame_color:
        if button_info == "White":
            update_frame2(["Tier 2", "Tier 3", "Tier 4"], button_info)
        else: 
            update_frame2(["Tier 1", "Tier 2", "Tier 3", "Tier 4"], button_info)
        show_frame(frame_tier)
    elif frame == frame_tier:
        show_frame(frame_levels)
    else:
        perform_final_actions()

def add_buttons_with_images(frame, button_info, prompt):
    for widget in frame.winfo_children():
        widget.destroy()

    prompt_label = tk.Label(frame, text=prompt, font=("Helvetica", 24))
    prompt_label.pack(side="top", pady=10)

    button_frame = tk.Frame(frame)
    button_frame.pack(pady=10)
    
    for info in button_info:
        subframe = tk.Frame(button_frame)
        subframe.pack(side="left", padx=10)

        photo = tk.PhotoImage(file=resource_path(info["image_path"]))
    
        label = tk.Label(subframe, image=photo)
        label.image = photo
        label.pack(side="top")

        button = tk.Button(subframe, text=info["button_text"], 
                           command=lambda f=frame, text=info["button_text"], path=info["file_path"]: handle_choice(f, text, path))
        button.pack(side="top")
    if frame in [frame_tier, frame_levels]:
        back_button = tk.Button(frame, text="Back", command=lambda f=frame: go_back(f))
        back_button.pack(side="bottom", pady=20)

def go_back(frame):
    global binpath
    if frame == frame_path:
        show_frame(frame_color)
    else:
        last_frame, last_path = history.pop()
        binpath = last_path
        show_frame(last_frame)

def open_saves():
    data = load_directories()
    os.startfile(data["bin_path"])

def perform_final_actions():
    global binpath
    print(f"All choices made, performing final actions...")
    finalpath = get_save_path(binpath)
    for item in [data["local_save"], data["steam_save"]]:
        shutil.copy(finalpath, item)
    if "second_account" in data:
        shutil.copy(finalpath, data["second_account"])
    steamurl = data["steam_shortcut"] + "/journey.url"
    os.startfile(steamurl)
    root.destroy()

root = tk.Tk()
root.title("Journey launcher")
root.tk.call("wm", "iconphoto", root._w, tk.PhotoImage(file=resource_path("data/icon.png")))

frame_color = tk.Frame(root)
frame_tier = tk.Frame(root)
frame_levels = tk.Frame(root)
frame_path = tk.Frame(root)
history = [] #binpath history

for frame in (frame_color, frame_tier, frame_levels, frame_path):
    frame.grid(row=0, column=0, sticky='news')

buttons_frame1 = [{"image_path": "data/red.png", "button_text": "Red", "file_path": "/red"},
                  {"image_path": "data/white.png", "button_text": "White", "file_path": "/white"}]
buttons_frame3 = [{"image_path": "data/bb.png", "button_text": "BB", "file_path": "/bb"},
                  {"image_path": "data/pd.png", "button_text": "PD", "file_path": "/pd"},
                  {"image_path": "data/sc.png", "button_text": "SC", "file_path": "/sc"},
                  {"image_path": "data/ug.png", "button_text": "UG", "file_path": "/ug"},
                  {"image_path": "data/tower.png", "button_text": "Tower", "file_path": "/tower"},
                  {"image_path": "data/snow.png", "button_text": "Snow", "file_path": "/snow"}]

directories_key = ["local_save", "steam_save", "steam_shortcut"]
if load_directories():
    data = load_directories()
else:
    data = {}
    for key in directories_key:
        data[key] = input_dir(key)
    save_directories(data)

if "bin_path" not in data:
    data["bin_path"] = setup_saves()
    save_directories(data)

binpath = data["bin_path"]

show_frame(frame_color)
add_buttons_with_images(frame_color, buttons_frame1, "Which color suits you best today ?")
subframe = tk.Frame(frame_color)
subframe.pack(side="top", padx=10, pady=10)
changepath_button = tk.Button(subframe, text="Change saves path", command=lambda: path_settings(frame_path, directories_key))
changepath_button.pack(side="left", padx=5, pady=10)
second_account = tk.Button(subframe, text="Add second account", command=lambda: add_second_account())
second_account.pack(side="left", padx=5, pady=10)
open_save_dir = tk.Button(subframe, text="Saves directory", command=lambda: open_saves())
open_save_dir.pack(side="left", padx=5, pady=10)

add_buttons_with_images(frame_levels, buttons_frame3, "Please select your starting level:")

root.mainloop()

