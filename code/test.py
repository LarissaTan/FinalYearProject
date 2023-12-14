from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64

def generate_key_pair():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key = private_key.public_key()
    return private_key, public_key

def encrypt_text(text, public_key):
    cipher_text = public_key.encrypt(
        text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(cipher_text).decode('utf-8')

def decrypt_text(encrypted_text, private_key):
    cipher_text = base64.b64decode(encrypted_text)
    decrypted_text = private_key.decrypt(
        cipher_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted_text.decode('utf-8')

def write_encrypted_text_to_file(file_path, encrypted_text):
    with open(file_path, 'w') as file:
        file.write(encrypted_text)

def read_encrypted_text_from_file(file_path):
    with open(file_path, 'r') as file:
        encrypted_text = file.read()
    return encrypted_text

# 生成密钥对
private_key, public_key = generate_key_pair()

# 要加密的文本
plain_text = b"45"

# 检查文件是否存在并删除内容
file_path = 'encrypted_data.txt'
try:
    with open(file_path, 'r') as file:
        if file.read():
            # 文件非空，删除内容
            with open(file_path, 'w') as empty_file:
                empty_file.write('')
except FileNotFoundError:
    pass

# 加密文本
encrypted_text = encrypt_text(plain_text, public_key)

# 将加密后的文本写入文件
write_encrypted_text_to_file(file_path, encrypted_text)
print(f"Encrypted Text has been written to '{file_path}'.")

# 从文件中读取加密后的文本
read_encrypted_text = read_encrypted_text_from_file(file_path)

# 解密文本
decrypted_text = decrypt_text(read_encrypted_text, private_key)
print("Decrypted Text:", decrypted_text)