"""실행: python main.py — 데이터는 이 파일 옆(프로젝트 루트)의 state.json 에 저장한다."""

import os

from quiz_game.game import QuizGame
from quiz_game.storage import StateStore

STATE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "state.json")


def main():
    game = QuizGame(StateStore(STATE_PATH))
    try:
        game.run()
    except (KeyboardInterrupt, EOFError):
        # Ctrl+C 나 입력 끝(Ctrl+D·파이프 종료)에도 트레이스백 대신 저장하고 끝낸다
        print()
        if game.loaded:
            print("⚠️ 입력이 중단되어 지금까지의 내용을 저장하고 종료합니다.")
            game.save()
        else:
            print("⚠️ 불러오는 중에 중단되어 저장하지 않고 종료합니다.")


if __name__ == "__main__":
    main()
