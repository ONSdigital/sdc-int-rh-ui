class AlreadyReceiptedUacError(Exception):
    """Raised when a user enters a used IAC code"""
    def __init__(self):
        super().__init__()


class InvalidForEqTokenGeneration(Exception):
    """ Raised when information is missing or invalid for getting the EQ token """
    def __init__(self, message):
        super().__init__()
        self.message = message


class InvalidIACError(Exception):
    """Raised when the IAC Service returns a 404"""


class SessionTimeout(Exception):
    """Raised when users session expires in journeys requiring sessions"""
    def __init__(self, user_journey, request_type=None):
        super().__init__()
        self.user_journey = user_journey
        self.request_type = request_type


class TooManyRequestsEQLaunch(Exception):
    """Raised when EQ returns a 429 error"""


class InactiveUacError(Exception):
    """Raised when a user attempts to use an inactive UAC"""
    def __init__(self):
        super().__init__()


# this class is not used anywhere
class InvalidDataError(Exception):
    """ Raised when user supplies invalid data in form fields (on english language page) """
    def __init__(self, message=None, message_type=None):
        super().__init__(message or 'The supplied value is invalid')
        self.message_type = message_type


# this class is not used anywhere
class InvalidDataErrorWelsh(Exception):
    """ Raised when user supplies invalid data in form fields (on welsh language page) """
    def __init__(self, message=None, message_type=None):
        super().__init__(message or "PLACEHOLDER WELSH Mae'r gwerth rydych wedi'i roi yn annilys")
        self.message_type = message_type


class InvalidAccessCode(Exception):
    """Raised when an invalid UAC is entered"""
