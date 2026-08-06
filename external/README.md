# External catalog

외부에서 가져오거나 참고하는 skill과 도구의 출처를 `catalog.yaml`에 기록합니다.

각 항목에는 최소한 다음 정보를 기록합니다.

- 고유한 이름
- 원본 repository 또는 package URL
- 고정한 commit, tag 또는 package version
- 라이선스
- 이 저장소에서 사용하는 이유
- 설치 또는 동기화 방식
- runtime dependency가 실패했을 때의 fallback

고정 재현이 실제로 필요하면 CDN 또는 package URL에 exact version을 기록합니다. 자동 drift validator는 두지 않고 문제가 발견됐을 때 갱신합니다.
