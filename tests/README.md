# Tests

실제 사용자 결과를 보호하는 capability 고유 테스트만 둡니다. 저장소 구조, 문서 index, 설치 도구와 Release 절차를 다시 검증하는 meta-test는 두지 않습니다.

`manage-focus-cycle`의 renderer 또는 schema 동작을 변경했을 때만 다음 로컬 테스트를 실행합니다.

```powershell
python -m unittest tests.test_manage_focus_cycle -v
```
