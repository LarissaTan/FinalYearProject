from cryptography.fernet import Fernet

file_path = 'encrypted_pulse_data.txt'

def generate_or_load_key(file_path='secret_pulse.key'):
    try:
        # 从文件中读取密钥
        with open(file_path, 'rb') as key_file:
            key = key_file.read()
    except FileNotFoundError:
        # 如果文件不存在，生成一个新的密钥并保存到文件中
        key = Fernet.generate_key()
        with open(file_path, 'wb') as key_file:
            key_file.write(key)

    return key

def initialize_cipher(key):
    return Fernet(key)

def encrypt_text(text, cipher):
    encrypted_text = cipher.encrypt(text.encode('utf-8'))
    return encrypted_text

def decrypt_text(encrypted_text, cipher):
    decrypted_text = cipher.decrypt(encrypted_text).decode('utf-8')
    return decrypted_text

def write_encrypted_text_to_file(file_path, encrypted_text):
    with open(file_path, 'ab') as file:
        file.write(encrypted_text)
        file.write(b'\n')

def read_encrypted_text_from_file(file_path):
    with open(file_path, 'rb') as file:
        encrypted_texts = [line.strip() for line in file.readlines()]
    return encrypted_texts

def clear_first_line(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    if len(lines) > 10:
        with open(file_path, 'w') as file:
            file.writelines(lines[1:])
            print("Deleted the first line.")
    else:
        print("File does not have at least 10 lines.")


def init_txt():
    # 生成或加载密钥
    key = generate_or_load_key()

    # 初始化加密算法
    cipher = initialize_cipher(key)
    return cipher




# 清空文件内容
def clear_file():
    with open(file_path, 'w') as file:
        file.write('')

def write_data_pulse(data):
    # 加密文本
    encrypted_text = encrypt_text(data, init_txt())
    # 将加密后的文本写入文件
    write_encrypted_text_to_file(file_path, encrypted_text)
    clear_first_line(file_path)
    print(f"Encrypted Text has been written to '{file_path}'.")

def read_data_pulse():
    # 从文件中读取加密后的文本
    read_encrypted_texts = read_encrypted_text_from_file(file_path)

    '''
    # 输出读取到的每一行密文
    for i, read_encrypted_text in enumerate(read_encrypted_texts):
        print(f"Line {i + 1}: {read_encrypted_text}")
    '''

    # 存储解密后的文本的数组
    decrypted_texts = []

    # 解密文本
    for read_encrypted_text in read_encrypted_texts:
        try:
            tmp = decrypt_text(read_encrypted_text, init_txt())
            decrypted_text = tmp.split(";")
            decrypted_texts.append(decrypted_text)
            #print("Decrypted Text:", decrypted_text)
        except Exception as e:
            print(f"Failed: {e}")

    return decrypted_texts
