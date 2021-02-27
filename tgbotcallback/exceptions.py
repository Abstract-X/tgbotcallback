

class CallbackDataIsTooLargeError(Exception):

    def __init__(self, data: str, length: int, length_limit: int):

        self.data = data
        self.length = length
        self.length_limit = length_limit

    def __str__(self):

        return f"the resulted callback_data '{self.data}' exceeded the maximum " \
               f"length limit ({self.length}/{self.length_limit} bytes)!"
