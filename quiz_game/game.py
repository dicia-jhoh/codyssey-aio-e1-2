"""게임 진행 — 메뉴를 보여 주고 고른 기능을 실행한다."""

from .defaults import default_quizzes
from .inputs import ask_int

LINE = "=" * 40
THIN = "-" * 40


class QuizGame:
    """퀴즈 목록과 점수를 들고 메뉴를 돌린다."""

    MENU = ("퀴즈 풀기", "퀴즈 추가", "퀴즈 목록", "점수 확인", "종료")

    def __init__(self, read=input):
        self.read = read
        self.quizzes = default_quizzes()

    def run(self):
        while True:
            self.show_menu()
            choice = ask_int("선택: ", 1, len(self.MENU), self.read)
            if choice == len(self.MENU):
                print("👋 게임을 종료합니다.")
                return
            print(f"🚧 「{self.MENU[choice - 1]}」 기능은 준비 중입니다.")

    def show_menu(self):
        print()
        print(LINE)
        print("       🎯 나만의 퀴즈 게임 🎯")
        print(LINE)
        for number, name in enumerate(self.MENU, 1):
            print(f"{number}. {name}")
        print(LINE)
