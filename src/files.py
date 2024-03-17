import json
import os
import pathlib
from math import floor

from httpx import Client

from src.models import Game

ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve()


def load_game_html(game_id):
    with Client() as client:
        response = client.get(f"https://j-archive.com/showgame.php?game_id={game_id}")
        return response.text


def load_games() -> list[Game]:
    games = []
    games_dict = load_games_dict()
    for game_dict in games_dict:
        game = Game.model_validate(game_dict)
        games.append(game)
    return games


def load_games_dict():
    with open(f"{ROOT_DIR}/output/all_games.json", "r") as f:
        return json.loads(f.read())


def get_file_path(game_id: int, ext: str = "html") -> str:
    dir_path = f"{ROOT_DIR}/data/games/{floor(game_id/100)*100}"
    os.makedirs(dir_path, exist_ok=True)
    return f"{dir_path}/{game_id}.{ext}"


def save_game_html_to_file(game_id, game_html, path: str = None):
    if not path:
        path = get_file_path(game_id)
    with open(path, "w", encoding="utf-8") as f:
        return f.write(game_html)


def load_game_html_from_file(game_id) -> str | None:
    try:
        with open(get_file_path(game_id), "r", encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return None
