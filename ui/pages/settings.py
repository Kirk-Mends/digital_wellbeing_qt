
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox,
#     QPushButton, QFileDialog, QHBoxLayout, QMessageBox
# )
# from PySide6.QtCore import Qt


# class SettingsPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)

#         # -------------------------
#         # PAGE TITLE
#         # -------------------------
#         title = QLabel("Settings")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # ============================================================
#         # THEME
#         # ============================================================
#         theme_label = QLabel("Theme")
#         theme_label.setObjectName("SectionLabel")
#         layout.addWidget(theme_label)

#         self.theme_combo = QComboBox()
#         self.theme_combo.addItems(["light", "dark", "blue"])
#         self.theme_combo.setCurrentText(self.settings.get("theme"))
#         self.theme_combo.currentTextChanged.connect(self.preview_theme)
#         layout.addWidget(self.theme_combo)

#         # ============================================================
#         # SOUND
#         # ============================================================
#         self.sound_toggle = QCheckBox("Enable Notification Sound")
#         self.sound_toggle.setChecked(self.settings.get("sound_enabled", True))
#         self.sound_toggle.stateChanged.connect(self.toggle_sound)
#         layout.addWidget(self.sound_toggle)

#         # ============================================================
#         # NOTIFICATIONS
#         # ============================================================
#         self.notify_toggle = QCheckBox("Enable Break Notifications")
#         self.notify_toggle.setChecked(self.settings.get("notifications_enabled", True))
#         self.notify_toggle.stateChanged.connect(self.toggle_notifications)
#         layout.addWidget(self.notify_toggle)

#         # ============================================================
#         # PROFILES
#         # ============================================================
#         profile_label = QLabel("Profile")
#         profile_label.setObjectName("SectionLabel")
#         layout.addWidget(profile_label)

#         profile_row = QHBoxLayout()

#         self.profile_combo = QComboBox()
#         self.profile_combo.addItems(self.settings.list_profiles())
#         self.profile_combo.setCurrentText(self.settings.current_profile)
#         self.profile_combo.currentTextChanged.connect(self.switch_profile)
#         profile_row.addWidget(self.profile_combo)

#         btn_new_profile = QPushButton("New")
#         btn_new_profile.clicked.connect(self.create_profile)
#         profile_row.addWidget(btn_new_profile)

#         btn_delete_profile = QPushButton("Delete")
#         btn_delete_profile.clicked.connect(self.delete_profile)
#         profile_row.addWidget(btn_delete_profile)

#         layout.addLayout(profile_row)

#         # ============================================================
#         # EXPORT / IMPORT
#         # ============================================================
#         export_btn = QPushButton("Export Settings")
#         export_btn.clicked.connect(self.export_settings)
#         layout.addWidget(export_btn)

#         import_btn = QPushButton("Import Settings")
#         import_btn.clicked.connect(self.import_settings)
#         layout.addWidget(import_btn)

#         # ============================================================
#         # RESET
#         # ============================================================
#         reset_btn = QPushButton("Reset to Defaults")
#         reset_btn.setObjectName("DangerButton")
#         reset_btn.clicked.connect(self.reset_settings)
#         layout.addWidget(reset_btn)

#         layout.addStretch()

#     # ============================================================
#     # THEME PREVIEW
#     # ============================================================
#     def preview_theme(self, theme_name):
#         self.settings.set("theme", theme_name)
#         self.main.apply_theme()

#     # ============================================================
#     # SOUND
#     # ============================================================
#     def toggle_sound(self, state):
#         self.settings.set("sound_enabled", bool(state))

#     # ============================================================
#     # NOTIFICATIONS
#     # ============================================================
#     def toggle_notifications(self, state):
#         self.settings.set("notifications_enabled", bool(state))

#     # ============================================================
#     # PROFILES
#     # ============================================================
#     def switch_profile(self, profile_name):
#         self.settings.switch_profile(profile_name)
#         self.refresh_ui()
#         self.main.apply_theme()

#     def create_profile(self):
#         name, ok = QFileDialog.getSaveFileName(
#             self, "Create Profile", "", "Profile (*.json)"
#         )
#         if not ok or not name:
#             return

#         profile_name = name.split("/")[-1].replace(".json", "")
#         self.settings.switch_profile(profile_name)
#         self.refresh_ui()

#     def delete_profile(self):
#         profile = self.profile_combo.currentText()
#         if profile == "default":
#             QMessageBox.warning(self, "Error", "Cannot delete the default profile.")
#             return

#         self.settings.delete_profile(profile)
#         self.profile_combo.clear()
#         self.profile_combo.addItems(self.settings.list_profiles())
#         self.profile_combo.setCurrentText(self.settings.current_profile)
#         self.refresh_ui()

#     # ============================================================
#     # EXPORT / IMPORT
#     # ============================================================
#     def export_settings(self):
#         path, ok = QFileDialog.getSaveFileName(
#             self, "Export Settings", "", "JSON Files (*.json)"
#         )
#         if ok and path:
#             self.settings.export_settings(path)

#     def import_settings(self):
#         path, ok = QFileDialog.getOpenFileName(
#             self, "Import Settings", "", "JSON Files (*.json)"
#         )
#         if ok and path:
#             self.settings.import_settings(path)
#             self.refresh_ui()
#             self.main.apply_theme()

#     # ============================================================
#     # RESET
#     # ============================================================
#     def reset_settings(self):
#         self.settings.reset()
#         self.refresh_ui()
#         self.main.apply_theme()

#     # ============================================================
#     # REFRESH UI
#     # ============================================================
#     def refresh_ui(self):
#         self.theme_combo.setCurrentText(self.settings.get("theme"))
#         self.sound_toggle.setChecked(self.settings.get("sound_enabled"))
#         self.notify_toggle.setChecked(self.settings.get("notifications_enabled"))
#         self.profile_combo.clear()
#         self.profile_combo.addItems(self.settings.list_profiles())
#         self.profile_combo.setCurrentText(self.settings.current_profile)

















# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
#     QStackedWidget, QLabel
# )
# from PySide6.QtCore import Qt

# class SettingsPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         # Root layout: sidebar (left) + content (right)
#         root = QHBoxLayout(self)
#         root.setContentsMargins(0, 0, 0, 0)
#         root.setSpacing(0)

#         # -------------------------
#         # SIDEBAR
#         # -------------------------
#         self.sidebar = QListWidget()
#         self.sidebar.setObjectName("SettingsSidebar")
#         self.sidebar.setFixedWidth(200)
#         self.sidebar.setSpacing(4)
#         self.sidebar.setSelectionMode(QListWidget.SingleSelection)

#         items = ["Appearance", "Notifications", "Profiles", "Data & Storage", "About"]
#         for name in items:
#             item = QListWidgetItem(name)
#             item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
#             self.sidebar.addItem(item)

#         root.addWidget(self.sidebar)

#         # -------------------------
#         # STACKED PAGES
#         # -------------------------
#         self.stack = QStackedWidget()
#         root.addWidget(self.stack)

#         # Create pages
#         self.page_appearance = AppearancePage(main)
#         self.page_notifications = NotificationsPage(main)
#         self.page_profiles = ProfilesPage(main)
#         self.page_storage = DataStoragePage(main)
#         self.page_about = AboutPage(main)

#         # Add to stack
#         self.stack.addWidget(self.page_appearance)
#         self.stack.addWidget(self.page_notifications)
#         self.stack.addWidget(self.page_profiles)
#         self.stack.addWidget(self.page_storage)
#         self.stack.addWidget(self.page_about)

#         # Connect sidebar selection
#         self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)

#         # Default selection
#         self.sidebar.setCurrentRow(0)
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QLabel, QComboBox, QCheckBox
# )
# from PySide6.QtCore import Qt


# # ============================================================
# # APPEARANCE PAGE
# # ============================================================
# class AppearancePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)

#         title = QLabel("Appearance")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # Theme selector
#         theme_label = QLabel("Theme")
#         theme_label.setObjectName("SectionLabel")
#         layout.addWidget(theme_label)

#         self.theme_combo = QComboBox()
#         self.theme_combo.addItems(["light", "dark", "blue"])
#         self.theme_combo.setCurrentText(self.settings.get("theme"))
#         self.theme_combo.currentTextChanged.connect(self.change_theme)
#         layout.addWidget(self.theme_combo)

#         layout.addStretch()

#     def change_theme(self, theme_name):
#         self.settings.set("theme", theme_name)
#         self.main.apply_theme()   # Live preview


# # ============================================================
# # NOTIFICATIONS PAGE
# # ============================================================
# class NotificationsPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)

#         title = QLabel("Notifications")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # Enable break notifications
#         self.notify_toggle = QCheckBox("Enable Break Notifications")
#         self.notify_toggle.setChecked(self.settings.get("notifications_enabled", True))
#         self.notify_toggle.stateChanged.connect(self.toggle_notifications)
#         layout.addWidget(self.notify_toggle)

#         # Enable sound
#         self.sound_toggle = QCheckBox("Enable Notification Sound")
#         self.sound_toggle.setChecked(self.settings.get("sound_enabled", True))
#         self.sound_toggle.stateChanged.connect(self.toggle_sound)
#         layout.addWidget(self.sound_toggle)

#         layout.addStretch()

#     def toggle_notifications(self, state):
#         self.settings.set("notifications_enabled", bool(state))

#     def toggle_sound(self, state):
#         self.settings.set("sound_enabled", bool(state))
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QLabel, QComboBox, QPushButton,
#     QHBoxLayout, QMessageBox, QInputDialog
# )
# from PySide6.QtCore import Qt


# # ============================================================
# # PROFILES PAGE
# # ============================================================
# class ProfilesPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)

#         title = QLabel("Profiles")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # -------------------------
#         # Profile selector
#         # -------------------------
#         label = QLabel("Active Profile")
#         label.setObjectName("SectionLabel")
#         layout.addWidget(label)

