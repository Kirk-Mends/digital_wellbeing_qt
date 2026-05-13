# from PySide6.QtWidgets import QApplication
# from ui.main_window import MainWindow
# import sys

# def main():
#     app = QApplication(sys.argv)

#     window = MainWindow()
#     window.show()

#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()






# from PySide6.QtWidgets import QApplication
# from ui.main_window import MainWindow
# import sys

# def main():
#     app = QApplication(sys.argv)

#     window = MainWindow()

#     # Detect custom protocol actions from Winotify
#     # Example: app://take_break
#     if any(arg.startswith("app://") for arg in sys.argv):
#         for arg in sys.argv:
#             if arg == "app://take_break":
#                 # Ensure last_engine_output exists
#                 if hasattr(window, "last_engine_output"):
#                     window.show_break_modal(window.last_engine_output)
#             elif arg == "app://busy":
#                 # User clicked "I'm Busy" — do nothing
#                 pass

#     window.show()
#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()














# 26th 

# import sys
# import os
# from PySide6.QtWidgets import QApplication
# from PySide6.QtNetwork import QLocalServer, QLocalSocket
# from ui.main_window import MainWindow

# def main():
#     # 1. Single Instance Check (Prevents multiple windows)
#     server_name = "K-Mends-Wellbeing-Instance"
#     socket = QLocalSocket()
#     socket.connectToServer(server_name)

#     # If we can connect, an instance is already running
#     if socket.waitForConnected(500):
#         print("K-Mends is already running in the background.")
#         sys.exit(0)

#     # If no instance is running, start this one as the 'Server'
#     app = QApplication(sys.argv)
#     server = QLocalServer()
#     server.listen(server_name)

#     # 2. Initialize Main Window
#     window = MainWindow()
    
#     # macOS specific: Keep app alive even if the main window is closed
#     app.setQuitOnLastWindowClosed(False)

#     # 3. Process Launch Arguments
#     args = sys.argv
#     is_startup = "--startup" in args
    
#     # Handle Winotify/Protocol links (e.g., app://take_break)
#     is_protocol = any(arg.startswith("app://") for arg in args)

#     if is_startup:
#         # Start quietly in the System Tray
#         window.hide()
#         print("K-Mends started in Background Mode.")
#     elif is_protocol:
#         # Handle specific notification clicks
#         for arg in args:
#             if arg == "app://take_break":
#                 if hasattr(window, "last_engine_output"):
#                     window.show_break_modal(window.last_engine_output)
#         window.show()
#     else:
#         # Standard manual launch
#         # window.show() # This will open the windo when it launches
#         window.hide()

#     sys.exit(app.exec())

# if __name__ == "__main__":
#     main()











# To make it start at the background


# import sys
# import os
# import time
# from PySide6.QtWidgets import QApplication
# from PySide6.QtNetwork import QLocalServer, QLocalSocket
# from ui.main_window import MainWindow

# def main():
#     # 1. Start the App Object FIRST
#     app = QApplication(sys.argv)
#     app.setQuitOnLastWindowClosed(False)

#     # 2. Single Instance Check
#     server_name = "K-Mends-Wellbeing-Instance"
#     socket = QLocalSocket()
#     socket.connectToServer(server_name)

#     if socket.waitForConnected(500):
#         print("K-Mends is already running. Exiting this attempt.")
#         return # Use return instead of sys.exit for a cleaner break

#     server = QLocalServer()
#     if not server.listen(server_name):
#         # If the server name is "stuck" in Windows memory, 
#         # this clears it so we can start.
#         QLocalServer.removeServer(server_name)
#         server.listen(server_name)

#     try:
#         # 3. Initialize Window
#         window = MainWindow()

#         # 4. AUTO-START (Wrapped in a small delay to prevent race conditions)
#         # We call these directly on the object
#         window.show_ai() 
#         window.toggle_monitoring() 
        
#         print("AI Engine Started Successfully.")

#         # 5. Determine Visibility
#         args = sys.argv
#         if "--startup" in args:
#             window.hide()
#         else:
#             # FOR NOW: Let's use show() so you can SEE it work.
#             # Change to hide() only after we confirm it stops closing.
#             window.hide()   #window.show()  for visible window

