## Desktop Clock and Date

A transparent, draggable desktop widget that shows **Earth time/date** and an approximate **Mars (Gale Crater) time/date** in a Mars-themed UI.

### Features

- **Dual clocks**: Earth standard time and Mars local solar time (Gale Crater).
- **Dual calendars**: Earth date and Darian calendar date for Mars.
- **Always-on-top style widget**: Borderless window you can drag anywhere.
- **Mars-inspired theme**: Colors and typography tuned to the design.
- **Optional custom fonts**: Uses Orbitron / Share Tech Mono if installed, falls back to system monospace fonts.

### Requirements

- **OS**: Windows.
- **Python**: 3.x with Tkinter available (standard in most Windows Python installs).
- **Optional fonts** (recommended for best look):
  - `Orbitron.ttf`
  - `ShareTechMono.ttf`

### Project files

- **`clock_widget.py`**: Main Tkinter widget script.
- **`run_clock.vbs`**: Windows Script Host launcher that runs the widget via `pythonw` with **no console window**.
- **`install_fonts.py`**: Installs fonts system-wide (usually requires running as administrator).
- **`install_fonts_user.py`**: Installs fonts just for the current user (no admin needed).
- **`fonts/`** (if present): Contains the `.ttf` font files used by the installers.

### Installing fonts (recommended)

From a terminal in `desktop-clock-and-date`:

```bash
python install_fonts_user.py
```

If you prefer system-wide installation and have admin rights:

```bash
python install_fonts.py
```

Then restart any running widgets so they can pick up the new fonts.

### Running the widget

- **Typical usage (no console window)**  
  Double‑click `run_clock.vbs` in Explorer.  
  This:
  - Sets the working directory to the script folder.
  - Runs `pythonw clock_widget.py` without opening a terminal window.

- **Debug / development mode (with console)**  
  From a terminal in `desktop-clock-and-date`:

  ```bash
  python clock_widget.py
  ```

### Interaction and layout

- **Default position**: Right side of the primary screen, slightly down from the top.
- **Dragging**: Click and hold anywhere on the widget, then move the mouse to reposition it.
- **Transparency**: Uses a key color so the panel appears as a floating HUD over your desktop.

