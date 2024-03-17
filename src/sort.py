from time import sleep

from bs4 import BeautifulSoup
from parser import build_game_from_soup
from files import load_game_html_from_file, load_game_html, save_game_html_to_file, ROOT_DIR, load_games
from output_writer import save_game, save_games, save_games_tsv
from src.models import Game, Question


def main():
    # load games from JSON
    games = load_games()
    # sort games
    games.sort(key=lambda x: x.air_date, reverse=True)
    # filter games
    games = filter_games(games)
    # output csv
    save_games_tsv(games, "sorted.tsv")


def is_question_included(question: Question) -> bool:
    if "[audio clue]" in question.clue or "[video clue]" in question.clue:
        return False
    return True


def is_game_included(game: Game) -> bool:
    include_keywords = ["Teen", "Kids", "Celebrity"]
    for include_keyword in include_keywords:
        if include_keyword in game.comments:
            return True
    return False


def filter_questions(questions: list[Question]) -> list[Question]:
    return [question for question in questions if is_question_included(question)]


def filter_games(games: list[Game]):
    filtered_games = []
    for game in games:
        if game.jeopardy:
            for category in game.jeopardy.categories:
                category.questions = filter_questions(category.questions)
        if game.double_jeopardy:
            for category in game.double_jeopardy.categories:
                category.questions = filter_questions(category.questions)
        if is_game_included(game):
            filtered_games.append(game)
    return filtered_games

main()
