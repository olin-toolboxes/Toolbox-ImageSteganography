"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    for i in range(x_size):
        for j in range(y_size):
            pixels[i, j] = 255*(red_channel.getpixel((i,j))%2)

    # pass #TODO: Fill in decoding functionality

    decoded_image.save("images/decoded_image.png")

def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    #Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="images/samoyed.jpg"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """

    decoded_image = Image.open(template_image)
    text_image = write_text(text_to_encode,decoded_image.size)
    # red_channel = decoded_image.split()[0]

    x_size = decoded_image.size[0]
    y_size = decoded_image.size[1]

    encoded_image = Image.new("RGB", decoded_image.size)
    pixels = encoded_image.load()
    for i in range(x_size):
        for j in range(y_size):
            red = decoded_image.getpixel((i,j))[0]
            green = decoded_image.getpixel((i,j))[1]
            blue = decoded_image.getpixel((i,j))[2]
            if text_image.getpixel((i,j))[0] > 1:
                pixels[i, j] = (2*(red//2), green, blue)
            else:
                pixels[i, j] = (2*(red//2)+1, green, blue)
    encoded_image.save("images/encoded_image.png")

if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    print("Encoding the image...")
    encode_image('Hello!')
