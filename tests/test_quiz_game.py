"""핵심 동작을 사람 없이 확인한다 — 입력 검증, 채점, 저장·재실행 유지, 손상 복구.

실행: python3 -m unittest discover -s tests -v
"""

import contextlib
import io
import json
import os
import tempfile
import unittest

from quiz_game.game import QuizGame
from quiz_game.inputs import ask_int
from quiz_game.quiz import Quiz
from quiz_game.storage import StateStore


def feeder(*answers):
    """input() 대신 넣을 가짜 키보드 — 준비한 답을 차례로 돌려준다."""
    it = iter(answers)
    return lambda prompt="": next(it)


class AskIntTest(unittest.TestCase):
    def test_blank_text_out_of_range_then_valid(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            value = ask_int("선택: ", 1, 6, read=feeder("", "abc", "9", "  3  "))
        self.assertEqual(value, 3)  # 앞뒤 공백은 지우고 받는다
        self.assertIn("입력이 비어 있습니다", out.getvalue())
        self.assertEqual(out.getvalue().count("잘못된 입력입니다"), 2)  # 문자·범위 밖


class QuizTest(unittest.TestCase):
    def test_is_correct_and_validation(self):
        q = Quiz("1+1?", ["1", "2", "3", "4"], 2)
        self.assertTrue(q.is_correct(2))
        self.assertFalse(q.is_correct(3))
        with self.assertRaises(ValueError):
            Quiz("선택지 3개", ["a", "b", "c"], 1)
        with self.assertRaises(ValueError):
            Quiz("정답 범위 밖", ["a", "b", "c", "d"], 5)


class PersistenceTest(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.TemporaryDirectory()
        self.path = os.path.join(self.dir.name, "state.json")

    def tearDown(self):
        self.dir.cleanup()

    def new_game(self, *answers):
        game = QuizGame(StateStore(self.path), read=feeder(*answers))
        with contextlib.redirect_stdout(io.StringIO()):
            game.load()
        return game

    def test_first_run_has_default_quizzes_and_saves(self):
        game = self.new_game()
        self.assertGreaterEqual(len(game.quizzes), 5)
        self.assertTrue(os.path.exists(self.path))

    def test_added_quiz_and_best_score_survive_restart(self):
        game = self.new_game()
        before = len(game.quizzes)
        game.quizzes.append(Quiz("새 문제", ["a", "b", "c", "d"], 1))
        with contextlib.redirect_stdout(io.StringIO()):
            game.record_result(80, 4, 5)
        again = self.new_game()  # 프로그램을 껐다 켠 것과 같다
        self.assertEqual(len(again.quizzes), before + 1)
        self.assertEqual(again.best["score"], 80)

    def test_broken_file_is_kept_and_defaults_load(self):
        with open(self.path, "w", encoding="utf-8") as f:
            f.write("{ 망가진 json")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            game = QuizGame(StateStore(self.path), read=feeder())
            game.load()
        self.assertIn("손상", out.getvalue())
        self.assertTrue(os.path.exists(self.path + ".broken"))  # 원본은 지우지 않고 보관
        self.assertGreaterEqual(len(game.quizzes), 5)
        with open(self.path, encoding="utf-8") as f:
            self.assertIn("quizzes", json.load(f))


if __name__ == "__main__":
    unittest.main()
