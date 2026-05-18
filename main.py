
# Connection Test

# Best one

# import os
# import sys
# import platform
# import multiprocessing
# import traceback

# # --- 0. THE GLOBAL PATH HACK ---
# # This ensures that ALL pages (Dashboard, Sidebar, etc.) find their 
# # .ui files and .qss themes inside the temporary PyInstaller folder.
# if hasattr(sys, '_MEIPASS'):
#     os.chdir(sys._MEIPASS)

# # --- 1. EMERGENCY PYNPUT PATCH ---
# # Fixes the 'AXIsProcessTrusted' KeyError on macOS with Python 3.12
# if platform.system() == "Darwin":
#     try:
#         from pynput._util import darwin
#         if hasattr(darwin, 'HIServices'):
#             darwin.HIServices.AXIsProcessTrusted = lambda: True
#         darwin.IS_TRUSTED = True
#         print("✅ Accessibility Patch Applied Successfully.")
#     except Exception as e:
#         print(f"⚠️ Accessibility Patch could not be applied: {e}")

# # --- 2. ENVIRONMENT SHIELD ---
# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# if platform.system() == "Darwin":
#     os.environ["PYQT_APPLE_DISABLE_APP_NAP"] = "1"

# from PySide6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon, QMenu
# from PySide6.QtGui import QIcon, QAction, QGuiApplication
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtNetwork import QLocalServer, QLocalSocket
# from ui.main_window import MainWindow

# # --- 3. RESOURCE PATH HELPER ---
# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.dirname(os.path.abspath(__file__))
#     return os.path.join(base_path, relative_path)

# def check_mac_permissions():
#     if platform.system() == "Darwin":
#         from PySide6.QtGui import QGuiApplication
#         if not QGuiApplication.screens():
#             msg = QMessageBox()
#             msg.setIcon(QMessageBox.Information)
#             msg.setText("Permissions Required")
#             msg.setInformativeText("Please ensure 'Accessibility' is enabled for K-Mends.")
#             msg.exec()

# def main():
#     multiprocessing.freeze_support()
#     if platform.system() == "Darwin":
#         QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

#     app = QApplication(sys.argv)
#     if platform.system() == "Darwin":
#         check_mac_permissions()
#     app.setQuitOnLastWindowClosed(False)

#     # Tray Setup
#     icon_path = resource_path("tray_icon.png")
#     tray = QSystemTrayIcon(QIcon(icon_path), app)
#     tray_menu = QMenu()
#     show_action = QAction("Open Dashboard", tray_menu)
#     quit_action = QAction("Quit K-Mends", tray_menu)
#     tray_menu.addAction(show_action)
#     tray_menu.addSeparator()
#     tray_menu.addAction(quit_action)
#     tray.setContextMenu(tray_menu)
#     tray.show()

#     # Single Instance Check
#     server_name = "com.kirkmends.wellbeing.localserver"
#     socket = QLocalSocket()
#     socket.connectToServer(server_name)
#     if socket.waitForConnected(500):
#         print("Already running.")
#         return 

#     server = QLocalServer()
#     if not server.listen(server_name):
#         QLocalServer.removeServer(server_name)
#         server.listen(server_name)

#     try:
#         window = MainWindow()
#         show_action.triggered.connect(lambda: (window.show(), window.raise_(), window.activateWindow()))
#         window.show_ai()
#         QTimer.singleShot(150, lambda: (window.toggle_monitoring(), window.ai_mode_page.sync_button_state()))
#         window.show() 
#         sys.exit(app.exec())
#     except Exception as e:
#         sys.exit(1)

# if __name__ == "__main__":
#     main()












# import os
# import sys
# import platform
# import multiprocessing
# import traceback

# # --- 0. THE GLOBAL PATH HACK ---
# if hasattr(sys, '_MEIPASS'):
#     os.chdir(sys._MEIPASS)

# # --- 1. EMERGENCY PYNPUT PATCH ---
# if platform.system() == "Darwin":
#     try:
#         from pynput._util import darwin
#         if hasattr(darwin, 'HIServices'):
#             darwin.HIServices.AXIsProcessTrusted = lambda: True
#         darwin.IS_TRUSTED = True
#         print("✅ Accessibility Patch Applied Successfully.")
#     except Exception as e:
#         print(f"⚠️ Accessibility Patch could not be applied: {e}")

# # --- 2. ENVIRONMENT SHIELD ---
# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# if platform.system() == "Darwin":
#     os.environ["PYQT_APPLE_DISABLE_APP_NAP"] = "1"

