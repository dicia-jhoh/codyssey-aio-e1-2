"""실행: python main.py — 데이터는 이 파일 옆(프로젝트 루트)의 state.json 에 저장한다."""

import os

from quiz_game.game import QuizGame
from quiz_game.storage import StateStore

STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


def main():
    QuizGame(StateStore(STATE_PATH)).run()


if __name__ == "__main__":
    main()
