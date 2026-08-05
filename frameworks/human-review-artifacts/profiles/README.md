# Domain Profiles

Domain Profile은 Human Review Artifacts Core에 분야별 의미, 섹션, 시각화와 검증 규칙을 추가합니다.

## 계약

- `profiles/<profile-name>/`에 소문자 kebab-case 이름으로 둡니다.
- Profile은 자체 `major.minor` 버전을 가집니다.
- Artifact Manifest의 `profiles` 배열에 이름과 버전을 선언합니다.
- Manifest 확장은 `extensions.<profile-name>` 아래에 둡니다.
- Core의 필수 필드, semantic section, 보안 또는 접근성 요구를 완화할 수 없습니다.
- Profile 전용 결정은 Profile 내부 또는 상위 framework의 `decisions/`에 적용 범위를 명시해 기록합니다.

첫 Profile은 Core가 중립 예시와 실제 사용에서 안정화된 뒤 추가합니다.
