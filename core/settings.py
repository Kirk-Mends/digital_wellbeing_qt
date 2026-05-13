









# core/settings.py

import json
import os
import sys
from typing import Dict, Any
from PySide6.QtCore import QStandardPaths

# -----------------------------
# DYNAMIC PATH HELPER
# -----------------------------
def get_base_save_path():
    """ 
    Ensures settings are saved in:
    /Users/username/Library/Application Support/KMends/
    """
    # This creates the path based on your App Name
    path = QStandardPaths.writableLocation(QStandardPaths.AppConfigLocation)
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)
    return path

BASE_PATH = get_base_save_path()

# Update these to use the BASE_PATH
APP_SETTINGS_FILE = os.path.join(BASE_PATH, "settings.json")
PROFILES_DIR = os.path.join(BASE_PATH, "profiles")

# -----------------------------
# GLOBAL CONSTANTS
# -----------------------------
DEFAULT_SETTINGS: Dict[str, Any] = {
    "theme": "light",
    "sound_enabled": True,
    "notifications_enabled": True
}

DEFAULT_PROFILE_NAME = "default"

# ... the rest of your SettingsManager class remains the same ...

# -----------------------------
# SETTINGS MANAGER
# -----------------------------

class SettingsManager:
    def __init__(self):
        # Ensure profiles directory exists
        os.makedirs(PROFILES_DIR, exist_ok=True)

        # Load app meta (current profile)
        self.app_meta = self._load_app_meta()

        # Active profile name
        self.current_profile = self.app_meta.get("current_profile", DEFAULT_PROFILE_NAME)

        # Load profile settings
        self.settings = DEFAULT_SETTINGS.copy()
        self.load()
        self.migrate()
        self.validate()
        self.save()

    # -------------------------
    # APP META (current profile)
    # -------------------------
    def _load_app_meta(self) -> Dict[str, Any]:
        if os.path.exists(APP_SETTINGS_FILE):
            try:
                with open(APP_SETTINGS_FILE, "r") as f:
                    return json.load(f)
            except Exception:
                pass
        return {"current_profile": DEFAULT_PROFILE_NAME}

    def _save_app_meta(self):
        self.app_meta["current_profile"] = self.current_profile
        try:
            with open(APP_SETTINGS_FILE, "w") as f:
                json.dump(self.app_meta, f, indent=4)
        except Exception:
            pass

    # -------------------------
    # PROFILE PATH
    # -------------------------
    def _profile_path(self, profile_name: str) -> str:
        return os.path.join(PROFILES_DIR, f"{profile_name}.json")

    # -------------------------
    # LOAD PROFILE SETTINGS
    # -------------------------
    def load(self):
        path = self._profile_path(self.current_profile)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                    self.settings.update(data)
            except Exception:
                self.settings = DEFAULT_SETTINGS.copy()
        else:
            self.settings = DEFAULT_SETTINGS.copy()

    # -------------------------
    # SAVE PROFILE SETTINGS
    # -------------------------
    def save(self):
        path = self._profile_path(self.current_profile)
        try:
            with open(path, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception:
            pass
        self._save_app_meta()

    # -------------------------
    # MIGRATE OLD KEYS
    # -------------------------
    def migrate(self):
        old = self.settings

        # Rename old keys
        if "sound_on" in old:
            old["sound_enabled"] = bool(old["sound_on"])
            del old["sound_on"]

        # Remove deprecated keys
        deprecated = [
            "break_mode",
            "break_interval_minutes",
            "dark_mode"
        ]
        for key in deprecated:
            if key in old:
                del old[key]

        self.settings = old

    # -------------------------
    # VALIDATE SETTINGS
    # -------------------------
    def validate(self):
        for key, default_value in DEFAULT_SETTINGS.items():
            if key not in self.settings:
                self.settings[key] = default_value

    # -------------------------
    # BASIC GET / SET
    # -------------------------
    def get(self, key: str, default=None):
        return self.settings.get(key, default)

    def set(self, key: str, value: Any):
        self.settings[key] = value
        self.save()

    # -------------------------
    # RESET CURRENT PROFILE
    # -------------------------
    def reset(self):
        self.settings = DEFAULT_SETTINGS.copy()
        self.save()

    # -------------------------
    # EXPORT / IMPORT SETTINGS
    # -------------------------
    def export_settings(self, export_path: str):
        """Export current profile settings to a JSON file."""
        try:
            with open(export_path, "w") as f:
                json.dump(self.settings, f, indent=4)
        except Exception:
            pass

    def import_settings(self, import_path: str):
        """Import settings from a JSON file into current profile."""
        if not os.path.exists(import_path):
            return
        try:
            with open(import_path, "r") as f:
                data = json.load(f)
            # Merge, then validate
            self.settings.update(data)
            self.migrate()
            self.validate()
            self.save()
        except Exception:
            pass

    # -------------------------
    # PROFILE MANAGEMENT
    # -------------------------
    def list_profiles(self):
        """Return a list of available profile names."""
        profiles = []
        for fname in os.listdir(PROFILES_DIR):
            if fname.endswith(".json"):
                profiles.append(os.path.splitext(fname)[0])
        if DEFAULT_PROFILE_NAME not in profiles:
            profiles.append(DEFAULT_PROFILE_NAME)
        return sorted(set(profiles))

    def switch_profile(self, profile_name: str):
        """Switch to another profile (creates it if missing)."""
        if not profile_name:
            profile_name = DEFAULT_PROFILE_NAME

        self.current_profile = profile_name
        self.load()
        self.migrate()
        self.validate()
        self.save()

    def delete_profile(self, profile_name: str):
        """Delete a profile (except the default)."""
        if profile_name == DEFAULT_PROFILE_NAME:
            return
        path = self._profile_path(profile_name)
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass
        # If we deleted the active profile, fall back to default
        if self.current_profile == profile_name:
            self.current_profile = DEFAULT_PROFILE_NAME
            self.load()
            self.migrate()
            self.validate()
            self.save()


