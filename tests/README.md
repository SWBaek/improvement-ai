# Tests

저장소 구조, framework와 skill metadata, CLI와 자동화 도구의 공통 동작 검증을 둡니다. 기본 저장소 계약은 `scripts/validate_repository.py`가 담당하고, framework 고유 검증은 각 framework의 `tests/`에 함께 둡니다.

전체 저장소 검증은 다음 순서로 실행합니다.

```powershell
python scripts/validate_repository.py
python -m unittest discover -s tests -p "test_*.py" -v
```
