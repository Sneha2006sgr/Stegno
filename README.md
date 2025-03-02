# Stegno

This README provides an overview of the Stegno project, including installation instructions, usage examples, and the provided code. Follow the instructions to encrypt and decrypt messages within an image using a passcode.

Stegno is a simple steganography application in Python that hides a secret message within an image and retrieves it using a passcode. The application consists of both encryption and decryption functionalities. The encryption process embeds the secret message into the image's pixel values, while the decryption process extracts the message from the image if the correct passcode is provided.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- An image file to use for embedding the secret message

## Installation

1. Install Python 3.x from the official website: https://www.python.org/
2. Install OpenCV using pip:
   ```sh
   pip install opencv-python
   ```

## Usage

### Encryption

1. Place the image file (e.g., download.jpg) in the same directory as the script.
2. Run the encryption script:
   ```sh
   python encrypt.py
   ```
3. Enter the secret message and passcode when prompted.
4. The script will create an encrypted image file named `encryptedImage.jpg` and open it using the default image viewer.

### Decryption

1. Ensure the encrypted image file (`encryptedImage.jpg`) is in the same directory as the script.
2. Run the decryption script:
   ```sh
   python decrypt.py
   ```
3. Enter the original passcode and the length of the secret message when prompted.
4. The script will print the decrypted message if the correct passcode is provided; otherwise, it will print an error message.

## Example

### Encryption

- Input: `download.jpg` (image file), `"Hello, World!"` (secret message), `"1234"` (passcode)
- Output: `encryptedImage.jpg` (modified image with the secret message embedded)

### Decryption

- Input: `encryptedImage.jpg` (modified image), `"1234"` (correct passcode), `13` (length of the secret message)
- Output: `"Hello, World!"` (decrypted message)

## Code

### Encryption Script (encrypt.py)

```python
import cv2
import os

img = cv2.imread("download.jpg")  # Replace with the correct image path

msg = input("Enter secret message:")
password = input("Enter a passcode:")

d = {}
c = {}

for i in range(255):
    d[chr(i)] = i
    c[i] = chr(i)

m = 0
n = 0
z = 0

# Encryption
for i in range(len(msg)):
    img[n, m, z] = d[msg[i]]
    z = (z + 1) % 3
    if z == 0:
        m += 1
        if m == img.shape[1]:
            m = 0
            n += 1

cv2.imwrite("encryptedImage.jpg", img)
os.system("start encryptedImage.jpg")  # Use 'start' to open the image on Windows
```

### Decryption Script (decrypt.py)

```python
import cv2

img = cv2.imread("encryptedImage.jpg")

decryp = {}
for i in range(255):
    decryp[i] = chr(i)

message = ""
n = 0
m = 0
z = 0

# Get the original passcode and message length
password = input("Enter the original passcode:")
msg_length = int(input("Enter the length of the secret message:"))

pas = input("Enter passcode for Decryption")
if password == pas:
    for i in range(msg_length):
        message += decryp[img[n, m, z]]
        z = (z + 1) % 3
        if z == 0:
            m += 1
            if m == img.shape[1]:
                m = 0
                n += 1
    print("Decryption message:", message)
else:
    print("YOU ARE NOT auth")
```
Troubleshooting
Ensure the image file path is correct.
Ensure the image is large enough to accommodate the entire secret message.
Ensure the correct passcode is entered during decryption.
If the decrypted message is incorrect, verify that the traversal logic for encoding and decoding is consistent.
