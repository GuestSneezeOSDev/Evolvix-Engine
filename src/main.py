# Copyright Vortex Engine
# Copyright GuestSneezeOSDev
# Copyright Evolvix
import os
import subprocess
from PIL import Image

def request_directory():
    dir_name = input("Enter the name of the directory to create: ")
    os.makedirs(dir_name, exist_ok=True)
    print(f"Directory '{dir_name}' created or already exists.")
    return dir_name

def request_texture():
    texture_path = input("Please provide the path to your texture file (e.g., PNG, TGA): ")
    if not os.path.exists(texture_path):
        print("File not found. Please try again.")
        return None
    return texture_path

def process_texture(texture_path, output_dir):
    img = Image.open(texture_path)
    width, height = img.size

    if (width & (width - 1)) != 0 or (height & (height - 1)) != 0:
        print("Resizing texture to the nearest power of two dimensions.")
        img = img.resize((1024, 1024), Image.ANTIALIAS)  

    processed_path = os.path.join(output_dir, "processed_texture.tga")
    img.save(processed_path)
    print(f"Processed texture saved as {processed_path}")
    return processed_path

def compile_texture(texture_path, mod_dir):
    vtex_path = "C:/Program Files (x86)/Steam/steamapps/common/SourceSDK/bin/source2007/bin/vtex.exe"

    if not os.path.exists(vtex_path):
        print("VTex not found. Please ensure the Source SDK 2013 and Source SDK is installed and vtex.exe is accessible.")
        return

    vtex_cmd = [
        vtex_path,
        "-game", mod_dir,  
        texture_path
    ]
    
    subprocess.run(vtex_cmd, check=True)
    print("Texture compiled successfully.")

def main():
    mod_dir = request_directory()
    texture_path = request_texture()
    if texture_path:
        processed_texture = process_texture(texture_path, mod_dir)
        compile_texture(processed_texture, mod_dir)

if __name__ == "__main__":
    main()
