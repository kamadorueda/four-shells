# Standard library
import os
import secrets
import tempfile

# Third party library
from cryptography.hazmat.primitives import (
    padding,
)
from cryptography.hazmat.primitives.ciphers import (
    algorithms,
    Cipher,
    modes,
)

# Encryption constants for AES256-CBC, in Bytes
KEY_LEN: int = 32
IV_LEN: int = 16
BLOCK_SIZE: int = 1024


def create_secret(n_bytes: int) -> str:
    return secrets.token_hex(n_bytes)


def encrypt(key_hex: str, path_input: str) -> None:
    if len(key := bytes.fromhex(key_hex)) != KEY_LEN:
        raise ValueError('Encryption key must be exactly 256 bit long')

    iv = os.urandom(IV_LEN)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(BLOCK_SIZE).padder()

    with tempfile.NamedTemporaryFile() as path_output_handle:
        with open(path_input, 'rb') as path_input_handle:
            # Write the initialization vector
            path_output_handle.write(iv)

            # Encrypt the stream
            while data := path_input_handle.read(BLOCK_SIZE):
                path_output_handle.write(encryptor.update(padder.update(data)))

            # Finalize the stream
            path_output_handle.write(encryptor.update(padder.finalize()))
            path_output_handle.write(encryptor.finalize())

        # Let's go to the begining of file
        path_output_handle.seek(0)

        # Dump output file into input file
        with open(path_input, 'wb') as path_input_handle:
            while data := path_output_handle.read(BLOCK_SIZE):
                path_input_handle.write(data)


def decrypt(key_hex: str, path_input: str) -> None:
    key = bytes.fromhex(key_hex)
    unpadder = padding.PKCS7(BLOCK_SIZE).unpadder()

    with tempfile.NamedTemporaryFile() as path_output_handle:
        with open(path_input, 'rb') as path_input_handle:
            iv = path_input_handle.read(IV_LEN)
            cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
            decryptor = cipher.decryptor()

            # Decrypt the stream
            while data := path_input_handle.read(BLOCK_SIZE):
                path_output_handle.write(unpadder.update(decryptor.update(data)))

            # Finalize the stream
            path_output_handle.write(unpadder.update(decryptor.finalize()))
            path_output_handle.write(unpadder.finalize())

        # Let's go to the begining of file
        path_output_handle.seek(0)

        # Dump output file into input file
        with open(path_input, 'wb') as path_input_handle:
            while data := path_output_handle.read(BLOCK_SIZE):
                path_input_handle.write(data)
