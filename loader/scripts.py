import os

from django.core.exceptions import ValidationError
from django.core.files import File
import imageio
import PIL
from PIL import Image

from hdick.settings import BASE_DIR, UPLOAD_DIR


# FORM VALIDATORS

# validates if uploaded file is .jpg
def validate_file_extension(value):
    if value.file.content_type != 'image/jpeg':
        raise ValidationError('Wrong file type. Use jpg')


# IMAGE MANIPULATORS

# resizes image size
def resize(i, basewidth, colour):
    if colour == True:
        colour = 'RGB'
    else:
        colour = 'L'

    img = Image.open(i).convert(colour)
    wpercent = (basewidth/float(img.size[0]))
    hsize = int((float(img.size[1])*float(wpercent)))
    img = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    img.save(i)


# reduces filesize to certain limit
def cut_size(file, old_size, new_size, size_name, extension):
    output_filesize = old_size
    output_file = os.path.join(BASE_DIR, UPLOAD_DIR, size_name + extension)
    img = Image.open(file)
    width, height = img.size
    ratio = float(width) / float(height)
    quality = 100
    cycles = 0

    while output_filesize > new_size:
        width -= 100
        quality -= 5
        height = int(width / ratio)
        img = img.resize((width, height), PIL.Image.ANTIALIAS)
        img.save(output_file, quality=quality)
        output_filesize = os.stat(output_file).st_size
        cycles = cycles +1
    os.remove(file)
    return output_filesize, output_file

# creates gif from jpg files
def make_gif(filenames, output_file, speed):
    images = []
    for filename in filenames:
        images.append(imageio.imread(filename))
    imageio.mimsave(output_file, images, duration=speed)


# opens gif, and makes it FileClass, so its possible to add it to db
def add_gif_to_db(source):
    opener = open(source, 'rb')
    django_file = File(opener)
    os.remove(source)
    return django_file


# translate widget on/off to boolean
def translate_color(color_raw):
    if color_raw == 'on':
        color = True
    else:
        color = False
    return color

