# 0004. Interaction 중심 framework 방향을 채택

- 상태: Accepted
- 날짜: 2026-08-06

## 결정

Human Review Artifacts의 장기 목적과 불변에 가까운 설계 원칙을 framework 루트의 `CHARTER.md`에 정의한다.

Framework의 주된 분류축은 문서 형식이나 업무 domain이 아니라 인간과 AI 사이의 interaction으로 한다. Core 위에서 인간에게 요청하는 행동을 Interaction Pattern으로, 정보를 보여주는 방식을 Representation Component로, 전문 의미를 Domain Vocabulary 또는 Project Extension으로 구분한다.

하나의 고정 HTML 템플릿으로 모든 논의를 표현하지 않는다. Artifact마다 하나의 주된 검토 목적을 두고, 목적에 맞는 제한된 pattern과 component를 조합한다.

## 이유

- Framework의 출발점은 HTML 문서 표준화가 아니라 긴 AI 대화를 사람이 이해하고 검토하기 좋은 workflow로 개선하는 것이었다.
- Architecture 사례의 데이터 구조를 먼저 일반화하면 프로젝트 고유 개념이 범용 계약에 섞이고 domain별 Profile이 과도하게 증가할 수 있다.
- 설명, 질문, 비교, 비평, 결정, 수정과 검증은 서로 다른 정보 구조와 인간 응답을 요구한다.
- 공통 상호작용 계약과 상황별 표현을 분리하면 동일한 workflow를 서로 다른 domain에서 재사용할 수 있다.

## 결과

- `CHARTER.md`를 향후 Core, Pattern, Component와 Profile 설계의 최상위 판단 기준으로 사용한다.
- AI-인간 interaction 사례와 taxonomy를 먼저 조사하고, 그 결과가 나오기 전에는 Architecture Profile을 확정하지 않는다.
- GM-TechB-V2G는 첫 실사용 사례로 분석하지만 그 vocabulary와 화면 구조를 그대로 공통 규격으로 승격하지 않는다.
- 기존 Core 0.2는 즉시 변경하지 않는다. 조사 결과를 기준으로 지원 범위와 부족한 interaction을 평가한 뒤 별도 결정으로 개정 여부를 판단한다.
- Charter의 핵심 방향 변경에는 이를 대체하는 새 framework decision이 필요하다.
