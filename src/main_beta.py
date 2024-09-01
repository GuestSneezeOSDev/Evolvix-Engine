import os
import subprocess
import shutil
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox

def request_directory():
    dir_name = filedialog.askdirectory(title="Select Directory")
    if not dir_name:
        return None
    os.makedirs(dir_name, exist_ok=True)
    messagebox.showinfo("Info", f"Directory '{dir_name}' created or already exists.")
    return dir_name

def clone_sdk_repo(target_dir):
    repo_url = "https://github.com/ValveSoftware/source-sdk-2013.git"
    temp_dir = "C:/source-sdk-temp"

    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    subprocess.run(["git", "clone", repo_url, temp_dir], check=True)
    os.chdir(temp_dir)
    
    return temp_dir

def move_sdk_folder(target_dir):
    folder_choice = tk.simpledialog.askstring("Input", "Which folder to move? (sp/mp)").strip().lower()
    
    valid_folders = {"sp": "sp", "mp": "mp"}
    
    if folder_choice not in valid_folders:
        messagebox.showerror("Error", "Invalid folder choice. Please choose 'sp' or 'mp'.")
        return
    
    folder_name = valid_folders[folder_choice]
    folder_path = os.path.join(os.getcwd(), folder_name)  
    
    if not os.path.isdir(folder_path):
        messagebox.showerror("Error", f"{folder_name} folder not found in the cloned repository.")
        return
    
    target_path = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), folder_name)  
    shutil.move(folder_path, target_path)
    messagebox.showinfo("Info", f"Moved '{folder_name}' folder to '{target_path}'.")

def request_texture():
    texture_path = filedialog.askopenfilename(title="Select Texture File", filetypes=[("Image Files", "*.png;*.tga")])
    if not texture_path:
        return None
    if not os.path.isfile(texture_path):
        messagebox.showerror("Error", "File not found. Please try again.")
        return None
    return texture_path

def resize_to_power_of_two(img):
    width, height = img.size
    
    def next_power_of_two(x):
        return 1 << (x - 1).bit_length()
    
    new_width = next_power_of_two(width)
    new_height = next_power_of_two(height)
    
    if new_width != width or new_height != height:
        img = img.resize((new_width, new_height), Image.ANTIALIAS)
    
    return img

def process_texture(texture_path, output_dir):
    try:
        img = Image.open(texture_path)
    except IOError:
        messagebox.showerror("Error", "Error opening image file. Please ensure it is a valid image format.")
        return None

    img = resize_to_power_of_two(img)
    
    processed_path = os.path.join(output_dir, "processed_texture.tga")
    img.save(processed_path)
    messagebox.showinfo("Info", f"Processed texture saved as {processed_path}")
    return processed_path

def compile_texture(texture_path, mod_dir):
    vtex_path = "C:/Program Files (x86)/Steam/steamapps/common/SourceSDK/bin/source2007/bin/vtex.exe"

    if not os.path.exists(vtex_path):
        messagebox.showerror("Error", "VTex not found. Please ensure the Source SDK 2013 and Source SDK is installed and vtex.exe is accessible.")
        return

    vtex_cmd = [
        vtex_path,
        "-game", mod_dir,
        texture_path
    ]
    
    try:
        subprocess.run(vtex_cmd, check=True)
        messagebox.showinfo("Info", "Texture compiled successfully.")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Error occurred during texture compilation. Please check the VTex log for details.")

def main():
    root = tk.Tk()
    root.withdraw() 
    
    mod_dir = request_directory()
    
    if mod_dir:
        clone_sdk_repo(mod_dir)
        move_sdk_folder(mod_dir)
        
        texture_path = request_texture()
        if texture_path:
            processed_texture = process_texture(texture_path, mod_dir)
            if processed_texture:
                compile_texture(processed_texture, mod_dir)

if __name__ == "__main__":
    main()
