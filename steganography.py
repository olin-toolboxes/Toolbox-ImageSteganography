"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images/encoded_sample.png", decoded_file="images/decoded_image.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0] # isolate the red_channel from the original RGB image.


    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    # iterate though each pixel in the encoded image red_channel
    for i in range(0,x_size):
        for j in range(0,y_size):
            # set the decode_image pixel to be (0, 0, 0) or (255, 255, 255)
            if red_channel.getpixel((i,j))%2 == 0: #check if number is even
                decoded_image.putpixel((i,j),(0,0,0))
            else:
                decoded_image.putpixel((i,j),(255,255,255))

    decoded_image.save(decoded_file)

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
    encoded_image = Image.open(template_image)
    red_channel = encoded_image.split()[0] # isolate the red_channel from the original RGB image.
    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    # Create a black and white picture
    text_to_write = text_to_encode
    image_size = encoded_image.size
    text_decode = write_text(text_to_write, image_size)

    # iterate through the picture to encode it
    for i in range(0,x_size):
        for j in range(0,y_size):
            # set the decode_image pixel to be (0, 0, 0) or (255, 255, 255)
            pixel=red_channel.getpixel((i,j))
            if text_decode.getpixel((i,j)) == (255,255,255):
                if pixel%2 == 0: #if even
                    r, g, b = encoded_image.getpixel((i,j))
                    encoded_image.putpixel((i,j), (r+1, g, b))# make the lsb odd
            else:
                if pixel%2 != 0: #if odd
                     r, g, b = encoded_image.getpixel((i,j))
                     encoded_image.putpixel((i,j), (r-1, g, b))# make the lsb odd

    new_file = "images/encoded_image.png"
    encoded_image.save(new_file) # save the encoded picture
    text_decode.save("images/decoded_text.png") # save the text image
    decode_image(new_file, "images/decoded_encoded_image.png") #save the decoded picture

if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()

    print("Encoding the image...")
    encode_image('This is another test')
