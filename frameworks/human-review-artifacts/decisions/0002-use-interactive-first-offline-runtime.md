# 0002. Interactive-first offline runtime을 사용

- 상태: Accepted
- 날짜: 2026-08-06

## 결정

Core 참조 Artifact는 탐색, 필터, 접기와 검토 결과 내보내기를 JavaScript로 제공한다. 모든 runtime과 style은 Artifact 안에 포함하며 자동 외부 통신과 외부 실행 코드는 허용하지 않는다.

## 이유

- 긴 문서를 읽는 대신 필요한 정보와 결정 지점을 탐색할 수 있다.
- 하나의 파일로 보관하고 로컬 브라우저에서 재현할 수 있다.
- 네트워크와 제3자 코드 의존성을 제거해 장기 보존성과 검토 가능성을 높인다.

## 결과

핵심 내용은 JavaScript 없이도 읽을 수 있어야 한다. 상호작용은 canonical 내용을 변경하거나 영구적인 숨은 상태를 만들지 않는다. CSP와 validator가 허용된 runtime 경계를 검사한다.
