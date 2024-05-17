from src.data_manager import data_manager

def main():
    data_handler = data_manager()

    data_handler.db_connect()

    #data_handler.populate_gamelogs(start_season_year=2012, end_season_year=2023)
    data_handler.update_elo()

    data_handler.db_disconnect()

if __name__ == "__main__":
    main()