from bs4 import BeautifulSoup
from parser import build_game_from_soup
from files import load_game_html_from_file, load_game_html, save_game_html_to_file
from output_writer import save_game
from src.models import Game


def process_game(game_id: int) -> Game:
    print(f"Processing Game {game_id}")
    was_downloaded = False
    game_html = load_game_html_from_file(game_id)
    if not game_html:
        game_html = load_game_html(game_id)
        was_downloaded = True
        save_game_html_to_file(game_id, game_html)
    soup = BeautifulSoup(game_html, 'html.parser')
    game = build_game_from_soup(soup)
    print(game.title)
    save_game(game_id, game)
    game.was_downloaded = was_downloaded
    return game
