# Local Project Continuity

## 상태

Idea note. 아직 Capability Blueprint, 구현 사양, 저장 형식 또는 특정 도구의 채택 결정이 아니다.

## 문제

AI 작업 세션의 Context는 유한하며 압축 과정에서 세부 정보가 손실될 수 있다. 새로운 Agent나 모델은 이전 세션에서 축적된 판단을 처음부터 알지 못한다. GitHub나 GitLab issue를 운영하지 않는 로컬 프로젝트에서는 현재 작업, 과거 결정, 조사 결과와 실패 경험을 이어받을 공통 장소도 부족하다.

최근 Agent 제품은 자동 메모리를 제공하기 시작했지만 그것만으로 프로젝트의 장기 연속성을 보장하기 어렵다.

- Agent 또는 제품별 저장소와 동작에 종속될 수 있다.
- 다른 모델, 다른 PC 또는 새로운 작업자에게 그대로 전달되지 않을 수 있다.
- 무엇이 저장·생략·폐기됐는지 프로젝트가 통제하기 어렵다.
- AI가 추출한 기억과 인간이 승인한 프로젝트 사실이 섞일 수 있다.
- 현재 상태, 결정 근거, 시행착오와 연구 지식은 서로 다른 lifecycle이 필요하다.

따라서 핵심 문제는 AI에게 무제한 기억을 주는 것이 아니다.

> 새로운 AI가 이전 대화를 몰라도 로컬 프로젝트의 현재 상태, 중요한 결정과 근거, 재사용할 학습과 다음 행동을 빠르고 신뢰성 있게 복구할 수 있어야 한다.

## 용어 선택

`AI Long-Term Memory`보다 `Project Continuity`를 우선 용어로 사용한다. 기억의 소유자는 특정 AI가 아니라 프로젝트여야 하며, 목표는 대화 전체의 재현이 아니라 작업 연속성의 복구이기 때문이다.

## 조사에서 확인된 접근법

공개 생태계에는 하나의 공인된 project-memory 표준이 없다. 대신 서로 다른 문제를 해결하는 접근법이 공존한다.

| 접근법 | 주로 해결하는 것 | 남는 한계 |
|---|---|---|
| `AGENTS.md`, `CLAUDE.md`, Rules | 항상 적용할 명령, 관례와 제약 | 현재 작업과 과거 논의의 이력을 담기에는 부적합 |
| Agent 자동 메모리 | 반복되는 선호, 발견과 debugging 학습 | 제품·기계 종속성과 자동 선별에 대한 신뢰 문제 |
| Memory Bank와 handoff file | 세션 간 현재 상태와 프로젝트 맥락 | 수동 유지, 중복, 비대화와 stale 정보 위험 |
| 로컬 issue·task graph | 작업 상태, blocker와 의존성 | 결정 근거와 연구 지식을 별도로 관리해야 함 |
| Spec-Driven Development | 의도, 요구사항, plan과 task | 지속적인 운영 경험이나 넓은 지식 축적은 범위 밖 |
| 로컬 Wiki와 지식베이스 | 연구·문서 지식의 누적 종합과 탐색 | 현재 작업 상태와 완료 판단을 별도로 구성해야 함 |
| RAG와 code index | 많은 자료에서 관련 Context 검색 | 검색된 내용의 현재 유효성과 권위를 결정하지 못함 |
| 전용 memory runtime·knowledge graph | 대규모 검색, 관계와 시간 변화 | 일반 로컬 프로젝트에는 운영 복잡도가 클 수 있음 |

연구와 실무 사례는 긴 대화를 그대로 유지하기보다 작은 상시 Context, 구조화된 현재 상태, 원본 기록과 필요할 때 검색하는 장기 저장소를 계층화하는 방향을 지지한다.

## 기억해야 하는 정보의 종류

하나의 `MEMORY.md`에 모든 정보를 넣지 않고 최소한 다음 성격을 구분할 필요가 있다.

### 운영 규칙

빌드 방법, 금지 작업, 코드 관례와 검증 절차처럼 대부분의 세션에서 적용되는 절차적 기억이다. 프로젝트의 Agent instruction이 적합하다.

### 현재 작업 상태

지금 해결하는 문제, 진행 위치, blocker, 다음 행동과 재개 조건이다. 작고 자주 갱신되는 authoritative record가 필요하다.

