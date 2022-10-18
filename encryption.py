from cryptography.fernet import Fernet
    key = Fernet.generate_key()
    fernet = Fernet(key)

    with open("key.key", "wb") as filekey:
        filekey.write(key)

    with open("key.key", "rb") as filekey:
        key = filekey.read()

    with open(file_name, "rb") as file:
        originalaudio = file.read()

    encrypted = fernet.encrypt(originalaudio)

    with open(file_name, "wb") as encrypted_file:
        encrypted_file.write(encrypted)

    fernet = Fernet(key)
    with open(encrypted, "rb") as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)

    with open(encrypted, "wb") as dec_file:
        dec_file.write(decrypted)
