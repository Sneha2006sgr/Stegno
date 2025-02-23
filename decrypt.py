import cv2
import os
import string
img = cv2.imread("encryptedImage.jpg")
decryp = {}
for i in range(255):
    decryp[i] = chr(i)
message = ""
n = 0       
m = 0
z = 0
password = input("Enter the original passcode:")
pas = input("Enter passcode for Decryption")
if password == pas:
    for i in range(10):
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

