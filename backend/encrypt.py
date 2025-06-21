import cv2
import numpy as np

def text_to_bin(data):
    return ''.join(format(ord(i), '08b') for i in data)

def encode_text(input_path, output_path, secret_text, password):
    # Combine secret + password as one string
    full_message = f"{password}::{secret_text}"

    img = cv2.imread(input_path)
    if img is None:
        raise ValueError("Could not load image")

    binary_secret = text_to_bin(full_message) + '1111111111111110'  # Delimiter to signal end
    data_index = 0
    total_bits = len(binary_secret)

    rows, cols, _ = img.shape

    for row in range(rows):
        for col in range(cols):
            pixel = img[row, col]
            for i in range(3):  # R, G, B
                if data_index < total_bits:
                    pixel[i] = (int(pixel[i]) & 254) | int(binary_secret[data_index])
                    data_index += 1
                else:
                    break
            img[row, col] = pixel
        if data_index >= total_bits:
            break

    if data_index < total_bits:
        raise ValueError("Image not large enough to hold data")

    # Always save as PNG to avoid compression artifacts
    cv2.imwrite(output_path, img)