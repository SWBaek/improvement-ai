# Human-AI Interaction Patterns

- 상태: Working Draft
- 기준일: 2026-08-06

## 목적

AI와 인간이 복잡한 작업을 함께 수행할 때 반복되는 interaction을 식별하고, Human Review Artifacts가 언제 어떤 표현과 응답을 제공해야 하는지 결정하기 위한 초기 taxonomy다.

이 목록은 아직 규격이 아니다. 실제 사례를 수집하면서 pattern을 합치거나 나누고 이름을 변경할 수 있다.

## 초기 관찰

효과적인 human-AI workflow는 AI가 결과를 한 번 전달하고 종료하는 과정이 아니라 기대 설정, 맥락 제공, 제안, 인간 피드백, 수정과 확인이 반복되는 mixed-initiative 과정에 가깝다.

선행 참고자료는 다음 설계 관점을 제공한다.

- Microsoft의 [Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/project/guidelines-for-human-ai-interaction/publications/)은 초기 기대 설정, 상황에 맞는 지원, 사용자의 수정과 조정, 시간에 따른 상호작용을 함께 다룬다.
- Google PAIR의 [Mental Models](https://pair.withgoogle.com/guidebook-v2/chapter/mental-models/)와 [Explainability + Trust](https://pair.withgoogle.com/guidebook-v2/chapter/explainability-trust/)는 사용자가 AI의 능력과 한계를 이해하고 적절한 설명과 피드백을 통해 신뢰를 조정해야 한다는 점을 강조한다.
- Horvitz의 [Principles of Mixed-Initiative User Interfaces](https://erichorvitz.com/uiact.htm)는 인간과 자동화 사이의 주도권, 불확실성, 비용과 사용자 주의에 관한 설계 원칙을 제시한다.
- [W3C Web Annotation Data Model](https://www.w3.org/TR/annotation-model/)은 응답을 target, body와 motivation으로 분리하고 commenting, assessing, questioning, editing 등의 의도를 표현한다.
- [W3C PROV-O](https://www.w3.org/TR/prov-o/)는 결과의 provenance를 Entity, Activity와 Agent 관계로 추적하는 공통 모델을 제공한다.
- [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/)는 인간의 역할과 감독, 피드백, 문서화와 후속 조치가 명시되어야 함을 요구한다.

표준을 그대로 구현하기보다 필요한 개념과 호환 지점을 식별하고, Core의 단순성과 self-contained 전달 특성을 유지한다.

## 초기 Interaction Taxonomy

| ID | Pattern | 인간의 목표 | AI의 책임 | 대표 응답 |
|---|---|---|---|---|
| `orient` | 상황 파악 | 범위와 현재 상태를 이해한다 | 요약, 구조, 상태와 한계를 제시한다 | 확인, 추가 설명 요청 |
| `elicit` | 요구 명료화 | 목표, 선호와 제약을 제공한다 | 필요한 질문과 영향 범위를 제시한다 | 답변, 제약 추가, 모름 |
| `explore` | 가능성 탐색 | 후보 방향을 발견하고 좁힌다 | 서로 다른 후보와 탐색 축을 제안한다 | 관심 표시, 후보 추가·제외 |
| `compare` | 대안 비교 | 기준과 trade-off로 대안을 평가한다 | 동일 기준의 비교와 불확실성을 제공한다 | 선택, 순위, 평가, 기준 변경 |
| `critique` | 산출물 검토 | 오류, 누락, 위험과 이견을 표현한다 | 주장과 검토 지점을 식별 가능하게 제시한다 | 의견, 반박, 변경 요청 |
| `decide` | 결정 | 대안 중 하나를 채택하거나 보류한다 | 선택지, 근거, 영향과 되돌림 비용을 제시한다 | 선택, 거부, 보류 |
| `revise` | 변경 확인 | 피드백이 올바르게 반영됐는지 본다 | 변경 전후와 미반영 항목을 보여준다 | 승인, 추가 변경 요청 |
| `verify` | 조건 검증 | 주장이나 결과가 기준을 만족하는지 판단한다 | 기대값, 실제값, 증거와 한계를 제시한다 | 통과, 실패, 이의 제기 |
| `plan` | 실행 조정 | 단계, 우선순위, 책임과 의존성을 정한다 | 작업 구조와 제약, 위험을 제시한다 | 우선순위·담당·일정 조정 |
| `resolve` | 논의 종결 | 충돌과 미결 항목을 닫거나 이관한다 | 결정 상태, 잔여 위험과 후속 작업을 요약한다 | 종료, 재개, 이관 |

## Pattern 공통 질문

각 pattern 후보는 다음 항목으로 분석한다.

- Trigger: 언제 대화 대신 Artifact가 필요한가?
- Human goal: 인간이 달성하려는 판단 또는 행동은 무엇인가?
- Required context: 판단 전에 반드시 보여야 하는 정보는 무엇인가?
- Review target: 응답이 가리키는 안정적인 대상은 무엇인가?
- Response acts: 인간이 표현할 수 있어야 하는 행동은 무엇인가?
- Completion: interaction이 완료됐다고 판단하는 조건은 무엇인가?
- Re-entry: 수정된 revision을 다시 검토해야 하는 조건은 무엇인가?
- Failure modes: 과도한 정보, automation bias, stale snapshot과 모호한 선택을 어떻게 방지하는가?

## Artifact 생성 가설

모든 대화를 HTML Artifact로 만들지 않는다. 다음 조건 중 하나 이상이 나타날 때 생성 가치가 높다는 가설을 검증한다.

- 여러 대상이나 대안을 동시에 비교해야 한다.
- 논의가 길어져 현재 상태와 미결 항목을 기억하기 어렵다.
- 특정 revision에 대한 승인이나 변경 요청이 필요하다.
- 주장, 근거, 가정과 위험의 관계를 함께 확인해야 한다.
- 여러 view, 표, 관계도 또는 timeline이 판단에 필요하다.
- 인간 응답을 구조화해 후속 AI 작업으로 전달해야 한다.

## Core 0.2 평가 과제

현재 `inform`, `comment`, `decide`, `approve` review mode와 Response disposition이 위 pattern을 어느 정도 표현하는지 사례별로 검증한다. 특히 답변, 순위, 기준별 평가, 인라인 annotation, 근거 요청과 재검토 상태가 Core 변경 없이 Profile로 표현 가능한지 확인한다.

평가가 끝나기 전에는 Core 0.2의 enum이나 Response Schema를 변경하지 않는다.
