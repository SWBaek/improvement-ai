# 0003. Human Review Artifacts를 폐기하고 Project Workspace로 재설계

- 상태: Partially Superseded by 0004
- 날짜: 2026-08-06

> `human-review-artifacts` 폐기 결정과 이유는 유효하다. Project Workspace를 다음 중심 구현으로 삼는 미래 방향은 ADR 0004가 대체한다.

## 결정

외부 프로젝트에서 사용한 적 없는 `human-review-artifacts` Core 0.3과 관련 규격, 연구 문서, 예시, validator, 테스트 및 전용 Node.js 도구를 저장소에서 제거한다. 별도의 legacy 디렉터리는 만들지 않으며 과거 구현은 Git 이력으로만 보존한다.

다음 구현은 AI 산출물의 검토 응답 형식이 아니라, 프로젝트 전 기간에 걸쳐 사람이 현재 상태와 논의를 빠르게 파악하는 **Human-AI Project Workspace**를 목표로 한다.

초기 방향은 다음 네 책임을 분리하는 것이다.

1. 구조화된 Project Model이 프로젝트 상태의 원본이 된다.
2. HTML Workspace는 진행 상황, 현재 Focus와 적응형 시각 논의 영역을 보여주는 사람용 표현이다.
3. 채팅은 인간의 질문, 선택과 피드백을 전달하는 기본 상호작용 채널이다.
4. AI는 대화와 프로젝트 변경을 Project Model에 반영하고 HTML을 갱신한다.

새 framework의 이름, schema, component taxonomy와 전용 CLI는 아직 확정하지 않는다. 먼저 실제 프로젝트에 최소 구현을 적용하고 재사용성이 확인된 요소만 이 저장소의 framework로 추출한다.

## 이유

기존 구현은 복잡한 AI 산출물을 불변 HTML Review Snapshot으로 만들고 HTML 안에서 구조화된 응답을 받는 문제에 집중했다. 그러나 실제 불편은 긴 Markdown을 읽는 부담, 프로젝트 전체 진행 상태의 부재, 현재 Focus와 결정 지점의 불명확함, 복잡한 논의를 적합한 도형·표·흐름으로 보지 못하는 데 있었다.

사람의 선택은 기존 채팅으로 충분하므로 HTML 입력 계약과 Review Response schema는 초기 목표에 비해 비용이 크다. 또한 기존 Core는 외부 소비자가 없고 GM 프로젝트에도 적용되지 않아 호환성을 유지할 이유가 없다.

## 결과

- 저장소에는 현재 유지 중인 framework가 없다.
- 기존 Artifact 규격과 도구에 대한 문서·CI 의존성이 사라진다.
- 계속 갱신되는 Project Workspace를 우선하며, 불변 Review Snapshot은 필요가 확인될 때 별도 하위 개념으로 검토한다.
- 다음 단계는 실제 프로젝트를 기준으로 Progress, Current Focus, Adaptive Discussion Surface의 최소 데이터와 표현을 정의하는 것이다.
- 범용화는 파일 구조를 먼저 확장하는 방식이 아니라 사용 결과에서 반복 요소를 추출하는 방식으로 진행한다.
