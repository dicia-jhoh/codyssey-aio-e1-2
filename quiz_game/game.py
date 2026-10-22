"""게임 진행 — 메뉴를 보여 주고 고른 기능을 실행한다."""

from .defaults import default_quizzes
from .inputs import ask_int, ask_text
from .quiz import Quiz

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
            elif choice == 2:
                self.add_quiz()
            elif choice == 3:
                self.list_quizzes()
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

    def add_quiz(self):
        """문제·선택지 4개·정답 번호를 받아 새 퀴즈를 등록한다."""
        print()
        print("📌 새로운 퀴즈를 추가합니다.")
        question = ask_text("문제를 입력하세요: ", self.read)
        choices = []
        while len(choices) < Quiz.CHOICE_COUNT:
            choice = ask_text(f"선택지 {len(choices) + 1}: ", self.read)
            if choice in choices:
                print("⚠️ 앞의 선택지와 같습니다. 다른 내용을 입력하세요.")
                continue
            choices.append(choice)
        answer = ask_int(f"정답 번호 (1-{Quiz.CHOICE_COUNT}): ", 1, Quiz.CHOICE_COUNT, self.read)
        self.quizzes.append(Quiz(question, choices, answer))
        print("✅ 퀴즈가 추가되었습니다!")

    def list_quizzes(self):
        """등록된 퀴즈의 문제를 번호와 함께 보여 준다."""
        print()
        if not self.quizzes:
            print("📭 등록된 퀴즈가 없습니다. 2번 메뉴에서 퀴즈를 추가하세요.")
            return
        print(f"📋 등록된 퀴즈 목록 (총 {len(self.quizzes)}개)")
        print(THIN)
        for number, quiz in enumerate(self.quizzes, 1):
            print(f"[{number}] {quiz.question}")
        print(THIN)
