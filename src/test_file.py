from time import sleep

from bs4 import BeautifulSoup
from parser import build_game_from_soup
from files import load_game_html_from_file, load_game_html, save_game_html_to_file, ROOT_DIR
from output_writer import save_game, save_games

from src.service import process_game


def main():
    game_id = 3067
    game_html = load_game_html(game_id)
    path = f"{ROOT_DIR}/{game_id}.html"
    save_game_html_to_file(game_id, game_html, path)
    soup = BeautifulSoup(game_html, 'html.parser')
    game = build_game_from_soup(soup)
    print(game.title)
    save_game(game_id, game)


main()
