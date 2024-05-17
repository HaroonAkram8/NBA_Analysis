import pandas as pd

from src.sql_db.sql_db_class import nba_psql
from src.utils.private_data_reader import private_data_reader
from src.globals import (
    PRIVATE_DATA, SQL_CLOUD_INFO, USERNAME_FIELD, PASSWORD_FIELD, SQL_HOST_FIELD, SQL_ADDR_FIELD,
    SQL_PORT, CLOUD_NBA_DB
)

class data_manager(nba_psql):
    def db_connect(self):
        sql_data = private_data_reader(private_data_path=PRIVATE_DATA, section_key=SQL_CLOUD_INFO)
        sql_username = sql_data[USERNAME_FIELD] + sql_data[SQL_ADDR_FIELD]

        return self._connect(sql_user=sql_username, sql_password=sql_data[PASSWORD_FIELD], sql_host=sql_data[SQL_HOST_FIELD], sql_port=SQL_PORT, sql_database=CLOUD_NBA_DB)

    def db_disconnect(self):
        self._disconnect()

    def get_all_teaminfo(self, pandas_format: bool=False):
        success, teaminfo = self._select_teaminfo()

        if pandas_format and success:
            teaminfo = pd.DataFrame(teaminfo['data'], columns=teaminfo['columns'])
        
        return success, teaminfo