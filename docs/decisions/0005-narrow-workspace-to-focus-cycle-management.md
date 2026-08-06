# 0005. Project Workspace 후보를 Focus Cycle Management로 축소

- 상태: Accepted
- 날짜: 2026-08-06

## 결정

ADR 0004와 README에서 첫 Candidate로 사용한 Human-AI Project Workspace 명칭과 범위를 **Focus Cycle Management** capability로 대체한다.

구성 요소 이름은 다음과 같이 구분한다.

- Capability: Focus Cycle Management
- Agent Skill: `manage-focus-cycle`
- Human-facing output: Focus Cycle Workspace

이 capability는 장기 Project 전체를 관리하거나 최종 완료율을 계산하지 않는다. 하나의 Primary Focus Cycle을 설정하고 Completion Contract에 따라 갱신·종료하며, 현재 Project Context와 Discussion을 임시 HTML Workspace로 보여준다.

초기 Skill은 project-native 기록을 우선하고 적절한 원본이 없을 때 `docs/focus/focus-cycle.md`를 사용한다. HTML은 durable state가 아닌 OS temp의 현재 projection이다. Framework, schema와 독립 renderer는 반복 사용에서 필요성이 확인되기 전까지 만들지 않는다.

## 이유

Human-AI Project Workspace는 모든 AI-인간 프로젝트 협업과 전체 프로젝트 상태를 소유하는 제품처럼 해석될 수 있다. 특히 종료점이 없는 maintenance와 research 프로젝트에 전체 진행률을 강제하면 가짜 목표와 영구적인 미완료 상태가 생긴다.

실제로 관리해야 하는 단위는 Project가 아니라 종료 조건을 가진 단기 Focus Cycle이다. Capability, Skill과 HTML output을 분리하면 Skill의 trigger와 책임이 좁아지고 Workspace 표현이 구현 수단임을 명확히 할 수 있다.

## 결과

- README와 Skill index는 Focus Cycle Management와 `manage-focus-cycle`을 사용한다.
- 한 Workspace에는 하나의 Primary Focus Cycle만 둔다.
- Completion Contract는 활성화와 종료 판단의 필수 입력이다.
- Project의 장기 방향은 context이며 progress denominator가 아니다.
- GM, SW-Common-Architecture와 sdoc-editor는 종속 대상이 아니라 서로 다른 pilot archetype으로만 사용한다.
- 실제 pilot과 promotion 판단은 tracking issue #10에서 관리한다.
