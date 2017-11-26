"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_dest, file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    im = red_channel.load()

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            val = int(format(im[i, j], '08b')[-1])
            pixels[i, j] = (255*val, 255*val, 255*val)

    decoded_image.save(file_dest)

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
    picture = Image.open(template_image)
    red_channel = picture.split()[0]
    green_channel = picture.split()[1]
    blue_channel = picture.split()[2]
    red_pixels = red_channel.load()
    green_pixels = green_channel.load()
    blue_pixels = blue_channel.load()

    x_size = picture.size[0]
    y_size = picture.size[1]

    text = write_text(text_to_encode, picture.size).split()[0].load()

    encoded_image = Image.new("RGB", picture.size)
    pixels = encoded_image.load()

    for i in range(x_size):
        for j in range(y_size):
            if int(format(red_pixels[i, j], '08b')[-1]) != int(format(text[i, j], '08b')[-1]):
                pixels[i,j] = (abs(red_pixels[i, j]-1), green_pixels[i, j], blue_pixels[i, j])
            else:
                pixels[i,j] = (red_pixels[i, j], green_pixels[i, j], blue_pixels[i, j])

    encoded_image.save("images/my_image.png")


if __name__ == '__main__':
    print("Encoding the image...")
    encode_image("Hello World!")
    print("Decoding the image...")
    decode_image("images/my_message.png", "images/my_image.png")
