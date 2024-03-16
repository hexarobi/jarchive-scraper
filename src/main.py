from time import sleep

from output_writer import save_games
from src.service import process_game

# Counts down
START_GAME_ID = 8842
END_GAME_ID = 0
PAGE_LOAD_DELAY = 15


def main():
    games = []
    game_id = START_GAME_ID
    while game_id > END_GAME_ID:
        try:
            game = process_game(game_id)
            if game.was_downloaded:
                sleep(PAGE_LOAD_DELAY)
            games.append(game)
        except Exception as e:
            print(f"Error processing game {game_id}: {e}")
            # raise
        game_id = game_id - 1

    save_games(games)


main()