### 결정과 현재 사실

어떤 선택을 왜 했는지, 어떤 제약과 가정이 현재 유효한지를 기록한다. 인간 승인, 근거, 적용 범위와 대체 관계가 중요하다.

### 경험과 증거

조사 출처, 실험 결과, 실패한 접근과 관찰처럼 이후 판단에 재사용할 수 있는 기록이다. 현재 사실과 섞지 않고 원본을 추적할 수 있어야 한다.

### 탐색 계층

Index, full-text search, embedding, graph와 HTML 화면처럼 앞의 기록을 찾거나 이해하기 쉽게 만드는 파생 계층이다. 삭제 후 다시 만들 수 있어야 하며 source of truth가 아니다.

## 현재 설계 가설

### 자율 생성보다 공통 계약을 우선한다

Local Project Continuity는 프로젝트마다 AI가 새로운 기억 체계를 자유롭게 발명하도록 맡겨서는 안 된다. 프로젝트가 바뀔 때마다 기록 위치, 정보의 의미, 현재성 판단과 인수인계 절차가 달라지면 새 Agent가 관리 체계부터 다시 해석해야 하며, 이는 이 Idea가 해결하려는 연속성 손실을 되살린다.

따라서 향후 Capability는 **고정된 Continuity Core와 제한된 Project Profile**로 구성한다.

- Continuity Core는 정보 유형, 권위, lifecycle, 필수 operation과 복구 계약을 모든 프로젝트에 동일하게 적용한다.
- Project Profile은 기존 tracker·문서 체계와의 연결, 저장 위치, 추가 metadata, 보안 정책과 표현 방식을 정한다.
- Profile은 Core의 의미를 바꾸거나 필수 기록을 생략할 수 없으며, 프로젝트별 용어는 공통 개념에 명시적으로 대응시킨다.
- 새 Agent는 프로젝트 고유 구조를 추측하지 않고 Core 계약과 Profile만으로 기록을 찾고 해석할 수 있어야 한다.

### 프로젝트가 기억을 소유한다

Canonical memory는 대상 프로젝트가 통제하는 로컬 기록이어야 한다. Agent 제품의 자동 메모리는 유용한 보조 계층일 수 있지만 공식 결정이나 필수 규칙의 유일한 원본이 되어서는 안 된다.

### 작은 Briefing과 큰 Archive를 분리한다

새 세션에는 모든 기록이 아니라 현재 목적, 상태, 핵심 제약과 다음 행동으로 구성된 제한된 Briefing을 제공한다. 상세 결정, 증거와 과거 기록은 필요할 때만 찾는다.

### 현재 상태와 역사를 분리한다

현재 상태는 빠르게 복구할 수 있도록 작게 유지한다. 과거 상태, superseded 결정과 세션별 사건은 역사로 보존하되 매번 Context에 넣지 않는다.

### 기억에는 lifecycle이 있다

각 기록은 가능한 범위에서 종류, 상태, 날짜, 출처, 적용 범위와 `supersedes` 관계를 가진다. 오래된 사실을 조용히 덮어쓰거나 서로 충돌한 채 함께 사용하지 않는다.

### 저장과 표현을 분리한다

사람이 보는 결과는 상황에 따라 HTML dashboard, timeline, graph, 표 또는 짧은 text가 될 수 있다. 표현물은 canonical memory에서 생성되는 projection이며 입력이나 공식 원본을 강제하지 않는다.

### 규모가 증명된 뒤 도구를 추가한다

작은 프로젝트는 파일과 기본 검색으로 시작할 수 있다. 문서 수, 관계 복잡도 또는 검색 실패가 실제로 확인된 뒤에 SQLite/FTS, local issue tracker, hybrid search, MCP 또는 temporal graph를 검토한다.

## Continuity Core의 최소 공통 정보 모델

구현 형식과 무관하게 모든 프로젝트는 다음 의미 영역을 구분해야 한다. 하나의 파일에 여러 영역을 담을 수는 있지만 서로 다른 종류와 권위를 가진 정보를 구별할 수 있어야 한다.

