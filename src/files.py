import pathlib

from httpx import Client

ROOT_DIR = pathlib.Path(__file__).parent.parent.resolve()


def load_game_html(game_id):
    with Client() as client:
        response = client.get(f"https://j-archive.com/showgame.php?game_id={game_id}")
        return response.text


def get_file_path(game_id: int, ext: str = "html") -> str:
    return f"{ROOT_DIR}/games_data/{game_id}.{ext}"


def save_game_html_to_file(game_id, game_html):
    with open(get_file_path(game_id), "w", encoding="utf-8") as f:
        return f.write(game_html)


def load_game_html_from_file(game_id) -> str | None:
    try:
        with open(get_file_path(game_id), "r", encoding='cp437') as f:
            return f.read()
    except FileNotFoundError:
        return None