#         row = QHBoxLayout()

#         self.profile_combo = QComboBox()
#         self.profile_combo.addItems(self.settings.list_profiles())
#         self.profile_combo.setCurrentText(self.settings.current_profile)
#         self.profile_combo.currentTextChanged.connect(self.switch_profile)
#         row.addWidget(self.profile_combo)

#         # Create profile
#         btn_new = QPushButton("New")
#         btn_new.clicked.connect(self.create_profile)
#         row.addWidget(btn_new)

#         # Delete profile
#         btn_delete = QPushButton("Delete")
#         btn_delete.clicked.connect(self.delete_profile)
#         row.addWidget(btn_delete)

#         layout.addLayout(row)
#         layout.addStretch()

#     # --------------------------------------------------------
#     # Switch profile
#     # --------------------------------------------------------
#     def switch_profile(self, name):
#         self.settings.switch_profile(name)
#         self.main.apply_theme()  # theme may differ per profile

#     # --------------------------------------------------------
#     # Create profile
#     # --------------------------------------------------------
#     def create_profile(self):
#         name, ok = QInputDialog.getText(
#             self, "Create Profile", "Enter profile name:"
#         )
#         if not ok or not name.strip():
#             return

#         name = name.strip()

#         if name in self.settings.list_profiles():
#             QMessageBox.warning(self, "Error", "A profile with this name already exists.")
#             return

#         self.settings.switch_profile(name)
#         self.refresh_ui()

#     # --------------------------------------------------------
#     # Delete profile
#     # --------------------------------------------------------
#     def delete_profile(self):
#         profile = self.profile_combo.currentText()

#         if profile == "default":
#             QMessageBox.warning(self, "Error", "You cannot delete the default profile.")
#             return

#         # Confirmation popup
#         confirm = QMessageBox.question(
#             self,
#             "Delete Profile",
#             f"This will permanently delete the profile '{profile}' and all its data.\n"
#             "This action cannot be undone.\n\n"
#             "Are you sure you want to continue?",
#             QMessageBox.Yes | QMessageBox.No
#         )

#         if confirm != QMessageBox.Yes:
#             return

#         self.settings.delete_profile(profile)
#         self.refresh_ui()

#     # --------------------------------------------------------
#     # Refresh UI
#     # --------------------------------------------------------
#     def refresh_ui(self):
#         self.profile_combo.clear()
#         self.profile_combo.addItems(self.settings.list_profiles())
#         self.profile_combo.setCurrentText(self.settings.current_profile)
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QFileDialog
# )
# from PySide6.QtCore import Qt


# # ============================================================
# # DATA & STORAGE PAGE
# # ============================================================
# class DataStoragePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings
#         self.engine = main.storage  # if needed for clearing data

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)

#         title = QLabel("Data & Storage")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # -------------------------
#         # EXPORT / IMPORT
#         # -------------------------
#         export_all_btn = QPushButton("Export All App Data")
#         export_all_btn.clicked.connect(self.export_all)
#         layout.addWidget(export_all_btn)

#         import_all_btn = QPushButton("Import All App Data")
#         import_all_btn.clicked.connect(self.import_all)
#         layout.addWidget(import_all_btn)

#         export_profile_btn = QPushButton("Export Current Profile")
#         export_profile_btn.clicked.connect(self.export_profile)
#         layout.addWidget(export_profile_btn)

#         import_profile_btn = QPushButton("Import Profile")
#         import_profile_btn.clicked.connect(self.import_profile)
#         layout.addWidget(import_profile_btn)

#         # -------------------------
#         # CLEAR DATA
#         # -------------------------
#         clear_analytics_btn = QPushButton("Clear Analytics Data")
#         clear_analytics_btn.clicked.connect(self.clear_analytics)
#         layout.addWidget(clear_analytics_btn)

#         clear_behavior_btn = QPushButton("Clear Behavior Logs")
#         clear_behavior_btn.clicked.connect(self.clear_behavior)
#         layout.addWidget(clear_behavior_btn)

#         clear_fatigue_btn = QPushButton("Clear Fatigue History")
#         clear_fatigue_btn.clicked.connect(self.clear_fatigue)
#         layout.addWidget(clear_fatigue_btn)

#         clear_breaks_btn = QPushButton("Clear Break History")
#         clear_breaks_btn.clicked.connect(self.clear_breaks)
#         layout.addWidget(clear_breaks_btn)

#         clear_supp_btn = QPushButton("Clear Suppression History")
#         clear_supp_btn.clicked.connect(self.clear_suppression)
#         layout.addWidget(clear_supp_btn)

#         layout.addStretch()

#     # ============================================================
#     # EXPORT / IMPORT
#     # ============================================================
#     def export_all(self):
#         path, ok = QFileDialog.getSaveFileName(
#             self, "Export All Data", "", "JSON Files (*.json)"
#         )
#         if ok and path:
#             self.settings.export_all_data(path)

#     def import_all(self):
#         path, ok = QFileDialog.getOpenFileName(
#             self, "Import All Data", "", "JSON Files (*.json)"
#         )
#         if ok and path:
#             self.settings.import_all_data(path)
#             self.main.apply_theme()

#     def export_profile(self):
#         path, ok = QFileDialog.getSaveFileName(
#             self, "Export Profile", "", "JSON Files (*.json)"
#         )
#         if ok and path:
#             self.settings.export_profile(path)

#     def import_profile(self):
#         path, ok = QFileDialog.getOpenFileName(
#             self, "Import Profile", "", "JSON Files (*.json)"
#         )
#         if ok and path:
#             self.settings.import_profile(path)
#             self.main.apply_theme()

#     # ============================================================
#     # CLEAR DATA (with confirmation popups)
#     # ============================================================
#     def _confirm(self, title, message):
#         return QMessageBox.question(
#             self, title, message,
#             QMessageBox.Yes | QMessageBox.No
#         ) == QMessageBox.Yes

#     def clear_analytics(self):
#         if self._confirm(
#             "Clear Analytics",
#             "This will permanently delete all analytics data for this profile.\n"
#             "AI Mode will need to relearn your patterns.\n\n"
#             "Are you sure?"
#         ):
#             self.engine.clear_analytics()

#     def clear_behavior(self):
#         if self._confirm(
#             "Clear Behavior Logs",
#             "This will permanently delete all behavior logs for this profile.\n"
#             "This action cannot be undone.\n\n"
#             "Are you sure?"
#         ):
#             self.engine.clear_behavior_logs()

#     def clear_fatigue(self):
#         if self._confirm(
#             "Clear Fatigue History",
#             "This will permanently delete all fatigue history.\n"
#             "AI Mode will need to relearn your fatigue curve.\n\n"
#             "Are you sure?"
#         ):
#             self.engine.clear_fatigue_history()

#     def clear_breaks(self):
#         if self._confirm(
#             "Clear Break History",
#             "This will permanently delete all break events.\n"
#             "This action cannot be undone.\n\n"
#             "Are you sure?"
#         ):
#             self.engine.clear_break_history()

#     def clear_suppression(self):
#         if self._confirm(
#             "Clear Suppression History",
#             "This will permanently delete all suppression events.\n"
#             "This action cannot be undone.\n\n"
#             "Are you sure?"
#         ):
#             self.engine.clear_suppression_history()
# import os
# from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
# from PySide6.QtCore import Qt


# # ============================================================
# # ABOUT PAGE
# # ============================================================
# class AboutPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)

#         title = QLabel("About")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # App name
#         name = QLabel("Wellbeing Assistant")
#         name.setObjectName("SectionLabel")
#         layout.addWidget(name)

#         # Version
#         version = QLabel("Version 1.0.0")
#         version.setObjectName("AnalyticsText")
#         layout.addWidget(version)

#         # Data folder
#         data_label = QLabel("Data Folder")
#         data_label.setObjectName("SectionLabel")
#         layout.addWidget(data_label)

#         data_path = QLabel(str(self.main.storage.db_path))
#         data_path.setTextInteractionFlags(Qt.TextSelectableByMouse)
#         layout.addWidget(data_path)

#         # Open folder button
#         btn_open = QPushButton("Open Data Folder")
#         btn_open.clicked.connect(self.open_folder)
#         layout.addWidget(btn_open)

#         # Credits
#         credits = QLabel("Created by Kirk‑Mends")
#         credits.setObjectName("AnalyticsText")
#         layout.addWidget(credits)

#         layout.addStretch()

#     def open_folder(self):
#         os.startfile(self.settings.data_folder)






















# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
#     QStackedWidget, QLabel, QComboBox, QCheckBox, QPushButton,
#     QMessageBox
# )
# from PySide6.QtCore import Qt
# import os


# # ============================================================
# # SETTINGS PAGE (ROOT)
# # ============================================================
# class SettingsPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         # Root layout: sidebar + content
#         root = QHBoxLayout(self)
#         root.setContentsMargins(0, 0, 0, 0)
#         root.setSpacing(0)

#         # -------------------------
#         # SIDEBAR
#         # -------------------------
#         self.sidebar = QListWidget()
#         self.sidebar.setObjectName("SettingsSidebar")
#         self.sidebar.setFixedWidth(200)
#         self.sidebar.setSpacing(4)
#         self.sidebar.setSelectionMode(QListWidget.SingleSelection)

#         # FINAL SIDEBAR ITEMS (NO PROFILES)
#         items = ["Appearance", "Notifications", "Data & Storage", "About"]
#         for name in items:
#             item = QListWidgetItem(name)
#             item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
#             self.sidebar.addItem(item)

#         root.addWidget(self.sidebar)

#         # -------------------------
#         # STACKED PAGES
#         # -------------------------
#         self.stack = QStackedWidget()
#         root.addWidget(self.stack)

