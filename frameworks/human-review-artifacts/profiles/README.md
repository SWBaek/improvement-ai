# Profiles

Profile은 Human Review Artifacts Core에 domain vocabulary와 추가 의미 검증을 제공합니다. 인간의 목표는 `interactions/`, 표현 계약은 `components/`에서 별도로 관리하며 프로젝트 고유 vocabulary를 곧바로 Profile로 승격하지 않습니다.

## 계약

- `profiles/<profile-name>/`에 소문자 kebab-case 이름으로 둡니다.
- Profile은 자체 `major.minor` 버전을 가집니다.
- Artifact Manifest의 `profiles` 배열에 이름과 버전을 선언합니다.
- Manifest 확장은 `extensions.<profile-name>` 아래에 둡니다.
- Profile runtime은 정적 semantic HTML을 보강할 때만 사용하며 Manifest `runtime.scripts`와 CSP에 이름, 버전과 digest를 선언합니다.
- Core Validator는 알 수 없는 Profile runtime의 무결성과 보안 경계만 검사하고 동작 미검증 경고를 제공합니다. Profile 의미 적합성은 별도 Profile Validator가 담당합니다.
- Core의 필수 필드, semantic section, 보안 또는 접근성 요구를 완화할 수 없습니다.
- Profile 전용 결정은 Profile 내부 또는 상위 framework의 `decisions/`에 적용 범위를 명시해 기록합니다.

첫 Profile 후보는 GM TechB V2G를 포함한 실제 interaction 사례 연구를 마친 뒤 결정합니다. 장기 방향은 [`../CHARTER.md`](../CHARTER.md), 현재 연구는 [`../research/`](../research/README.md)를 따릅니다.
