import csv
import json

from models import Game
from files import get_file_path, ROOT_DIR

OUTPUT_TSV_COLUMNS = ['air_date', 'show_number', 'category', 'value', 'question', 'answer']


def save_game(game_id, game: Game):
    with open(get_file_path(game_id, "json"), "w", encoding="utf-8") as f:
        f.write(game.model_dump_json(indent=4))

    with open(get_file_path(game_id, "tsv"), 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = OUTPUT_TSV_COLUMNS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        write_game_questions(writer, game)


def save_games(games: list[Game]):
    save_games_json(games)
    save_games_tsv(games)


def save_games_json(games: list[Game]):
    with open(f"{ROOT_DIR}/output/all_games.json", "w", encoding="utf-8") as f:
        games_dict = [game.model_dump(mode='json') for game in games]
        f.write(json.dumps(games_dict, indent=4))


def save_games_tsv(games: list[Game], file_name: str = None):
    if not file_name:
        file_name = 'all_games.tsv'
    with open(f"{ROOT_DIR}/output/{file_name}", 'w', newline='', encoding="utf-8") as csvfile:
        fieldnames = OUTPUT_TSV_COLUMNS
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter="\t")
        writer.writeheader()
        for game in games:
            if isinstance(game, dict):
                game = Game.model_validate(game)
            write_game_questions(writer, game)


def write_game_questions(writer, game: Game):
    if game.jeopardy:
        for category in game.jeopardy.categories:
            for question in category.questions:
                write_question_row(writer, game, question)
    if game.double_jeopardy:
        for category in game.double_jeopardy.categories:
            for question in category.questions:
                write_question_row(writer, game, question)
    if game.final_jeopardy:
        write_question_row(writer, game, game.final_jeopardy)


def clean(value):
    if isinstance(value, str):
        return value.replace("\n", "\\n")
    return value


def write_question_row(writer, game, question):
    row = {
        'air_date': clean(game.air_date.isoformat()),
        'show_number': game.show_number,
        # 'title': clean(game.title),
        # 'comments': clean(game.comments),
        'category': clean(question.category),
        'value': clean(question.value),
        'question': clean(question.clue),
        'answer': clean(question.answer),
    }
    writer.writerow(row)
