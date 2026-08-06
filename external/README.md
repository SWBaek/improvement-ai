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

CDN 또는 package URL은 재현 가능한 exact version으로 고정합니다. Skill asset의 URL과 catalog version drift는 저장소 validator가 차단합니다.
