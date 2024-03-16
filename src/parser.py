import datetime
import re
from dateutil.parser import parse

from bs4 import BeautifulSoup

from models import QuestionBoard, Question, Category, Game


def build_game_from_soup(soup: BeautifulSoup) -> Game:
    error_elem = soup.find(class_="error")
    if error_elem:
        raise ValueError(f"Page Error: {error_elem.text}")
    game = Game(
        title=build_game_title(soup),
        comments=build_game_comments(soup),
        show_number=build_game_id(soup),
        air_date=build_game_date(soup),
        jeopardy=build_question_round(soup, "jeopardy_round"),
        double_jeopardy=build_question_round(soup, "double_jeopardy_round"),
        final_jeopardy=build_final_round(soup),
    )
    # print(game)
    return game


def build_game_title(soup: BeautifulSoup) -> str:
    return soup.find(id="game_title").text


def build_game_comments(soup: BeautifulSoup) -> str:
    return soup.find(id="game_comments").text or ""


def build_game_id(soup: BeautifulSoup):
    title = build_game_title(soup)
    matches = re.search(r"^Show #(\d+) -", title)
    if not matches:
        return 0
    return matches[1]


def build_game_date(soup: BeautifulSoup) -> datetime.date:
    title = build_game_title(soup)
    matches = re.search(r"- (.*)$", title)
    return parse(matches[1])


def build_final_round(soup: BeautifulSoup) -> Question | None:
    final_cell = soup.find(class_="final_round")
    if not final_cell:
        print("Missing final_round")
        return None
    else:
        return Question(
            category=final_cell.find(class_="category_name").get_text(),
            clue=final_cell.find(class_="clue_text").get_text(),
            answer=final_cell.find(class_="correct_response").get_text(),
            value=0,
        )


def build_question_round(soup: BeautifulSoup, board_id: str) -> QuestionBoard:
    categories = []
    board = soup.find(id=board_id)
    if not board:
        print(f"Missing {board_id}")
    else:
        for row_index, row in enumerate(board.find("table").find_all("tr")):

            # Build categories
            if row_index == 0:
                for cell_index, cell in enumerate(row.find_all("td", class_="category_name")):
                    categories.append(Category(name=cell.get_text(), questions=[]))
                continue

            for cell_index, cell in enumerate(row.find_all("td", class_="clue")):
                try:
                    category = categories[cell_index]
                    question = Question(
                        category=category.name,
                        clue=build_clue_text(cell),
                        answer=cell.find("em", class_="correct_response").get_text(),
                        value=build_clue_value(cell),
                    )
                    # print(question)
                    category.questions.append(question)
                except Exception as e:
                    # print(f"Error processing question: {e}")
                    pass

    return QuestionBoard(
        categories=categories
    )


def build_clue_text(cell: BeautifulSoup) -> str:
    clue_text_cell = cell.find("td", class_="clue_text")
    if clue_text_cell:
        return clue_text_cell.get_text()
    raise ValueError("Could not load clue text")


def build_clue_value(cell: BeautifulSoup) -> int:
    clue_value_cell = cell.find("td", class_="clue_value")
    if clue_value_cell:
        return int(re.sub(r"\D", "", clue_value_cell.get_text()))
    else:
        clue_value_cell = cell.find("td", class_="clue_value_daily_double")
        if clue_value_cell:
            return int(re.sub(r"\D", "", clue_value_cell.get_text()))
    raise ValueError("Could not load clue value")
