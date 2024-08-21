import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random
from math import gcd
from sympy import primerange
import os


# Generate a prime number with a specific number of digits
def generate_prime(digits):
    return random.choice(list(primerange(10 ** (digits - 1), 10 ** digits)))


# RSA encryption function
def rsa_encryption(message, e, n):
    encrypted_message = [str(pow(ord(char), e, n)) for char in message]
    encrypted_string = ' '.join(encrypted_message)
    return encrypted_string


# RSA decryption function
def rsa_decryption(encrypted_message, d, n):
    decrypted_message = ''.join([chr(pow(int(char), d, n)) for char in encrypted_message.split()])
    return decrypted_message


# Main RSA function to generate keys and process the content
def rsa(message_content, operation, key_file='rsa_keys.txt'):
    if operation == 'decrypt':
        with open(key_file, 'r') as kf:
            keys = kf.read().split()
            p = int(keys[0])
            q = int(keys[1])
            e = int(keys[2])
            d = int(keys[3])
            n = int(keys[4])
            phi_n = int(keys[5])
        return rsa_decryption(message_content, d, n)
    else:
        # Convert the message to a list of ASCII values
        ascii_values = [ord(char) for char in message_content]
        digits = len(str(max(ascii_values)))

        # Generate two random prime numbers p and q
        p = generate_prime(digits)
        while True:
            q = generate_prime(digits)
            if gcd(p, q) == 1 and p != q:
                break

        # Calculate n = p * q
        n = p * q

        # Calculate phi_n = (p-1) * (q-1)
        phi_n = (p - 1) * (q - 1)

        # Generate a list of prime numbers less than phi_n
        primes = list(primerange(1, phi_n))

        # Select a random prime number that is relatively prime to phi_n
        e = random.choice(primes)
        while gcd(e, phi_n) != 1:
            e = random.choice(primes)

        # Calculate d = e^-1 mod phi_n
        d = pow(e, -1, phi_n)

        # Save the keys for later use
        with open(key_file, 'w') as kf:
            kf.write(f"{p} {q} {e} {d} {n} {phi_n}")

        return rsa_encryption(message_content, e, n)


class RSAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("RSA Encryption/Decryption")
        self.root.geometry("800x600")

        # Load the background image
        self.original_bg_image = Image.open("background.png")
        self.bg_image = ImageTk.PhotoImage(self.original_bg_image)
        self.background_label = tk.Label(self.root, image=self.bg_image)
        self.background_label.place(relwidth=1, relheight=1)

        # File selection
        self.label = tk.Label(root, text="Select a text file:", font = ('TIMES new roman', 15) ,width=20, bg='white')
        self.label.place(relx=0.5, rely=0.2, anchor='center')

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file, bg='green',width=15, fg='white')
        self.browse_button.place(relx=0.5, rely=0.3, anchor='center')

        self.encrypt_button = tk.Button(root, text="Encrypt", command=lambda: self.process_file('encrypt'), bg='blue',
                                        width=15, fg='white')
        self.decrypt_button = tk.Button(root, text="Decrypt", command=lambda: self.process_file('decrypt'), bg='red',
                                        width=15, fg='white')

        self.encrypt_button.place(relx=0.4, rely=0.4, anchor='center')
        self.decrypt_button.place(relx=0.6, rely=0.4, anchor='center')

        self.result_label = tk.Label(root, text="", bg='white')
        self.result_label.place(relx=0.5, rely=0.5, anchor='center')

    def browse_file(self):
        self.file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.file_path:
            self.result_label.config(text=f"Selected file: {os.path.basename(self.file_path)}")

    def process_file(self, action):
        if not hasattr(self, 'file_path') or not self.file_path:
            messagebox.showerror("Error", "No file selected!")
            return

        with open(self.file_path, 'r') as file:
            content = file.read()

        processed_message = rsa(content, action)

        with open(self.file_path, 'w') as file:
            file.write(processed_message)

        self.result_label.config(text=f"File successfully {action}ed.")

    def resize_bg_image(self, event):
        new_width = event.width
        new_height = event.height
        resized_bg_image = self.original_bg_image.resize((new_width, new_height), Image.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(resized_bg_image)
        self.background_label.config(image=self.bg_image)


if __name__ == "__main__":
    root = tk.Tk()
    app = RSAApp(root)
    root.bind("<Configure>", app.resize_bg_image)
    root.mainloop()