#         # Create pages
#         self.page_appearance = AppearancePage(main)
#         self.page_notifications = NotificationsPage(main)
#         self.page_storage = DataStoragePage(main)
#         self.page_about = AboutPage(main)

#         # Add to stack
#         self.stack.addWidget(self.page_appearance)
#         self.stack.addWidget(self.page_notifications)
#         self.stack.addWidget(self.page_storage)
#         self.stack.addWidget(self.page_about)

#         # Connect sidebar selection
#         self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)

#         # Default selection
#         self.sidebar.setCurrentRow(0)
# # ============================================================
# # APPEARANCE PAGE
# # ============================================================
# class AppearancePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)

#         title = QLabel("Appearance")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # Theme selector
#         theme_label = QLabel("Theme")
#         theme_label.setObjectName("SectionLabel")
#         layout.addWidget(theme_label)

#         self.theme_combo = QComboBox()
#         self.theme_combo.addItems(["light", "dark", "blue"])
#         self.theme_combo.setCurrentText(self.settings.get("theme"))
#         self.theme_combo.currentTextChanged.connect(self.change_theme)
#         layout.addWidget(self.theme_combo)

#         layout.addStretch()

#     def change_theme(self, theme_name):
#         self.settings.set("theme", theme_name)
#         self.main.apply_theme()   # Live preview
# # ============================================================
# # NOTIFICATIONS PAGE
# # ============================================================
# class NotificationsPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)

#         title = QLabel("Notifications")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # Enable break notifications
#         self.notify_toggle = QCheckBox("Enable Break Notifications")
#         self.notify_toggle.setChecked(self.settings.get("notifications_enabled", True))
#         self.notify_toggle.stateChanged.connect(self.toggle_notifications)
#         layout.addWidget(self.notify_toggle)

#         # Enable sound
#         self.sound_toggle = QCheckBox("Enable Notification Sound")
#         self.sound_toggle.setChecked(self.settings.get("sound_enabled", True))
#         self.sound_toggle.stateChanged.connect(self.toggle_sound)
#         layout.addWidget(self.sound_toggle)

#         layout.addStretch()

#     def toggle_notifications(self, state):
#         self.settings.set("notifications_enabled", bool(state))

#     def toggle_sound(self, state):
#         self.settings.set("sound_enabled", bool(state))
# # ============================================================
# # DATA & STORAGE PAGE
# # ============================================================
# class DataStoragePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.engine = main.storage  # Correct engine (SQLite)

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)

#         title = QLabel("Data & Storage")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # -------------------------
#         # CLEAR DATA
#         # -------------------------
#         btn_clear_analytics = QPushButton("Clear All Analytics Data")
#         btn_clear_analytics.clicked.connect(self.clear_analytics)
#         layout.addWidget(btn_clear_analytics)

#         btn_clear_behavior = QPushButton("Clear Behavior Logs")
#         btn_clear_behavior.clicked.connect(self.clear_behavior)
#         layout.addWidget(btn_clear_behavior)

#         btn_clear_fatigue = QPushButton("Clear Fatigue History")
#         btn_clear_fatigue.clicked.connect(self.clear_fatigue)
#         layout.addWidget(btn_clear_fatigue)

#         btn_clear_breaks = QPushButton("Clear Break History")
#         btn_clear_breaks.clicked.connect(self.clear_breaks)
#         layout.addWidget(btn_clear_breaks)

#         btn_clear_supp = QPushButton("Clear Suppression History")
#         btn_clear_supp.clicked.connect(self.clear_suppression)
#         layout.addWidget(btn_clear_supp)

#         layout.addStretch()

#     # -------------------------
#     # Confirmation helper
#     # -------------------------
#     def _confirm(self, title, message):
#         return QMessageBox.question(
#             self, title, message,
#             QMessageBox.Yes | QMessageBox.No
#         ) == QMessageBox.Yes

#     # -------------------------
#     # Clear functions
#     # -------------------------
#     def clear_analytics(self):
#         if self._confirm("Clear Analytics",
#             "This will permanently delete ALL analytics data.\n"
#             "This action cannot be undone.\n\nContinue?"):
#             self.engine.clear_analytics()

#     def clear_behavior(self):
#         if self._confirm("Clear Behavior Logs",
#             "Delete all behavior logs?\nThis cannot be undone."):
#             self.engine.clear_behavior_logs()

#     def clear_fatigue(self):
#         if self._confirm("Clear Fatigue History",
#             "Delete all fatigue history?\nThis cannot be undone."):
#             self.engine.clear_fatigue_history()

#     def clear_breaks(self):
#         if self._confirm("Clear Break History",
#             "Delete all break events?\nThis cannot be undone."):
#             self.engine.clear_break_history()

#     def clear_suppression(self):
#         if self._confirm("Clear Suppression History",
#             "Delete all suppression events?\nThis cannot be undone."):
#             self.engine.clear_suppression_history()
# # ============================================================
# # ABOUT PAGE
# # ============================================================
# class AboutPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(30, 30, 30, 30)
#         layout.setSpacing(20)

#         title = QLabel("About")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # App name
#         name = QLabel("Digital Wellbeing Assistant")
#         name.setObjectName("SectionLabel")
#         layout.addWidget(name)

#         # Version
#         version = QLabel("Version 1.0.0")
#         layout.addWidget(version)

#         # Data file path
#         data_label = QLabel("Data File Location")
#         data_label.setObjectName("SectionLabel")
#         layout.addWidget(data_label)

#         data_path = QLabel(str(self.main.storage.db_path))
#         data_path.setTextInteractionFlags(Qt.TextSelectableByMouse)
#         layout.addWidget(data_path)

#         # Open folder button
#         btn_open = QPushButton("Open Data Folder")
#         btn_open.clicked.connect(self.open_folder)
#         layout.addWidget(btn_open)

#         # Credits
#         credits = QLabel("Created by Kirk‑Mends")
#         layout.addWidget(credits)

#         layout.addStretch()

#     def open_folder(self):
#         folder = os.path.dirname(str(self.main.storage.db_path))
#         os.startfile(folder)













# 26th March
# Design for apple review
# import os
# import platform
# import subprocess
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
#     QStackedWidget, QLabel, QComboBox, QCheckBox, QPushButton,
#     QMessageBox, QFrame, QFileDialog
# )
# from PySide6.QtCore import Qt

# # ============================================================
# # SETTINGS PAGE (ROOT)
# # ============================================================
# class SettingsPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         # Root layout: sidebar + content
#         root = QHBoxLayout(self)
#         root.setContentsMargins(0, 0, 0, 0)
#         root.setSpacing(0)

#         # -------------------------
#         # SIDEBAR
#         # -------------------------
#         self.sidebar = QListWidget()
#         self.sidebar.setObjectName("SettingsSidebar")
#         self.sidebar.setFixedWidth(220)
#         self.sidebar.setSpacing(6)
#         self.sidebar.setSelectionMode(QListWidget.SingleSelection)

#         # Sidebar Items with Icons
#         items = [
#             ("Appearance", "🎨"),
#             ("Notifications", "🔔"),
#             ("Data & Storage", "💾"),
#             ("About & Privacy", "🛡️")
#         ]
        
#         for name, icon in items:
#             item = QListWidgetItem(f"{icon}  {name}")
#             item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
#             self.sidebar.addItem(item)

#         root.addWidget(self.sidebar)

#         # -------------------------
#         # STACKED PAGES
#         # -------------------------
#         self.stack = QStackedWidget()
#         root.addWidget(self.stack)
        
#         self.setup_sidebar_style()

#         # Create sub-pages
#         self.page_appearance = AppearancePage(main)
#         self.page_notifications = NotificationsPage(main)
#         self.page_storage = DataStoragePage(main)
#         self.page_about = AboutPage(main)

#         # Add to stack in order of sidebar items
#         self.stack.addWidget(self.page_appearance)
#         self.stack.addWidget(self.page_notifications)
#         self.stack.addWidget(self.page_storage)
#         self.stack.addWidget(self.page_about)

#         # Connect sidebar selection
#         self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
#         self.sidebar.setCurrentRow(0)

#     def setup_sidebar_style(self):
#         # Keep original style
#         self.sidebar.setStyleSheet("""
#             QListWidget {
#                 background-color: rgba(128, 128, 128, 0.03);
#                 border: none;
#                 border-right: 1px solid rgba(128, 128, 128, 0.1);
#                 outline: none;
#                 padding: 15px 10px;
#             }
#             QListWidget::item {
#                 padding: 12px 15px;
#                 border-radius: 10px;
#                 margin-bottom: 4px;
#                 color: #64748B;
#                 font-weight: 500;
#             }
#             QListWidget::item:selected {
#                 background-color: palette(highlight);
#                 color: white;
#                 font-weight: 600;
#             }
#             QListWidget::item:hover:!selected {
#                 background-color: rgba(128, 128, 128, 0.08);
#             }
#         """)

# # ============================================================
# # APPEARANCE PAGE
# # ============================================================
# class AppearancePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(20)

#         title = QLabel("Appearance")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         theme_label = QLabel("Visual Theme")
#         theme_label.setObjectName("SectionLabel")
#         layout.addWidget(theme_label)

#         self.theme_combo = QComboBox()
#         self.theme_combo.addItems(["light", "dark", "blue"])
#         self.theme_combo.setCurrentText(self.settings.get("theme", "light"))
#         self.theme_combo.currentTextChanged.connect(self.change_theme)
#         layout.addWidget(self.theme_combo)
        
#         theme_desc = QLabel("Personalize the look and feel of your assistant. Changes apply instantly.")
#         theme_desc.setStyleSheet("color: #64748B; font-size: 11px;")
#         layout.addWidget(theme_desc)

#         layout.addStretch()

#     def change_theme(self, theme_name):
#         self.settings.set("theme", theme_name)
#         self.main.apply_theme()

# # ============================================================
# # NOTIFICATIONS PAGE
# # ============================================================
# class NotificationsPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(20)

