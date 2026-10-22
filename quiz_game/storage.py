"""state.json 읽기·쓰기 — 이 게임에서 파일과 json 을 다루는 곳은 여기 하나다."""

import json
import os


class StateStore:
    """state.json 한 파일을 읽고 쓴다. 실패해도 예외를 밖으로 던지지 않고 안내 문구를 돌려준다."""

    def __init__(self, path):
        self.path = path
        # 읽을 수 없는 파일을 옮기지도 못했으면 덮어쓰지 않도록 저장을 막는다
        self.blocked = False

    def load(self):
        """(데이터, 안내 문구)를 돌려준다. 첫 실행·손상·읽기 오류면 데이터 자리가 None."""
        try:
            with open(self.path, encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return None, "📂 저장 파일이 없어 기본 퀴즈로 시작합니다. (첫 실행)"
        except (json.JSONDecodeError, UnicodeDecodeError):
            return None, f"⚠️ state.json 이 손상되어 기본 퀴즈로 복구합니다.{self._keep_broken()}"
        except OSError as e:
            # 권한 문제 등으로 못 읽은 파일은 손상 파일처럼 옆에 보관한다. 옮기지도 못하면 저장을 막아
            # 기본 퀴즈가 사용자의 데이터를 덮어쓰지 않게 한다
            kept = self._keep_broken()
            if not kept:
                self.blocked = True
                return None, (f"⚠️ state.json 을 읽지 못했습니다({e.strerror}). 기존 파일을 지키려고 "
                              "이번 실행은 저장하지 않고 기본 퀴즈로 진행합니다.")
            return None, f"⚠️ state.json 을 읽지 못해 기본 퀴즈로 시작합니다. ({e.strerror}){kept}"
        if not isinstance(data, dict) or not isinstance(data.get("quizzes"), list):
            return None, f"⚠️ state.json 형식이 맞지 않아 기본 퀴즈로 복구합니다.{self._keep_broken()}"
        return data, ""

    def save(self, data):
        """(성공 여부, 안내 문구). 임시 파일에 다 쓴 뒤 바꿔치기해서 쓰다 끊겨도 원본이 반쯤 덮이지 않는다."""
        if self.blocked:
            return False, "⚠️ 기존 state.json 을 읽지 못해 이번 실행의 변경은 저장하지 않습니다."
        tmp = self.path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
                f.write("\n")
            os.replace(tmp, self.path)
        except OSError as e:
            return False, f"⚠️ 저장하지 못했습니다. ({e.strerror}) 게임은 계속되지만 이번 변경은 남지 않습니다."
        return True, ""

    def _keep_broken(self):
        """손상된 파일을 지우지 않고 옆에 보관한다(직접 열어 고칠 수 있게)."""
        broken = self.path + ".broken"
        try:
            os.replace(self.path, broken)
        except OSError:
            return ""
        return f" (손상된 파일은 {os.path.basename(broken)} 로 보관)"
