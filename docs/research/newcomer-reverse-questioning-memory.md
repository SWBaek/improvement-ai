# 신입 역질문과 비서 장기기억

- 조사일: 2026-08-13
- 상태: Research note. 채택된 ADR이나 Blueprint 계약이 아니다.
- 목적: “모르는 것에 대해 신입처럼 끈질기게 역질문해 장기기억을 쌓는다”는 가설을, 공개 연구·제품·커뮤니티 자료와 기존 WorkOs 운영 맥락으로 구분한다.

## 조사 질문

1. 방향 자체는 타당한가. 즉, 침묵 가정 대신 질문을 통해 암묵 지식을 끌어내는 것이 비서 기억의 실제 공백인가는.
2. 메커니즘은 타당한가. 즉, 완전 신입 페르소나와 매 발화마다의 끈질긴 질문은 그 공백을 푸는 좋은 기본값인가.
3. 시장과 연구는 이미 무엇을 풀었고, 무엇을 남겼는가. 특히 GitHub, X, Reddit, Hugging Face와 학술 논문.
4. 이 가설보다 더 나은 아이디어가 있는가. 특히 WorkOs처럼 이미 커진 human-owned vault에서.

## 비교 기준

- 1차 출처: 측정이 있는 논문, 제품 시스템 프롬프트, 스타가 있는 저장소, 재현 가능한 벤치마크
- 2차 출처: 프롬프트 팁, 컨설팅 글, 소셜 논의. 측정이 없을 때는 관찰로만 쓴다
- 구분: 관찰(공개된 측정·제품 규칙·저장소 분포)과 추론(왜 그 규칙이 생겼는지, WorkOs에 무엇을 뜻하는지)

조사 대상 아이디어는 다음 세 층으로 나눈다.

| 층 | 내용 | 이 조사에서의 위치 |
|---|---|---|
| 문제 | 커진 업무 vault를 AI가 신입처럼 모른 채 추측하면 기억이 쌓이지 않고, 사람은 반복 설명에 지친다 | 출발점. WorkOs 운영 중 나온 불편 |
| 방향 | 모르는 엔티티·슬롯·상태에 대해 질문을 강제해 지식을 축적한다 | 타당성 평가 대상 |
| 메커니즘 | 완전 신입 페르소나. “내일 회의있어”면 어떤 회의인지, 언제인지, 누가 오는지 끈질기게 묻는다 | 더 나은 대안과 대조 |

## 출발점: WorkOs에서 나온 불편

이 가설은 일반 메모리 연구가 아니라, 이미 커진 개인 업무 vault를 운영하다가 생긴 과부하에서 나왔다. 조사 시점의 WorkOs는 프로젝트, 회의, Knowledge, Daily, Dashboard, local skill을 가진 human-owned 운영 체계다. 선행 판단은 이미 있다.

- [[AI 장기기억과 WorkOs Vault]]와 [[LLM-Wiki-Pattern-for-PKM]]는 Karpathy LLM Wiki를 **Adapt**한다. LLM은 owner가 아니라 compiler, librarian, reviewer다.
- [[AI-Native-PKM-Landscape-and-WorkOs-Position]]는 시장이 Knowledge OS / Work OS / lint / 제품형 second brain으로 수렴한다고 본다. WorkOs는 실행층이 두껍다.
- [[WorkOs-Dual-User-함께-성장하는-루프]]는 “규칙을 쌓으면 가벼워진다”가 한 달 만에 “근육이 노동이 됨”으로 뒤집힌 과정을 기록한다.
- 현재 `AGENTS.md`는 Capture에서 “대상, 날짜, 소유자, 약속에 실질적 모호함이 있으면 **질문 하나**를 하거나 raw Capture를 판단 필요로 남긴다”고 이미 제한한다.

같은 vault에는 가설의 예시인 GM 맥락이 이미 파일로 있다. `10-Projects/GM-TechB/GM-TechB.md`는 프로젝트 목적, 현재 상태, 다음 회의(`2026-08-19` V2G Weekly), 담당자, 미결을 본문에 둔다. `30-Meetings/`에는 같은 주의 GM·Ford 회의 노트가 있다.

관찰: 이 가설이 풀려는 “AI가 GM이 뭔지 모른다”는 상태는, 최소한 이 vault에서는 **파일이 없어서가 아니라 조회하지 않아서** 생길 수 있다.

