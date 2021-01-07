import sqlite3


class ChessDB:
    """Create a sqlite database of recorded chess games with relevant metadata"""

    def __init__(self, df):
        self.df = df
        self._conn = sqlite3.connect('.\data\chess_games.db')
        self._cursor = self._conn.cursor()
        ChessDB.wipe_db(self)
        ChessDB.generate_chess_db(self)
        self._conn.commit()
        self._conn.close()

    def generate_chess_db(self):
        """Method to read a DataFrame to a sqlite database.
        Args:
            games: PGN text file of recorded chess games.
        """
        self.df.to_sql('chess_data', con=self._conn)


    def wipe_db(self):
        self._cursor.execute('DROP TABLE chess_data')
