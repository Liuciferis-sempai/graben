import sys
import os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        # Когда приложение упаковано в .exe
        return os.path.join(sys._MEIPASS, relative_path)
    # В режиме разработки
    return os.path.join(os.path.abspath("."), relative_path)