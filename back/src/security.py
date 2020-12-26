# Standard library
import os
import secrets
import tempfile

# Third party library
from cryptography.hazmat.primitives.ciphers import (
    algorithms,
    Cipher,
    modes,
)


def create_secret(n_bytes: int) -> str:
    return secrets.token_hex(n_bytes)


def encrypt(key_hex: str, path_input: str) -> None:
    key = bytes.fromhex(key_hex)
    key_len = len(key)

    if key_len != 32:
        raise ValueError('Encryption key must be exactly 256 bit long')

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()

    with tempfile.NamedTemporaryFile() as path_output_handle:
        with open(path_input) as path_input_handle:
            # Write the initialization vector
            path_output_handle.write(iv)

            # Encrypt the stream
            while data := path_input_handle.read(1024):
                path_output_handle.write(encryptor.update(data))

            # Finalize the stream
            path_output_handle.write(encryptor.finalize())

        # Let's go to the begining of file
        path_output_handle.seek(0)

        # Dump output file into input file
        with open(path_input, 'wb') as path_input_handle:
            while data := path_output_handle.read(1024):
                path_input_handle.write(data)


def decrypt(key_hex: str, path_input: str) -> None:
    key = bytes.fromhex(key_hex)
    key_len = len(key)

    with tempfile.NamedTemporaryFile() as path_output_handle:
        with open(path_input) as path_input_handle:
            iv = path_input_handle.read(16)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()

            # Decrypt the stream
            while data := path_input_handle.read(1024):
                path_output_handle.write(decryptor.update(data))

            # Finalize the stream
            path_output_handle.write(decryptor.finalize())

        # Let's go to the begining of file
        path_output_handle.seek(0)

        # Dump output file into input file
        with open(path_input, 'wb') as path_input_handle:
            while data := path_output_handle.read(1024):
                path_input_handle.write(data)
