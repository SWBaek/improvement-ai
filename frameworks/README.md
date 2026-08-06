# Frameworks

둘 이상의 Skill, tool 또는 package가 실제로 공유하는 versioned contract를 관리합니다.

Framework는 다음 조건을 모두 만족할 때만 추가합니다.

- 서로 다른 둘 이상의 capability가 같은 계약을 사용합니다.
- 계약의 독립적인 version과 compatibility 규칙이 필요합니다.
- 각 소비자에 계약을 복제하는 것보다 canonical source가 명확한 이점을 제공합니다.

각 Framework는 `frameworks/<framework-name>/README.md`를 진입점으로 사용하고 다음 원칙을 따릅니다.

- 특정 agent나 소비 도구에 의존하지 않습니다.
- 공개한 규격과 schema에는 version을 명시합니다.
- 도입한 계약에는 그 규모에 맞는 검증 수단을 제공합니다.
- 내부 결정이 필요하면 자체 `decisions/`에 기록합니다.
- 확장은 기존 Core 계약을 호환성 없이 완화하거나 변경하지 않습니다.

## 현재 상태

현재 유지 중인 Framework는 없습니다.
