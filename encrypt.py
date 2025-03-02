
from PIL import Image

def text_to_binary(message):
    """Convert text to binary."""
    return ''.join(format(ord(char), '08b') for char in message)

def hide_message(image_path, output_path, message):
    """Hide a message inside an image using LSB steganography."""
    img = Image.open(image_path)
    img = img.convert("RGB")
    pixels = list(img.getdata())  # Get pixel data as a flat list

    binary_message = text_to_binary(message)
    message_length = len(binary_message)
    binary_length = format(message_length, '032b')  # 32-bit binary length storage

    total_pixels = len(pixels) * 3  # Each pixel has 3 color channels

    if message_length + 32 > total_pixels:
        print("Error: Message too long for the given image!")
        return

    binary_data = binary_length + binary_message  # Combine length info and message
    index = 0
    new_pixels = []

    for pixel in pixels:
        new_pixel = list(pixel)  # Convert tuple to list for modification
        for i in range(3):  # Modify R, G, B channels
            if index < len(binary_data):
                new_pixel[i] = (new_pixel[i] & 0xFE) | int(binary_data[index])  # Replace LSB
                index += 1
        new_pixels.append(tuple(new_pixel))  # Convert back to tuple

    img.putdata(new_pixels)  # Apply modified pixels to image
    img.save(output_path, "PNG")
    print(f"Message successfully hidden in {output_path}")

# User input
input_image = input("Enter input image filename: ")
output_image = input("Enter output image filename: ")
secret_message = input("Enter the message to hide: ")

hide_message(input_image, output_image, secret_message)
