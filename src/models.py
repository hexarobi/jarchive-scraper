import datetime
from pydantic import BaseModel


class Question(BaseModel):
    category: str
    clue: str
    answer: str
    value: int


class Category(BaseModel):
    name: str
    questions: list[Question]


class QuestionBoard(BaseModel):
    categories: list[Category]


class Game(BaseModel):
    was_downloaded: bool = False
    title: str
    comments: str
    show_number: int
    air_date: datetime.date
    jeopardy: QuestionBoard | None
    double_jeopardy: QuestionBoard | None
    final_jeopardy: Question | None
