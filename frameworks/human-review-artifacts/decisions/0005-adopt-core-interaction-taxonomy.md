# 0005. Core Interaction Taxonomy v0.1을 채택

- 상태: Accepted
- 날짜: 2026-08-06

## 결정

첫 범용 Interaction Taxonomy는 `orient`, `compare`, `decide`, `revise`, `verify` 다섯 pattern으로 제한한다. Interaction은 Domain Profile과 분리된 first-class framework 영역으로 두고, Representation Component와 조합한다.

Core 0.2의 `review.mode`는 pattern, target별 허용 행동과 완료 조건을 충분히 표현하지 못하므로 Core 0.3에서 `interaction` 계약으로 교체한다.

## 이유

- 서로 다른 중립 사례에서 이해, 비교, 결정, 변경 확인과 기준 검증이라는 인간 목표가 반복된다.
- 같은 데이터도 인간이 수행할 행동에 따라 필요한 표현과 응답이 달라진다.
- domain 중심 Profile만으로는 인간 목표와 응답 의미를 공통으로 검증하기 어렵다.
- 모든 대화 동작을 첫 버전에 포함하면 사례 근거 없이 taxonomy를 과도하게 고정하게 된다.

## 결과

- 다섯 pattern은 각각 0.1 계약과 적합성 검사를 갖는다.
- `elicit`, `explore`, `critique`, `plan`, `resolve`는 연구 후보로 유지한다.
- `profiles/`는 domain vocabulary와 추가 의미 검증에 사용한다.
- `interactions/`와 `components/`를 framework의 독립 영역으로 추가한다.
- 특정 외부 프로젝트는 Core 0.3과 taxonomy v0.1의 설계 근거나 합격 기준에서 제외한다.
