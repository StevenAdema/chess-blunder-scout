![Blunder Scout Logo](/static/css/blunder_scout.png)

### &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Correct blunders from your previous games on Chess.com


## Briefly
A Flask app that randomly selects previously played positions where you had made an innacuracy. Improve your chess by finding the moves you missed! 

## Screenshot

![Blunder Scout Screenshot](/static/blunder_scout_screenshot.png)

<br/>

## Installation

1. ``` git clone https://github.com/StevenAdema/blunder-scout.git ```
2. ``` pip install -r requirements.txt ```
3. ```env\Scripts\activate```
4. ```python app.py```
5. Open http://127.0.0.1:5000/ in the browser

## How it works
1. User submits their chess.com username.
2. read_pgn.py calls the chess.com API to retrieve game history.
3. python-chess library analyzes a random set of games.
4. A DataFrame of all moves, optimal moves determined by the engine, and game metadata is created.
5. A random innacurate move is selected and fed to the appropriate template HTML file.

## WIP
- display feedback message on move guesses
- show hints (e.g. highlight piece to move)
- reveal best move on both board and in button
