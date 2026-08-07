"""
backup_manager.py

Handles database backup and restore.

Ramdev Billing Software
"""

import os
import shutil
from datetime import datetime

from .schema import DATABASE_NAME


class BackupManager:

    def __init__(self):
        self.backup_folder = os.path.join("database", "backups")
        os.makedirs(self.backup_folder, exist_ok=True)

    def create_backup(self):
        """
        Create a timestamped backup of the database.
        """

        if not os.path.exists(DATABASE_NAME):
            return None

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_name = f"Database_Backup_{timestamp}.xlsx"

        backup_path = os.path.join(
            self.backup_folder,
            backup_name
        )

        shutil.copy2(DATABASE_NAME, backup_path)

        return backup_path

    def list_backups(self):
        """
        Return all available backups.
        """

        backups = []

        if not os.path.exists(self.backup_folder):
            return backups

        for file in os.listdir(self.backup_folder):

            if file.endswith(".xlsx"):

                backups.append(file)

        backups.sort(reverse=True)

        return backups

    def restore_backup(self, backup_file):
        """
        Restore selected backup.
        """

        backup_path = os.path.join(
            self.backup_folder,
            backup_file
        )

        if not os.path.exists(backup_path):
            return False

        shutil.copy2(backup_path, DATABASE_NAME)

        return True

    def delete_backup(self, backup_file):
        """
        Delete backup file.
        """

        backup_path = os.path.join(
            self.backup_folder,
            backup_file
        )

        if os.path.exists(backup_path):
            os.remove(backup_path)
            return True

        return False

    def latest_backup(self):
        """
        Return latest backup filename.
        """

        backups = self.list_backups()

        if backups:
            return backups[0]

        return None

    def backup_count(self):
        """
        Return total number of backups.
        """

        return len(self.list_backups())