#         sys.exit(app.exec())

#     except Exception as e:
#         print(f"CRITICAL ERROR DURING STARTUP: {e}")
#         import traceback
#         traceback.print_exc()

# if __name__ == "__main__":
#     main()















# import os
# import sys

# # --- 1. THE "ANTI-SCALING" SHIELD (MUST BE AT THE VERY TOP) ---
# # We set these BEFORE importing PySide6 so the engine doesn't start with bad settings
# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
# os.environ["QT_SCALE_FACTOR"] = "1"

# import time
# import traceback
# from PySide6.QtWidgets import QApplication
# from PySide6.QtCore import Qt
# from PySide6.QtNetwork import QLocalServer, QLocalSocket
# from ui.main_window import MainWindow

# # --- 2. RESOURCE PATH HELPER ---
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # --- 3. HIGH DPI ATTRIBUTES ---
# QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
# QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# def main():
#     # 4. Start the App Object
#     app = QApplication(sys.argv)
#     app.setQuitOnLastWindowClosed(False)

#     # 5. Single Instance Check
#     server_name = "K-Mends-Wellbeing-Instance"
#     socket = QLocalSocket()
#     socket.connectToServer(server_name)

#     if socket.waitForConnected(500):
#         print("K-Mends is already running. Exiting.")
#         return 

#     server = QLocalServer()
#     if not server.listen(server_name):
#         QLocalServer.removeServer(server_name)
#         server.listen(server_name)

#     try:
#         # 6. Initialize Window
#         window = MainWindow()

#         # 7. AI Logic Start
#         window.show_ai() 
#         window.toggle_monitoring() 
        
#         print("AI Engine Started Successfully.")

#         # 8. Visibility Control
#         # If you want it to pop up on your screen, change window.hide() to window.show()
#         window.hide() 

#         sys.exit(app.exec())

#     except Exception as e:
#         print(f"CRITICAL ERROR DURING STARTUP: {e}")
#         traceback.print_exc()

# if __name__ == "__main__":
#     main()

















# import os
# import sys

# # --- 1. THE "ANTI-SCALING" SHIELD (MUST BE AT THE VERY TOP) ---
# # We set these BEFORE importing PySide6 so the engine doesn't start with bad settings
# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
# os.environ["QT_SCALE_FACTOR"] = "1"

# import time
# import traceback
# from PySide6.QtWidgets import QApplication
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtNetwork import QLocalServer, QLocalSocket
# from ui.main_window import MainWindow


# # --- 2. RESOURCE PATH HELPER ---
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # --- 3. HIGH DPI ATTRIBUTES ---
# QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
# QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# def main():
#     # 4. Start the App Object
#     app = QApplication(sys.argv)
#     app.setQuitOnLastWindowClosed(False)

#     # 5. Single Instance Check
#     server_name = "K-Mends-Wellbeing-Instance"
#     socket = QLocalSocket()
#     socket.connectToServer(server_name)

#     if socket.waitForConnected(500):
#         print("K-Mends is already running. Exiting.")
#         return 

#     server = QLocalServer()
#     if not server.listen(server_name):
#         QLocalServer.removeServer(server_name)
#         server.listen(server_name)

#     try:
#         # 6. Initialize Window
#         window = MainWindow()

#         # 7. AI Logic Start
#         window.show_ai()

#         # Start monitoring AFTER UI is built
#         QTimer.singleShot(50, lambda: (
#             window.toggle_monitoring(),
#             window.ai_mode_page.sync_button_state()
#         ))
 
        
#         print("AI Engine Started Successfully.")

#         # 8. Visibility Control
#         # If you want it to pop up on your screen, change window.hide() to window.show()
#         window.hide() 

#         sys.exit(app.exec())

#     except Exception as e:
#         print(f"CRITICAL ERROR DURING STARTUP: {e}")
#         traceback.print_exc()

# if __name__ == "__main__":
#     main()










# # main.py
# import os
# import sys
# import platform

