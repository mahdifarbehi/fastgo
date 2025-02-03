import re
from backbone.base_exceptions import ValueErrorException

PHONE_PATTERN = r"^09[0-9]{9}$"
USERNAME_PATTERN = r"^[A-Za-z0-9._-]+$"


class BaseValidator:

    @staticmethod
    def phone(phone: str):
        if re.match(PHONE_PATTERN, phone) is None:
            raise ValueErrorException(detail="Invalid phone number")
        return True

    @staticmethod
    def username(username: str):
        if re.match(USERNAME_PATTERN, username) is None:
            raise ValueErrorException(detail="Invalid username")

        return True
