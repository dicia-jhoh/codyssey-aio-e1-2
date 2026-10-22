"""게임 진행 — 메뉴를 보여 주고 고른 기능을 실행한다."""

from .defaults import default_quizzes
from .inputs import ask_int, ask_text
from .quiz import Quiz

LINE = "=" * 40
THIN = "-" * 40


class QuizGame:
    """퀴즈 목록과 점수를 들고 메뉴를 돌린다."""

    # (메뉴 이름, 실행할 메서드 이름). 마지막 항목은 종료 — 메뉴를 늘릴 때 이 표 한 줄만 고친다
    MENU = (
        ("퀴즈 풀기", "play"),
        ("퀴즈 추가", "add_quiz"),
        ("퀴즈 목록", "list_quizzes"),
        ("점수 확인", "show_score"),
        ("종료", None),
    )

    def __init__(self, store, read=input):
        self.store = store
        self.read = read
        self.quizzes = []
        self.best = None  # {"score": 점수, "correct": 맞힌 수, "total": 푼 수} — 아직 안 풀었으면 None

    def load(self):
        """state.json 을 읽는다. 없거나 망가졌으면 기본 퀴즈로 시작하고 바로 저장한다."""
        data, message = self.store.load()
        if data is None:
            print(message)
            self.quizzes = default_quizzes()
            self.best = None
            self.save()
            return
        self.quizzes = []
        skipped = 0
        for item in data["quizzes"]:
            try:
                self.quizzes.append(Quiz.from_dict(item))
            except ValueError:
                skipped += 1
        self.best = data.get("best_score") if _is_best(data.get("best_score")) else None
        best_text = f"{self.best['score']}점" if self.best else "기록 없음"
        print(f"📂 저장된 데이터를 불러왔습니다. (퀴즈 {len(self.quizzes)}개, 최고점수 {best_text})")
        if skipped:
            print(f"⚠️ 형식이 맞지 않는 퀴즈 {skipped}개는 건너뛰었습니다.")

    def save(self):
        ok, message = self.store.save(self.to_state())
        if not ok:
            print(message)
        return ok

    def to_state(self):
        return {"quizzes": [quiz.to_dict() for quiz in self.quizzes], "best_score": self.best}

    def run(self):
        self.load()
        while True:
            self.show_menu()
            choice = ask_int("선택: ", 1, len(self.MENU), self.read)
            action = self.MENU[choice - 1][1]
            if action is None:
                self.save()
                print("👋 게임을 종료합니다.")
                return
            getattr(self, action)()

    def show_menu(self):
        print()
        print(LINE)
        print("       🎯 나만의 퀴즈 게임 🎯")
        print(LINE)
        for number, (name, _) in enumerate(self.MENU, 1):
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
        self.record_result(score, correct, len(order))

    def record_result(self, score, correct, total):
        """결과를 보여 주고 최고 점수보다 높으면 갱신한다."""
        print(LINE)
        print(f"🏆 결과: {total}문제 중 {correct}문제 정답! ({score}점)")
        if self.best is None or score > self.best["score"]:
            self.best = {"score": score, "correct": correct, "total": total}
            print("🎉 새로운 최고 점수입니다!")
        print(LINE)
        self.save()

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
        self.save()
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

    def show_score(self):
        print()
        if self.best is None:
            print("📭 아직 퀴즈를 풀지 않았습니다. 1번 메뉴에서 도전해 보세요.")
            return
        best = self.best
        print(f"🏆 최고 점수: {best['score']}점 ({best['total']}문제 중 {best['correct']}문제 정답)")


def _is_best(value):
    """best_score 가 {"score", "correct", "total"} 정수 묶음인지 확인한다."""
    if not isinstance(value, dict):
        return False
    return all(
        isinstance(value.get(key), int) and not isinstance(value.get(key), bool)
        for key in ("score", "correct", "total")
    )
