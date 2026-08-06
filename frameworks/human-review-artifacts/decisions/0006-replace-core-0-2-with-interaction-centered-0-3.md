# 0006. Core 0.2를 interaction 중심 Core 0.3으로 교체

- 상태: Accepted
- 날짜: 2026-08-06

## 결정

외부 적용 전에 Core 0.2의 `review.mode` 중심 계약을 폐기하고 first-class `interaction` 계약을 제공하는 Core 0.3으로 교체한다. Review Response도 action과 pattern을 명시하는 0.2로 교체한다.

## 이유

- `inform`, `comment`, `decide`, `approve` 하나로는 인간 목표와 target별 허용 행동을 독립적으로 표현할 수 없다.
- 비교 순위, challenge, 필수 target 응답과 pattern version을 검증할 수 없다.
- 아직 외부 소비자가 없어 호환 분기와 migration 비용보다 단일 계약의 명확성이 중요하다.

## 결과

- 저장소는 Core 0.3과 Review Response 0.2만 지원한다.
- Core 0.2 spec, schema, template, 예시와 validator fallback은 제거한다.
- Interaction Pattern과 Representation Component는 Core와 별도로 versioning한다.
- ADR 0001, 0002의 self-contained HTML과 offline progressive enhancement 원칙은 유지한다.
