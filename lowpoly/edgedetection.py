import cv2
import numpy as np


class EdgeDetection:

    def binary_threshold(self, image_grayscale, min_threshold=0, max_threshold=255):
        """Binary Threshold"""

        return (
            cv2.threshold(
                image_grayscale, min_threshold, max_threshold, cv2.THRESH_BINARY
            )
        )[1]

    def adaptive_mean_binary_threshold(
        self, image_grayscale, max_value, bsize=11, const=2
    ):
        """Adaptive Mean Threshold"""

        return cv2.adaptiveThreshold(
            image_grayscale,
            max_value,
            cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY,
            bsize,
            const,
        )

    def adaptive_gaussian_binary_threshold(
        self, image_grayscale, max_value, bsize=11, const=2
    ):
        """Adaptive Gaussian Threshold"""

        return cv2.adaptiveThreshold(
            image_grayscale,
            max_value,
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY,
            bsize,
            const,
        )

    def gaussian_blur(self, image_grayscale, kernel=(1, 1), sigma_x=0, sigma_y=0):
        """Apply Gaussian Blur"""

        return cv2.GaussianBlur(image_grayscale, kernel, sigma_x, sigma_y)

    def sharpening(
        self,
        image_grayscale,
        kernel=np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]),
        depth=-1,
    ):
        """Apply Sharpening Filter"""

        return cv2.filter2D(image_grayscale, depth, kernel)

    def edge_gray(self, image_filtered, image_gray):
        """Filtered image times grayscale"""

        return np.multiply(image_filtered, image_gray)

    def edge_gray_threshold(
        self,
        image_filtered,
        image_grayscale,
        minimum_threshold=0,
        maximum_threshold=255,
    ):
        """Thresholding filtered image times grayscale"""

        return self.binary_threshold(
            np.multiply(image_filtered, image_grayscale),
            minimum_threshold,
            maximum_threshold,
        )

    def canny(self, image_grayscale, minimum_threshold=20, maximum_threshold=70):
        """Canny Edge detection"""

        return cv2.Canny(image_grayscale, minimum_threshold, maximum_threshold)

    def sobel(
        self,
        image_grayscale,
        depth=cv2.CV_8U,
        size=3,
        scl=1,
        x_weight=0.5,
        y_weight=0.5,
        add_scaler=0,
    ) -> cv2.typing.MatLike:
        """Sobel Edge detection"""

        x = cv2.Sobel(image_grayscale, depth, 1, 0, size, scl)
        y = cv2.Sobel(image_grayscale, depth, 0, 1, size, scl)
        absolute_x = cv2.convertScaleAbs(x)
        absolute_y = cv2.convertScaleAbs(y)

        return cv2.addWeighted(absolute_x, x_weight, absolute_y, y_weight, add_scaler)
