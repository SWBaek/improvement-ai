# GM-TechB-V2G Interaction Case Study

- Case ID: `CASE-001`
- 상태: Initial Analysis
- 기준일: 2026-08-06

## 맥락

GM-TechB-V2G 프로젝트는 AI와 인간이 V2G CTRL 계획 및 아키텍처를 점진적으로 논의한다. 프로젝트는 구조화된 Architecture JSON을 Authoring SSOT로 두고, 생성된 HTML을 사람이 보는 projection으로 사용하며, 확정된 결정은 별도 Decision Log에 보존한다.

이 사례는 Human Review Artifacts Core 개선의 근거가 되었지만 아직 framework 적합 구현은 아니다.

## 인간의 목표

- 복잡한 시스템 경계와 책임 배분을 전체적으로 이해한다.
- 한 번에 하나의 큰 아키텍처 질문을 검토한다.
- SW, CTRL, VICM, Driver와 HW 사이의 역할 충돌과 누락을 찾는다.
- 대안의 영향과 근거를 확인하고 결정을 내린다.
- 합의 전 모델과 확정된 Decision Log를 구분한다.
- 수정된 구조가 기존 결정과 일치하는지 재검토한다.

## 관찰된 Interaction Sequence

```text
orient
→ critique
→ elicit / explore
→ compare
→ decide
→ revise
→ verify
→ 다음 질문
```

실제 논의는 이 순서를 앞뒤로 이동할 수 있다. 특히 새로운 제약이 발견되면 결정 후에도 다시 explore 또는 compare로 돌아간다.

## 유용했던 구조

- Architecture JSON과 생성 HTML의 분리
- 안정적인 component, interface, question과 decision ID
- 하나의 `nextQuestionId`
- 현재 구조와 Decision Log의 역할 분리
- 기능 축, 계층, 책임, interface를 서로 다른 view로 표현
- deterministic generation과 최신 상태 검사

## 현재 한계

- 기존 HTML의 핵심 내용이 JavaScript 생성에 의존한다.
- Artifact revision, provenance와 표준 Review Response가 없다.
- 질문에 대한 인간 응답을 target과 연결해 다시 AI에게 전달하는 공통 형식이 없다.
- Architecture, development planning과 프로젝트 종료 조건이 한 화면에 함께 커질 가능성이 있다.
- 프로젝트 고유 필드와 범용 architecture 표현의 경계가 명시되지 않았다.

## Pattern 후보

| 검토 상황 | Interaction | 필요한 표현 | 인간 응답 |
|---|---|---|---|
| 전체 경계 파악 | `orient` | context map, summary, legend | 확인, 상세 요청 |
| 역할 누락·충돌 검토 | `critique` | responsibility matrix, issue list | comment, change request |
| 두 allocation 비교 | `compare` | option matrix, impact view | 기준 조정, 선택, 보류 |
| 다음 질문 확정 | `decide` | question, options, evidence | select, reject, defer |
| 변경 반영 확인 | `revise` | before/after diff, unresolved list | approve, request changes |
| 결정 정합성 확인 | `verify` | traceability view, validation result | pass, dispute |

## Domain과 Interaction의 경계

다음은 다른 프로젝트에서도 재사용할 가능성이 높은 interaction 또는 representation 후보다.

- 하나의 현재 질문
- 식별 가능한 검토 대상
- 대안과 trade-off 비교
- 책임 매트릭스
- 관계 및 계층 view
- 결정 추적과 변경 전후 검토

다음은 GM-TechB-V2G vocabulary 또는 Project Extension으로 유지한다.

- SW, CTRL, VICM, Driver 역할명
- IEEE 1547 관련 기준
- S0-S5 development stage
- D1-D5 deliverable package
- Early Track과 Isolated Track
- 프로젝트 고유 신호와 전력제어 의미

## 다음 검증

1. 현재 아키텍처 논의 한 회차를 interaction 단위로 재구성한다.
2. 동일 데이터에서 `orient`, `compare`, `decide` Artifact를 각각 만들었을 때 이해 시간과 응답 명확성이 개선되는지 확인한다.
3. Core 0.2 Response가 실제 인간 응답을 손실 없이 표현하는지 확인한다.
4. Architecture vocabulary 없이도 재사용 가능한 pattern과 component만 추출한다.
5. 결과를 기준으로 Core 변경, Interaction Pattern과 Domain Vocabulary의 경계를 결정한다.