#         title = QLabel("Notifications")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # DARK MODE CONTRAST FIX FOR SUBTITLES
#         is_dark = self.settings.get("theme") == "dark"
#         sub_color = "#94A3B8" if is_dark else title.palette().color(title.foregroundRole()).name()

#         # SECTION: GENERAL
#         general_label = QLabel("DELIVERY SETTINGS")
#         general_label.setStyleSheet(f"color: {sub_color}; font-weight: 800; font-size: 10px; letter-spacing: 1px;")
#         layout.addWidget(general_label)

#         self.notify_toggle = QCheckBox("Enable Break Notifications")
#         self.notify_toggle.setChecked(self.settings.get("notifications_enabled", True))
#         self.notify_toggle.stateChanged.connect(lambda s: self.settings.set("notifications_enabled", bool(s)))
#         layout.addWidget(self.notify_toggle)

#         self.sound_toggle = QCheckBox("Enable Audio Cues")
#         self.sound_toggle.setChecked(self.settings.get("sound_enabled", True))
#         self.sound_toggle.stateChanged.connect(lambda s: self.settings.set("sound_enabled", bool(s)))
#         layout.addWidget(self.sound_toggle)

#         layout.addSpacing(15)

#         # SECTION: PRIVACY
#         advanced_label = QLabel("NOTIFICATION PRIVACY")
#         advanced_label.setStyleSheet(f"color: {sub_color}; font-weight: 800; font-size: 10px; letter-spacing: 1px;")
#         layout.addWidget(advanced_label)

#         self.safe_mode_toggle = QCheckBox("Hide Sensitive Details (Safe Mode)")
#         self.safe_mode_toggle.setChecked(self.settings.get("safe_mode", False))
#         self.safe_mode_toggle.stateChanged.connect(lambda s: self.settings.set("safe_mode", bool(s)))
#         layout.addWidget(self.safe_mode_toggle)
        
#         safe_desc = QLabel("When enabled, notifications will not show specific behavioral data to keep your logs private in shared environments.")
#         safe_desc.setStyleSheet("color: #64748B; font-size: 11px; margin-left: 25px;")
#         safe_desc.setWordWrap(True)
#         layout.addWidget(safe_desc)

#         layout.addStretch()

# # ============================================================
# # DATA & STORAGE PAGE
# # ============================================================
# class DataStoragePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings
#         self.engine = main.storage

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(25)

#         title = QLabel("Data & Storage")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # DARK MODE CONTRAST FIX FOR SUBTITLES
#         is_dark = self.settings.get("theme") == "dark"
#         sub_color = "#94A3B8" if is_dark else title.palette().color(title.foregroundRole()).name()

#         # SECTION 1: EXPORT/IMPORT
#         backup_label = QLabel("PORTABILITY & BACKUPS")
#         backup_label.setStyleSheet(f"color: {sub_color}; font-weight: 800; font-size: 10px; letter-spacing: 1.2px;")
#         layout.addWidget(backup_label)

#         self.backup_group = QFrame()
#         self.backup_group.setStyleSheet(self._get_card_style(is_danger=False))
#         backup_layout = QVBoxLayout(self.backup_group)
        
#         btn_export = QPushButton(" 📤 Export History to JSON")
#         btn_export.clicked.connect(self.export_all)
#         backup_layout.addWidget(btn_export)

#         btn_import = QPushButton(" 📥 Import Archive Data")
#         btn_import.clicked.connect(self.import_all)
#         backup_layout.addWidget(btn_import)
#         layout.addWidget(self.backup_group)

#         # SECTION 2: CLEANUP
#         cleanup_label = QLabel("DANGER ZONE")
#         cleanup_label.setStyleSheet("color: #EF4444; font-weight: 800; font-size: 10px; letter-spacing: 1.2px;")
#         layout.addWidget(cleanup_label)

#         self.cleanup_group = QFrame()
#         self.cleanup_group.setStyleSheet(self._get_card_style(is_danger=True))
#         group_layout = QVBoxLayout(self.cleanup_group)

#         actions = [
#             ("Reset AI Analytics", self.clear_analytics),
#             ("Clear Behavior Logs", self.clear_behavior),
#             ("Clear Break History", self.clear_breaks)
#         ]

#         for text, slot in actions:
#             btn = QPushButton(f"  → {text}")
#             btn.clicked.connect(slot)
#             group_layout.addWidget(btn)

#         layout.addWidget(self.cleanup_group)
#         layout.addStretch()

#     def _get_card_style(self, is_danger=False):
#         is_dark = self.settings.get("theme") == "dark"
        
#         # Keep original logic but force contrast if Dark
#         base_text = "palette(text)"
#         if is_dark and not is_danger:
#             base_text = "#E2E8F0" # Light gray text for dark mode cards
            
#         color = "#EF4444" if is_danger else base_text
#         hover = "rgba(239, 68, 68, 0.1)" if is_danger else "rgba(128, 128, 128, 0.1)"
        
#         return f"QFrame {{ background: rgba(128, 128, 128, 0.05); border-radius: 12px; border: 1px solid rgba(128, 128, 128, 0.1); }} \
#                  QPushButton {{ background: transparent; border: none; text-align: left; padding: 12px; color: {color}; font-weight: 600; font-size: 12px; }} \
#                  QPushButton:hover {{ background: {hover}; border-radius: 10px; }}"

#     def export_all(self):
#         path, ok = QFileDialog.getSaveFileName(self, "Export Data", "", "JSON Files (*.json)")
#         if ok and path:
#             self.settings.export_all_data(path)
#             QMessageBox.information(self, "Export Success", "Data exported successfully.")

#     def import_all(self):
#         path, ok = QFileDialog.getOpenFileName(self, "Import Data", "", "JSON Files (*.json)")
#         if ok and path:
#             self.settings.import_all_data(path)
#             self.main.apply_theme()
#             QMessageBox.information(self, "Import Success", "Data imported successfully.")

#     def _confirm(self, title, message):
#         msg = QMessageBox(self)
#         msg.setWindowTitle(title)
#         msg.setText(message)
#         msg.setInformativeText("This will wipe learned AI patterns. This cannot be undone.")
#         msg.setIcon(QMessageBox.Warning)
#         msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
#         return msg.exec() == QMessageBox.Yes

#     def clear_analytics(self):
#         if self._confirm("Clear AI Data", "Permanently delete AI metrics?"): self.engine.clear_analytics()

#     def clear_behavior(self):
#         if self._confirm("Clear Logs", "Delete all behavior logs?"): self.engine.clear_behavior_logs()

#     def clear_breaks(self):
#         if self._confirm("Clear Breaks", "Delete all break history?"): self.engine.clear_break_history()

# # ============================================================
# # ABOUT & PRIVACY PAGE
# # ============================================================
# class AboutPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         is_dark = self.main.settings.get("theme") == "dark"

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(25)

#         title = QLabel("About & Privacy")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # PRIVACY CARD (Dark Mode Overrides)
#         bg = "rgba(34, 197, 94, 0.1)" if is_dark else "rgba(34, 197, 94, 0.05)"
#         text_color = "#BBF7D0" if is_dark else "palette(text)"
        
#         privacy_card = QFrame()
#         privacy_card.setStyleSheet(f"QFrame {{ background: {bg}; border-radius: 12px; border: 1px solid rgba(34, 197, 94, 0.2); padding: 15px; }}")
#         p_lay = QVBoxLayout(privacy_card)
#         p_text = QLabel("🔒 <b>Local-First Privacy</b><br>All behavior logs and AI insights are stored locally on your device. No data is ever shared or uploaded to the cloud.")
#         p_text.setWordWrap(True)
#         p_text.setStyleSheet(f"font-size: 12px; color: {text_color};")
#         p_lay.addWidget(p_text)
#         layout.addWidget(privacy_card)

#         # APP INFO
#         info_lay = QVBoxLayout()
#         name = QLabel("Digital Wellbeing Assistant")
#         name.setStyleSheet("font-size: 16px; font-weight: bold;")
#         version = QLabel("Version 1.0.0 • Build Stable")
#         version.setStyleSheet("color: #64748B; font-size: 12px;")
#         info_lay.addWidget(name)
#         info_lay.addWidget(version)
#         layout.addLayout(info_lay)

#         btn_update = QPushButton("🚀 Check for Updates")
#         btn_update.clicked.connect(lambda: QMessageBox.information(self, "Update", "You are up to date!"))
#         layout.addWidget(btn_update)

#         # DATA PATH
#         path_label = QLabel("DATA FOLDER")
#         path_label.setObjectName("SectionLabel")
#         layout.addWidget(path_label)

#         self.path_display = QLabel(str(self.main.storage.db_path))
#         self.path_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
#         # Path Box Contrast fix
#         path_bg = "rgba(255, 255, 255, 0.08)" if is_dark else "rgba(128, 128, 128, 0.1)"
#         self.path_display.setStyleSheet(f"background: {path_bg}; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 11px;")
#         layout.addWidget(self.path_display)

#         btn_open = QPushButton("📂 Open Data Folder")
#         btn_open.clicked.connect(self.open_folder)
#         layout.addWidget(btn_open)

#         layout.addStretch()
#         credits = QLabel("Created by Kirk‑Mends")
#         credits.setAlignment(Qt.AlignCenter)
#         credits.setStyleSheet("color: #94A3B8; font-size: 11px;")
#         layout.addWidget(credits)

#     def open_folder(self):
#         path = os.path.dirname(str(self.main.storage.db_path))
#         if platform.system() == "Windows": os.startfile(path)
#         elif platform.system() == "Darwin": subprocess.Popen(["open", path])
#         else: subprocess.Popen(["xdg-open", path])















#EDITING TO MAKE IT WORK But is still didn't

# import os
# import platform
# import subprocess
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
#     QStackedWidget, QLabel, QComboBox, QCheckBox, QPushButton,
#     QMessageBox, QFrame, QFileDialog
# )
# from PySide6.QtCore import Qt

