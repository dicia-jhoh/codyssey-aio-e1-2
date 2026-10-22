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
            if choice == 1:
                self.play()
            else:
                print(f"🚧 「{self.MENU[choice - 1]}」 기능은 준비 중입니다.")

    def show_menu(self):
        print()
        print(LINE)
        print("       🎯 나만의 퀴즈 게임 🎯")
        print(LINE)
        for number, name in enumerate(self.MENU, 1):
            print(f"{number}. {name}")
        print(LINE)

    def play(self):
        """모든 퀴즈를 차례로 내고, 정답 수와 점수를 보여 준다."""
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 2번 메뉴에서 먼저 퀴즈를 추가하세요.")
            return
        order = list(self.quizzes)
        print()
        print(f"📝 퀴즈를 시작합니다! (총 {len(order)}문제)")
        correct = 0
        for number, quiz in enumerate(order, 1):
            print(THIN)
            quiz.display(number)
            answer = ask_int("정답 입력: ", 1, quiz.CHOICE_COUNT, self.read)
            if quiz.is_correct(answer):
                correct += 1
                print("✅ 정답입니다!")
            else:
                print(f"❌ 오답입니다. 정답은 {quiz.answer_text()} 입니다.")
        score = round(correct / len(order) * 100)
        print(LINE)
        print(f"🏆 결과: {len(order)}문제 중 {correct}문제 정답! ({score}점)")
        print(LINE)
