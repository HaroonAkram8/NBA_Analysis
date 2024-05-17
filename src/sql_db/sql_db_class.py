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
    
    def _select_games_for_elo(self):
        success = False
        games = {}

        with self.connection.cursor() as cursor:
            query = "SELECT g1.season_year AS season_year, g1.game_id AS game_id, g1.team_id AS h_team_id, g2.team_id AS a_team_id, g1.pts AS h_pts, g2.pts AS a_pts \
                    FROM Gamelogs g1 JOIN Gamelogs g2 \
                    ON g1.game_id = g2.game_id AND g1.at_home AND NOT g2.at_home \
                    ORDER BY g1.game_date;"
            
            cursor.execute(query)

            games['columns'] = ['season_year', 'game_id', 'h_team_id', 'a_team_id', 'h_pts', 'a_pts']
            games['data'] = cursor.fetchall()

            self.connection.commit()
            success = True
        
        return success, games
    
    def _insert_elos(self, elo_ratings: list):
        success = False

        with self.connection.cursor() as cursor:
            query = "UPDATE Gamelogs SET elo_rating = %s \
                    WHERE game_id = %s AND team_id = %s;"
            
            for i in tqdm(range(0, len(elo_ratings)), desc=f"Setting ELO rating for each game"):
                game_id, h_team_id, a_team_id, h_elo, a_elo = elo_ratings[i]
                
                cursor.execute(query, (h_elo, game_id, h_team_id))
                cursor.execute(query, (a_elo, game_id, a_team_id))

            self.connection.commit()
            success = True

        return success