# # ============================================================
# # SETTINGS PAGE (ROOT)
# # ============================================================
# class SettingsPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         # Root layout: sidebar + content
#         root = QHBoxLayout(self)
#         root.setContentsMargins(0, 0, 0, 0)
#         root.setSpacing(0)

#         # -------------------------
#         # SIDEBAR
#         # -------------------------
#         self.sidebar = QListWidget()
#         self.sidebar.setObjectName("SettingsSidebar")
#         self.sidebar.setFixedWidth(220)
#         self.sidebar.setSpacing(6)
#         self.sidebar.setSelectionMode(QListWidget.SingleSelection)

#         # Sidebar Items with Icons
#         items = [
#             ("Appearance", "🎨"),
#             ("Notifications", "🔔"),
#             ("Data & Storage", "💾"),
#             ("About & Privacy", "🛡️")
#         ]
        
#         for name, icon in items:
#             item = QListWidgetItem(f"{icon}  {name}")
#             item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
#             self.sidebar.addItem(item)

#         root.addWidget(self.sidebar)

#         # -------------------------
#         # STACKED PAGES
#         # -------------------------
#         self.stack = QStackedWidget()
#         root.addWidget(self.stack)
        
#         self.setup_sidebar_style()

#         # Create sub-pages
#         self.page_appearance = AppearancePage(main)
#         self.page_notifications = NotificationsPage(main)
#         self.page_storage = DataStoragePage(main)
#         self.page_about = AboutPage(main)

#         # Add to stack in order of sidebar items
#         self.stack.addWidget(self.page_appearance)
#         self.stack.addWidget(self.page_notifications)
#         self.stack.addWidget(self.page_storage)
#         self.stack.addWidget(self.page_about)

#         # Connect sidebar selection
#         self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
#         self.sidebar.setCurrentRow(0)

#     def setup_sidebar_style(self):
#         # Keep original style
#         self.sidebar.setStyleSheet("""
#             QListWidget {
#                 background-color: rgba(128, 128, 128, 0.03);
#                 border: none;
#                 border-right: 1px solid rgba(128, 128, 128, 0.1);
#                 outline: none;
#                 padding: 15px 10px;
#             }
#             QListWidget::item {
#                 padding: 12px 15px;
#                 border-radius: 10px;
#                 margin-bottom: 4px;
#                 color: #64748B;
#                 font-weight: 500;
#             }
#             QListWidget::item:selected {
#                 background-color: palette(highlight);
#                 color: white;
#                 font-weight: 600;
#             }
#             QListWidget::item:hover:!selected {
#                 background-color: rgba(128, 128, 128, 0.08);
#             }
#         """)

# # ============================================================
# # APPEARANCE PAGE
# # ============================================================
# class AppearancePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(20)

#         title = QLabel("Appearance")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         theme_label = QLabel("Visual Theme")
#         theme_label.setObjectName("SectionLabel")
#         layout.addWidget(theme_label)

#         self.theme_combo = QComboBox()
#         self.theme_combo.addItems(["light", "dark", "blue"])
#         self.theme_combo.setCurrentText(self.settings.get("theme", "light"))
#         self.theme_combo.currentTextChanged.connect(self.change_theme)
#         layout.addWidget(self.theme_combo)
        
#         theme_desc = QLabel("Personalize the look and feel of your assistant. Changes apply instantly.")
#         theme_desc.setStyleSheet("color: #64748B; font-size: 11px;")
#         layout.addWidget(theme_desc)

#         layout.addStretch()

#     def change_theme(self, theme_name):
#         self.settings.set("theme", theme_name)
#         self.main.apply_theme()

# # ============================================================
# # NOTIFICATIONS PAGE
# # ============================================================
# class NotificationsPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(20)

#         title = QLabel("Notifications")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # CHANGE 1: Subtitles Cream White for Dark Mode
#         is_dark = self.settings.get("theme") == "dark"
#         sub_color = "#E2E8F0" if is_dark else title.palette().color(title.foregroundRole()).name()

#         # SECTION: GENERAL
#         general_label = QLabel("DELIVERY SETTINGS")
#         general_label.setStyleSheet(f"color: {sub_color}; font-weight: 800; font-size: 10px; letter-spacing: 1px;")
#         layout.addWidget(general_label)

#         self.notify_toggle = QCheckBox("Enable Break Notifications")
#         self.notify_toggle.setChecked(self.settings.get("notifications_enabled", True))
#         self.notify_toggle.stateChanged.connect(lambda s: self.settings.set("notifications_enabled", bool(s)))
#         layout.addWidget(self.notify_toggle)

#         self.sound_toggle = QCheckBox("Enable Audio Cues")
#         self.sound_toggle.setChecked(self.settings.get("sound_enabled", True))
#         self.sound_toggle.stateChanged.connect(lambda s: self.settings.set("sound_enabled", bool(s)))
#         layout.addWidget(self.sound_toggle)

#         layout.addSpacing(15)

#         # SECTION: PRIVACY
#         advanced_label = QLabel("NOTIFICATION PRIVACY")
#         advanced_label.setStyleSheet(f"color: {sub_color}; font-weight: 800; font-size: 10px; letter-spacing: 1px;")
#         layout.addWidget(advanced_label)

#         self.safe_mode_toggle = QCheckBox("Hide Sensitive Details (Safe Mode)")
#         self.safe_mode_toggle.setChecked(self.settings.get("safe_mode", False))
#         self.safe_mode_toggle.stateChanged.connect(lambda s: self.settings.set("safe_mode", bool(s)))
#         layout.addWidget(self.safe_mode_toggle)
        
#         safe_desc = QLabel("When enabled, notifications will not show specific behavioral data to keep your logs private in shared environments.")
#         safe_desc.setStyleSheet("color: #64748B; font-size: 11px; margin-left: 25px;")
#         safe_desc.setWordWrap(True)
#         layout.addWidget(safe_desc)

#         layout.addStretch()

# # ============================================================
# # DATA & STORAGE PAGE
# # ============================================================
# class DataStoragePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings
#         self.engine = main.storage

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(25)

#         title = QLabel("Data & Storage")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # CHANGE 1 (cont): Subtitle Cream White for Dark Mode
#         is_dark = self.settings.get("theme") == "dark"
#         sub_color = "#E2E8F0" if is_dark else title.palette().color(title.foregroundRole()).name()

#         # SECTION 1: EXPORT/IMPORT
#         backup_label = QLabel("PORTABILITY & BACKUPS")
#         backup_label.setStyleSheet(f"color: {sub_color}; font-weight: 800; font-size: 10px; letter-spacing: 1.2px;")
#         layout.addWidget(backup_label)

#         self.backup_group = QFrame()
#         self.backup_group.setStyleSheet(self._get_card_style(is_danger=False))
#         backup_layout = QVBoxLayout(self.backup_group)
        
#         btn_export = QPushButton(" 📤 Export History to JSON")
#         btn_export.clicked.connect(self.export_all)
#         backup_layout.addWidget(btn_export)

#         btn_import = QPushButton(" 📥 Import Archive Data")
#         btn_import.clicked.connect(self.import_all)
#         backup_layout.addWidget(btn_import)
#         layout.addWidget(self.backup_group)

#         # SECTION 2: CLEANUP
#         cleanup_label = QLabel("DANGER ZONE")
#         cleanup_label.setStyleSheet("color: #EF4444; font-weight: 800; font-size: 10px; letter-spacing: 1.2px;")
#         layout.addWidget(cleanup_label)

#         self.cleanup_group = QFrame()
#         self.cleanup_group.setStyleSheet(self._get_card_style(is_danger=True))
#         group_layout = QVBoxLayout(self.cleanup_group)

#         actions = [
#             ("Reset AI Analytics", self.clear_analytics),
#             ("Clear Behavior Logs", self.clear_behavior),
#             ("Clear Break History", self.clear_breaks)
#         ]

#         for text, slot in actions:
#             btn = QPushButton(f"  → {text}")
#             btn.clicked.connect(slot)
#             group_layout.addWidget(btn)

#         layout.addWidget(self.cleanup_group)
#         layout.addStretch()

#     def _get_card_style(self, is_danger=False):
#         is_dark = self.settings.get("theme") == "dark"
        
#         # CHANGE 2: White text (#FFFFFF) for Export/Import Buttons only in Dark Mode
#         base_text = "palette(text)"
#         if is_dark and not is_danger:
#             base_text = "#FFFFFF" 
            
#         color = "#EF4444" if is_danger else base_text
#         hover = "rgba(239, 68, 68, 0.1)" if is_danger else "rgba(128, 128, 128, 0.1)"
        
#         return f"QFrame {{ background: rgba(128, 128, 128, 0.05); border-radius: 12px; border: 1px solid rgba(128, 128, 128, 0.1); }} \
#                  QPushButton {{ background: transparent; border: none; text-align: left; padding: 12px; color: {color}; font-weight: 600; font-size: 12px; }} \
#                  QPushButton:hover {{ background: {hover}; border-radius: 10px; }}"

#     def export_all(self):
#         path, ok = QFileDialog.getSaveFileName(self, "Export Data", "", "JSON Files (*.json)")
#         if ok and path:
#             self.settings.export_all_data(path)
#             QMessageBox.information(self, "Export Success", "Data exported successfully.")

#     def import_all(self):
#         path, ok = QFileDialog.getOpenFileName(self, "Import Data", "", "JSON Files (*.json)")
#         if ok and path:
#             self.settings.import_all_data(path)
#             self.main.apply_theme()
#             QMessageBox.information(self, "Import Success", "Data imported successfully.")