# # --- 1. THE "ANTI-SCALING" & "ANTI-NAP" SHIELD (MUST BE AT THE VERY TOP) ---
# # Prevent blurry UI on Windows
# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
# os.environ["QT_SCALE_FACTOR"] = "1"

# # CRITICAL FOR MAC: Prevent macOS from "napping" (freezing) the AI engine when hidden
# if platform.system() == "Darwin":
#     os.environ["PYQT_APPLE_DISABLE_APP_NAP"] = "1"

# import time
# import traceback
# from PySide6.QtWidgets import QApplication
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtNetwork import QLocalServer, QLocalSocket
# from ui.main_window import MainWindow


# # --- 2. RESOURCE PATH HELPER ---
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller """
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # --- 3. HIGH DPI ATTRIBUTES ---
# # Modern PySide6 handles this automatically on Mac; we only force it for Windows 
# # to avoid the DeprecationWarnings you saw in your terminal.
# if platform.system() == "win32":
#     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
#     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# from PySide6.QtWidgets import QMessageBox # Add this to your imports

# def check_mac_permissions():
#     """ 
#     A simple check for Apple Reviewers to ensure they 
#     know to enable Accessibility permissions.
#     """
#     if platform.system() == "Darwin":
#         # On macOS, if we can't see any windows, we likely lack permissions
#         from PySide6.QtGui import QGuiApplication
#         if not QGuiApplication.screens():
#             msg = QMessageBox()
#             msg.setIcon(QMessageBox.Information)
#             msg.setText("Permissions Required")
#             msg.setInformativeText(
#                 "To categorize focus work accurately, please ensure 'Accessibility' "
#                 "is enabled for K-Mends in System Settings > Privacy & Security."
#             )
#             msg.exec()

# def main():
#     app = QApplication(sys.argv)
    
#     # CALL THE PERMISSION CHECK HERE
#     if platform.system() == "Darwin":
#         check_mac_permissions()
        
#     app.setQuitOnLastWindowClosed(False)

#     # 5. Single Instance Check
#     server_name = "K-Mends-Wellbeing-Instance"
#     socket = QLocalSocket()
#     socket.connectToServer(server_name)

#     if socket.waitForConnected(500):
#         print("K-Mends is already running. Exiting.")
#         return 

#     server = QLocalServer()
#     if not server.listen(server_name):
#         QLocalServer.removeServer(server_name)
#         server.listen(server_name)

#     try:
#         # 6. Initialize Window
#         window = MainWindow()

#         # 7. AI Logic Start
#         window.show_ai()

#         # Start monitoring AFTER UI is built
#         QTimer.singleShot(50, lambda: (
#             window.toggle_monitoring(),
#             window.ai_mode_page.sync_button_state()
#         ))
 
#         print("AI Engine Started Successfully.")

#         # 8. Visibility Control
#         # Hidden by default to run as a background assistant
#         window.hide() 

#         sys.exit(app.exec())

#     except Exception as e:
#         print(f"CRITICAL ERROR DURING STARTUP: {e}")
#         traceback.print_exc()

# if __name__ == "__main__":
#     main()












# import os
# import sys
# import platform
# import multiprocessing
# import traceback

# # --- 1. THE "ANTI-SCALING" & "ANTI-NAP" SHIELD ---
# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# os.environ["QT_SCREEN_SCALE_FACTORS"] = "1"
# os.environ["QT_SCALE_FACTOR"] = "1"

# if platform.system() == "Darwin":
#     os.environ["PYQT_APPLE_DISABLE_APP_NAP"] = "1"

# from PySide6.QtWidgets import QApplication, QMessageBox
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtNetwork import QLocalServer, QLocalSocket
# from ui.main_window import MainWindow

# # --- 2. RESOURCE PATH HELPER ---
# def resource_path(relative_path):
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         base_path = os.path.abspath(".")
#     return os.path.join(base_path, relative_path)

# # --- 3. HIGH DPI ATTRIBUTES ---
# if platform.system() == "win32":
#     QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
#     QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

