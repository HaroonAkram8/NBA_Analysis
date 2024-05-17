import json
from getpass import getpass

from src.utils.encryption_keys import generate_key, load_key
from src.globals import (
    PRIVATE_DATA, SQL_CLOUD_INFO, USERNAME_FIELD, PASSWORD_FIELD, SQL_HOST_FIELD, SQL_ADDR_FIELD, KEY_PATH
)

def setup_access():
    print('LOG: Generating key...')
    generate_key()
    print('SUCCESS: Key created at ' + KEY_PATH + '...')

    fernet = load_key()
    print('SUCCESS: Loaded key from ' + KEY_PATH + '...')

    private_data_dict = {SQL_CLOUD_INFO: {}}

    private_data_dict[SQL_CLOUD_INFO][USERNAME_FIELD] = input("Enter your cloud Postgresql username: ")
    private_data_dict[SQL_CLOUD_INFO][PASSWORD_FIELD] = getpass('Enter your cloud Postgresql password: ')
    private_data_dict[SQL_CLOUD_INFO][SQL_HOST_FIELD] = getpass('Enter your cloud Postgresql host address: ')
    private_data_dict[SQL_CLOUD_INFO][SQL_ADDR_FIELD] = getpass('Enter your cloud Postgresql address: ')

    private_data_str = str(json.dumps(private_data_dict))
    
    enc_priv_data = fernet.encrypt(private_data_str.encode())
    with open(PRIVATE_DATA, 'wb') as file:
        file.write(enc_priv_data)
        print('SUCCESS: Wrote your data to ' + PRIVATE_DATA + '...')

if __name__ == "__main__":
    setup_access()