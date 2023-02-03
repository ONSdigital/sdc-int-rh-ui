class AlreadyReceiptedUacError(Exception):
    """Raised when a user enters a used IAC code"""
    def __init__(self):
        super().__init__()


class InvalidForEqTokenGeneration(Exception):
    """ Raised when information is missing or invalid for getting the EQ token """
    def __init__(self, message):
        super().__init__()
        self.message = message


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


class InvalidAccessCode(Exception):
    """Raised when an invalid UAC is entered"""
