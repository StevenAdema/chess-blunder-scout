from flask import Flask, render_template, url_for, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from read_pgn import PGNReader
import pandas as pd
import chess
import chess.pgn
import chess.engine
import chess.svg
from flask_fontawesome import FontAwesome

app = Flask(__name__)
fa = FontAwesome(app)
app.static_folder = 'static' 
app.secret_key = "poppadontpreach"
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/blunders', methods=['POST', 'GET'])
def greeter():
    # chess_user = str(request.form['name_input'])
    chess_user = 'stevenadema'
    pgn = PGNReader(chess_user, 1)
    pgn.filter_time_control('600') 
    df = pgn.df
    # print(df)
    # df = pd.read_csv('df3.csv', sep='|')
    df = df[df['difs'] > 150]
    move_no = df['move_no'].values[0]
    best_move = str(df['best_move_san'].values[0])
    best_move_uci = str(df['best_move_uci'].values[0])
    my_move_uci = str(df['my_move_uci'].values[0])
    fen = df['fen_x'].values[0]
    url = df['url'].values[0]
    user = df['user_username'].values[0]
    user_color = df['user_color'].values[0]
    user_rating = df['user_rating'].values[0]
    opp = df['opp_username'].values[0]
    opp_rating = df['opp_rating'].values[0]
    url = df['url'].values[0]
    date = df['end_time'].values[0]
    date = pd.to_datetime(str(date))
    date = date.strftime('%d.%m.%Y')
    content = {
        'url':url,
        'user':user,
        'user_rating':user_rating,
        'opp':opp,
        'opp_rating':opp_rating,
        'move_no':move_no,
        'date':date,
        'best_move':best_move,
        'best_move_uci':best_move_uci,
        'my_move_uci':my_move_uci

    }

    board = chess.Board(fen) 

    bm_from = chess.parse_square(name=best_move_uci[0:2])
    bm_to = chess.parse_square(name=best_move_uci[2:4])
    mm_from = chess.parse_square(name=my_move_uci[0:2])
    mm_to = chess.parse_square(name=my_move_uci[2:4])

    flipped = False
    if user_color == 'black':
        flipped = True

    board_svg = chess.svg.board(
        board,
        colors={'square light': '#aeced6', 'square dark': '#4f6c73'},
        arrows=[(bm_from,bm_to),(mm_from, mm_to)],
        flipped=flipped
        )

    file = open("svg.txt", "w")
    file.write(board_svg)
    file.close()

    return render_template("blunders.html", svg=board_svg, **content)


if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
