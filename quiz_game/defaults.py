"""기본 퀴즈 — 주제: AI·개발 기초 상식(입학 연수에서 쓰는 터미널·Git·Docker·Python·AI 연산)."""

from .quiz import Quiz

_DEFAULTS = (
    ("터미널에서 지금 있는 폴더의 전체 경로를 출력하는 명령은?",
     ["ls", "pwd", "cd", "mkdir"], 2, "print working directory 의 줄임말"),
    ("Git 에서 바뀐 파일을 다음 커밋에 담는(스테이징하는) 명령은?",
     ["git commit", "git push", "git add", "git init"], 3, "'더하다'라는 뜻의 영어 단어"),
    ("Docker 에서 멈춘 컨테이너까지 모두 보여 주는 명령은?",
     ["docker images", "docker ps -a", "docker run", "docker logs"], 2, "-a 는 all(전부)"),
    ("파이썬에서 '키: 값' 쌍으로 데이터를 저장하는 자료형은?",
     ["list", "tuple", "dict", "str"], 3, "사전(dictionary)처럼 단어로 뜻을 찾는다"),
    ("신경망 계산의 대부분을 차지하는 '곱해서 더하기' 연산의 이름은?",
     ["MAC", "CPU", "API", "SQL"], 1, "Multiply-ACcumulate"),
    ("JSON 파일을 열어 파이썬 객체로 읽어 오는 함수는?",
     ["json.dumps", "json.load", "json.write", "json.open"], 2, "s 가 붙은 쪽은 문자열(string)용"),
    ("파일 권한 755 에서 '그룹' 사용자가 가진 권한은?",
     ["읽기·쓰기·실행", "읽기·실행", "읽기만", "권한 없음"], 2, "5 = 4(읽기) + 1(실행)"),
)


def default_quizzes():
    """첫 실행이나 파일 복구 때 쓸 기본 퀴즈 목록(매번 새 객체)."""
    return [Quiz(question, list(choices), answer, hint) for question, choices, answer, hint in _DEFAULTS]
