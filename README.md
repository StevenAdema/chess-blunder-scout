![Blunder Scout Logo](/static/css/blunder_scout.png)

Correct blunders from previous games on chess.com.

## Screenshot

![Blunder Scout Screenshot](/static/blunder_scout_screenshot.png)

<br/>

## Installation

1. ``` git clone https://github.com/StevenAdema/blunder-scout.git ```
2. ``` pip install -r requirements.txt ```
3. ```env\Scripts\activate```
4. ```python app.py```
5. Open http://127.0.0.1:5000/ in the browser

### How it works
1. A user submits their chess.com username.
2. read_pgn.py calls the chess.com API to retrieve game history.
3. python-chess library analyzes a random set of games.
4. A dictionary of innacurate moves is created by comparing the pov score of played moves against the optimal moves determined by the engine.