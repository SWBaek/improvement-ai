# Interaction Research Source Matrix

- 상태: Research Baseline
- 기준일: 2026-08-06

## 목적

Human Review Artifacts의 설계 선택이 단일 프로젝트의 화면 취향에 의존하지 않도록 선행 연구와 웹 표준에서 채택할 원칙과 채택하지 않을 구현을 구분한다.

| 출처 | 확인한 개념 | 채택 | 채택하지 않음 |
|---|---|---|---|
| [Microsoft Guidelines for Human-AI Interaction](https://www.microsoft.com/en-us/research/publication/guidelines-for-human-ai-interaction/) | 능력·한계 설명, 상황 관련성, 수정 지원, granular feedback, 행동 결과 전달 | 목적·한계·수정 경로와 응답 영향을 visible contract로 표현 | 18개 guideline을 Artifact schema enum으로 복제 |
| [Google PAIR Mental Models](https://pair.withgoogle.com/guidebook-v2/chapter/mental-models/) | 사용자가 AI의 동작과 자신의 피드백 영향을 이해해야 함 | summary와 provenance에서 AI 역할과 한계를 설명 | 인간처럼 보이는 persona를 필수화 |
| [Horvitz, Mixed-Initiative UI](https://erichorvitz.com/uiact.htm) | 인간과 자동화의 주도권, 불확실성, 사용자 주의 비용 | Artifact 생성 trigger와 인간 통제 원칙 | AI가 판단을 자동 확정하는 workflow |
| [W3C Web Annotation](https://www.w3.org/TR/annotation-model/) | target, body, motivation과 특정 부분 선택 | 안정적인 target ID와 action이 있는 Response | JSON-LD, IRI와 전체 Annotation vocabulary 의무화 |
| [W3C PROV-O](https://www.w3.org/TR/prov-o/) | Entity, Activity, Agent, revision과 derivation | 입력 digest, generator, revision과 책임 추적 | RDF/OWL 직렬화 의무화 |
| [NIST AI RMF Core](https://airc.nist.gov/airmf-resources/airmf/5-sec-core/) | 인간 역할, 감독, 한계, feedback와 후속 조치 문서화 | 인간 action과 completion을 명시하고 후속 처리를 추적 | 위험관리 framework 전체를 Artifact 적합성으로 편입 |
| [Kunz와 Rittel, Issues as Elements of Information Systems](https://escholarship.org/uc/item/5cj786v8) | issue, position, argument와 resolution | question, option, evidence, decision 관계의 참고 모델 | 모든 interaction을 논쟁 그래프로 강제 |

## 공통 결론

- 사람은 AI의 제안뿐 아니라 현재 목적, 한계와 자신의 행동 결과를 알아야 한다.
- 응답은 문서 전체가 아니라 안정적인 target과 revision을 가리켜야 한다.
- AI가 잘못됐을 때 comment 외에도 변경 요청과 challenge가 가능해야 한다.
- 설명, 비교, 결정, 수정 확인과 기준 검증은 완료 조건이 다르다.
- 표준의 전체 데이터 모델을 복제하기보다 필요한 최소 의미만 호환 가능한 형태로 차용한다.
