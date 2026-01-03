# clipboard.py
# Clipboard copy with auto-clear

import pyperclip
import threading
import time


def copy_with_timeout(text, timeout=10):
    pyperclip.copy(text)

    def clear():
        time.sleep(timeout)
        pyperclip.copy("")

    threading.Thread(target=clear, daemon=True).start()
