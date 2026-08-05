# Frameworks

여러 skill, tool과 agent adapter가 공유하는 규약, 스키마, 참조 구현과 확장 체계를 관리합니다.

각 framework는 다음 원칙을 따릅니다.

- 특정 에이전트나 소비 도구에 종속되지 않습니다.
- 규격과 스키마의 버전을 명시합니다.
- 참조 구현과 검증 수단을 함께 제공합니다.
- framework 내부 결정은 자체 `decisions/`에 기록합니다.
- domain 확장은 Core 계약을 완화하지 않습니다.

현재 framework:

- [`human-review-artifacts`](human-review-artifacts/README.md): 복잡한 AI 산출물을 사람이 검토하고 결정하기 위한 self-contained HTML Artifact 계약
