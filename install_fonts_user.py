"""
Install custom fonts to user's local fonts directory (no admin needed)
"""
import os
import shutil
from pathlib import Path
import winreg

def install_font_user(font_path):
    """Install a font to user's local fonts directory"""
    font_path = Path(font_path)
    if not font_path.exists():
        print(f"Font not found: {font_path}")
        return False

    # User's local fonts directory
    local_appdata = Path(os.environ['LOCALAPPDATA'])
    fonts_dir = local_appdata / 'Microsoft' / 'Windows' / 'Fonts'
    fonts_dir.mkdir(parents=True, exist_ok=True)

    # Copy font
    dest = fonts_dir / font_path.name

    try:
        if not dest.exists():
            shutil.copy2(font_path, dest)
            print(f"Copied {font_path.name} to {fonts_dir}")
        else:
            print(f"{font_path.name} already installed")

        # Register in user registry
        font_name = font_path.stem + " (TrueType)"
        registry_path = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"

        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_SET_VALUE)
        winreg.SetValueEx(key, font_name, 0, winreg.REG_SZ, str(dest))
        winreg.CloseKey(key)

        print(f"Registered {font_name} in registry")
        return True

    except Exception as e:
        print(f"Error installing font: {e}")
        return False

if __name__ == "__main__":
    script_dir = Path(__file__).parent
    fonts_dir = script_dir / "fonts"

    if not fonts_dir.exists():
        print(f"Fonts directory not found: {fonts_dir}")
        exit(1)

    print("Installing fonts to user directory (no admin needed)...\n")

    # Install Orbitron
    orbitron = fonts_dir / "Orbitron.ttf"
    if orbitron.exists():
        install_font_user(orbitron)

    # Install Share Tech Mono
    share_tech = fonts_dir / "ShareTechMono.ttf"
    if share_tech.exists():
        install_font_user(share_tech)

    print("\nDone! Fonts installed to user directory.")
    print("Note: You may need to restart the Python script for fonts to be available.")