| 영역 | 반드시 답할 질문 | 권위와 갱신 원칙 |
|---|---|---|
| Project Brief | 이 프로젝트는 무엇이며 현재 어떤 제약 아래 운영되는가? | 안정적인 목적·범위만 유지하고 임시 작업 상태를 섞지 않는다. |
| Active Focus | 지금 집중하는 유한한 목표와 완료 조건은 무엇인가? | 동시에 무엇이 활성 상태인지 명확해야 하며 완료·중단 시 상태를 닫는다. |
| Work State | 어디까지 진행했고 blocker, 검증 결과와 다음 행동은 무엇인가? | 재개 가능한 최신 상태의 authoritative record를 하나만 둔다. |
| Decisions | 무엇을 누가 어떤 근거와 범위로 결정했는가? | 인간 승인 여부와 `supersedes` 관계를 보존하고 조용히 덮어쓰지 않는다. |
| Knowledge and Evidence | 어떤 조사·실험·실패가 이후 판단에 재사용되는가? | 관찰, 추론과 출처를 구분하며 현재 결정으로 자동 승격하지 않는다. |
| Handoffs | 다른 Agent가 즉시 이어서 작업하려면 무엇을 알아야 하는가? | 세션 요약이 아니라 정확한 재개 지점과 미완료 위험을 남긴다. |
| Archive | 무엇이 종료·폐기·대체되었으며 왜 현재 Context에서 제외되는가? | 검색 가능하게 보존하되 현재 유효한 정보처럼 노출하지 않는다. |

초기 Pilot에서는 사람이 읽을 수 있는 파일 기반 표현을 우선 검토한다. 그러나 구체적인 디렉터리명, Markdown frontmatter 또는 schema는 이 Idea 단계에서 확정하지 않는다. 먼저 위 정보 모델이 서로 다른 프로젝트에서도 충분하고 모호하지 않은지 검증한다.

## Core와 Project Profile의 경계

```text
Continuity Core                     Project Profile
├─ 공통 정보 유형과 의미            ├─ 실제 저장 위치와 파일 대응
├─ 권위와 인간 승인 경계            ├─ 기존 issue·Wiki·ADR 연동
├─ 상태 lifecycle과 supersession    ├─ 도메인별 추가 metadata
├─ 필수 operation의 의미            ├─ 보안·보존 정책
└─ 최소 복구·감사 계약              └─ HTML·TUI·검색 등 표현과 도구
```

Project Profile은 별도의 관리 체계를 만드는 허가가 아니라 기존 프로젝트 구조를 Core에 연결하는 adapter다. 예를 들어 기존 ADR은 `Decisions`, 실험 노트는 `Knowledge and Evidence`, 로컬 task tracker는 `Work State`의 원본으로 대응할 수 있다. 같은 정보를 Continuity 전용 파일에 복제하기보다 원본 위치와 권위를 Profile에 선언해야 한다.

## 개념적 흐름

```text
프로젝트의 규칙·상태·결정·증거
              ↓
       프로젝트 소유 기록
       ├─ 작은 현재 Briefing
       ├─ 결정과 현재 사실
       ├─ 경험·증거와 역사
       └─ 선택적 파생 index
              ↓
새 Agent가 필요한 Context만 복구
              ↓
작업과 인간 논의
              ↓
재사용 가치가 있는 변화만 기록·대체·정리
```

## 필수 operation 후보

이 operation들의 이름, Skill 분할과 사용자 명령은 아직 확정하지 않지만 의미와 기대 결과는 프로젝트마다 같아야 한다.

1. **Initialize**: 기존 문서, 기록, Agent와 로컬 도구를 조사하고 최소 기억 구성을 제안한다.
2. **Brief**: 새 세션이나 Agent가 현재 상태와 관련 Context를 제한된 크기로 복구한다.
3. **Capture**: 관찰, 추론, 결정 후보, 증거와 중요한 실패를 그 성격과 출처가 드러나게 기록한다.
4. **Decide**: 인간 승인 규칙에 따라 결정 후보를 확정하고 적용 범위와 근거를 남긴다.
5. **Handoff**: 진행 중 작업의 상태, 검증 결과와 정확한 재개 지점을 남긴다.
6. **Query**: 관련 기록을 출처, 적용 범위와 현재 유효성을 포함해 찾는다.
7. **Supersede**: 더 이상 유효하지 않은 사실이나 결정을 새 기록과 명시적으로 연결한다.
8. **Consolidate**: 중복을 병합하고 상세 기록을 archive하며 작은 Briefing을 유지한다.
9. **Audit**: 근거 없는 주장, 충돌, stale 정보, 고아 기록과 과도한 Context를 찾는다.

