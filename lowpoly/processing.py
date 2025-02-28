from pathlib import Path

import cv2

from lowpoly.exception import InvalidColourImageError


class ImageProcessing:

    def __init__(self, image_path: Path):
        self.user_image = self._read_image(image_path)
        self.height, self.width, _ = self.user_image.shape

    def _read_image(self, path: Path):
        """Read in image"""

        return cv2.imread(str(path))

    def colour_2_grayscale(self, image, flg=cv2.COLOR_BGR2GRAY):
        """Convert colourspace to grayscale"""

        if len(image.shape) == 3:
            return cv2.cvtColor(image, flg)
        else:
            raise InvalidColourImageError
