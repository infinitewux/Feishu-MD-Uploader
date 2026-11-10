"""Choose a Markdown file and run the uploader from the project directory."""

import os
from pathlib import Path
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox


def enable_windows_dpi_awareness():
    """Let Windows render the file dialog at the display's native DPI."""
    if sys.platform != 'win32':
        return

    import ctypes

    try:
        # PER_MONITOR_AWARE_V2 also handles moving the dialog between monitors.
        if ctypes.windll.user32.SetProcessDpiAwarenessContext(ctypes.c_void_p(-4)):
            return
    except (AttributeError, OSError):
        pass

    try:
        if ctypes.windll.shcore.SetProcessDpiAwareness(2) == 0:
            return
    except (AttributeError, OSError):
        pass

    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except (AttributeError, OSError):
        pass


def main():
    project_dir = Path(__file__).resolve().parent.parent
    enable_windows_dpi_awareness()
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    if not (project_dir / '.env').is_file():
        messagebox.showerror('配置缺失', '请先复制 .env.example 为 .env，并填写飞书应用凭据。', parent=root)
        root.destroy()
        return 1

    filename = filedialog.askopenfilename(
        parent=root,
        title='选择要上传的 Markdown 文件',
        filetypes=[('Markdown 文件', '*.md *.markdown'), ('所有文件', '*.*')],
    )
    root.destroy()
    if not filename:
        print('已取消选择。')
        return 0

    print(f'已选择：{filename}', flush=True)
    env = os.environ.copy()
    env['PYTHONIOENCODING'] = 'utf-8'
    result = subprocess.run(
        [sys.executable, str(project_dir / 'src' / 'uploader.py'), filename],
        cwd=project_dir,
        env=env,
        check=False,
    )
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