## 예상 불변 조건

- Agent가 추론한 내용을 인간이 승인한 결정처럼 저장하지 않는다.
- 관찰된 사실, 추론, 미확인 정보와 인간 결정을 구분한다.
- 현재 상태를 나타내는 authoritative record를 중복 생성하지 않는다.
- 원본 대화 전체를 기본 기억으로 보존하지 않고 재사용 가치가 있는 결과만 추출한다.
- 코드나 실행 결과에서 안정적으로 다시 확인할 수 있는 정보를 불필요하게 복제하지 않는다.
- 모든 중요한 기억은 사람이 읽고 수정하거나 폐기할 수 있어야 한다.
- Agent 자체 메모리, 검색 index와 HTML projection을 canonical source로 취급하지 않는다.
- 네트워크나 특정 AI 제공자가 없어도 canonical memory를 열람할 수 있어야 한다.
- 민감 정보, 개인 세션 기록과 인증 정보는 명시적 정책 없이 수집하지 않는다.
- 외부 시스템 쓰기와 중요한 결정 확정에는 대상 프로젝트의 인간 승인 규칙을 따른다.

## 프로젝트 규모에 따른 적응 가능성

| 조건 | 검토할 수 있는 최소 구성 |
|---|---|
| 작고 짧은 작업 | 현재 상태, 소수 결정과 handoff file |
| 일반적인 장기 프로젝트 | 파일 기반 canonical memory, index와 archive |
| 작업 의존성이 복잡함 | canonical memory와 로컬 issue·task tracker 조합 |
| 연구 자료가 계속 증가함 | immutable source와 AI 유지 Wiki 또는 knowledge layer |
| 검색 대상이 매우 큼 | 재생성 가능한 SQLite/FTS 또는 hybrid retrieval index |
| 사실의 시간 변화가 핵심 | temporal metadata 또는 knowledge graph 검토 |

Blueprint가 된다면 Core의 정보 의미와 operation은 고정하되 특정 파일명, Markdown, JSON, DB, UI 또는 Skill 수는 Pilot evidence 없이 고정하지 않는다. 대상 프로젝트를 조사한 결과는 Core를 변경하는 데 쓰는 것이 아니라 기존 기록과 도구를 Project Profile로 대응시키는 데 우선 사용한다.

## 기존 capability와의 관계

`manage-focus-cycle`은 끝이 없는 프로젝트 안에서 지금 집중할 하나의 제한된 목표와 종료 조건을 관리한다. Local Project Continuity는 그 Focus Cycle을 포함한 프로젝트 상태와 학습이 세션·Agent 교체를 견디게 하는 더 넓은 연속성 문제다.

둘은 결합할 수 있지만 동일한 capability는 아니다. Focus Cycle 없이도 결정과 연구 지식의 연속성이 필요할 수 있고, Project Continuity가 전체 roadmap이나 프로젝트 완료율을 관리해서도 안 된다.

## 비목표

- AI에게 완전하거나 무제한인 인간형 기억을 제공하는 것
- 모든 대화와 tool output을 영구 보존하는 것
- 모든 정보를 하나의 범용 `MEMORY.md`에 혼합하거나 동일한 물리 파일 배치를 모든 프로젝트에 강제하는 것
- 처음부터 vector DB, MCP server 또는 knowledge graph를 배포하는 것
- 프로젝트의 기존 문서, tracker와 결정 기록을 또 하나의 체계로 복제하는 것
- AI가 기억할 가치와 현재의 진실을 단독으로 결정하게 하는 것
- 이 저장소가 소비 프로젝트의 기억을 중앙 수집하거나 동기화하는 것

## 위험과 반례

### 기억 비대화

기록이 많다는 이유만으로 연속성이 좋아지지 않는다. Briefing 예산, archive와 정기적인 consolidation이 없으면 Context 오염이 다시 발생한다.

### Stale memory

과거 사실이 현재 코드보다 권위 있게 사용될 수 있다. 현재 유효성, 근거와 supersession을 확인하지 않는 검색은 잘못된 자신감을 만들 수 있다.

