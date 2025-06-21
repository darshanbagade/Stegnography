import cv2

def bin_to_text(binary_data):
    chars = [binary_data[i:i+8] for i in range(0, len(binary_data), 8)]
    return ''.join([chr(int(char, 2)) for char in chars])

def decode_text(image_path, password_input):
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not load image")

    binary_data = ''
    delimiter = '1111111111111110'
    found = False

    for row in img:
        for pixel in row:
            for i in range(3):  # R, G, B
                binary_data += str(pixel[i] & 1)
                if binary_data.endswith(delimiter):
                    found = True
                    break
            if found:
                break
        if found:
            break

    if not found:
        raise ValueError("No hidden data found in image")

    binary_data = binary_data[:-16]  # remove delimiter
    print("Decoded binary:", binary_data)
    try:
        decoded_text = bin_to_text(binary_data)
        print("Decoded text:", decoded_text)
    except Exception:
        raise ValueError("Could not decode binary to text")

    if "::" not in decoded_text:
        raise ValueError("Invalid data or image not encrypted using this method")

    password_saved, secret_message = decoded_text.split("::", 1)

    if password_input != password_saved:
        raise ValueError("Incorrect password!")

    return secret_message