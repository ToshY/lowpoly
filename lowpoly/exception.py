class InvalidPolygonError(Exception):
    ERROR_MESSAGE = "Invalid polygon. Expected at least 3 points, {message} given."

    def __init__(self, message):
        self.message = self.ERROR_MESSAGE.format(message=message)
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidPolygonGeometryError(Exception):
    ERROR_MESSAGE = "Invalid polygon geometry."

    def __init__(self):
        self.message = self.ERROR_MESSAGE
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidPolygonOutputError(Exception):
    ERROR_MESSAGE = "No polygon output found."

    def __init__(self):
        self.message = self.ERROR_MESSAGE
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidViewBoxError(Exception):
    ERROR_MESSAGE = "Invalid view box specified. Please make sure that the view box only contains numerical values."

    def __init__(self):
        self.message = self.ERROR_MESSAGE
        super().__init__(self.message)

    def __str__(self):
        return self.message


class InvalidColourImageError(Exception):
    ERROR_MESSAGE = (
        "Cannot convert colour to grayscale image: given image is already grayscale."
    )

    def __init__(self):
        self.message = self.ERROR_MESSAGE
        super().__init__(self.message)

    def __str__(self):
        return self.message


class SvgToPngImageError(Exception):
    ERROR_MESSAGE = "Cannot convert SVG to PNG. Reason: {message}."

    def __init__(self, message):
        self.message = self.ERROR_MESSAGE.format(message=message)
        super().__init__(self.message)

    def __str__(self):
        return self.message
