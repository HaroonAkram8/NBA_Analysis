from src.data_manager import data_manager

def main():
    data_handler = data_manager()

    test = data_handler.db_connect()
    print(test)

    _, teaminfo = data_handler.get_all_teaminfo()
    print(teaminfo)

    _, teaminfo = data_handler.get_all_teaminfo(pandas_format=True)
    print(teaminfo)

    data_handler.db_disconnect()

if __name__ == "__main__":
    main()