from PIL import Image
import os

def is_color_within_tolerance(color, target_color):
    deviation = (1 / 100) * 255

    return all(target_color[i] - deviation <= color[i] <= target_color[i] + deviation for i in range(3))

def find_pixel(img, target_color, firstOrLast):

    _, height = img.size
    if firstOrLast == 'first':
        for y in range(height):
            pixel_color = img.getpixel((0, y))
            if is_color_within_tolerance(pixel_color, target_color):
                return y
    else:
        for y in range(height - 1, -1, -1):
            pixel_color = img.getpixel((0, y))
            if is_color_within_tolerance(pixel_color, target_color):
                return y

    return None

def crop_image(img):
    target_color_white = (240,218,181)
    target_color_black = (181,135,99)
    width, _ = img.size
    
    first_pixel = find_pixel(img, target_color_white, 'first')
    last_pixel = find_pixel(img, target_color_black, 'last')
    cropped_img = img.crop((0, first_pixel, width, last_pixel))
    return cropped_img

