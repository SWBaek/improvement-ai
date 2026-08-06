# 0003. 미사용 Core 0.1을 폐기하고 0.2로 교체

- 상태: Accepted
- 날짜: 2026-08-06

## 결정

실사용되거나 외부 배포된 적이 없는 Core 0.1은 호환 대상으로 유지하지 않고 폐기한다. 저장소의 현재 규격, Manifest Schema, 참조 템플릿, 예시와 Validator를 Core 0.2 단일 계약으로 교체한다.

Core 0.2는 외부 Authoring Model과 HTML Review Snapshot의 권위 경계를 명확히 하고, revision, 입력 digest, 식별 가능한 review target, 표준 Review Response와 선언형 Profile runtime을 도입한다.

## 이유

- 사용자가 명시적으로 Core 0.1 미사용을 확인했다.
- 실제 적용 사례에서 발견한 요구를 반영하면서 불필요한 버전 라우팅과 중복 템플릿을 피할 수 있다.
- 초기 framework 단계에서 더 단순하고 명확한 단일 계약을 유지할 수 있다.

## 결과

- `core-0.1.md`와 `manifest-0.1.schema.json`은 제거한다.
- `artifact.html`, 예시와 Validator는 Core 0.2만 지원한다.
- 0.1 migration 문서, 호환 template과 Validator fallback은 제공하지 않는다.
- ADR 0001과 0002의 self-contained HTML, semantic HTML, offline progressive enhancement 원칙은 계속 유효하다.
