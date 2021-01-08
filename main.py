import chess
import chess.pgn
import chess.engine
import pandas as pd
from read_pgn import PGNReader
from db import ChessDB
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 200)


def main():
    # pgn = PGNReader('stevenadema', 2)
    # pgn.filter_time_control('600')
    df = pd.read_csv('df.csv', sep="|")
    # db = ChessDB(pgn.df)
    print(df.shape)
    df = df[['url','fen_y','mv','mv_score','bmv','bmv_score','difs']]
    df = df[df['difs'] > 100]
    print(df.shape)
    df = df.drop_duplicates(subset=['url', 'mv'])
    print(df.shape)
    df.to_csv('df3.csv', sep="|", index=False)
    df2 = df.groupby(by=['fen_y']).count()
    df2 = df2.sort_values(by='mv', ascending=False)
    print(df2)
    df.to_csv('df4.csv', sep="|", index=False)
    exit()


    fen = df.iloc[2]['fen_y']
    print(df.iloc[2])
    board = chess.Board(fen)
    engine = chess.engine.SimpleEngine.popen_uci('C:/Users/Steven/Downloads/stockfish_12_win_x64_bmi2/stockfish_20090216_x64_bmi2.exe')
    info = engine.analyse(board, chess.engine.Limit(depth=20))
    print(board)
    print(info)
    


if __name__ == "__main__":
    main()
