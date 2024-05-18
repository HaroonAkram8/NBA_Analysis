from src.data_manager import data_manager
from src.models.baseline.baseline import Baseline_Model
from src.nba_data.seasons import seasons_list
from src.models.print_results import print_results
from src.globals import VAL_SEASONS

def main():
    data_handler = data_manager()

    data_handler.db_connect()
    _, elo_input = data_handler.get_h2h_elo(pandas_format=True)
    data_handler.db_disconnect()

    val_seasons = seasons_list(*VAL_SEASONS)

    model = Baseline_Model(data=elo_input)
    model.inference(start_season=val_seasons[0], end_season=val_seasons[-1])
    stats = model.get_stats()

    print_results(model_name="Baseline Model", stats=stats)

if __name__ == "__main__":
    main()