#     def _confirm(self, title, message):
#         msg = QMessageBox(self)
#         msg.setWindowTitle(title)
#         msg.setText(message)
#         msg.setInformativeText("This will wipe learned AI patterns. This cannot be undone.")
#         msg.setIcon(QMessageBox.Warning)
#         msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
#         return msg.exec() == QMessageBox.Yes

#     def clear_analytics(self):
#         if self._confirm("Clear AI Data", "Permanently delete AI metrics?"): self.engine.clear_analytics()

#     def clear_behavior(self):
#         if self._confirm("Clear Logs", "Delete all behavior logs?"): self.engine.clear_behavior_logs()

#     def clear_breaks(self):
#         if self._confirm("Clear Breaks", "Delete all break history?"): self.engine.clear_break_history()

# # ============================================================
# # ABOUT & PRIVACY PAGE
# # ============================================================
# class AboutPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         is_dark = self.main.settings.get("theme") == "dark"

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(25)

#         title = QLabel("About & Privacy")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # CHANGE 3: Writing inside green box White (#FFFFFF) only in Dark Mode
#         bg = "rgba(34, 197, 94, 0.1)" if is_dark else "rgba(34, 197, 94, 0.05)"
#         text_color = "#FFFFFF" if is_dark else "palette(text)"
        
#         privacy_card = QFrame()
#         privacy_card.setStyleSheet(f"QFrame {{ background: {bg}; border-radius: 12px; border: 1px solid rgba(34, 197, 94, 0.2); padding: 15px; }}")
#         p_lay = QVBoxLayout(privacy_card)
#         p_text = QLabel("🔒 <b>Local-First Privacy</b><br>All behavior logs and AI insights are stored locally on your device. No data is ever shared or uploaded to the cloud.")
#         p_text.setWordWrap(True)
#         p_text.setStyleSheet(f"font-size: 12px; color: {text_color};")
#         p_lay.addWidget(p_text)
#         layout.addWidget(privacy_card)

#         # APP INFO
#         info_lay = QVBoxLayout()
#         name = QLabel("Digital Wellbeing Assistant")
#         name.setStyleSheet("font-size: 16px; font-weight: bold;")
#         version = QLabel("Version 1.0.0 • Build Stable")
#         version.setStyleSheet("color: #64748B; font-size: 12px;")
#         info_lay.addWidget(name)
#         info_lay.addWidget(version)
#         layout.addLayout(info_lay)

#         btn_update = QPushButton("🚀 Check for Updates")
#         btn_update.clicked.connect(lambda: QMessageBox.information(self, "Update", "You are up to date!"))
#         layout.addWidget(btn_update)

#         # DATA PATH
#         path_label = QLabel("DATA FOLDER")
#         path_label.setObjectName("SectionLabel")
#         layout.addWidget(path_label)

#         self.path_display = QLabel(str(self.main.storage.db_path))
#         self.path_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
#         # Path Box Contrast fix for dark mode
#         path_bg = "rgba(255, 255, 255, 0.08)" if is_dark else "rgba(128, 128, 128, 0.1)"
#         self.path_display.setStyleSheet(f"background: {path_bg}; padding: 10px; border-radius: 6px; font-family: monospace; font-size: 11px;")
#         layout.addWidget(self.path_display)

#         btn_open = QPushButton("📂 Open Data Folder")
#         btn_open.clicked.connect(self.open_folder)
#         layout.addWidget(btn_open)

#         layout.addStretch()
#         credits = QLabel("Created by Kirk‑Mends")
#         credits.setAlignment(Qt.AlignCenter)
#         credits.setStyleSheet("color: #94A3B8; font-size: 11px;")
#         layout.addWidget(credits)

#     def open_folder(self):
#         path = os.path.dirname(str(self.main.storage.db_path))
#         if platform.system() == "Windows": os.startfile(path)
#         elif platform.system() == "Darwin": subprocess.Popen(["open", path])
#         else: subprocess.Popen(["xdg-open", path])














# This edit used the qss

# import os
# import platform
# import subprocess
# from PySide6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
#     QStackedWidget, QLabel, QComboBox, QCheckBox, QPushButton,
#     QMessageBox, QFrame, QFileDialog
# )
# from PySide6.QtCore import Qt

# # ============================================================
# # SETTINGS PAGE (ROOT)
# # ============================================================
# class SettingsPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         root = QHBoxLayout(self)
#         root.setContentsMargins(0, 0, 0, 0)
#         root.setSpacing(0)

#         # SIDEBAR
#         self.sidebar = QListWidget()
#         self.sidebar.setObjectName("SettingsSidebar")
#         self.sidebar.setFixedWidth(220)
#         self.sidebar.setSpacing(6)
#         self.sidebar.setSelectionMode(QListWidget.SingleSelection)

#         items = [
#             ("Appearance", "🎨"),
#             ("Notifications", "🔔"),
#             ("Data & Storage", "💾"),
#             ("About & Privacy", "🛡️")
#         ]
        
#         for name, icon in items:
#             item = QListWidgetItem(f"{icon}  {name}")
#             item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
#             self.sidebar.addItem(item)

#         root.addWidget(self.sidebar)

#         # STACKED PAGES
#         self.stack = QStackedWidget()
#         root.addWidget(self.stack)
        
#         self.setup_sidebar_style()

#         self.page_appearance = AppearancePage(main)
#         self.page_notifications = NotificationsPage(main)
#         self.page_storage = DataStoragePage(main)
#         self.page_about = AboutPage(main)

#         self.stack.addWidget(self.page_appearance)
#         self.stack.addWidget(self.page_notifications)
#         self.stack.addWidget(self.page_storage)
#         self.stack.addWidget(self.page_about)

#         self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
#         self.sidebar.setCurrentRow(0)

#     def setup_sidebar_style(self):
#         self.sidebar.setStyleSheet("""
#             QListWidget {
#                 background-color: rgba(128, 128, 128, 0.03);
#                 border: none;
#                 border-right: 1px solid rgba(128, 128, 128, 0.1);
#                 outline: none;
#                 padding: 15px 10px;
#             }
#             QListWidget::item {
#                 padding: 12px 15px;
#                 border-radius: 10px;
#                 margin-bottom: 4px;
#                 color: #64748B;
#                 font-weight: 500;
#             }
#             QListWidget::item:selected {
#                 background-color: palette(highlight);
#                 color: white;
#                 font-weight: 600;
#             }
#             QListWidget::item:hover:!selected {
#                 background-color: rgba(128, 128, 128, 0.08);
#             }
#         """)

# # ============================================================
# # APPEARANCE PAGE
# # ============================================================
# class AppearancePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(20)

#         title = QLabel("Appearance")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         theme_label = QLabel("Visual Theme")
#         theme_label.setObjectName("SectionLabel")
#         layout.addWidget(theme_label)

#         self.theme_combo = QComboBox()
#         self.theme_combo.addItems(["light", "dark", "blue"])
#         self.theme_combo.setCurrentText(self.settings.get("theme", "light"))
#         self.theme_combo.currentTextChanged.connect(self.change_theme)
#         layout.addWidget(self.theme_combo)
        
#         theme_desc = QLabel("Personalize the look and feel of your assistant. Changes apply instantly.")
#         theme_desc.setStyleSheet("color: #64748B; font-size: 11px;")
#         layout.addWidget(theme_desc)

#         layout.addStretch()

#     def change_theme(self, theme_name):
#         self.settings.set("theme", theme_name)
#         self.main.apply_theme()

# # ============================================================
# # NOTIFICATIONS PAGE
# # ============================================================
# class NotificationsPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(20)

#         title = QLabel("Notifications")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # SECTION: GENERAL
#         general_label = QLabel("DELIVERY SETTINGS")
#         general_label.setObjectName("SectionLabel")
#         layout.addWidget(general_label)

#         self.notify_toggle = QCheckBox("Enable Break Notifications")
#         self.notify_toggle.setChecked(self.settings.get("notifications_enabled", True))
#         self.notify_toggle.stateChanged.connect(lambda s: self.settings.set("notifications_enabled", bool(s)))
#         layout.addWidget(self.notify_toggle)

#         self.sound_toggle = QCheckBox("Enable Audio Cues")
#         self.sound_toggle.setChecked(self.settings.get("sound_enabled", True))
#         self.sound_toggle.stateChanged.connect(lambda s: self.settings.set("sound_enabled", bool(s)))
#         layout.addWidget(self.sound_toggle)

#         layout.addSpacing(15)

#         # SECTION: PRIVACY
#         advanced_label = QLabel("NOTIFICATION PRIVACY")
#         advanced_label.setObjectName("SectionLabel")
#         layout.addWidget(advanced_label)

#         self.safe_mode_toggle = QCheckBox("Hide Sensitive Details (Safe Mode)")
#         self.safe_mode_toggle.setChecked(self.settings.get("safe_mode", False))
#         self.safe_mode_toggle.stateChanged.connect(lambda s: self.settings.set("safe_mode", bool(s)))
#         layout.addWidget(self.safe_mode_toggle)
        
#         safe_desc = QLabel("When enabled, notifications will not show behavioral data to keep logs private.")
#         safe_desc.setStyleSheet("color: #64748B; font-size: 11px; margin-left: 25px;")
#         safe_desc.setWordWrap(True)
#         layout.addWidget(safe_desc)

#         layout.addStretch()

# # ============================================================
# # DATA & STORAGE PAGE
# # ============================================================
# class DataStoragePage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main
#         self.settings = main.settings
#         self.engine = main.storage

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(25)

#         title = QLabel("Data & Storage")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # SECTION 1: EXPORT/IMPORT
#         backup_label = QLabel("PORTABILITY & BACKUPS")
#         backup_label.setObjectName("SectionLabel")
#         layout.addWidget(backup_label)

#         self.backup_group = QFrame()
#         self.backup_group.setStyleSheet(self._get_card_style(is_danger=False))
#         backup_layout = QVBoxLayout(self.backup_group)
        
