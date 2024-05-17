import pandas as pd
import psycopg2 as pg
from tqdm import tqdm

from src.globals import GAMELOG_COLUMNS

class nba_psql:
    def __init__(self):
        self.connection = None

    def _connect(self, sql_user: str, sql_password: str, sql_host: str, sql_port: int, sql_database: str):
        try:
            self.connection = pg.connect(user=sql_user, password=sql_password, host=sql_host, port=sql_port, database=sql_database)
            return True
        except pg.Error:
            return False
    
    def _disconnect(self):
        try:
            if self.connection and not self.connection.closed:
                self.connection.close()
            return True
        except pg.Error:
            return False

    def _select_teaminfo(self):
        success = False
        teams = {}

        with self.connection.cursor() as cursor:
            query = 'SELECT id, abbr, name from teaminfo;'
            cursor.execute(query)

            teams['columns'] = ['id', 'abbr', 'name']
            teams['data'] = cursor.fetchall()

            self.connection.commit()
            success = True
        
        return success, teams
    
    def _insert_gamelogs(self, df_gamelogs: pd.DataFrame):
        success = False
        df_gamelogs = df_gamelogs[GAMELOG_COLUMNS + ['AT_HOME']]
        tuples = [tuple(x) for x in df_gamelogs.to_numpy()]

        with self.connection.cursor() as cursor:
            query = "INSERT INTO gamelogs (game_id, season_year, game_date, team_id, wl, pts, min, fgm,fga, fg_pct, fg3m, fg3a, fg3_pct, \
                    ftm, fta, ft_pct, oreb, dreb, reb, ast, tov, stl, blk, blka, pf, pfd, plus_minus, at_home) \
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING;"
            
            for i in tqdm(range(0, len(tuples)), desc=f"Uploading to the gamelogs table"):
                cursor.execute(query, tuples[i])

            self.connection.commit()
            success = True

        return success