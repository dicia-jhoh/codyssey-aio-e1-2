"""콘솔 입력 공통 처리 — 앞뒤 공백을 지우고, 빈 입력·숫자 아님·범위 밖은 안내 후 다시 묻는다."""


def ask_int(prompt, low, high, read=input):
    """low~high 사이 정수를 받을 때까지 묻는다."""
    while True:
        raw = read(prompt).strip()
        if not raw:
            print(f"⚠️ 입력이 비어 있습니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        try:
            value = int(raw)
        except ValueError:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        if not low <= value <= high:
            print(f"⚠️ 잘못된 입력입니다. {low}-{high} 사이의 숫자를 입력하세요.")
            continue
        return value


def ask_text(prompt, read=input):
    """비어 있지 않은 글자를 받을 때까지 묻는다."""
    while True:
        text = read(prompt).strip()
        if text:
            return text
        print("⚠️ 빈 칸은 입력할 수 없습니다. 다시 입력하세요.")