#         btn_export = QPushButton(" 📤 Export History to JSON")
#         btn_export.clicked.connect(self.export_all)
#         backup_layout.addWidget(btn_export)

#         btn_import = QPushButton(" 📥 Import Archive Data")
#         btn_import.clicked.connect(self.import_all)
#         backup_layout.addWidget(btn_import)
#         layout.addWidget(self.backup_group)

#         # SECTION 2: CLEANUP
#         cleanup_label = QLabel("DANGER ZONE")
#         cleanup_label.setObjectName("SectionLabel") 
#         # Note: We'll keep the Danger Zone red via CSS QPushButton[text*="→"]
#         layout.addWidget(cleanup_label)

#         self.cleanup_group = QFrame()
#         self.cleanup_group.setStyleSheet(self._get_card_style(is_danger=True))
#         group_layout = QVBoxLayout(self.cleanup_group)

#         actions = [
#             ("Reset AI Analytics", self.clear_analytics),
#             ("Clear Behavior Logs", self.clear_behavior),
#             ("Clear Break History", self.clear_breaks)
#         ]

#         for text, slot in actions:
#             btn = QPushButton(f"  → {text}")
#             btn.clicked.connect(slot)
#             group_layout.addWidget(btn)

#         layout.addWidget(self.cleanup_group)
#         layout.addStretch()

#     def _get_card_style(self, is_danger=False):
#         # We removed the color property here so CSS can take over
#         hover = "rgba(239, 68, 68, 0.1)" if is_danger else "rgba(128, 128, 128, 0.1)"
        
#         return f"""
#             QFrame {{ 
#                 background: rgba(128, 128, 128, 0.05); 
#                 border-radius: 12px; 
#                 border: 1px solid rgba(128, 128, 128, 0.1); 
#             }}
#             QPushButton {{ 
#                 background: transparent; 
#                 border: none; 
#                 text-align: left; 
#                 padding: 12px; 
#                 font-weight: 600; 
#                 font-size: 12px; 
#             }}
#             QPushButton:hover {{ 
#                 background: {hover}; 
#                 border-radius: 10px; 
#             }}
#         """

#     def export_all(self):
#         path, ok = QFileDialog.getSaveFileName(self, "Export Data", "", "JSON Files (*.json)")
#         if ok and path:
#             self.settings.export_all_data(path)
#             QMessageBox.information(self, "Export Success", "Data exported successfully.")

#     def import_all(self):
#         path, ok = QFileDialog.getOpenFileName(self, "Import Data", "", "JSON Files (*.json)")
#         if ok and path:
#             self.settings.import_all_data(path)
#             self.main.apply_theme()
#             QMessageBox.information(self, "Import Success", "Data imported successfully.")

#     def _confirm(self, title, message):
#         msg = QMessageBox(self)
#         msg.setWindowTitle(title)
#         msg.setText(message)
#         msg.setInformativeText("This will wipe learned AI patterns. This cannot be undone.")
#         msg.setIcon(QMessageBox.Warning)
#         msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
#         return msg.exec() == QMessageBox.Yes

#     def clear_analytics(self):
#         if self._confirm("Clear AI Data", "Permanently delete AI metrics?"): self.engine.clear_analytics()

#     def clear_behavior(self):
#         if self._confirm("Clear Logs", "Delete all behavior logs?"): self.engine.clear_behavior_logs()

#     def clear_breaks(self):
#         if self._confirm("Clear Breaks", "Delete all break history?"): self.engine.clear_break_history()

# # ============================================================
# # ABOUT & PRIVACY PAGE
# # ============================================================
# class AboutPage(QWidget):
#     def __init__(self, main):
#         super().__init__()
#         self.main = main

#         layout = QVBoxLayout(self)
#         layout.setContentsMargins(35, 35, 35, 35)
#         layout.setSpacing(25)

#         title = QLabel("About & Privacy")
#         title.setObjectName("PageTitle")
#         layout.addWidget(title)

#         # PRIVACY CARD 
#         privacy_card = QFrame()
#         privacy_card.setStyleSheet("QFrame { background: rgba(34, 197, 94, 0.1); border-radius: 12px; border: 1px solid rgba(34, 197, 94, 0.2); padding: 15px; }")
#         p_lay = QVBoxLayout(privacy_card)
#         p_text = QLabel("🔒 <b>Local-First Privacy</b><br>All behavior logs and AI insights are stored locally on your device. No data is ever shared or uploaded to the cloud.")
#         p_text.setWordWrap(True)
#         # We removed the hardcoded color from here:
#         p_text.setStyleSheet("font-size: 12px;") 
#         p_lay.addWidget(p_text)
#         layout.addWidget(privacy_card)

#         # APP INFO
#         info_lay = QVBoxLayout()
#         name = QLabel("Digital Wellbeing Assistant")
#         name.setStyleSheet("font-size: 16px; font-weight: bold;")
#         version = QLabel("Version 1.0.0 • Build Stable")
#         version.setStyleSheet("color: #64748B; font-size: 12px;")
#         info_lay.addWidget(name)
#         info_lay.addWidget(version)
#         layout.addLayout(info_lay)

#         btn_update = QPushButton("🚀 Check for Updates")
#         btn_update.clicked.connect(lambda: QMessageBox.information(self, "Update", "You are up to date!"))
#         layout.addWidget(btn_update)

#         # DATA PATH
#         path_label = QLabel("DATA FOLDER")
#         path_label.setObjectName("SectionLabel")
#         layout.addWidget(path_label)

#         self.path_display = QLabel(str(self.main.storage.db_path))
#         self.path_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        
#         # We only keep layout styling here, CSS handles the color
#         self.path_display.setStyleSheet("padding: 10px; border-radius: 6px; font-family: monospace; font-size: 11px;")
#         layout.addWidget(self.path_display)

#         btn_open = QPushButton("📂 Open Data Folder")
#         btn_open.clicked.connect(self.open_folder)
#         layout.addWidget(btn_open)

#         layout.addStretch()
#         credits = QLabel("Created by Kirk‑Mends")
#         credits.setAlignment(Qt.AlignCenter)
#         credits.setStyleSheet("color: #94A3B8; font-size: 11px;")
#         layout.addWidget(credits)

#     def open_folder(self):
#         path = os.path.dirname(str(self.main.storage.db_path))
#         if platform.system() == "Windows": os.startfile(path)
#         elif platform.system() == "Darwin": subprocess.Popen(["open", path])
#         else: subprocess.Popen(["xdg-open", path])












import os
import platform
import subprocess
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem,
    QStackedWidget, QLabel, QComboBox, QCheckBox, QPushButton,
    QMessageBox, QFrame, QFileDialog
)
from PySide6.QtCore import Qt

# ============================================================
# SETTINGS PAGE (ROOT)
# ============================================================
class SettingsPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.settings = main.settings

        root = QHBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        # SIDEBAR
        self.sidebar = QListWidget()
        self.sidebar.setObjectName("SettingsSidebar")
        self.sidebar.setFixedWidth(220)
        self.sidebar.setSpacing(6)
        self.sidebar.setSelectionMode(QListWidget.SingleSelection)

        items = [
            ("Appearance", "🎨"),
            ("Notifications", "🔔"),
            ("Data & Storage", "💾"),
            ("About & Privacy", "🛡️")
        ]
        
        for name, icon in items:
            item = QListWidgetItem(f"{icon}  {name}")
            item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.sidebar.addItem(item)

        root.addWidget(self.sidebar)

        # STACKED PAGES
        self.stack = QStackedWidget()
        root.addWidget(self.stack)
        
        self.setup_sidebar_style()

        self.page_appearance = AppearancePage(main)
        self.page_notifications = NotificationsPage(main)
        self.page_storage = DataStoragePage(main)
        self.page_about = AboutPage(main)

        self.stack.addWidget(self.page_appearance)
        self.stack.addWidget(self.page_notifications)
        self.stack.addWidget(self.page_storage)
        self.stack.addWidget(self.page_about)

        self.sidebar.currentRowChanged.connect(self.stack.setCurrentIndex)
        self.sidebar.setCurrentRow(0)

    def setup_sidebar_style(self):
        self.sidebar.setStyleSheet("""
            QListWidget {
                background-color: rgba(128, 128, 128, 0.03);
                border: none;
                border-right: 1px solid rgba(128, 128, 128, 0.1);
                outline: none;
                padding: 15px 10px;
            }
            QListWidget::item {
                padding: 12px 15px;
                border-radius: 10px;
                margin-bottom: 4px;
                color: #64748B;
                font-weight: 500;
            }
            QListWidget::item:selected {
                background-color: palette(highlight);
                color: white;
                font-weight: 600;
            }
            QListWidget::item:hover:!selected {
                background-color: rgba(128, 128, 128, 0.08);
            }
        """)

# ============================================================
# APPEARANCE PAGE
# ============================================================
class AppearancePage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.settings = main.settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(20)

        title = QLabel("Appearance")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        theme_label = QLabel("Visual Theme")
        theme_label.setObjectName("SectionLabel")
        layout.addWidget(theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["light", "dark", "blue"])
        self.theme_combo.setCurrentText(self.settings.get("theme", "light"))
        self.theme_combo.currentTextChanged.connect(self.change_theme)
        layout.addWidget(self.theme_combo)
        
        theme_desc = QLabel("Personalize the look and feel of your assistant. Changes apply instantly.")
        theme_desc.setStyleSheet("color: #64748B; font-size: 11px;")
        layout.addWidget(theme_desc)

        layout.addStretch()

    def change_theme(self, theme_name):
        self.settings.set("theme", theme_name)
        self.main.apply_theme()