# from PySide6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon, QMenu
# from PySide6.QtGui import QIcon, QAction, QGuiApplication
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtNetwork import QLocalServer, QLocalSocket
# from ui.main_window import MainWindow

# # --- 3. RESOURCE PATH HELPER ---
# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.dirname(os.path.abspath(__file__))
#     return os.path.join(base_path, relative_path)

# def check_mac_permissions():
#     if platform.system() == "Darwin":
#         from PySide6.QtGui import QGuiApplication
#         if not QGuiApplication.screens():
#             msg = QMessageBox()
#             msg.setIcon(QMessageBox.Information)
#             msg.setText("Permissions Required")
#             msg.setInformativeText("Please ensure 'Accessibility' is enabled for K-Mends.")
#             msg.exec()

# def main():
#     multiprocessing.freeze_support()
#     if platform.system() == "Darwin":
#         QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

#     app = QApplication(sys.argv)
#     if platform.system() == "Darwin":
#         check_mac_permissions()
    
#     # Crucial: Keep the app alive even if the window is hidden
#     app.setQuitOnLastWindowClosed(False)

#     # --- TRAY SETUP (COMMENTED OUT TO PREVENT DOUBLE ICONS) ---
#     # We are now using the tray setup inside ui/main_window.py instead.
#     """
#     icon_path = resource_path("tray_icon.png")
#     tray = QSystemTrayIcon(QIcon(icon_path), app)
#     tray_menu = QMenu()
#     show_action = QAction("Open Dashboard", tray_menu)
#     quit_action = QAction("Quit K-Mends", tray_menu)
#     tray_menu.addAction(show_action)
#     tray_menu.addSeparator()
#     tray_menu.addAction(quit_action)
#     tray.setContextMenu(tray_menu)
#     tray.show()
#     """

#     # Single Instance Check
#     server_name = "com.kirkmends.wellbeing.localserver"
#     socket = QLocalSocket()
#     socket.connectToServer(server_name)
#     if socket.waitForConnected(500):
#         print("Already running.")
#         return 

#     server = QLocalServer()
#     if not server.listen(server_name):
#         QLocalServer.removeServer(server_name)
#         server.listen(server_name)

#     try:
#         window = MainWindow()
        
#         # We removed the show_action connection here because the tray icon 
#         # is now created inside MainWindow's setup_system_tray() method.
        
#         window.show_ai()
#         QTimer.singleShot(150, lambda: (window.toggle_monitoring(), window.ai_mode_page.sync_button_state()))
#         window.show() 
#         sys.exit(app.exec())
#     except Exception as e:
#         print(f"❌ Application crashed: {e}")
#         traceback.print_exc()
#         sys.exit(1)

# if __name__ == "__main__":
#     main()











# import os
# import sys
# import platform
# import multiprocessing
# import traceback

# # --- 1. RESOURCE PATH HELPER ---
# # This ensures the app can find its assets whether running from source or as a .app bundle
# def resource_path(relative_path):
#     try:
#         # PyInstaller creates a temp folder and stores path in _MEIPASS
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.dirname(os.path.abspath(__file__))
#     return os.path.join(base_path, relative_path)

# # --- 2. EMERGENCY PYNPUT/ACCESSIBILITY PATCH ---
# if platform.system() == "Darwin":
#     try:
#         from pynput._util import darwin
#         if hasattr(darwin, 'HIServices'):
#             darwin.HIServices.AXIsProcessTrusted = lambda: True
#         darwin.IS_TRUSTED = True
#         print("✅ Accessibility Patch Applied Successfully.")
#     except Exception as e:
#         print(f"⚠️ Accessibility Patch could not be applied: {e}")

# # --- 3. ENVIRONMENT SHIELD ---
# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# if platform.system() == "Darwin":
#     os.environ["PYQT_APPLE_DISABLE_APP_NAP"] = "1"

# from PySide6.QtWidgets import QApplication, QMessageBox
# from PySide6.QtGui import QGuiApplication
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtNetwork import QLocalServer, QLocalSocket
# from ui.main_window import MainWindow

# def check_mac_permissions():
#     """Checks if the app has permission to interact with the screen/keyboard"""
#     if platform.system() == "Darwin":
#         if not QGuiApplication.screens():
#             msg = QMessageBox()
#             msg.setIcon(QMessageBox.Information)
#             msg.setText("Permissions Required")
#             msg.setInformativeText("Please ensure 'Accessibility' is enabled for K-Mends Wellbeing in System Settings.")
#             msg.exec()

