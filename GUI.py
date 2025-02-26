import cv2
import os
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox

def generate_mappings():
    d = {chr(i): i for i in range(255)}
    c = {i: chr(i) for i in range(255)}
    return d, c

def encrypt_message(image_path, message, password, output_path="encryptedImage.jpg"):
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Image not found.")
        return
    
    d, _ = generate_mappings()
    n, m, z = 0, 0, 0
    
    for char in message:
        img[n, m, z] = d[char]
        n += 1
        m += 1
        z = (z + 1) % 3
    
    cv2.imwrite(output_path, img)
    messagebox.showinfo("Success", "Message encrypted successfully.")
    os.system(f"start {output_path}")
    return password

def decrypt_message(image_path, original_message_length, password):
    img = cv2.imread(image_path)
    if img is None:
        messagebox.showerror("Error", "Image not found.")
        return
    
    _, c = generate_mappings()
    
    pas = simpledialog.askstring("Input", "Enter passcode for Decryption:", show='*')
    if password != pas:
        messagebox.showerror("Error", "YOU ARE NOT AUTHORIZED")
        return
    
    message = ""
    n, m, z = 0, 0, 0
    
    for _ in range(original_message_length):
        message += c[img[n, m, z]]
        n += 1
        m += 1
        z = (z + 1) % 3
    
    messagebox.showinfo("Decryption Successful", f"Decrypted message: {message}")

def select_image():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.png;*.bmp")])
    return file_path

def main():
    root = tk.Tk()
    root.withdraw()
    
    image_path = select_image()
    if not image_path:
        return
    
    msg = simpledialog.askstring("Input", "Enter secret message:")
    password = simpledialog.askstring("Input", "Enter a passcode:", show='*')
    
    stored_password = encrypt_message(image_path, msg, password)
    decrypt_message("encryptedImage.jpg", len(msg), stored_password)

if __name__ == "__main__":
    main()
