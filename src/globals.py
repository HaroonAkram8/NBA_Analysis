# File paths
PRIVATE_DATA = "private_data.txt"
KEY_PATH = "backend_key.key"


# Private data parsing fields
SQL_CLOUD_INFO = "SQL_CLOUD_INFO"
USERNAME_FIELD = "username"
PASSWORD_FIELD = "password"
SQL_HOST_FIELD = "sql_host"
SQL_ADDR_FIELD = "sql_addr"


# PSQL constants
SQL_PORT = 5432
CLOUD_NBA_DB = "postgres"


# NBA API
HEADERS = {'Accept': 'application/json, text/plain, */*',
          'Accept-Encoding': 'gzip, deflate, br',
          'Accept-Language': 'en-US,en;q=0.9',
          'Connection': 'keep-alive',
          'Host': 'stats.nba.com',
          'Origin': 'https://www.nba.com',
          'Referer': 'https://www.nba.com/',
          'sec-ch-ua': '"Google Chrome";v="87", "\"Not;A\\Brand";v="99", "Chromium";v="87"',
          'sec-ch-ua-mobile': '?1',
          'Sec-Fetch-Dest': 'empty',
          'Sec-Fetch-Mode': 'cors',
          'Sec-Fetch-Site': 'same-site',
          'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Mobile Safari/537.36',
          'x-nba-stats-origin': 'stats',
          'x-nba-stats-token': 'true'}


# Game constants
WIN = True
LOSS = False
SEASON_TYPE = "Regular Season"


# Game columns
GAMELOG_COLUMNS = ['GAME_ID', 'SEASON_YEAR', 'GAME_DATE', 'TEAM_ID', 'WL', 'PTS', 'MIN', 'FGM','FGA','FG_PCT','FG3M','FG3A','FG3_PCT','FTM','FTA','FT_PCT','OREB','DREB','REB','AST','TOV','STL','BLK','BLKA','PF','PFD','PLUS_MINUS']