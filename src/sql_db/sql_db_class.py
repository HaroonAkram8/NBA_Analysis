import psycopg2 as pg

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
    
    # =====================================================
    #     SELECT QUERIES
    # =====================================================

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