# def check_mac_permissions():
#     if platform.system() == "Darwin":
#         from PySide6.QtGui import QGuiApplication
#         if not QGuiApplication.screens():
#             msg = QMessageBox()
#             msg.setIcon(QMessageBox.Information)
#             msg.setText("Permissions Required")
#             msg.setInformativeText(
#                 "To categorize focus work accurately, please ensure 'Accessibility' "
#                 "is enabled for K-Mends in System Settings > Privacy & Security."
#             )
#             msg.exec()

# def main():
#     # CRITICAL: Prevent infinite process spawning in Sandboxed apps
#     multiprocessing.freeze_support()

#     app = QApplication(sys.argv)
    
#     if platform.system() == "Darwin":
#         check_mac_permissions()
        
#     app.setQuitOnLastWindowClosed(False)

#     # 5. Sandbox-Safe Single Instance Check
#     # Prefixed with Bundle ID to ensure it stays within the Sandbox container
#     server_name = "com.kirkmends.wellbeing.localserver"
#     socket = QLocalSocket()
#     socket.connectToServer(server_name)

#     if socket.waitForConnected(500):
#         print("K-Mends is already running. Exiting.")
#         return 

#     server = QLocalServer()
#     if not server.listen(server_name):
#         QLocalServer.removeServer(server_name)
#         server.listen(server_name)

#     try:
#         # 6. Initialize Window
#         window = MainWindow()

#         # 7. AI Logic Start
#         window.show_ai()

#         # Start monitoring AFTER UI is built
#         QTimer.singleShot(50, lambda: (
#             window.toggle_monitoring(),
#             window.ai_mode_page.sync_button_state()
#         ))
 
#         print("AI Engine Started Successfully.")

#         # 8. Visibility Control
#         # CRITICAL FOR SANDBOX: Show the window briefly then hide it. 
#         # If we hide it immediately, macOS may never register the UI thread.
#         window.show() 
#         QTimer.singleShot(100, window.hide) 

#         sys.exit(app.exec())

#     except Exception as e:
#         # Use a real UI popup for errors because we can't see the terminal in TestFlight
#         error_msg = QMessageBox()
#         error_msg.critical(None, "Startup Error", f"An error occurred: {e}\n\n{traceback.format_exc()}")
#         sys.exit(1)

# if __name__ == "__main__":
#     main()










# import os
# import sys
# import platform
# import multiprocessing
# import traceback

# # --- 1. EMERGENCY PYNPUT PATCH ---
# # Fixes the 'AXIsProcessTrusted' KeyError on macOS with Python 3.12
# if platform.system() == "Darwin":
#     try:
#         from pynput._util import darwin
#         if hasattr(darwin, 'HIServices'):
#             # Manually inject the missing attribute into the library at runtime
#             darwin.HIServices.AXIsProcessTrusted = lambda: True
#         darwin.IS_TRUSTED = True
#         print("✅ Accessibility Patch Applied Successfully.")
#     except Exception as e:
#         print(f"⚠️ Accessibility Patch could not be applied: {e}")

# # --- 2. THE "SMART SCALING" & "ANTI-NAP" SHIELD ---
# # We use '1' for auto-scaling but REMOVE forced factors to let Retina work
# os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
# if platform.system() == "Darwin":
#     os.environ["PYQT_APPLE_DISABLE_APP_NAP"] = "1"

# from PySide6.QtWidgets import QApplication, QMessageBox, QSystemTrayIcon, QMenu
# from PySide6.QtGui import QIcon, QAction, QGuiApplication
# from PySide6.QtCore import Qt, QTimer
# from PySide6.QtNetwork import QLocalServer, QLocalSocket
# from ui.main_window import MainWindow

# # --- 3. IMPROVED RESOURCE PATH HELPER ---
# def resource_path(relative_path):
#     """ Get absolute path to resource, works for dev and for PyInstaller bundle """
#     try:
#         base_path = sys._MEIPASS
#     except Exception:
#         # Ensures files are found relative to this script's location
#         base_path = os.path.dirname(os.path.abspath(__file__))
#     return os.path.join(base_path, relative_path)

