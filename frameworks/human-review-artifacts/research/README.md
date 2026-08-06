# Human Review Artifacts Research

이 디렉터리는 규격을 만들기 전에 실제 AI-인간 interaction을 조사하고 설계 가설을 검증하는 작업 공간입니다. 이곳의 문서는 Working Draft이며 Core나 Profile의 규범적 요구사항이 아닙니다.

## 현재 연구 질문

1. 인간과 AI는 복잡한 작업에서 어떤 상호작용을 반복하는가?
2. 각 interaction에서 인간이 알아야 할 맥락과 수행할 행동은 무엇인가?
3. 긴 Markdown 또는 채팅에서 어떤 정보가 잘 보이지 않거나 유실되는가?
4. 어떤 interaction과 representation이 domain을 넘어 재사용되는가?
5. 언제 대화를 계속하고 언제 HTML Review Artifact를 생성해야 하는가?
6. 인간의 응답을 AI가 안전하게 후속 작업에 사용할 수 있도록 어떻게 구조화해야 하는가?

## 문서

- [`human-ai-interaction-patterns.md`](human-ai-interaction-patterns.md): 선행 연구와 초기 interaction taxonomy
- [`interaction-case-catalog.md`](interaction-case-catalog.md): 실제 사례 수집 형식과 현재 사례 목록
- [`source-matrix.md`](source-matrix.md): 선행 연구에서 채택하거나 제외한 설계 근거
- [`artifact-trigger.md`](artifact-trigger.md): 대화와 HTML Artifact의 선택 기준
- [`benchmarks/`](benchmarks/): 범용성을 검증하는 중립 사례와 Markdown baseline
- [`prototypes/`](prototypes/): 규격 확정 전 정보 구조를 검토하는 저충실도 HTML
- [`evaluations/`](evaluations/README.md): 직접 인간 검토 결과
- [`deferred/`](deferred/): 현재 설계 근거에서 제외한 향후 적용 사례

## 연구에서 규격으로 승격하는 기준

후보 개념은 다음 조건을 확인한 뒤 Core, Pattern 또는 Component로 승격합니다.

- 둘 이상의 사례에서 같은 사용자 목적과 응답 의미가 반복된다.
- 자유로운 표현만으로는 대상, 상태 또는 결과가 모호해진다.
- 기계 검증이나 구조화된 왕복이 실질적인 이점을 제공한다.
- 프로젝트 vocabulary를 제거해도 독립적인 의미가 유지된다.
- 기존 계약과 중복되지 않고 책임 경계가 설명된다.

첫 프로젝트에서만 나타난 개념은 우선 사례 또는 Project Extension으로 유지합니다.

## 현재 연구 범위

v0.1은 `orient`, `compare`, `decide`, `revise`, `verify`만 승격 대상으로 삼습니다. `elicit`, `explore`, `critique`, `plan`, `resolve`는 추가 사례가 확보될 때까지 후보로 유지합니다.

특정 외부 프로젝트는 taxonomy의 근거나 합격 기준으로 사용하지 않습니다. 먼저 중립 사례에서 계약과 표현을 검증한 뒤 별도 적용 단계에서 평가합니다.
