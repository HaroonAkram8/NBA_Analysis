import numpy as np
import pandas as pd
from tqdm import tqdm

from nba_api.stats import endpoints
from src.globals import HEADERS, GAMELOG_COLUMNS, WIN, LOSS

def get_gamelogs(team_ids: list, seasons: list, season_type: str):
    columns = GAMELOG_COLUMNS + ['MATCHUP']
    df_all_game_logs = pd.DataFrame(columns=columns)

    for season in seasons:
        for i in tqdm(range(0, len(team_ids)), desc=f"Retrieving game logs for each NBA team in the {season} season"):
            df_team_game_logs = query_gamelogs(team_id=team_ids[i], season_type=season_type, season=season, columns=columns)
            df_all_game_logs = pd.concat([df_all_game_logs, df_team_game_logs], ignore_index=True)

    df_all_game_logs['GAME_DATE'] = df_all_game_logs['GAME_DATE'].apply(lambda x: x.replace('T00:00:00', ''))
    df_all_game_logs['WL'] = np.where(df_all_game_logs['WL'] == 'W', WIN, LOSS)
    df_all_game_logs['AT_HOME'] = df_all_game_logs['MATCHUP'].apply(lambda x: not '@' in x)
    df_all_game_logs = df_all_game_logs.drop('MATCHUP', axis=1)

    return df_all_game_logs

def query_gamelogs(team_id: int, season_type: str, season: str, columns: list):
    team_game_logs = endpoints.teamgamelogs.TeamGameLogs(team_id_nullable=team_id, season_type_nullable=season_type, season_nullable=season, headers=HEADERS)
    df_team_game_logs = team_game_logs.get_data_frames()
    return df_team_game_logs[0][columns]