# def check_mac_permissions():
#     """ Provides a helpful hint if the app isn't seeing screens (permission check) """
#     if platform.system() == "Darwin":
#         from PySide6.QtGui import QGuiApplication
#         if not QGuiApplication.screens():
#             msg = QMessageBox()
#             msg.setIcon(QMessageBox.Information)
#             msg.setText("Permissions Required")
#             msg.setInformativeText(
#                 "To categorize focus work accurately, please ensure 'Accessibility' "
#                 "is enabled for K-Mends in System Settings > Privacy & Security."
#             )
#             msg.exec()

# def main():
#     multiprocessing.freeze_support()

#     # Enable High-Resolution sharp text for Mac Retina displays
#     if platform.system() == "Darwin":
#         QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

#     app = QApplication(sys.argv)
    
#     if platform.system() == "Darwin":
#         check_mac_permissions()
        
#     # CRITICAL: Keeps app running in background when window is closed/hidden
#     app.setQuitOnLastWindowClosed(False)

#     # --- 4. SYSTEM TRAY ICON (Menu Bar Fix) ---
#     icon_path = resource_path("tray_icon.png")
#     tray = QSystemTrayIcon(QIcon(icon_path), app)
    
#     # Create the Menu for the Top Tray Icon
#     tray_menu = QMenu()
#     show_action = QAction("Open Dashboard", tray_menu)
#     quit_action = QAction("Quit K-Mends", tray_menu)
    
#     tray_menu.addAction(show_action)
#     tray_menu.addSeparator()
#     tray_menu.addAction(quit_action)
    
#     tray.setContextMenu(tray_menu)
#     tray.show() # Puts the 'K' icon in the top right menu bar

#     # --- 5. SINGLE INSTANCE CHECK (Sandbox Safe) ---
#     server_name = "com.kirkmends.wellbeing.localserver"
#     socket = QLocalSocket()
#     socket.connectToServer(server_name)

#     if socket.waitForConnected(500):
#         print("K-Mends is already running. Exiting duplicate instance.")
#         return 

#     server = QLocalServer()
#     if not server.listen(server_name):
#         QLocalServer.removeServer(server_name)
#         server.listen(server_name)

#     try:
#         # 6. Initialize Window
#         window = MainWindow()
        
#         # Connect the tray "Open" action to bringing the window to front
#         show_action.triggered.connect(lambda: (window.show(), window.raise_(), window.activateWindow()))

#         # 7. Start AI Logic
#         window.show_ai()

#         # Start monitoring with a slight delay for stability
#         QTimer.singleShot(150, lambda: (
#             window.toggle_monitoring(),
#             window.ai_mode_page.sync_button_state()
#         ))
 
#         print("🚀 AI Engine Started Successfully.")

#         # 8. INITIAL VISIBILITY
#         # Launching with the window visible so the user knows it's working.
#         window.show() 
#         window.raise_()
#         window.activateWindow()

#         sys.exit(app.exec())

#     except Exception as e:
#         error_msg = QMessageBox()
#         error_msg.critical(None, "Startup Error", f"An error occurred: {e}\n\n{traceback.format_exc()}")
#         sys.exit(1)

# if __name__ == "__main__":
#     main()









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











import os
import sys
import platform
import multiprocessing
import traceback

# --- 1. RESOURCE PATH HELPER ---
# This ensures the app can find its assets whether running from source or as a .app bundle
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
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
    # Required for PyInstaller + Multiprocessing
    multiprocessing.freeze_support()
    
    if platform.system() == "Darwin":
        QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

    app = QApplication(sys.argv)
    
    if platform.system() == "Darwin":
        check_mac_permissions()
    
    # Crucial: Keeps the app running in the tray even if the main window is closed
    app.setQuitOnLastWindowClosed(False)

    # --- 4. SINGLE INSTANCE CHECK ---
    # Prevents multiple copies of the app from running at once
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
        # MainWindow handles its own tray setup in ui/main_window.py
        window = MainWindow()
        
        # Initial UI Setup
        window.show_ai()
        
        # Small delay before starting monitoring to ensure UI is ready
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