"""
Install custom fonts to Windows system
Run this script as administrator if possible
"""
import os
import shutil
from pathlib import Path
import ctypes
from ctypes import wintypes

def install_font(font_path):
    """Install a font file to Windows"""
    font_path = Path(font_path)
    if not font_path.exists():
        print(f"Font not found: {font_path}")
        return False

    # Windows fonts directory
    fonts_dir = Path(os.environ['WINDIR']) / 'Fonts'

    # Copy font to Windows Fonts directory
    dest = fonts_dir / font_path.name

    try:
        # Copy the font file
        if not dest.exists():
            shutil.copy2(font_path, dest)
            print(f"Copied {font_path.name} to {fonts_dir}")
        else:
            print(f"{font_path.name} already exists in {fonts_dir}")

        # Register the font with Windows using Windows API
        gdi32 = ctypes.WinDLL('gdi32')
        # AddFontResourceW returns number of fonts added
        result = gdi32.AddFontResourceW(str(dest))

        if result > 0:
            print(f"Successfully registered {font_path.name}")

            # Notify all windows that fonts have changed
            HWND_BROADCAST = 0xFFFF
            WM_FONTCHANGE = 0x001D
            user32 = ctypes.WinDLL('user32')
            user32.SendMessageW(HWND_BROADCAST, WM_FONTCHANGE, 0, 0)
            print("Notified system of font changes")
            return True
        else:
            print(f"Failed to register {font_path.name}")
            return False

    except Exception as e:
        print(f"Error installing font: {e}")
        return False

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    fonts_dir = script_dir / "fonts"

    if not fonts_dir.exists():
        print(f"Fonts directory not found: {fonts_dir}")
        exit(1)

    print("Installing fonts...")
    print("Note: You may need to run this as administrator\n")

    # Install Orbitron
    orbitron = fonts_dir / "Orbitron.ttf"
    if orbitron.exists():
        install_font(orbitron)

    # Install Share Tech Mono
    share_tech = fonts_dir / "ShareTechMono.ttf"
    if share_tech.exists():
        install_font(share_tech)

    print("\nDone! You may need to restart applications for fonts to appear.")
