# Tests

저장소 구조, Skill catalog와 release 계약, renderer 보안, framework와 자동화 도구의 공통 동작 검증을 둡니다. 기본 저장소 계약은 `scripts/validate_repository.py`가 담당하고 capability 고유 검증은 관련 test module과 fixture에 둡니다.

전체 저장소 검증은 다음 순서로 실행합니다.

```powershell
python scripts/validate_repository.py
python scripts/render_skill_index.py --check
python -m unittest discover -s tests -p "test_*.py" -v
python scripts/smoke_install.py
```

`smoke_install.py`는 격리된 임시 project에서 검증된 `skills` CLI version으로 Codex 설치 결과를 확인합니다.
