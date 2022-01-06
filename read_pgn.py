import chess
import chess.pgn
import chess.engine
import pandas as pd
from datetime import date
from dateutil.relativedelta import relativedelta
import requests
import json
import io
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 300)


class PGNReader:
    engine_path = 'C:/Users/Steven/Documents/Unsorted/stockfish_14.1_win_x64_avx2.exe'
    eval_time = 0.3  # Set time for move evaluation
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
        self.format_df()
        self.df = self.df.head(1)
        self.df_moves = self.get_move_scores()
        self.df = pd.merge(self.df_moves, self.df, on='url', how='left')
        self.df_moves.to_csv('df4.csv', sep="|", index=False)
        self.df.to_csv('df.csv', index=False, sep='|')

    def get_games(self, username, lookback):
        """ Retrieve monthly game archive via Chess.com API"""
        dt = date.today()
        while lookback > 0:
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

    def format_df(self):
        self.df.drop(columns=['black', 'white'], inplace=True)
        self.df['end_time'] = pd.to_datetime(self.df['end_time'], unit='s')

    def filter_time_control(self, time_control):
        self.df = self.df.loc[self.df['time_control'] == time_control]
        self.df.reset_index(drop=True, inplace=True)

    def get_move_scores(self):
        url, fen, mv, mv_score, bmv, bmv_score, difs = [], [], [], [], [], [], []

        def get_move_score(board_info, color, mate=1500):
            if color == 'white':
                if board_info['score'].is_mate():
                    m = board_info['score'].white().score(mate_score=mate)
                else: 
                    m = int(format(board_info['score'].white().score()))
            else:
                if board_info['score'].is_mate():
                    m = board_info['score'].black().score(mate_score=mate)
                else: 
                    m = int(format(board_info['score'].black().score()))

            return m

        for index, row in self.df.iterrows():
            g = self.df.iloc[index]['pgn']
            print('analyzing game ', index)

            user_color = self.df.iloc[index]['user_color']
            pgn = io.StringIO(g)
            game = chess.pgn.read_game(pgn)

            # setup board and engine
            board = chess.Board()
            engine = chess.engine.SimpleEngine.popen_uci(self.engine_path)
            i = 0

            for move in game.mainline_moves():
                # Only analyse user moves
                if (i % 2 == 0 and user_color == 'black') or (i % 2 == 1 and user_color == 'white'):
                    board.push(move)
                    i += 1
                    continue

                # Get move, score and difference of user move and best move
                mymove_info = engine.analyse(board, chess.engine.Limit(time=self.eval_time))
                best_move = mymove_info['pv'][0]
                fen.append(str(board.fen()))
                board.push(move)
                mymove_info = engine.analyse(board, chess.engine.Limit(time=self.eval_time))
                mymove_score = get_move_score(mymove_info, user_color)
                board.pop()
                board.push(best_move)
                bestmove_info = engine.analyse(board, chess.engine.Limit(time=self.eval_time))
                bestmove_score = get_move_score(bestmove_info, user_color)
                dif = bestmove_score - mymove_score
                board.pop()
                board.push(move)

                # get fens, labels, povscores, difs
                url.append(self.df.iloc[index]['url'])
                mv.append(str(move))
                mv_score.append(mymove_score)
                bmv.append(str(best_move))
                bmv_score.append(bestmove_score)
                difs.append(dif)

                if i > self.limit:
                    break
                i += 1

            engine.quit()

        game_moves_df = pd.DataFrame(
            {'url': url,
             'fen': fen,
             'mv': mv,
             'mv_score': mv_score,
             'bmv': bmv,
             'bmv_score': bmv_score,
             'difs': difs
             })

        return game_moves_df

# pgn = PGNReader('stevenadema', 1)
# df = pgn.df
# df = df[['url','fen_x','mv','mv_score','bmv','bmv_score','difs']]
# # df = df[df['difs'] > 100]
# print(df)