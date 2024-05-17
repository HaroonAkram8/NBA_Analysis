import json

from src.utils.encryption_keys import load_key

def private_data_reader(private_data_path: str, section_key: str):
    with open(private_data_path, 'rb') as file:
        token = file.read()

    fernet = load_key()
    data_str = fernet.decrypt(token).decode()
    data_dict = json.loads(data_str)

    return data_dict[section_key]