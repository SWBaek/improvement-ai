# Newcomer Reverse Questioning

## Status

- State: `Exploring`
- Last reviewed: 2026-08-13
- Next trigger: WorkOs Capture 20건에서 신입 상시 질문과 look-before-ask+잔여 질문을 대조해, 이미 파일에 있는 정의를 다시 묻는 비율과 7일 뒤 재사용 Claims 수를 재기 시작할 때 갱신한다.

아직 Capability Blueprint, 실행 도구, schema 또는 구현 사양이 아니다. 조사는 [`docs/research/newcomer-reverse-questioning-memory.md`](../research/newcomer-reverse-questioning-memory.md)에 있다.

## 문제와 배경

이 가설은 일반 메모리 연구가 아니라, 이미 커진 개인 업무 vault를 운영하다가 생긴 과부하에서 나왔다. WorkOs는 프로젝트·회의·Knowledge·Dashboard·local skill을 가진 human-owned 운영 체계인데, 규모가 커지자 사람이 전체를 관리하지 못하겠다는 느낌이 들었다.

같은 시점에 AI 비서의 장기기억 연구는 이미 많다. 대부분은 대화를 사후에 추출하거나, 위키로 컴파일하거나, 그래프에 넣는다. 이 Idea가 본 공백은 저장 형식이 아니다. 사람이 “내일 회의있어” 또는 “내일 GM 프로젝트 회의있어”처럼 전제를 생략하면, 모델은 빈칸을 질문하지 않고 채운다. 그러면 암묵 지식은 계속 사람 머리에만 남는다.

원래 가설은 이것이다. AI를 완전 신입사원으로 두고, 모르는 엔티티·슬롯·상태에 대해 끈질기게 역질문해 지식으로 쌓는다.

## 현재 관찰

- 기본 모델은 모호성을 어느 정도 알면서도 QA에서는 거의 항상 바로 답한다. 검색 context가 있으면 질문은 더 줄어든다.
- 2026년 공개 메모리 저장소와 논문은 저장·검색·망각·예산에 몰려 있다. 신입 인터뷰를 기억 전략의 본체로 두는 인기 구현은 거의 없다.
- 코딩 Agent의 `AskQuestions`와 Claude 제품 규칙은 질문을 허용하되, 메모리와 도구를 먼저 보고 예산을 1–3으로 제한한다.
- Reddit은 “모호하면 물어라”는 지시와 “질문을 너무 많이 한다”는 불만을 동시에 반복한다.
- WorkOs는 이미 `AGENTS.md`에서 Capture 질문을 하나로 제한하고, `GM-TechB.md`처럼 가설 예시의 엔티티 정의를 파일로 갖고 있다.
- 선행 WorkOs 판단은 LLM Wiki를 Adapt하고, Dual-user 루프는 사람이 던지고 AI가 구조화한다고 본다. 상시 신입 인터뷰는 이 루프를 뒤집는다.

자세한 출처와 관찰·추론 구분은 조사 note를 따른다.

## 현재 가설

방향은 유지하고 메커니즘을 바꾼다.

가칭 `Residual Gap Elicitation`은 다음을 뜻한다. Agent는 모르는 것을 침묵한 채 채우지 않는다. 그러나 신입처럼 모든 빈칸을 사람에게 돌리지도 않는다. 기존 vault·회의·캘린더를 먼저 조회하고, 실행을 바꾸는 잔여 공백만 질문하며, 답은 chat이 아니라 엔티티 노트나 Knowledge에 남긴다. 암묵 지식의 큰 덩어리는 일상 Capture가 아니라 Review나 별도 인터뷰 세션에서 꺼낸다.

원래의 완전 신입 페르소나는 이 가설의 한 모드일 수 있다. 진입 조건은 vault가 비어 있거나, 조회가 실패했거나, 사람이 온보딩 세션을 열었을 때뿐이다.

```text
입력
  “내일 GM 프로젝트 회의있어”
        ↓
조회와 해소
  GM-TechB.md, 30-Meetings, 다음 일정
        ↓
잔여만 질문
  실행이 갈라질 때만 1–3문항
        ↓
원장에 기록
  회의 노트 / Current Status / Open Questions
        ↓
지식 부채는 배치
  Review 또는 주간 인터뷰
```

## 기대 효과와 비목표

기대하는 결과는 다음이다.

- “내일 회의있어”처럼 슬롯이 비면, 이미 있는 후보를 먼저 고르게 한다.
- “GM 프로젝트”처럼 파일이 있는 엔티티는 정의를 다시 묻지 않는다.
- 조회 실패로 남은 공백은 사람에게 돌아가고, 그 답이 다음 세션의 전제가 된다.
- Capture는 형식 없이 던질 수 있고, 인터뷰는 잔여와 배치 세션에만 열린다.

비목표는 다음과 같다.

- 완전 신입 페르소나를 기본 운영 모드로 고정하는 일
- Mem0, Zep, 새 벡터 DB, schema, generator, validator를 이 Idea가 도입하는 일
- 모든 모호한 입력을 질문 없이 가정하고 실행하는 일
- WorkOs 전체를 LLM-owned wiki로 바꾸는 일

## 위험과 반례

- 질문 예산을 빼면 Reddit이 반복 보고하는 질문 폭주가 된다.
- 조회를 빼면 사람은 자신이 쓴 프로젝트 노트를 입으로 복습한다.
- 답이 파일에 안 남으면 신입은 같은 것을 다시 묻는다. 페르소나는 기억이 아니다.
- Inbox마다 인터뷰가 열리면 Capture가 사라진다. 이것이 WorkOs가 이미 겪은 운영 노동이다.

반례: 빈 vault, 첫 등장 약어, 명시적 온보딩 세션에서는 신입에 가까운 질문이 맞다. 그때도 상시 모드가 아니라 진입 조건이 필요하다.

## 검증 기준 또는 실험 질문

1. 이미 노트가 있는 엔티티에서 신입 페르소나는 정의를 다시 묻는가.
2. 잔여 질문의 답이 project/Knowledge에 남을 때, 7일 뒤 재사용률은 chat-only보다 높은가.
3. 매 턴 1문항과 주 1회 5문항 중 어느 쪽이 재사용 Claims를 더 만드는가.
4. Capture 20건에서 인간 중단 횟수는 어느 쪽이 적은가.

측정 전에는 Candidate issue나 Blueprint로 올리지 않는다.

## 향후 탐색

- WorkOs Capture 한 줄과 회의 준비 요청에 look-before-ask를 먼저 적용해 본다.
- “모르는 엔티티 대기열”을 Review에만 쌓는 습관이 질문 폭주 없이 지식을 늘리는지 본다.
- 잔여 질문 계약이 여러 프로젝트에서 반복되면, 그때만 대상 프로젝트의 always-on 지침 후보로 재검토한다.

## 관련 출처와 후속 링크

- [`docs/research/newcomer-reverse-questioning-memory.md`](../research/newcomer-reverse-questioning-memory.md)
- [`docs/idea/local-project-continuity.md`](local-project-continuity.md)
- WorkOs: `AI 장기기억과 WorkOs Vault`, `LLM-Wiki-Pattern-for-PKM`, `WorkOs-Dual-User-함께-성장하는-루프`
