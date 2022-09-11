from typing import List

from PIL.Image import Image

ASCII_CHARS = ["@", "#", "$", "%", "?", "*", "+", ";", ":", ",", "."]


def pixel_to_ascii(image: Image):
    pixels: List[int] = image.getdata()  # type: ignore
    ascii_str = ""
    pixel: int
    for pixel in pixels:
        ascii_str += ASCII_CHARS[pixel // 25]
    return ascii_str


def convert_to_ascii_art(img: Image) -> str:
    """Converts an image to ASCII art."""
    # set height to 20 and width according to aspect ratio
    width, height = img.size
    aspect_ratio = height / width
    new_width = 60
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))

    img = img.convert("L")
    # add newlines
    pixels = pixel_to_ascii(img)
    length = len(pixels)
    ascii_image = ""
    for i in range(0, length, new_width):
        ascii_image += pixels[i : i + new_width] + "\n"
    return ascii_image


def codeblock(content: str, lang: str = "enoki") -> str:
    """Converts a string to a codeblock."""
    return f"```{lang}\n{content}\n```"
