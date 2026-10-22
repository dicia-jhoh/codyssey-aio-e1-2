"""퀴즈 한 문제 — 문제·선택지 4개·정답 번호(1~4)·힌트(선택)."""


class Quiz:
    """퀴즈 한 문제. 만들 때 값을 검사해 잘못된 퀴즈는 아예 생기지 않게 한다."""

    CHOICE_COUNT = 4

    def __init__(self, question, choices, answer, hint=""):
        if not isinstance(question, str) or not question.strip():
            raise ValueError("문제는 비어 있지 않은 글자여야 합니다.")
        if not isinstance(choices, list) or len(choices) != self.CHOICE_COUNT:
            raise ValueError(f"선택지는 {self.CHOICE_COUNT}개여야 합니다.")
        for choice in choices:
            if not isinstance(choice, str) or not choice.strip():
                raise ValueError("선택지는 비어 있지 않은 글자여야 합니다.")
        # bool 은 int 의 하위 타입이라 True 가 1 로 통과하지 않게 따로 막는다
        if isinstance(answer, bool) or not isinstance(answer, int):
            raise ValueError("정답은 번호(정수)여야 합니다.")
        if not 1 <= answer <= self.CHOICE_COUNT:
            raise ValueError(f"정답 번호는 1~{self.CHOICE_COUNT} 사이여야 합니다.")
        if not isinstance(hint, str):
            raise ValueError("힌트는 글자여야 합니다.")
        self.question = question.strip()
        self.choices = [choice.strip() for choice in choices]
        self.answer = answer
        self.hint = hint.strip()

    def display(self, number):
        """[문제 N] 과 선택지를 출력한다."""
        print(f"[문제 {number}]")
        print(self.question)
        for index, choice in enumerate(self.choices, 1):
            print(f"{index}. {choice}")

    def is_correct(self, choice):
        return choice == self.answer

    def answer_text(self):
        return f"{self.answer}번 {self.choices[self.answer - 1]}"

    def to_dict(self):
        return {
            "question": self.question,
            "choices": list(self.choices),
            "answer": self.answer,
            "hint": self.hint,
        }

    @classmethod
    def from_dict(cls, data):
        """state.json 의 퀴즈 한 개를 Quiz 로 만든다. 형식이 틀리면 ValueError."""
        if not isinstance(data, dict):
            raise ValueError("퀴즈 항목은 객체여야 합니다.")
        # hint 는 나중에 생긴 필드라 없는 옛 데이터도 읽는다
        return cls(data.get("question"), data.get("choices"), data.get("answer"), data.get("hint", ""))
