"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def getRed(tup):
    return tup[1]

white = (255,255,255)
black = (0,0,0)

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

    #Iterates throgh each pixel
    for x in range(x_size):
        for y in range(y_size):
            Pix = red_channel.getpixel((x,y))
            #isolates the red and if the red has an LSB of 1
            #then turn that color white
            if Pix & 1 == 1:
                decoded_image.putpixel( (x,y), (255,255,255))
            else:
                decoded_image.putpixel( (x,y), (0,0,0))

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
    encodingimage = Image.open(template_image)
    x, y = encodingimage.size
    to_encode = write_text(text_to_encode, (x, y))
    #prepares the image to be the same size as the image that it will be incoded in
    x_size = to_encode.size[0]
    y_size = to_encode.size[1]
    for x in range(x_size):
        for y in range(y_size):
            #iterates through the secrets that we are about to encode to see if it is a black
            #or a white pixel
            Pix = to_encode.getpixel((x,y))
            TemplateRed = encodingimage.getpixel((x,y))[0]
            TemplateBlue = encodingimage.getpixel((x,y))[1]
            TemplateGreen = encodingimage.getpixel((x,y))[2]
            if Pix == white:
                if TemplateRed & 1 == 1:
                    pass
                else:
                    encodingimage.putpixel((x,y), (TemplateRed + 1, TemplateBlue, TemplateGreen))
                    #if it is white and the LSB of the Red is not 1, it will add 1 to the red
            if Pix == black:
                if TemplateRed & 1 == 0:
                    pass
                else:
                    encodingimage.putpixel((x,y), (TemplateRed + 1, TemplateBlue, TemplateGreen))
                    #if it is black and the LSB of the Red is not 0, it will add 1 to the red
    encodingimage.save("images/encodedish_image.png")

if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    print("Encoding the image...")
    encode_image('Secrets')
