









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