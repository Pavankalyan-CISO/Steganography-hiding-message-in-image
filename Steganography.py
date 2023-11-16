# Requires the following libraries- hashlib,getpass,warnings,OpenCV,os,string.
# In my case i have used "Kali.jpg" as cover file
import hashlib
import getpass
import warnings
import cv2
import os
import string

warnings.filterwarnings("ignore", category=UserWarning, module="getpass")

def hash_password(password):
    hash_object = hashlib.sha256(password.encode())
    return hash_object.hexdigest()

def evaluate_password_strength(password):
    if len(password) < 8:
        return "Weak: Password should be at least 8 characters long."
    elif not any(char.isdigit() for char in password):
        return "Weak: Password should contain at least one digit."
    elif not any(char.isalpha() for char in password):
        return "Weak: Password should contain at least one letter."
    else:
        return "Strong: Password meets minimum strength criteria."

def encrypt_image(img, msg):
    d = {chr(i): i for i in range(255)}
    m, n, z = 0, 0, 0

    for i in range(len(msg)):
        img[n, m, z] = d[msg[i]]
        n, m, z = n + 1, m + 1, (z + 1) % 3

    return img

def decrypt_message(img, stored_hashed_password):
    c = {i: chr(i) for i in range(255)}
    message = ""
    n, m, z = 0, 0, 0

    attempt_count = 0
    max_attempts = 3

    while attempt_count < max_attempts:
        entered_password = getpass.getpass("Enter passcode for Decryption: ")
        entered_hashed_password = hash_password(entered_password)

        if stored_hashed_password == entered_hashed_password:
            for i in range(len(msg)):
                message += c[img[n, m, z]]
                n, m, z = n + 1, m + 1, (z + 1) % 3
            print("Decryption message:", message)
            break
        else:
            attempt_count += 1
            print(f"Incorrect password,try again-attempt {attempt_count}/{max_attempts}")

    if attempt_count == max_attempts:
        print("Sorry,Maximum attempts reached. Exiting...")

if __name__ == "__main__":
    img = cv2.imread("Kali.jpg")

    msg = input("Enter secret message: ")

    while True:
        password = getpass.getpass("Enter password: ")
        strength_message = evaluate_password_strength(password)
        print(strength_message)
        if "Strong" in strength_message:
            break

    hashed_password = hash_password(password)

    img = encrypt_image(img, msg)
    cv2.imwrite("Encryptedmsg.jpg", img)
    os.system("start Encryptedmsg.jpg")

    decrypt_message(img, hashed_password)
