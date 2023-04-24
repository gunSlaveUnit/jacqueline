import sys
import ctypes

from PySide6.QtGui import QGuiApplication, QColor, QIcon
from PySide6.QtQml import QQmlApplicationEngine

from desktop.src.settings import ICONS_DIR, LAYOUTS_DIR, APP_ID

if __name__ == '__main__':
    if sys.platform == 'win32':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)

    app = QGuiApplication(sys.argv)
    app.setPalette(QColor("black"))

    icon_file_path = ICONS_DIR / "icon.png"
    app.setWindowIcon(QIcon(str(icon_file_path)))

    engine = QQmlApplicationEngine()

    start_file_location = LAYOUTS_DIR / "main.qml"
    engine.load(start_file_location)

    app.exec()
