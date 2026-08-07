"""
login_manager.py

Handles user authentication.

Ramdev Billing Software
"""

from datetime import datetime

from database.excel_manager import ExcelManager
from database.schema import USERS_SHEET


class LoginManager:

    def __init__(self):
        self.db = ExcelManager()

    def login(self, username, password):
        """
        Authenticate user.
        """

        users = self.db.get_all_records(USERS_SHEET)

        for user in users:

            if (
                user["Username"] == username
                and user["Password"] == password
            ):

                if user["Status"] != "Active":
                    return False, "User account is inactive."

                self.update_last_login(username)

                return True, user

        return False, "Invalid username or password."

    def update_last_login(self, username):
        """
        Update last login date & time.
        """

        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        self.db.update_record(
            USERS_SHEET,
            "Username",
            username,
            {
                "Last Login": now
            }
        )

    def change_password(
        self,
        username,
        old_password,
        new_password
    ):
        """
        Change user password.
        """

        user = self.db.find_record(
            USERS_SHEET,
            "Username",
            username
        )

        if not user:
            return False, "User not found."

        if user["Password"] != old_password:
            return False, "Current password is incorrect."

        self.db.update_record(
            USERS_SHEET,
            "Username",
            username,
            {
                "Password": new_password
            }
        )

        return True, "Password changed successfully."

    def create_user(
        self,
        username,
        password,
        role="Staff"
    ):
        """
        Create new user.
        """

        if self.db.record_exists(
            USERS_SHEET,
            "Username",
            username
        ):
            return False, "Username already exists."

        user = {
            "Username": username,
            "Password": password,
            "Role": role,
            "Status": "Active",
            "Created Date": datetime.now().strftime("%d-%m-%Y"),
            "Last Login": ""
        }

        self.db.insert_record(
            USERS_SHEET,
            user
        )

        return True, "User created successfully."

    def delete_user(self, username):
        """
        Delete user.
        """

        return self.db.delete_record(
            USERS_SHEET,
            "Username",
            username
        )

    def get_all_users(self):
        """
        Return all users.
        """

        return self.db.get_all_records(
            USERS_SHEET
        )

    def activate_user(self, username):
        """
        Activate user account.
        """

        return self.db.update_record(
            USERS_SHEET,
            "Username",
            username,
            {
                "Status": "Active"
            }
        )

    def deactivate_user(self, username):
        """
        Deactivate user account.
        """

        return self.db.update_record(
            USERS_SHEET,
            "Username",
            username,
            {
                "Status": "Inactive"
            }
        )
