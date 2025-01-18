import framebuf


class LandscapeBuffer(framebuf.FrameBuffer):
    def __init__(self, width: int, height: int) -> None:
        """
        A wrapper around framebuf.FrameBuffer
        that inverts bytes to fit with E-paper landscape.

        Note that `width` and `height` arguments should
        be provided as if already landscape.
        """
        self.width = width
        self.height = height

        self._buffer = bytearray(self.width * self.h)
        self._buffer_epaper = bytearray(self.width * self.h)
        self.frame_buffer = super().__init__(
            self._buffer, self.width, self.height, framebuf.MONO_VLSB
        )

    @property
    def h(self):
        return self.height // 8

    def invert_buffer(self):
        """
        Get the buffer in landscape format, formatted
        ready for the E-paper device.
        """
        x = 0
        y = 0
        n = 1
        R = 0
        for i in range(1, self.h + 1):
            for _ in range(self.width):
                R = (n - x) + ((n - y) * (self.h - 1))
                self._buffer_epaper[R - 1] = self._buffer[n - 1]
                n += 1
            x = n + i - 1
            y = n - 1

        return self._buffer_epaper


def load_bitmap(buffer: framebuf.FrameBuffer, image: list, width: int, height: int):
    for y in range(height):
        for x in range(width):
            if image[y * (width // 8) + (x // 8)] & (128 >> (x % 8)):
                buffer.pixel(x, y, 0x00)
