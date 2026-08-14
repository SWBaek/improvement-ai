# Local Project Continuity

## Status

- State: `Promoted`
- Last reviewed: 2026-08-14
- Next trigger: 사용자 개입을 기본값으로 삼지 않는 더 작은 continuity 가설이 제안되어 최초 문제와 이 탐색의 record-first 가정을 다시 비교할 때 재검토한다.
- Follow-up: [`maintain-project-continuity`](../../blueprints/maintain-project-continuity/BLUEPRINT.md), [tracking issue #21](https://github.com/SWBaek/improvement-ai/issues/21)

이 문서는 탐색 배경과 v0.1 설계 가설을 보존하는 동결된 기록이며 더 이상 규범적 원본이 아니다. 현재 계약은 canonical Blueprint에서, Pilot 진행 상태와 evidence는 tracking issue에서만 관리한다.

2026-08-14 재검토에서 세션 간 복구 문제 자체는 남아 있지만, 많은 record 유형과 사전 선택으로 복구를 보장하려던 가설은 첫 실사용의 사용자 인지 부하를 정당화하지 못했다. 구체적인 결과와 후속 상태는 tracking issue에서 관리한다.

## 문제

AI 작업 세션의 Context는 유한하고 압축 과정에서 세부 정보가 손실될 수 있다. 새로운 Agent나 모델은 이전 세션에서 축적한 판단을 처음부터 알지 못한다. GitHub나 GitLab issue를 사용하지 않는 로컬 프로젝트에서는 현재 작업, 과거 결정, 조사 결과와 실패 경험을 이어받을 공통 장소도 부족하다.

Agent 제품의 자동 메모리만으로는 프로젝트의 장기 연속성을 보장하기 어렵다.

- Agent, 제품 또는 기계에 종속될 수 있다.
- 무엇이 저장·생략·폐기됐는지 프로젝트가 통제하기 어렵다.
- AI가 추출한 기억과 인간이 승인한 사실이 섞일 수 있다.
- 현재 상태, 결정 근거, 시행착오와 연구 지식은 서로 다른 lifecycle이 필요하다.

핵심 문제는 AI에게 무제한 기억을 주는 것이 아니다.

> 새로운 AI가 이전 대화를 몰라도 로컬 프로젝트의 현재 상태, 중요한 결정과 근거, 재사용할 학습과 다음 행동을 빠르고 신뢰성 있게 복구할 수 있어야 한다.

## 용어

`AI Long-Term Memory`보다 `Project Continuity`를 우선 사용한다. 기억의 소유자는 특정 AI가 아니라 프로젝트이며, 목표는 대화 전체의 재현이 아니라 작업 연속성의 복구이기 때문이다.

## 조사에서 얻은 교훈

공개 생태계에는 하나의 공인된 project-memory 표준이 없다. 대신 다음 접근법이 문제의 일부를 해결한다.

| 접근법 | 가져올 원칙 | 피해야 할 한계 |
|---|---|---|
| `AGENTS.md`, `CLAUDE.md`, Rules | 항상 적용할 운영 규칙을 작게 유지 | 현재 작업과 과거 논의를 한곳에 누적 |
| Cline Memory Bank와 handoff file | 안정적 맥락과 자주 변하는 현재 상태 분리 | 모든 파일을 매번 읽거나 AI가 과도하게 기록 |
| Nygard ADR과 MADR | 중요한 결정 하나를 짧고 독립적으로 기록하고 대체 이력 보존 | 사소한 선택까지 ADR로 만들거나 큰 양식 강제 |
| Spec-Driven Development | source of truth와 변경·보존 방식을 명시 | spec, plan, task와 실제 상태의 중복·drift |
| 로컬 issue·task graph | 작업 상태와 의존성을 구조화 | 결정·지식까지 복잡한 DB와 동기화 체계에 결합 |
| Wiki, RAG와 code index | 큰 자료를 필요할 때 검색 | 검색 결과의 권위와 현재성을 자동으로 신뢰 |

Nygard는 큰 문서보다 짧고 독립적인 결정 기록이 유지될 가능성이 높다고 보았고, MADR은 상태와 대체 관계를 포함한 작은 형식을 제공한다. Spec Kit은 어떤 artifact가 원본이며 변경 시 어떻게 유지할지를 명시하지 않으면 silent drift가 생길 수 있음을 보여준다. Beads는 구조화된 장기 작업의 가능성을 보여주지만 DB, JSONL, Git 동기화가 결합된 구조는 이 Idea의 초기 범위에는 과도하다.

따라서 초기 해법은 **작고 사람이 읽을 수 있는 프로젝트 소유 기록**이어야 한다. DB, 검색 index와 화면은 관찰된 실패를 해결할 때만 파생 계층으로 추가한다.

## 핵심 설계

### 고정된 Core와 제한된 Project Profile

프로젝트마다 AI가 새로운 기억 체계를 자유롭게 발명하게 해서는 안 된다. 기록 위치, 정보 의미, 현재성 판단과 인수인계 절차가 매번 달라지면 새 Agent가 관리 체계부터 다시 해석해야 한다.

향후 Capability는 다음 두 층으로 구성한다.

```text
Continuity Core                     Project Profile
├─ 공통 정보 유형과 의미            ├─ 실제 저장 위치와 파일 대응
├─ 권위와 인간 승인 경계            ├─ 기존 issue·Wiki·ADR 연동
├─ 상태 lifecycle과 supersession    ├─ 도메인별 추가 metadata
├─ 필수 operation의 의미            ├─ 보안·보존 정책
└─ 최소 복구·감사 계약              └─ HTML·TUI·검색 등 표현과 도구
```

- Core는 모든 프로젝트에서 동일하게 해석되어야 한다.
- Profile은 Core를 프로젝트의 기존 기록과 도구에 연결하는 adapter다.
- Profile은 Core 의미를 바꾸거나 필수 정보를 조용히 생략할 수 없다.
- 기존 ADR, tracker와 연구 문서를 복제하지 않고 그 원본 위치와 권위를 Profile에 선언한다.

각 정보 영역은 도입 시 다음 중 하나를 선택한다.

- **Integration**: 기존 문서나 tracker를 원본으로 유지하고 Profile이 그 위치와 역할을 연결한다.
- **Migration**: 기존 정보를 Continuity 구조로 이전하고 이후 Continuity record를 원본으로 사용한다.

선택은 프로젝트 전체가 아니라 Project Brief, Work Item, Decision, Knowledge 등의 영역별로 할 수 있다. 그러나 한 영역의 같은 정보에 두 원본을 두는 이중 관리는 어떤 mode에서도 허용하지 않는다.

### 프로젝트가 기억을 소유한다

Canonical record는 대상 프로젝트가 통제하는 로컬 파일이어야 한다. Agent 제품의 자동 메모리는 보조 수단일 수 있지만 공식 결정이나 필수 규칙의 유일한 원본이 되어서는 안 된다.

### 작은 현재 상태와 큰 역사를 분리한다

새 세션에는 현재 목적, Focus, 핵심 제약과 다음 행동만 제공한다. 상세 결정, 증거와 과거 기록은 필요할 때 찾는다. 현재 상태는 작게 유지하고 종료·폐기·대체된 정보는 매번 Context에 넣지 않는다.

### 저장, 교환과 표현을 분리한다

- 사람이 감사할 canonical record는 Markdown 본문과 제한된 YAML metadata로 구성한다. 사람은 AI에게 변경을 지시하는 운영을 기본으로 하되 전용 도구 없이 내용을 읽을 수 있어야 한다.
- JSON Schema는 YAML metadata의 검증과 Agent·도구 간 교환 계약에 사용한다.
- HTML dashboard, 검색 index, embedding과 graph는 canonical record에서 생성되는 파생물이다.

## 최소 공통 정보 모델

구현 형식과 관계없이 다음 의미 영역을 구분한다. 개념은 구분하되 각각을 별도 파일로 만들 필요는 없다.

| 영역 | 반드시 답할 질문 | 갱신 원칙 |
|---|---|---|
| Project Brief | 이 프로젝트는 무엇이며 어떤 제약 아래 운영되는가? | 기존 README 등을 원본으로 연결하고 임시 상태를 섞지 않는다. |
| Work Items | 현재 열려 있는 유한한 목표와 각각의 완료 조건은 무엇인가? | 여러 항목을 동시에 열 수 있으며 항목별 authoritative record는 하나만 둔다. |
| Session Focus | 이번 세션에서 어떤 Work Item을 다루는가? | 열린 항목을 요약·추천한 뒤 인간이 세션마다 선택한다. |
| Decisions | 무엇을 누가 어떤 근거와 범위로 결정했는가? | 인간 승인과 `supersedes` 관계를 보존한다. |
| Knowledge and Evidence | 어떤 조사·실험·실패가 재사용되는가? | 관찰, 추론과 출처를 구분하고 결정으로 자동 승격하지 않는다. |
| Handoff | 다음 Agent가 현재 시점에서 즉시 이어받으려면 무엇을 알아야 하는가? | 최신 인수인계서 하나에 정확한 재개 지점과 미완료 위험을 남긴다. |
| Historical Records | 무엇이 완료·취소·대체되었는가? | 파일을 이동·삭제하지 않고 상태로 구분하며 현재 Brief에서 기본 제외한다. |

## 최소 물리 구조 가설

첫 Pilot에서는 다음 최소 구조를 검토한다. Integration으로 연결한 영역에는 대응하는 Continuity record를 중복 생성하지 않는다.

```text
.project-continuity/
├─ profile.yaml
├─ work-items/
│  └─ WI-0001-*.md
├─ decisions/
│  └─ DR-0001-*.md
└─ handoff.md
```

### `profile.yaml`

프로젝트 정보 자체를 복사하지 않고 기존 원본의 위치와 역할을 선언한다.

```yaml
schema_version: "0.1"
project_id: "example-project"
ownership:
  project_brief: integration
  work_items: integration
  decisions: continuity
  handoff: continuity
sources:
  project_brief: README.md
  instructions:
    - AGENTS.md
  work_tracker:
    kind: local-files
  decisions: .project-continuity/decisions
  knowledge:
    - docs/
authority:
  decision_approval: project-owner
  work_item_completion: project-owner
```

### `work-items/`

Migration mode에서 Continuity가 Work Item을 소유할 때 작업 하나당 파일 하나를 둔다. 여러 Work Item이 동시에 `active`일 수 있으며, 각 파일은 완료 조건, 현재 위치, 다음 행동, blocker와 마지막 검증 결과를 가진다. 상태는 다음 다섯 개로 제한한다.

```text
planned → active → completed
             ↕
          blocked

어느 열린 상태에서든 → cancelled
```

`paused`는 별도로 두지 않고 필요하면 이유와 함께 `planned`로 되돌린다. `completed`와 `cancelled` record는 이동하거나 삭제하지 않는다. AI는 진행 상태와 증거를 자동 갱신할 수 있지만 완료 조건별 증거를 제시한 뒤 인간 승인을 받아야 `completed`로 전환할 수 있다.

### `decisions/`

중요한 결정 하나를 짧은 record 하나로 관리한다. 상태는 `proposed`, `accepted`, `rejected`, `superseded`로 제한한다. AI는 장기 영향 기준을 충족하는 초안을 자동으로 `proposed`로 기록할 수 있지만 인간의 명확한 선택이 있어야 `accepted`로 전환한다. “이 방식을 사용하자”처럼 명시적인 응답은 승인으로 인정하며 이중 확인하지 않는다.

모든 승인된 결정은 `Context`, `Decision`, `Consequences`를 포함한다. 외부 `source_refs`는 실제 근거가 있을 때만 추가한다. 승인 주체는 Profile에 정의된 `project-owner`, `maintainer` 같은 역할 또는 식별자로 기록하고 실명은 강제하지 않는다.

승인된 결정의 의미가 바뀌면 새 Decision Record가 기존 record를 `supersedes`한다. 기존 record는 `superseded`로 남기며, 직접 수정은 의미가 변하지 않는 오탈자나 깨진 링크 정정에만 허용한다.

### `handoff.md`

현재 시점에서 마지막으로 완료한 것, Session Focus, 정확한 재개 지점, 미검증 사항과 관련 참조만 유지한다. 최신 Handoff 하나를 계속 갱신하며 세션별 파일을 누적하지 않는다. 지속할 내용은 Work Item이나 Decision에 반영하고 Git 저장소의 과거 변경은 Git history에 맡긴다.

Work Item의 시작·상태 변경, 의미 있는 단계 완료, blocker 발생·해소, 중요한 검증 결과, 작업 종료나 전환처럼 의미 있는 경계에서 AI가 별도 승인 없이 Work Item과 Handoff를 갱신한다. 상태 변화가 없는 단순 질의응답에서는 갱신하지 않는다.

이 구조는 아직 확정안이 아니다. 기존 구조가 있는 프로젝트에서는 새 파일을 중복 생성하지 않고 Profile을 통해 대응할 수 있어야 한다.

## 최소 JSON Schema 가설

JSON Schema는 필요하지만 JSON 파일을 유일한 사람이 편집하는 원본으로 강제하지 않는다. YAML frontmatter나 Profile을 동일한 데이터 모델로 검증하고, 필요할 때 표준 JSON으로 투영하는 **Canonical Interchange Schema** 역할을 우선한다.

초기에는 두 schema만 검토한다.

```text
schemas/
├─ profile.schema.json
└─ record.schema.json
```

`record.schema.json`은 유형별 모든 내용을 고정하지 않고 공통 envelope만 정의한다. Continuity 소유 record는 `WI-0001`, `DR-0001`처럼 유형 접두사와 재사용하지 않는 증가 번호를 사용한다. 연결된 외부 record는 원래 식별자를 유지한다.

```json
{
  "schema_version": "0.1",
  "id": "DR-0001",
  "type": "decision",
  "status": "accepted",
  "updated_at": "2026-08-07T12:00:00+09:00",
  "authority": {
    "kind": "human-approved",
    "approved_by": "project-owner"
  },
  "supersedes": [],
  "source_refs": [],
  "extensions": {
    "example-domain": {}
  }
}
```

Core의 최상위 필드는 고정하며 프로젝트·도메인별 metadata는 이름이 구분된 `extensions` 아래에서만 허용한다. Schema는 필드 형식만 검증한다. 참조 대상의 존재, 순환하는 `supersedes`, 실제 인간 승인과 stale 상태는 operation의 semantic audit가 확인해야 한다. 유형별 schema는 두 Pilot에서 공통 필요가 확인된 뒤에만 분리한다.

## 최소 operation

사용자가 많은 명령을 기억하지 않도록 처음에는 다섯 동작으로 제한한다. 이름과 Skill 분할은 아직 확정하지 않지만 의미와 기대 결과는 프로젝트마다 같아야 한다.

1. **Initialize**: 기존 문서와 도구를 읽기 전용으로 조사한다. 영역별 Integration/Migration, 기존 원본, 생성·이전할 파일과 충돌을 구체적으로 제안하고 인간 승인 후에만 변경한다.
2. **Brief**: 먼저 열린 Work Item을 한 줄씩 요약하고 근거와 함께 우선 항목을 추천한다. 사용자가 Session Focus를 선택한 뒤 그 항목에 관련된 결정과 증거만 상세히 불러온다.
3. **Record Decision**: 장기 영향 기준에 해당하는 결정 후보를 `proposed`로 작성하고 인간의 명확한 선택 후 `accepted`로 전환한다.
4. **Handoff**: 의미 있는 작업 경계에서 Work Item과 최신 인수인계서의 검증 결과, 다음 행동과 정확한 재개 지점을 자동 갱신한다.
5. **Audit**: 깨진 참조, source-of-truth 충돌, 잘못된 상태·대체 관계, stale 상태와 과도한 Context를 읽기 전용으로 찾고 근거와 수정안을 제시한다.

Capture, Query, Supersede와 Consolidate는 우선 이 다섯 operation 내부 행동으로 둔다. 반복 사용에서 독립된 사용자 의도가 확인될 때만 별도 operation으로 승격한다.

## Capture 기준

모든 대화와 tool output을 기록하지 않는다. 다음 중 하나에 해당할 때만 장기 기록 후보로 본다.

- 다음 세션이 모르면 잘못된 작업을 할 가능성이 높다.
- 코드와 현재 파일만으로 선택 이유를 복구하기 어렵다.
- 실패한 접근을 다시 반복할 가능성이 있다.
- 인간이 장기적으로 적용할 결정임을 승인했다.
- 정확한 다음 행동이나 blocker 없이는 작업을 재개하기 어렵다.

일시적 추론, 원본 없이 생성된 요약, 코드에서 쉽게 재확인할 사실과 일상적인 명령 출력은 기본적으로 기록하지 않는다.

## 불변 조건

- Agent의 추론을 인간이 승인한 결정처럼 저장하지 않는다.
- 관찰, 추론, 미확인 정보와 인간 결정을 구분한다.
- 현재 상태의 authoritative record를 중복 생성하지 않는다.
- Integration과 Migration은 영역별로 선택할 수 있지만 같은 정보의 원본은 하나만 둔다.
- 오래된 사실을 조용히 덮어쓰지 않고 대체 관계를 남긴다.
- 기존 문서와 tracker를 Continuity 전용 파일에 불필요하게 복제하지 않는다.
- 사람이 모든 canonical record를 읽고 수정하거나 폐기할 수 있어야 한다.
- Agent 메모리, 검색 index와 HTML projection을 source of truth로 취급하지 않는다.
- 네트워크나 특정 AI 제공자가 없어도 canonical record를 열람할 수 있어야 한다.
- 인증 정보, 원본 대화 전체와 개인 세션 기록을 기본 수집하지 않는다.
- 기록 간 의미 있는 충돌은 자동 해결하지 않고 출처, 시점과 실행 증거를 인간에게 제시한다.
- Audit은 읽기 전용이며 수정은 별도 인간 승인 후 수행한다.

## 복잡도 예산

초기 Pilot에는 다음을 포함하지 않는다.

- SQLite, vector DB 또는 knowledge graph
- MCP server, background daemon 또는 자동 Git hook
- HTML dashboard
- 다중 Agent 동시 쓰기와 lock protocol
- 전체 대화 자동 수집
- 새로운 범용 task tracker
- 유형마다 분리된 세부 schema와 대규모 validator

기능은 다음 실패가 반복 관찰될 때만 추가한다.

| 관찰된 실패 | 다음에 검토할 최소 기능 |
|---|---|
| 기록을 찾는 시간이 반복적으로 길어짐 | 작은 index 또는 full-text search |
| 참조와 상태 오류가 반복됨 | 해당 오류만 검사하는 validator |
| 여러 Agent가 동시에 같은 record를 수정함 | append-only 기록 또는 좁은 lock 규칙 |
| 사람이 현재 상태를 파악하기 어려움 | 읽기 전용 HTML projection |
| 기존 tracker와 중복 입력이 발생함 | 단방향 adapter 또는 원본 참조 강화 |
| 수백 개 결정의 관계 탐색이 어려움 | SQLite 또는 graph의 비용 검토 |

## 기존 capability와의 관계

`manage-focus-cycle`은 끝이 없는 프로젝트 안에서 지금 집중할 하나의 제한된 목표와 종료 조건을 관리한다. Local Project Continuity는 그 Focus Cycle을 포함한 프로젝트 상태와 학습이 세션·Agent 교체를 견디게 한다.

둘은 결합할 수 있지만 동일한 capability는 아니다. Project Continuity가 전체 roadmap이나 프로젝트 완료율을 대신 관리해서도 안 된다.

## 비목표

- AI에게 완전하거나 무제한인 인간형 기억 제공
- 모든 대화와 tool output의 영구 보존
- 모든 정보를 하나의 `MEMORY.md`에 혼합
- 모든 프로젝트에 동일한 물리 파일 배치 강제
- 처음부터 DB, MCP, 검색 service 또는 UI 배포
- AI가 기억할 가치와 현재의 진실을 단독 결정
- 이 저장소가 소비 프로젝트의 기록을 중앙 수집하거나 동기화

## Pilot 검증 질문

서로 다른 유형의 로컬 프로젝트 두 곳에서 다음을 확인해야 한다.

- 이전 대화를 볼 수 없는 새 Agent가 열린 Work Item을 요약하고 선택된 Session Focus의 완료 조건과 다음 행동을 정확히 설명하는가?
- 다른 Agent 제품이나 모델에서도 같은 Core 의미를 해석하는가?
- 기존 README, ADR, tracker와 중복 source of truth가 생기지 않는가?
- 결정의 승인, 근거, 적용 범위와 대체 관계를 추적할 수 있는가?
- 실패했던 접근이 불필요하게 반복되지 않는가?
- 시작 Briefing이 프로젝트가 커져도 제한된 크기를 유지하는가?
- Profile과 record가 최소 Schema를 통과하면서 사람도 쉽게 수정할 수 있는가?
- 유지 비용이 재설명, 재조사와 중복 작업 감소보다 작은가?

## 향후 결정할 사항

- Project Profile이 Core 의미를 훼손하지 않았음을 판정하는 기준
- Markdown/YAML과 JSON interchange 사이의 정규 변환 규칙
- stale state의 기준과 Audit 주기
- Git이 없는 폴더에서 history와 archive를 유지하는 최소 방법
- 여러 Agent가 같은 구조를 해석하는 상호운용성 평가 scenario

## 참고한 주요 출처

- [Nygard — Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [MADR — Markdown Architectural Decision Records](https://adr.github.io/madr/)
- [Cline Memory Bank](https://github.com/nickbaumann98/cline_docs/blob/main/prompting/custom%20instructions%20library/cline-memory-bank.md)
- [GitHub Spec Kit — Spec Persistence Models](https://github.github.com/spec-kit/concepts/spec-persistence.html)
- [GitHub Spec Kit — Spec of Specs](https://github.github.com/spec-kit/concepts/spec-of-specs.html)
- [Beads — Agent용 로컬 작업 그래프](https://github.com/gastownhall/beads)
- [Beads의 JSON·DB·Git 복잡성에 관한 사용자 피드백](https://github.com/gastownhall/beads/issues/376)
- [Anthropic — Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Anthropic — Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents)
- [LongMemEval](https://arxiv.org/abs/2410.10813)
- [LoCoMo](https://arxiv.org/abs/2402.17753)
- [MemGPT](https://arxiv.org/abs/2310.08560)
- [Karpathy — LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [Basic Memory](https://docs.basicmemory.com/reference/technical-information)
