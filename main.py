import chess
import chess.pgn
import chess.engine
import chess.svg
import pandas as pd
from read_pgn import PGNReader
from db import ChessDB
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 200)

df = pd.read_csv('df3.csv', sep='|')
# df['fen_x'] = [x.split('-')[-0] for x in df['fen_x']]
# print(df)
# print(df['fen_x'].value_counts())
df['fen_x'].value_counts().to_csv('df4.csv')

fen = df.iloc[1]['fen_x']
# print(df.iloc[1])
board = chess.Board(fen)
engine = chess.engine.SimpleEngine.popen_uci('C:/Users/Steven/Documents/Unsorted/stockfish_14.1_win_x64_avx2.exe')
print(chess.svg.board(board, colors={'square light': '#aeced6', 'square dark': '#4f6c73'},arrows=[chess.svg.Arrow(chess.F3, chess.E5)]))
info = engine.analyse(board, chess.engine.Limit(depth=20))
exit()

def main():
    pgn = PGNReader('stevenadema', 10)
    pgn.filter_time_control('600')
    # df = pd.read_csv('df.csv', sep="|")
    # db = ChessDB(pgn.df)
    df = pgn.df
    df = df[['url','fen_x','move_no','my_move_uci','my_move_score','best_move_uci','best_move_score','difs']]
    df.to_csv('df.csv', sep="|", index=False)
    df3 = df[df['difs'] > 80]
    df3 = df3.drop_duplicates(subset=['url', 'my_move_uci'])
    df3.to_csv('df3.csv', sep="|", index=False)
    exit()

if __name__ == "__main__":
    main()
