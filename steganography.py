"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image.

    Parameters
    ----------
    file_location: str
        The location of the image file to decode. This defaults to the provided
        encoded image in the images folder.
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    # The above could also be written as one of:
    #   red_channel, green_channel, blue_channel = encoded_image.split()
    #   red_channel, _, _ = encoded_image.split()
    #   red_channel, *_ = encoded_image.split()
    # The first has the disadvantage of creating temporary variables that aren't
    # used. The special variable name _ (underscore) is conventionally named
    # an unused variable.

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]
    # The above could also be written as:
    #   x_size, y_size = encoded_image.size[0]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    pass  # TODO: Fill in decoding functionality

    decoded_image.save("images/decoded_image.png")


def write_text(text_to_write, image_size):
    """Write text to an RGB image. Automatically line wraps.

    Parameters
    ----------
    text_to_write: str
        The text to write to the image.
    image_size: (int, int)
        The size of the resulting text image.
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return image_text


def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encode a text message into an image.

    Parameters
    ----------
    text_to_encode: str
        The text to encode into the template image.
    template_image: str
        The image to use for encoding. An image is provided by default.
    """
    pass  # TODO: Fill out this function


if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    print("Encoding the image...")
    encode_image()
