import chess
import chess.pgn
import chess.engine
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import requests
import json
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 20)


class PGNReader:
    engine_path = 'C:/Users/Steven/Downloads/stockfish_12_win_x64_bmi2/stockfish_20090216_x64_bmi2.exe'
    eval_time = 0.25  # Set time for move evaluation
    limit = 20 # move limit for analysis
    df_cols = ['url', 'pgn', 'time_control', 'end_time', 'rated', 'time_class',
               'user_rating', 'user_username', 'user_result', 'user_color', 'opp_rating',
               'opp_username', 'opp_result', 'opp_color']

    df = pd.DataFrame(columns=df_cols)

    def __init__(self, username, lookback):
        self.username = username
        self.lookback = lookback
        self.get_games(self.username, self.lookback)
        self.parse_player_stats()

    def get_games(self, username, lookback):
        """ Retrieve monthly game archive via Chess.com API"""
        dt = date.today()
        while lookback > -1:
            d = dt - relativedelta(months=lookback)
            d = d.strftime('%Y/%m')
            response = requests.get(
                r'https://api.chess.com/pub/player/' + username + '/games/' + d)
            j = json.loads(response.content.decode('utf-8'))
            self.df = self.df.append(pd.DataFrame(j['games']), sort=True)
            lookback -= 1

    def parse_player_stats(self):
        """ Parse the PGN JSON to assign white/black player to user/opponent """
        for index, row in self.df.iterrows():
            if self.df.iloc[index]['black']['username'] == self.username:
                user = 'black'
                opp = 'white'
            else:
                user = 'white'
                opp = 'black'

            self.df['user_rating'][index] = self.df.iloc[index][user]['rating']
            self.df['user_username'][index] = self.df.iloc[index][user]['username']
            self.df['user_result'][index] = self.df.iloc[index][user]['result']
            self.df['user_color'][index] = user
            self.df['opp_rating'][index] = self.df.iloc[index][opp]['rating']
            self.df['opp_username'][index] = self.df.iloc[index][opp]['username']
            self.df['opp_result'][index] = self.df.iloc[index][opp]['result']
            self.df['opp_color'][index] = opp


g = PGNReader('stevenadema', 2)
print(g.df)
g.df.to_csv('df.csv', index=False, sep='|')
