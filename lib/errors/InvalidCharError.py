from errors.Error import Error

class InvalidCharError(Error):
    def __init__(self, pos_start, pos_end, details):
        super().__init__(pos_start, pos_end, "InvalidCharError", details)