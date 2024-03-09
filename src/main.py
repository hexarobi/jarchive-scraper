from time import sleep

from bs4 import BeautifulSoup
from parser import build_game_from_soup
from files import load_game_html_from_file, load_game_html, save_game_html_to_file
from output_writer import save_game, save_games

START_GAME_ID = 8840
END_GAME_ID = 8800
PAGE_LOAD_DELAY = 30


def main():
    games = []
    game_id = START_GAME_ID
    while game_id > END_GAME_ID:
        try:
            print(f"Processing Game {game_id}")
            game_html = load_game_html_from_file(game_id)
            if not game_html:
                game_html = load_game_html(game_id)
                save_game_html_to_file(game_id, game_html)
                sleep(PAGE_LOAD_DELAY)
            soup = BeautifulSoup(game_html, 'html.parser')
            game = build_game_from_soup(soup)
            print(game.title)
            save_game(game_id, game)
            games.append(game)
        except Exception as e:
            print(f"Error procesing game {game_id}: {e}")
            # raise
        game_id = game_id - 1

    save_games(games)


main()