# def main():
#     # Required for PyInstaller + Multiprocessing
#     multiprocessing.freeze_support()
    
#     if platform.system() == "Darwin":
#         QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

#     app = QApplication(sys.argv)
    
#     if platform.system() == "Darwin":
#         check_mac_permissions()
    
#     # Crucial: Keeps the app running in the tray even if the main window is closed
#     app.setQuitOnLastWindowClosed(False)

#     # --- 4. SINGLE INSTANCE CHECK ---
#     # Prevents multiple copies of the app from running at once
#     server_name = "com.kirkmends.wellbeing.localserver"
#     socket = QLocalSocket()
#     socket.connectToServer(server_name)
#     if socket.waitForConnected(500):
#         print("K-Mends is already running.")
#         return 

#     server = QLocalServer()
#     if not server.listen(server_name):
#         QLocalServer.removeServer(server_name)
#         server.listen(server_name)

#     # --- 5. MAIN EXECUTION ---
#     try:
#         # MainWindow handles its own tray setup in ui/main_window.py
#         window = MainWindow()
        
#         # Initial UI Setup
#         window.show_ai()
        
#         # Small delay before starting monitoring to ensure UI is ready
#         QTimer.singleShot(150, lambda: (
#             window.toggle_monitoring(), 
#             window.ai_mode_page.sync_button_state()
#         ))
        
#         window.show() 
#         sys.exit(app.exec())
        
#     except Exception as e:
#         print(f"❌ Application crashed: {e}")
#         traceback.print_exc()
#         sys.exit(1)

# if __name__ == "__main__":
#     main()















import os
import sys
import platform
import multiprocessing
import traceback

# --- 1. RESOURCE PATH HELPER ---
# This looks up custom modules inside the root bundle directory
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
        
    # Check for paths inside the verified Mac App Store layout
    prod_path = os.path.join(base_path, relative_path)
    if os.path.exists(prod_path):
        return prod_path

    # Fallback checking up one level if called inside nested sub-framework hooks
    fallback_path = os.path.join(base_path, "..", "Resources", relative_path)
    if os.path.exists(fallback_path):
        return fallback_path

    return os.path.join(base_path, relative_path)

# --- 2. EMERGENCY PYNPUT/ACCESSIBILITY PATCH ---
if platform.system() == "Darwin":
    try:
        from pynput._util import darwin
        if hasattr(darwin, 'HIServices'):
            darwin.HIServices.AXIsProcessTrusted = lambda: True
        darwin.IS_TRUSTED = True
        print("✅ Accessibility Patch Applied Successfully.")
    except Exception as e:
        print(f"⚠️ Accessibility Patch could not be applied: {e}")

# --- 3. ENVIRONMENT SHIELD ---
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
if platform.system() == "Darwin":
    os.environ["PYQT_APPLE_DISABLE_APP_NAP"] = "1"

from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtGui import QGuiApplication
from PySide6.QtCore import Qt, QTimer
from PySide6.QtNetwork import QLocalServer, QLocalSocket
from ui.main_window import MainWindow

def check_mac_permissions():
    """Checks if the app has permission to interact with the screen/keyboard"""
    if platform.system() == "Darwin":
        if not QGuiApplication.screens():
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Permissions Required")
            msg.setInformativeText("Please ensure 'Accessibility' is enabled for K-Mends Wellbeing in System Settings.")
            msg.exec()

def main():
    multiprocessing.freeze_support()
    
    if platform.system() == "Darwin":
        QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    
    if platform.system() == "Darwin":
        check_mac_permissions()
    
    app.setQuitOnLastWindowClosed(False)

    # --- 4. SINGLE INSTANCE CHECK ---
    server_name = "com.kirkmends.wellbeing.localserver"
    socket = QLocalSocket()
    socket.connectToServer(server_name)
    if socket.waitForConnected(500):
        print("K-Mends is already running.")
        return 

    server = QLocalServer()
    if not server.listen(server_name):
        QLocalServer.removeServer(server_name)
        server.listen(server_name)

    # --- 5. MAIN EXECUTION ---
    try:
        window = MainWindow()
        window.show_ai()
        
        QTimer.singleShot(150, lambda: (
            window.toggle_monitoring(), 
            window.ai_mode_page.sync_button_state()
        ))
        
        window.show() 
        sys.exit(app.exec())
        
    except Exception as e:
        print(f"❌ Application crashed: {e}")
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()