# ============================================================
# NOTIFICATIONS PAGE
# ============================================================
class NotificationsPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.settings = main.settings

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(20)

        title = QLabel("Notifications")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        general_label = QLabel("DELIVERY SETTINGS")
        general_label.setObjectName("SectionLabel")
        layout.addWidget(general_label)

        self.notify_toggle = QCheckBox("Enable Break Notifications")
        self.notify_toggle.setChecked(self.settings.get("notifications_enabled", True))
        self.notify_toggle.stateChanged.connect(lambda s: self.settings.set("notifications_enabled", bool(s)))
        layout.addWidget(self.notify_toggle)

        self.sound_toggle = QCheckBox("Enable Audio Cues")
        self.sound_toggle.setChecked(self.settings.get("sound_enabled", True))
        self.sound_toggle.stateChanged.connect(lambda s: self.settings.set("sound_enabled", bool(s)))
        layout.addWidget(self.sound_toggle)

        layout.addSpacing(15)

        advanced_label = QLabel("NOTIFICATION PRIVACY")
        advanced_label.setObjectName("SectionLabel")
        layout.addWidget(advanced_label)

        self.safe_mode_toggle = QCheckBox("Hide Sensitive Details (Safe Mode)")
        self.safe_mode_toggle.setChecked(self.settings.get("safe_mode", False))
        self.safe_mode_toggle.stateChanged.connect(lambda s: self.settings.set("safe_mode", bool(s)))
        layout.addWidget(self.safe_mode_toggle)
        
        safe_desc = QLabel("When enabled, notifications will not show behavioral data to keep logs private.")
        safe_desc.setStyleSheet("color: #64748B; font-size: 11px; margin-left: 25px;")
        safe_desc.setWordWrap(True)
        layout.addWidget(safe_desc)

        layout.addStretch()

# ============================================================
# DATA & STORAGE PAGE
# ============================================================
class DataStoragePage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        self.settings = main.settings
        self.engine = main.storage

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(25)

        title = QLabel("Data & Storage")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        backup_label = QLabel("PORTABILITY & BACKUPS")
        backup_label.setObjectName("SectionLabel")
        layout.addWidget(backup_label)

        self.backup_group = QFrame()
        self.backup_group.setStyleSheet(self._get_card_style(is_danger=False))
        backup_layout = QVBoxLayout(self.backup_group)
        
        btn_export = QPushButton(" 📤 Export History to JSON")
        btn_export.clicked.connect(self.export_all)
        backup_layout.addWidget(btn_export)

        btn_import = QPushButton(" 📥 Import Archive Data")
        btn_import.clicked.connect(self.import_all)
        backup_layout.addWidget(btn_import)
        layout.addWidget(self.backup_group)

        cleanup_label = QLabel("DANGER ZONE")
        cleanup_label.setObjectName("SectionLabel") 
        layout.addWidget(cleanup_label)

        self.cleanup_group = QFrame()
        self.cleanup_group.setStyleSheet(self._get_card_style(is_danger=True))
        group_layout = QVBoxLayout(self.cleanup_group)

        actions = [
            ("Reset AI Analytics", self.clear_analytics),
            ("Clear Behavior Logs", self.clear_behavior),
            ("Clear Break History", self.clear_breaks)
        ]

        for text, slot in actions:
            btn = QPushButton(f"  → {text}")
            btn.clicked.connect(slot)
            
            # --- THE KEY FIX: Add a specific CSS class name ---
            btn.setProperty("class", "danger-button")
            
            group_layout.addWidget(btn)

        layout.addWidget(self.cleanup_group)
        layout.addStretch()

    def _get_card_style(self, is_danger=False):
        hover = "rgba(239, 68, 68, 0.1)" if is_danger else "rgba(128, 128, 128, 0.1)"
        return f"""
            QFrame {{ 
                background: rgba(128, 128, 128, 0.05); 
                border-radius: 12px; 
                border: 1px solid rgba(128, 128, 128, 0.1); 
            }}
            QPushButton {{ 
                background: transparent; 
                border: none; 
                text-align: left; 
                padding: 12px; 
                font-weight: 600; 
                font-size: 12px; 
            }}
            QPushButton:hover {{ 
                background: {hover}; 
                border-radius: 10px; 
            }}
        """

    # def export_all(self):
    #     path, ok = QFileDialog.getSaveFileName(self, "Export Data", "K-Mends-Export.json", "JSON Files (*.json)")
    #     #path, ok = QFileDialog.getSaveFileName(self, "Export Data", "", "JSON Files (*.json)")
    #     if ok and path:
    #         self.engine.export_all_data(path)
    #         QMessageBox.information(self, "Export Success", "Data exported successfully.")

    # def import_all(self):
    #     path, ok = QFileDialog.getOpenFileName(self, "Import Data", "", "JSON Files (*.json)")
    #     if ok and path:
    #         self.engine.import_all_data(path)
    #         self.main.apply_theme()
    #         QMessageBox.information(self, "Import Success", "Data imported successfully.")

    def export_all(self):
        # 1. Start specifically in the Downloads folder (which we have an entitlement for)
        default_path = os.path.expanduser("~/Downloads/K-Mends-Export.json")
        
        # 2. Open the dialog starting at that path
        path, ok = QFileDialog.getSaveFileName(
            self, 
            "Export Data", 
            default_path, 
            "JSON Files (*.json)"
        )
        
        if ok and path:
            # 3. Double-check the extension (Sandbox safety)
            if not path.endswith(".json"):
                path += ".json"
            
            # 4. Try the write
            try:
                self.engine.export_all_data(path)
                QMessageBox.information(self, "Export Success", f"Data exported successfully to:\n{path}")
            except Exception as e:
                # This will help us debug if the Sandbox still blocks it
                QMessageBox.critical(self, "Export Error", f"Could not save file: {e}")
            
    def import_all(self):
        # Start looking in Downloads since that's where we export to
        default_dir = os.path.expanduser("~/Downloads")
        path, ok = QFileDialog.getOpenFileName(self, "Import Data", default_dir, "JSON Files (*.json)")
        if ok and path:
            self.engine.import_all_data(path)
            self.main.apply_theme()
            QMessageBox.information(self, "Import Success", "Data imported successfully.")

    def _confirm(self, title, message):
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setInformativeText("This will wipe learned AI patterns. This cannot be undone.")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        return msg.exec() == QMessageBox.Yes

    def clear_analytics(self):
        if self._confirm("Clear AI Data", "Permanently delete AI metrics?"): self.engine.clear_analytics()

    def clear_behavior(self):
        if self._confirm("Clear Logs", "Delete all behavior logs?"): self.engine.clear_behavior_logs()

    def clear_breaks(self):
        if self._confirm("Clear Breaks", "Delete all break history?"): self.engine.clear_break_history()

# ============================================================
# ABOUT & PRIVACY PAGE
# ============================================================
class AboutPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main

        layout = QVBoxLayout(self)
        layout.setContentsMargins(35, 35, 35, 35)
        layout.setSpacing(17)

        title = QLabel("About & Privacy")
        title.setObjectName("PageTitle")
        layout.addWidget(title)

        privacy_card = QFrame()
        privacy_card.setStyleSheet("QFrame { background: rgba(34, 197, 94, 0.1); border-radius: 12px; border: 1px solid rgba(34, 197, 94, 0.2); padding: 15px; }")
        privacy_card.setMinimumHeight(200)
        p_lay = QVBoxLayout(privacy_card)
        #p_text = QLabel("🔒 <b>Local-First Privacy</b><br>All behavior logs and AI insights are stored locally on your device. No data is ever shared or uploaded to the cloud.")
        # In settings.py inside AboutPage __init__
        p_text = QLabel(
            "🛡️ <b>Research Privacy & Data Transparency</b><br><br>"
            "This application is a Digital Wellbeing tool designed for behavioral research. "
            "It utilizes <b>Local-Only Processing</b> to analyze focus patterns. "
            "All data (fatigue scores, behavior logs) is stored in a private SQLite database "
            "on your local device. <b>No behavioral data is ever transmitted over the network "
            "or shared with third parties.</b>"
        )
        p_text.setWordWrap(True)
        p_text.setStyleSheet("font-size: 12px;") 
        p_lay.addWidget(p_text)
        layout.addWidget(privacy_card)

        info_lay = QVBoxLayout()
        name = QLabel("Digital Wellbeing Assistant")
        name.setStyleSheet("font-size: 16px; font-weight: bold;")
        version = QLabel("Version 1.0.0 • Build Stable")
        version.setStyleSheet("color: #64748B; font-size: 12px;")
        info_lay.addWidget(name)
        info_lay.addWidget(version)
        layout.addLayout(info_lay)

        btn_update = QPushButton("🚀 Check for Updates")
        btn_update.clicked.connect(lambda: QMessageBox.information(self, "Update", "You are up to date!"))
        layout.addWidget(btn_update)

        path_label = QLabel("DATA FOLDER")
        path_label.setObjectName("SectionLabel")
        layout.addWidget(path_label)

        self.path_display = QLabel(str(self.main.storage.db_path))
        self.path_display.setTextInteractionFlags(Qt.TextSelectableByMouse)
        #self.path_display.setStyleSheet("padding: 10px; border-radius: 6px; font-family: monospace; font-size: 11px;")
        self.path_display.setStyleSheet("padding: 10px; border-radius: 6px; font-family: 'Menlo', 'Consolas', 'Courier New', monospace; font-size: 11px;")
        layout.addWidget(self.path_display)

        btn_open = QPushButton("📂 Open Data Folder")
        btn_open.clicked.connect(self.open_folder)
        layout.addWidget(btn_open)

        layout.addStretch()
        credits = QLabel("Created by Kirk‑Mends")
        credits.setAlignment(Qt.AlignCenter)
        credits.setStyleSheet("color: #94A3B8; font-size: 11px;")
        layout.addWidget(credits)

    def open_folder(self):
        path = os.path.dirname(str(self.main.storage.db_path))
        if platform.system() == "Windows": os.startfile(path)
        elif platform.system() == "Darwin": subprocess.Popen(["open", path])
        else: subprocess.Popen(["xdg-open", path])