## 1차 출처

| 출처 | 종류 | 핵심 측정 또는 규칙 | 이 조사에서의 역할 |
|---|---|---|---|
| [Su & Cardie, 2026. *Knowing but Not Showing*](https://arxiv.org/abs/2605.25284) | 모호성 인식 vs 질문 행동 | 모델은 명시적으로 물으면 모호성을 꽤 맞히지만, QA에서는 거의 항상 바로 답한다. 검색된 context가 있으면 정확도는 오르고 역질문율은 더 떨어진다. Claude 계열도 모호 질문에서 역질문율이 최대 약 5% | 기본 모델은 신입이 아니라 **추측하는 선배**다. 질문 강제는 기본값을 뒤집는 개입이다 |
| [Zhang, Knox & Choi, 2024/2025. *Modeling Future Conversation Turns*](https://arxiv.org/abs/2410.13788) | 언제 물을지 학습 | 미래 해석이 갈라질 때만 질문을 보상한다. 모호하지 않은 질의에도 질문하면 손해 | “항상 묻기”가 아니라 **질문의 정보가치**가 학습 대상임을 보여 준다 |
| [Siro et al., 2024. AGENT-CQ](https://arxiv.org/abs/2410.19692) | 질문 생성·평가 | ClariQ 위에서 LLM이 질문을 만들고 CrowdLLM이 품질을 평가한다 | 질문 생성은 연구 주제이지, 기억 저장 주제와 다르다 |
| [Kim, 2021. Amazon Science / ASRU](https://www.amazon.science/blog/reducing-unnecessary-clarification-questions-from-voice-agents) | 질문 억제 측정 | Alexa 분석에서 경쟁 가설이 높아도 상위 가설이 맞는 경우가 77%. 질문 여부 분류기가 heuristic 대비 F1 +81% | 대규모 제품은 “더 묻기”가 아니라 **불필요한 질문을 줄이는** 쪽으로 최적화한다 |
| [Claude 제품 프롬프트, 2026 유출본](https://github.com/asgeirtj/system_prompts_leaks/blob/main/Anthropic/claude-fable-5.md) | 상용 assistant 규칙 | 사람·프로젝트·선호를 묻기 **전에** memory listing을 읽는다. 이미 있는 것을 다시 묻는 것은 연속성을 깨뜨린다. 사소한 누락은 가정하고 진행하고, 가정만 짧게 남긴다. 도구로 찾을 수 있으면 사람에게 조회를 떠넘기지 않는다 | 2026년 frontier assistant의 기본값은 **신입 인터뷰가 아니라 look-before-ask**다 |
| [VS Code / Copilot AskQuestions](https://code.visualstudio.com/docs/agents/best-practices) | 코딩 Agent 도구 | 모호할 때 구현 전에 질문하라고 권한다. Custom Agent의 `AskQuestions`는 보통 1–3문항, 선택지를 준다 | 질문은 기억 축적이 아니라 **잘못된 실행을 막기 위한 게이트**다 |
| [mem-agent / Dria, 2025](https://huggingface.co/blog/driaforall/mem-agent) | RL로 학습한 메모리 Agent | 능력 세 가지: 검색, 갱신, **메모리와 모순·공백일 때만** 확인 질문 | 질문은 항상이 아니라 메모리 충돌의 잔여 단계에서만 나온다 |
| GitHub `topic:agent-memory` (조사일 상위) | 저장소 분포 | cognee 29.9k, supermemory 28.9k, OpenViking 28.3k, Memori 15.8k, memU 14.3k, EverOS 12.0k. “clarifying questions conversational search” 검색 상위는 스타 한 자리 학술 재현 저장소 | 공개 생태계는 **저장·검색 인프라**에 몰려 있고, 신입 인터뷰형 기억 제품은 거의 없다 |

## 관찰

### 1. 메모리 시장은 “어떻게 묻나”가 아니라 “어디에 쌓나”를 푼다

2025–2026의 공개 메모리 스택은 대체로 대화를 **사후에 추출**한다.

- Mem0: 대화에서 fact를 골라 저장·검색한다
- Zep / Graphiti: 시간축이 있는 지식 그래프로 사실의 변화를 추적한다
- Letta / MemGPT: context를 OS 메모리처럼 페이징한다
- A-MEM: Zettelkasten식 노트가 새 정보에 맞춰 진화한다
- Cognee, supermemory, OpenViking, EverOS: vault·그래프·로컬 Markdown을 Agent 메모리로 쓴다

독립 재현 논쟁도 저장 품질에 쏠려 있다. 2026년 공개 비교는 Mem0의 LoCoMo 수치가 벤치마크 산술 오류와 재현 부재로 흔들렸고, Letta는 대화를 파일에 두고 `grep`만 해도 발표 점수를 넘겼다고 보고했다. 이것은 “질문을 더 하면 기억이 좋아진다”는 증거가 아니다. **이미 말한 것을 어떻게 다시 찾느냐**의 경쟁이다.

Hugging Face Daily Papers의 agent memory 흐름도 같다. A-MEM, Hindsight, FadeMem(망각), BudgetMem(비용), R^3Mem(압축)은 모두 저장·검색·망각·예산이다. “신입이 되어 사람을 인터뷰한다”는 축은 거의 없다.

### 2. 역질문은 별도 연구 줄기다. 목적은 기억이 아니라 모호성 해소다

대화 검색과 task-oriented dialog는 오래전부터 질문을 다룬다. Qulac, ClariQ, ClarQ, ClarQ-LLM, AGENT-CQ, RAC(검색으로 질문을 grounding)가 그 줄기다.

공통 전제는 다음이다.

- 사용자 질의가 여러 해석을 허용할 때, 추측보다 한 질문이 나을 수 있다
- 좋은 질문은 미래 답의 분기를 줄인다
- 나쁜 질문은 이미 답할 수 있는 입력에도 끼어든다

Su & Cardie(2026)는 이 줄기의 현재 기본 행동을 측정한다. 모델은 모호성을 **알고도 보여 주지 않는다**. 검색 context가 생기면 “답할 수 있다”는 신호로 받아 질문을 더 안 한다. 따라서 “질문을 강제한다”는 개입은 빈 공간이 맞다. 다만 그 빈 공간의 이름은 **기억 시스템**이 아니라 **모호성 표면화**다.

### 3. 상용 제품은 신입 페르소나를 버리고 look-before-ask로 수렴한다

코딩 Agent와 일반 assistant는 질문을 허용하되 범위를 좁힌다.

- VS Code: 모호하면 구현 전에 물어라. 목적은 정확한 패치다
- Copilot Custom Agent `AskQuestions`: 1–3문항, 선택지. 인터뷰가 아니라 게이트
- Claude 2026 프롬프트: 메모리 파일을 먼저 읽고, 도구로 찾고, 사소한 누락은 가정하고 진행한다. “누가 그 사람인가, 저 프로젝트는 무엇인가”를 사람에게 다시 묻는 것은 실패로 적혀 있다
- WorkOs `AGENTS.md`: 질문 예산은 이미 1개다

X의 실무 조언도 같은 쪽이다. 한 YC 인터뷰 설계 답변(2026-04, `@adxtyahq`)은 모호한 “저거 더 크게”를 모델 기억이 아니라 **정규 상태 + 참조 해소 + 확신도 게이트**로 푼다. 확신이 낮을 때만 묻는다. Karpathy(2025-06)는 LLM을 전향성 기억상실 동료로 비유하고, 완화책은 인터뷰가 아니라 대화 밖 지식 축적(ChatGPT Memory, 이후 LLM Wiki)이라고 본다.

### 4. 커뮤니티는 “질문이 부족하다”와 “질문이 많다”를 동시에 호소한다

Reddit의 반복 패턴은 두 갈래다.

- 정확도를 위해 “모호하면  Clarifying question을 하라”는 custom instruction이 자주 복사된다
- 동시에 r/ChatGPT의 반복 불만은 GPT-5가 질문을 너무 많이 한다, follow-up을 끄고 싶다는 것이다 ([예시](https://www.reddit.com/r/ChatGPT/comments/1mn8o6j/gpt5_wastes_your_responses_by_asking_way_too_many/), [예시](https://www.reddit.com/r/ChatGPT/comments/1k9cavc/how_can_i_stop_chatgpt_from_asking_followup/))

즉 사용자는 “추측하지 마라”와 “신입처럼 나를 가르치게 하지 마라”를 동시에 원한다. 강제 신입 페르소나는 한쪽만 만족한다.

### 5. 지식 추출(elicitation)은 1980년대부터 병목으로 알려져 있다

Feigenbaum이 이름 붙인 knowledge acquisition bottleneck은 전문가 머릿속의 암묵 지식을 기계에 넣는 비용이 시스템을 죽였다는 진단이다. 2025–2026에도 같은 문제가 다시 보인다.

- 퇴사자·SME 인터뷰 Agent, 맞춤 설문, 음성 인터뷰로 지식 패키지를 만드는 기업 제품이 있다
- Aniccai 등 실무 글은 “첫 Agent는 assistant가 아니라 interviewer”라고 한다. 다만 권고는 **별도 세션 3–4회, 회당 20분, 한 번에 질문 하나**다. 일상 Capture 한 줄마다 신입이 달라붙는 설계가 아니다
- IDEA2(2026) 같은 논문은 ontology competency question을 LLM + expert-in-the-loop로 뽑는다. 역시 배치 워크플로다

관찰: “질문을 통해 암묵 지식을 꺼낸다”는 아이디어 자체는 새롭지 않다. 새롭게 보이려면 **일상 비서 루프에 신입 인터뷰를 기본값으로 넣는 것**이어야 한다. 공개 제품과 연구는 그 기본값을 거의 채택하지 않는다.

### 6. GitHub에서 신입 기억 Agent는 주류가 아니다

조사일 GitHub 검색의 비대칭이 크다.

- `topic:agent-memory`는 만 단위 스타의 저장·그래프·로컬 Markdown 엔진이 채운다
- clarifying question 재현 저장소(USi, ZeroshotCQGen, AGENT-CQ-Data)는 스타 0–8이다
- “intern persona + memory elicitation”에 해당하는 인기 제품 저장소는 이 검색에서 나오지 않았다

추론이 아니라 분포 관찰이다. 사람들이 복제하는 것은 인터뷰 페르소나가 아니라 **파일이 기억이 되는 구조**다. 이것은 WorkOs가 이미 선택한 길과 같다.

## 추론

### 방향은 맞다. 공백의 이름은 “저장 부족”이 아니라 “침묵 가정”이다

모델은 모르는 엔티티를 빈칸으로 두지 않고 채운다. Su & Cardie가 측정한 행동이 그것이다. WorkOs 예시로 옮기면, “내일 회의있어”에 대해 없는 일정을 지어 내거나, “GM 프로젝트”를 일반 GM으로 해석하는 실패가 먼저다. 질문을 아예 금지하면 암묵 지식은 계속 사람 머리에만 남는다.

따라서 “모르는 것을 모르는 채로 두지 않는다”는 계약은 타당하다.

### 메커니즘은 과하다. 완전 신입은 이미 있는 기억을 다시 세금으로 부과한다

가설의 예시는 두 종류를 한 페르소나로 묶는다.

| 입력 | 필요한 것 | 신입 페르소나가 하는 일 | 더 싼 일 |
|---|---|---|---|
| “내일 회의있어” | 일정 슬롯 해소 | 어떤 회의, 언제, 누가 | `30-Meetings/`와 캘린더를 먼저 조회. 후보가 하나면 확인 한 줄. 여러 개면 선택지 |
| “내일 GM 프로젝트 회의있어” | 엔티티 grounding | GM이 뭔지, 상태가 뭔지 | `GM-TechB.md`를 읽는다. 없는 필드만 남긴다 |

WorkOs에서 두 번째 예시는 특히 위험하다. 프로젝트 정의와 상태가 이미 있다. 신입이 “GM이 무엇입니까”를 물으면, 사람은 자신이 이미 써 둔 문서를 입으로 다시 읽게 된다. Claude 프롬프트가 “이미 파일에 있는 것을 물으면 연속성이 깨진다”고 적은 바로 그 실패다.

더 깊은 충돌은 운영 철학이다. Dual-user 루프의 합의는 **사람이 던지고 AI가 구조화한다**는 것이다. 완전 신입 페르소나는 이를 뒤집는다. AI가 던지고 사람이 가르친다. 출발점이 “커지는 WorkOs를 관리하지 못하겠다”인 사람에게, 매 Capture마다 인터뷰는 세 번째 시대의 사인(정렬이 주의력을 잡아먹음)을 재현한다.

### 더 나은 아이디어는 신입이 아니라 잔여 공백 추출이다

공개 자료가 가리키는 공통 설계는 다음 파이프라인이다.

```text
1. 조회: vault, 회의, 메일, 캘린더, 기존 Knowledge를 먼저 본다
2. 해소: 약어·프로젝트·사람을 기존 엔티티에 붙인다
3. 분류: 지금 실행을 바꾸는 공백인가, 나중에 채워도 되는 지식 부채인가
4. 질문: 실행을 바꾸는 잔여만, 예산 1–3, 가능하면 선택지
5. 기록: 답은 chat이 아니라 엔티티 노트·Open Questions·Knowledge에 남긴다
6. 배치: 지식 부채는 주간 인터뷰나 Review에서 묶어서 꺼낸다
```

이 파이프라인은 가설의 방향을 보존하면서 메커니즘을 바꾼다. 질문을 없애지 않는다. 질문을 **조회 실패의 잔여**로 격하시킨다.

WorkOs에 이미 있는 부품과 대응하면 새 시스템이 아니다.

| 단계 | 이미 있는 것 | 비어 있는 것 |
|---|---|---|
| 조회 | `AGENTS.md` discovery, project/meeting notes, `rg` | “이 엔티티를 이미 아는가”를 질문 전에 의무로 두는 계약 |
| 해소 | wikilink, project `projects:` 필드 | 약어·별칭 사전. GM / TechB / V2G Weekly 연결 |
| 질문 예산 | Capture 시 질문 하나 | 실행 게이트 질문과 지식 부채 질문의 분리 |
| 기록 | Knowledge provenance, query-to-page filing | 답변을 Open Questions에서 Claims로 올리는 짧은 루프 |
| 배치 | Review, semantic lint 후보 | “모르는 엔티티 대기열”을 Review에 쌓는 습관 |

### 경쟁 아이디어 순위

더 낫다고 보는 순서는 이 출처들의 교차다. 측정이 있는 것을 위에 둔다.

1. **Look-before-ask + 잔여 공백.** Claude 규칙, mem-agent의 clarification, WorkOs의 기존 파일. 이미 있는 기억을 세금으로 만들지 않는다.
2. **확신도 게이트.** Amazon의 질문 여부 분류, 정규 상태 + confidence. 실행이 갈라질 때만 막는다.
3. **배치 지식 추출.** SME interviewer, Aniccai의 세션형 인터뷰, IDEA2. 암묵 지식은 일상 Capture가 아니라 따로 꺼낸다.
4. **Compiled wiki / 파일 기억.** Karpathy, Letta+grep, WorkOs `20-Knowledge/`. 질문은 입력 수단이 아니라, 이미 말한 것을 복리로 남기는 일이 본체다.
5. **수동 추출 메모리 레이어.** Mem0, Zep. 말한 것을 저장하는 데는 낫고, 말하지 않은 것을 꺼내는 데는 약하다.
6. **완전 신입 상시 역질문.** 방향은 맞지만, 질문 비용·승인 피로·이미 있는 문서의 재진술을 기본값으로 만든다.

1–3이 가설보다 낫다고 보는 이유는 같다. 사람의 주의력이 희소하고, WorkOs의 실패 모드는 지식 부족이 아니라 **운영 노동의 증가**이기 때문이다.

## WorkOs 예시에 대한 재해석

가설의 첫 예시 “내일 회의있어”를 신입에게 주면 슬롯 인터뷰가 시작된다. 같은 입력을 잔여 공백 추출로 처리하면 순서가 바뀐다.

1. 오늘이 2026-08-13이면 내일 후보를 `30-Meetings/`에서 찾는다
2. 후보가 하나면 “Ford OBGI ePTO Internal로 보고 잡을까요?”처럼 확인 한 줄
3. 후보가 여러 개면 선택지만 준다
4. 후보가 없으면 그때만 시간·참석자·프로젝트를 묻는다
5. 답은 새 회의 노트와 관련 project의 Current Status로 남긴다. chat memory로 남기지 않는다

둘째 예시 “내일 GM 프로젝트 회의있어”는 조회가 더 중요하다. `GM-TechB.md`는 이미 “무엇이며 지금 무슨 상태인지”를 가지고 있다. 신입이 프로젝트 정의를 다시 물으면 vault는 늘지 않고 사람만 소모된다. 남은 질문이 있다면 “이번 건 8/19 V2G Weekly인가, 다른 슬롯인가”처럼 **일정 충돌**뿐이다.

추론: 사용자가 느낀 “도저히 관리하지 못하겠다”는 증상은 질문이 부족해서가 아니라, 이미 쌓인 원장을 AI가 먼저 읽지 않고, 사람은 원장과 채팅을 동시에 먹여야 해서 생긴다. 신입 페르소나는 그 증상을 지식 부족으로 오진한다.

## 위험과 반례

- **질문 폭주.** Reddit이 이미 측정 없이, 그러나 반복적으로 보고하는 실패다. 강제 신입은 이 실패를 기능으로 승격한다.
- **이미 있는 지식의 재진술.** look-before-ask를 빼면 사람은 자신이 쓴 `GM-TechB.md`를 입으로 복습한다.
- **지식 오염.** 유도 질문과 잘못된 슬롯이 사실로 고정되면, 수동 추출 메모리와 같은 복리 환각이 생긴다. WorkOs의 provenance 규칙이 여기에도 필요하다.
- **Capture 지연.** Inbox의 존재 이유는 형식 없이 던지는 것이다. 던질 때마다 인터뷰가 열리면 Capture가 사라진다.
- **이중 진실 공급원.** 질문에 대한 답이 chat에만 남고 파일에 안 남으면, 신입은 다음 세션에 같은 것을 다시 묻는다. 페르소나만으로는 기억이 되지 않는다.
- **Expert-system 함정.** 질문을 많이 할수록 온톨로지가 두꺼워지고, 두꺼운 온톨로지가 다시 관리 대상이 된다. 이것이 1980년대 bottleneck과 2026년 WorkOs 과부하의 공통점이다.

반례로 신입 페르소나가 맞는 경우도 있다.

- vault가 비어 있는 첫 주
- 새 고객·새 약어가 처음 등장했고 조회가 실패했을 때
- 사람이 “지금은 가르쳐도 좋다”고 연 온보딩 세션
- 실행이 아니라 명시적 지식 추출을 요청했을 때

이 경우에도 완전 신입 **상시** 모드가 아니라, 조회 실패 또는 명시 세션이라는 진입 조건이 있다.

## 검증 질문

아직 이 저장소가 측정하지 않은 것이다.

1. WorkOs Capture 20건에서, 신입 상시 질문과 look-before-ask+잔여 질문의 인간 키스트로크·중단 횟수·나중에 재사용된 사실 수는 얼마인가.
2. “GM 프로젝트”처럼 이미 노트가 있는 엔티티에서, 신입 페르소나는 얼마나 자주 이미 적힌 정의를 다시 묻는가.
3. 질문의 답을 chat에만 남긴 경우와 project/Knowledge에 남긴 경우, 7일 뒤 재사용률은 어떻게 다른가.
4. 지식 부채를 Review에 쌓아 주 1회 5문항으로 꺼내는 편이, 매 턴 1문항보다 재사용 가능한 Claims를 더 많이 만드는가.

이 네 질문이 측정되기 전에는 Blueprint나 schema를 만들 이유가 없다.

## 결론

방향은 타당하다. 기본 모델은 모르는 것을 질문하지 않고 채운다. 비서 기억의 공백 중 하나는 저장 형식이 아니라, **말하지 않은 전제를 침묵한 채 진행하는 습관**이다.

메커니즘은 타당하지 않다. 완전 신입 페르소나와 끈질긴 상시 역질문은 그 공백을 과잉 교정한다. 2026년의 공개 연구·제품·저장소는 반대로 수렴한다. 먼저 찾고, 잔여만 묻고, 질문 예산을 두며, 암묵 지식은 일상 루프가 아니라 배치 인터뷰로 꺼낸다.

WorkOs 맥락에서는 이 차이가 더 크다. vault는 이미 크고, GM 같은 엔티티는 이미 파일로 있으며, 실패 모드는 지식 공백이 아니라 운영 노동이다. 더 나은 아이디어는 신입을 상주시키는 것이 아니라, **조회 실패의 잔여 공백만 사람에게 돌려주고 그 답을 원장에 남기는 것**이다.

## 출처

### 학술·벤치마크

- [Su & Cardie, 2026. Knowing but Not Showing: LLMs Recognize Ambiguity but Rarely Ask Clarifying Questions](https://arxiv.org/abs/2605.25284)
- [Zhang, Knox & Choi, 2024/2025. Modeling Future Conversation Turns to Teach LLMs to Ask Clarifying Questions](https://arxiv.org/abs/2410.13788)
- [Siro et al., 2024. AGENT-CQ](https://arxiv.org/abs/2410.19692)
- [Gan et al., 2024. ClarQ-LLM](https://arxiv.org/abs/2409.06097)
- [RAC: Retrieval-Augmented Clarification, 2026](https://arxiv.org/html/2601.11722v1)
- [Aliannejadi et al., ClariQ / Qulac](https://arxiv.org/abs/2009.11352)
- [Kim, 2021. Deciding whether to ask clarifying questions in large-scale spoken language understanding](https://www.amazon.science/publications/deciding-whether-to-ask-clarifying-questions-in-large-scale-spoken-language-understanding)
- [Xu et al., 2026. IDEA2 competency question elicitation](https://arxiv.org/html/2604.01344v1)
- Feigenbaum, 1984. knowledge acquisition bottleneck

### 제품·프롬프트·저장소

- [Claude memory look-before-ask 규칙 (유출 프롬프트)](https://github.com/asgeirtj/system_prompts_leaks/blob/main/Anthropic/claude-fable-5.md)
- [VS Code: Tell the AI to ask clarifying questions](https://code.visualstudio.com/docs/agents/best-practices)
- [Hugging Face: mem-agent clarification 능력](https://huggingface.co/blog/driaforall/mem-agent)
- [Mem0 블로그: user memory vs org memory](https://mem0.ai/blog/ai-memory-management-for-llms-and-agents)
- GitHub: [topoteretes/cognee](https://github.com/topoteretes/cognee), [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory), [volcengine/OpenViking](https://github.com/volcengine/OpenViking), [EverMind-AI/EverOS](https://github.com/EverMind-AI/EverOS), [agiresearch/A-mem](https://github.com/agiresearch/A-mem)
- [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

### 커뮤니티

- [r/ChatGPT: GPT-5 asks too many questions](https://www.reddit.com/r/ChatGPT/comments/1mn8o6j/gpt5_wastes_your_responses_by_asking_way_too_many/)
- [r/ChatGPT: stop follow-up questions](https://www.reddit.com/r/ChatGPT/comments/1k9cavc/how_can_i_stop_chatgpt_from_asking_followup/)
- [r/ChatGPTPromptGenius: Ask Clarifying Questions + store summaries](https://www.reddit.com/r/ChatGPTPromptGenius/comments/1jqzpi9/finally_i_found_a_way_to_keep_chatgpt_remember/)
- X: Karpathy, 2025-06-03, anterograde amnesia coworker ([1930003172246073412](https://x.com/karpathy/status/1930003172246073412))
- X: `@adxtyahq`, 2026-04-23, canonical state + confidence gate ([2047295014678782291](https://x.com/adxtyahq/status/2047295014678782291))
- X: `@sage4xx`, 2026-08-05, treat AI like a hire and make it ask when unsure ([2084893291057733903](https://x.com/sage4xx/status/2084893291057733903))

### 지식 추출 실무

- [Aniccai: first agent should be an interviewer](https://aniccai.com/en/knowledge/Agents/ai-expertise-elicitation-agent)
- [Hardman, 2026. Has AI finally fixed L&D's SME problem?](https://drphilippahardman.substack.com/p/has-ai-finally-fixed-l-and-ds-sme)

### Vault 내부 선행

- WorkOs `50-Personal/Thinking/AI 장기기억과 WorkOs Vault.md`
- WorkOs `20-Knowledge/Tools-Methods/LLM-Wiki-Pattern-for-PKM.md`
- WorkOs `20-Knowledge/Tools-Methods/AI-Native-PKM-Landscape-and-WorkOs-Position.md`
- WorkOs `50-Personal/Thinking/WorkOs-Dual-User-함께-성장하는-루프.md`
- WorkOs `AGENTS.md` Capture 규칙
- WorkOs `10-Projects/GM-TechB/GM-TechB.md`
