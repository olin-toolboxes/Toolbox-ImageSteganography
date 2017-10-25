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

    pixels2 = red_channel.load()
    print(pixels2[0, 0])

    for x in range(x_size):
        for y in range(y_size):
            if pixels2[x , y] % 2 == 1:
                pixels[x , y] = (0,0,0)
            else:
                pixels[x , y] = (255,255,255)

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
    unencoded_image = Image.open(template_image)
    red_channel = unencoded_image.split()[0]
    green_channel = unencoded_image.split()[1]
    blue_channel = unencoded_image.split()[2]

    unencoded_pixels_r = red_channel.load()
    unencoded_pixels_g = green_channel.load()
    unencoded_pixels_b = blue_channel.load()

    x_size = unencoded_image.size[0]
    y_size = unencoded_image.size[1]

    encode_image = Image.new("RGB", unencoded_image.size)
    pixels = encode_image.load()

    hidden_text_image = write_text(text_to_encode,(x_size, y_size))
    red_channel_hidden = hidden_text_image.split()[0]
    hidden_pixels = red_channel_hidden.load()

    for x in range(x_size):
        for y in range(y_size):
            if hidden_pixels[x,y] == 0:
                if unencoded_pixels_r[x,y] % 2 == 1:
                    pixels[x,y] = (unencoded_pixels_r[x,y] - 1, unencoded_pixels_g[x,y], unencoded_pixels_b[x,y])
                else:
                    pixels[x,y] = (unencoded_pixels_r[x,y], unencoded_pixels_g[x,y], unencoded_pixels_b[x,y])
            else:
                if unencoded_pixels_r[x,y] % 2 == 0:
                    pixels[x,y] = (unencoded_pixels_r[x,y] - 1, unencoded_pixels_g[x,y], unencoded_pixels_b[x,y])
                else:
                    pixels[x,y] = (unencoded_pixels_r[x,y], unencoded_pixels_g[x,y], unencoded_pixels_b[x,y])

    encode_image.save("images/encode_image.png")

if __name__ == '__main__':
    print("Encoding the image...")
    encode_image("Tony is an awesome NINJA!!")

    print("Decoding the image...")
    decode_image("images/encode_image.png")