### 기록 체계의 중복

이미 프로젝트에 plan, ADR, 실험 log 또는 tracker가 있다면 새 저장소를 만드는 것보다 그 기록을 우선 사용해야 한다.

### 자동 추출 오류

AI가 대화에서 잘못된 결론이나 일시적 상황을 장기기억으로 승격할 수 있다. 중요한 결정과 민감한 기록에는 review boundary가 필요하다.

### 과도한 운영비

기억 관리가 실제 작업보다 더 큰 부담이 될 수 있다. 기록의 기대 재사용 가치가 유지 비용보다 클 때만 capture해야 한다.

## 유용성 검증 가설

이 개념을 Candidate나 Blueprint로 승격하기 전에 다음을 서로 다른 유형의 로컬 프로젝트에서 검증할 필요가 있다.

- 이전 대화를 볼 수 없는 새 Agent가 현재 작업과 다음 행동을 정확히 설명한다.
- 다른 Agent 제품이나 모델로 바꿔도 프로젝트 연속성이 유지된다.
- 과거 결정의 선택, 근거, 적용 범위와 대체 결정을 추적할 수 있다.
- 실패했던 접근이 불필요하게 반복되지 않는다.
- 오래된 사실과 현재 사실이 충돌할 때 이를 탐지하고 인간에게 보여준다.
- 시작 Briefing은 프로젝트가 커져도 제한된 크기를 유지한다.
- 검색 결과가 원본 근거와 현재 유효성을 제시한다.
- 로컬·비공개 환경에서 외부 issue service 없이 동작한다.
- 사람이 기억 내용을 감사하고 잘못된 항목을 수정하거나 폐기할 수 있다.
- 시스템 유지 비용이 재설명, 재조사와 중복 작업 감소보다 작다.

## 향후 탐색

- 제안한 최소 공통 정보 모델에서 빠지거나 중복된 영역은 무엇인가?
- 각 정보 유형의 최소 metadata와 상태 전이는 무엇이어야 하는가?
- Project Profile이 Core 의미를 훼손하지 않았음을 어떻게 판정할 것인가?
- 서로 다른 저장 구조를 사용하는 Agent 사이의 상호운용성을 어떤 scenario로 검증할 것인가?
- 어떤 기록은 자동 capture하고 어떤 기록은 인간 승인을 요구해야 하는가?
- 새 세션 Briefing의 크기와 포함 기준을 어떻게 검증할 것인가?
- 코드에서 재유도할 정보와 명시적으로 기억할 정보를 어떻게 구분할 것인가?
- Git이 없는 로컬 폴더와 Git 저장소에서 같은 원칙을 어떻게 적용할 것인가?
- 여러 Agent가 동시에 기록할 때 충돌과 권위를 어떻게 다룰 것인가?
- 기존 project tracker나 Wiki가 있을 때 새 기록을 만들지 않는 adaptation 규칙은 무엇인가?
- 이 문제를 하나의 Blueprint로 다룰지, continuity와 knowledge accumulation으로 나눌지?

## 참고한 주요 출처

- [AGENTS.md — coding agent용 공개 프로젝트 지침 형식](https://github.com/agentsmd/agents.md)
- [Codex local memories](https://learn.chatgpt.com/docs/customization/memories.md)
- [Claude Code project memory와 auto memory](https://code.claude.com/docs/en/memory)
- [GitHub Copilot Memory](https://docs.github.com/en/copilot/concepts/agents/copilot-memory)
- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [LongMemEval — 장기 대화 기억 평가](https://arxiv.org/abs/2410.10813)
- [LoCoMo — 장기 대화의 시간·인과 기억 평가](https://arxiv.org/abs/2402.17753)
- [MemGPT — 계층형 virtual context management](https://arxiv.org/abs/2310.08560)
- [Karpathy — LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Basic Memory — local-first file source와 파생 database](https://docs.basicmemory.com/reference/technical-information)
- [Beads — AI Agent용 로컬 작업 그래프](https://github.com/gastownhall/beads)
- [git-bug — Git 기반 offline-first issue tracker](https://github.com/git-bug/git-bug)
- [GitHub Spec Kit — Spec-Driven Development와 artifact persistence](https://github.github.com/spec-kit/concepts/spec-persistence.html)
