from time import sleep

from bs4 import BeautifulSoup
from parser import build_game_from_soup
from files import load_game_html_from_file, load_game_html, save_game_html_to_file, ROOT_DIR, load_games
from output_writer import save_game, save_games, save_games_tsv


def main():
    # load games from JSON
    games = load_games()
    # sort games
    games.sort(key=lambda x: x['air_date'], reverse=True)
    # output csv
    save_games_tsv(games, "sorted.tsv")


main()
