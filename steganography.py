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
    hidden_image = [[]]*y_size

    for i in range(x_size):
        for j in range(y_size):
            pixel = encoded_image.getpixel((i,j))
            if pixel[0] % 2 == 1:
                decoded_image.putpixel((i,j),(255,255,255))
            else:
                decoded_image.putpixel((i,j),(0,0,0))

    
    


    print("hidded Immage")
    decoded_image.show()




    

    pass #TODO: Fill in decoding functionality

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
    encoded_image = Image.open(template_image)
    
    red_channel = encoded_image.split()[0]
    
    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]
    message = write_text(text_to_encode, (x_size,y_size))
    


   # decoded_image = Image.new("RGB", encoded_image.size)
   # decoded_image.show()
   # pixels = encoded_image.load()
   # hidden_image = [[]]*y_size
    message.show()
    for i in range(x_size):
        for j in range(y_size):
            pixel = encoded_image.getpixel((i,j))
            signal = message.getpixel((i,j))
            if signal[0] == 0:           #if the pixle is black
                if pixel[0] % 2 == 1:
                    encoded_image.putpixel((i,j),(pixel[0]+1,pixel[1],pixel[2]))
               
            else:
                if pixel[0] % 2 == 0:
                    encoded_image.putpixel((i,j),(pixel[0]+1,pixel[1],pixel[2]))
    
    encoded_image.save("images/samoyed1.jpg")

    encoded_image.show()
    decode_image("images/samoyed1.jpg")
    pass #TODO: Fill out this function

if __name__ == '__main__':
    print("Decoding the image...")
    decode_image()
    
    print("Encoding the image...")
    encode_image("You are my favorite NINJA")
