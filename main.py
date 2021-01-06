import chess
import chess.pgn
import chess.engine
import pandas as pd
pd.set_option('display.max_rows', 15)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 100)


def main():
    # pgn = PGNReader('stevenadema', 2)
    # pgn.filter_time_control('600')
    df = pd.read_csv('df.csv', sep="|")

    print(df.shape)
    df = df[df['difs'] > 50]
    df = df.loc[df['time_control'] == 600]
    df = df.reset_index()
    print(df.shape)
    # df = df.groupby(['fen_y']).count()
    df = df.sort_values(by='index', ascending=False)

    fen = df.iloc[2]['fen_y']
    print(df.iloc[2])
    board = chess.Board(fen)
    engine = chess.engine.SimpleEngine.popen_uci('C:/Users/Steven/Downloads/stockfish_12_win_x64_bmi2/stockfish_20090216_x64_bmi2.exe')
    info = engine.analyse(board, chess.engine.Limit(depth=20))
    print(board)
    print(info)
    


if __name__ == "__main__":
    main()
