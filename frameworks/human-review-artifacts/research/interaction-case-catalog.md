# Interaction Case Catalog

- 상태: Working Draft
- 기준일: 2026-08-06

## 목적

추상적인 화면 아이디어가 아니라 실제 AI-인간 작업 사례에서 반복되는 interaction을 찾기 위한 카탈로그다. 사례는 성공 사례뿐 아니라 긴 Markdown, 모호한 응답, stale 결과와 과도한 UI처럼 실패한 경험도 포함한다.

## 사례 기록 형식

| 필드 | 의미 |
|---|---|
| Case ID | 안정적인 사례 식별자 |
| Context | 프로젝트와 작업 맥락 |
| Human goal | 인간이 실제로 판단하거나 수행하려던 일 |
| AI contribution | AI가 생성·분석·제안한 내용 |
| Interaction sequence | 질문, 비교, 결정, 수정 등 실제 순서 |
| Information objects | 주장, 근거, 대안, 위험, 작업 등 다룬 대상 |
| Human response acts | 선택, 의견, 승인, 변경 요청 등 실제 응답 |
| Markdown friction | 기존 대화나 문서에서 어려웠던 점 |
| Useful views | 판단에 도움이 되었거나 필요했던 표현 |
| Durable outcome | 모델, 결정, 계획, 코드 등 최종 반영 위치 |
| Candidate reuse | 다른 프로젝트에서 반복될 가능성 |
| Evidence | 관련 파일, revision 또는 관찰 기록 |

## 현재 사례

| Case ID | 사례 | 주된 interaction | 상태 |
|---|---|---|---|
| `CASE-001` | GM-TechB-V2G 아키텍처 논의 | orient, critique, decide, revise | 분석 중 |

## 수집 규칙

- 사람이 원했던 행동을 문서 종류보다 먼저 기록한다.
- AI가 제시한 화면이 아니라 실제로 필요했던 판단 단위를 기록한다.
- 프로젝트 고유 vocabulary와 재사용 가능한 interaction을 분리한다.
- 하나의 사례에 여러 pattern이 있으면 실제 순서를 보존한다.
- 민감 정보, 개인 절대 경로와 전체 대화 원문은 복사하지 않는다.
- 규격 승격은 사례 하나만으로 결정하지 않는다.
