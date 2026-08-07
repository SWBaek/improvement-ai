# Karpathy LLM Wiki 생태계와 Blueprint 전략 Benchmark

- 조사일: 2026-08-07
- 상태: Research note. 채택된 결정이나 Blueprint 계약이 아니다.
- 목적: `improvement-ai`의 동기가 된 Karpathy `llm-wiki.md` 이후의 유사 구현을 비교하고 Blueprint-only 전략의 적합성, 차별점과 위험을 평가한다.

## 조사 질문

1. Karpathy의 Idea File 이후 어떤 delivery form이 등장했는가?
2. 원래의 “개념 문서 → AI의 현지 구현” 방식을 유지한 사례가 있는가?
3. 완성 Skill, framework, CLI, Plugin과 App은 어떤 사용성과 유지비를 선택했는가?
4. `improvement-ai`의 project-owned Blueprint 전략은 어디에서 강하고 무엇을 Pilot로 증명해야 하는가?

## 기준점: Karpathy `llm-wiki.md`

Karpathy의 [`llm-wiki.md`](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)는 완성된 프로그램이 아니라 다음 핵심을 가진 Idea File이다.

- raw sources, LLM-maintained wiki와 schema의 계층
- Ingest, Query, Lint라는 최소 operation
- 원본과 파생 지식의 관계
- LLM이 wiki의 구조화와 bookkeeping을 담당한다는 책임 모델

문서 하나를 다양한 AI에게 제공해도 유사한 운영 구조가 생성된 점은 충분히 강한 의미 계약이 generator 없이 현지 구현을 유도할 수 있다는 가설을 지지한다. `improvement-ai`는 특정 wiki를 구현하는 대신 이 delivery mechanism을 여러 project-scoped capability에 적용한다.

## 생태계의 delivery form

| 유형 | 대표 사례 | 중앙에서 제공하는 것 | 현지 적응 방식 |
|---|---|---|---|
| Idea File | Karpathy `llm-wiki.md` | 개념, schema와 operation | AI가 사용 환경에 맞게 직접 생성 |
| Agent repository | [SamurAIGPT/llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent) | Agent instructions, 고정 workspace와 tools | 저장소를 clone하고 그 안에서 운영 |
| Agent Skill | [Hermes LLM Wiki Skill](https://github.com/NousResearch/hermes-agent/blob/main/skills/research/llm-wiki/SKILL.md), [praneybehl/llm-wiki-plugin](https://github.com/praneybehl/llm-wiki-plugin) | 완성된 `SKILL.md`와 명령 | Agent Skill 경로에 설치 |
| Multi-agent framework | [Ar9av/obsidian-wiki](https://github.com/Ar9av/obsidian-wiki) | CLI와 다수의 Agent Skill | 여러 Agent에 설치하고 중앙 vault에 연결 |
| Desktop application | [nashsu/llm_wiki](https://github.com/nashsu/llm_wiki) | Tauri App, graph, review, MCP | App project와 별도 Agent Skill 사용 |
| Obsidian Plugin | [Karpathy LLM Wiki Plugin](https://community.obsidian.md/plugins/karpathywiki) | Obsidian UI, provider와 wiki runtime | vault 안에서 설정 |
| Compiler, CLI와 MCP | [atomicstrata/llm-wiki-compiler](https://github.com/atomicstrata/llm-wiki-compiler) | compiler, schema, retrieval, lint, eval과 MCP | package 설치와 project config |
| Skill portfolio | [mattpocock/skills](https://github.com/mattpocock/skills), [anthropics/skills](https://github.com/anthropics/skills) | 선택 가능한 완성 Skill | installer 또는 plugin과 repo별 setup |
| Workflow framework | [GitHub Spec Kit](https://github.com/github/spec-kit), [obra/superpowers](https://github.com/obra/superpowers) | 전체 workflow, template와 Agent adapter | CLI·plugin으로 프로젝트에 설치 |

공통적인 진화 방향은 다음과 같다.

```text
Idea File
  → 고정 Skill
  → installer와 Agent adapter
  → CLI / MCP / Plugin / App
  → schema, migration, evaluation과 Release 운영
```

즉시 사용성은 높아지지만 중앙 유지보수 책임도 함께 증가한다.

## 주요 benchmark

### SamurAIGPT `llm-wiki-agent`

`raw/`, `wiki/`, `graph/`와 여러 Agent instruction을 함께 제공한다. Ingest, Query, Lint를 자연어로 실행하고 graph JSON과 HTML을 생성하므로 첫 사용까지의 거리가 짧다.

배울 점:

- 고정된 디렉터리와 명령으로 빠르게 시작한다.
- AI가 Markdown을 직접 관리해 별도 API runtime 의존을 줄인다.
- 시각적 결과와 자연어 trigger를 즉시 제공한다.

차이와 한계:

- 저장소 자체가 workspace이므로 기존 성숙 프로젝트에 얇게 결합하는 모델이 아니다.
- 구조와 operation이 이미 구현되어 AI가 프로젝트별 Skill 경계를 다시 설계하지 않는다.

### Ar9av `obsidian-wiki`

다수의 Markdown Skill과 CLI를 여러 Agent에 설치하고 하나의 개인 vault를 여러 프로젝트에서 사용한다. source manifest, delta ingest, provenance 분류, lint와 graph export를 제공한다.

배울 점:

- URL 하나로 Agent-driven setup을 시작하는 진입 UX가 단순하다.
- Markdown ownership과 Agent independence를 유지한다.
- source change와 추론·모호성 provenance를 명시적으로 다룬다.

전략적 차이:

- 개인 wiki는 본질적으로 cross-project이므로 global Skill과 중앙 vault가 자연스럽다.
- `improvement-ai`의 현재 Blueprint는 project-specific source, authority와 state를 소유하므로 project-local 설치가 적합하다.
- 따라서 전역 설치 금지는 현재 두 Blueprint에는 타당하지만, 미래의 개인 지식 또는 무상태 capability를 같은 저장소에서 다루는 범위는 제한한다.

### Atomic Strata `llm-wiki-compiler`

source hash, incremental compilation, schema, hybrid retrieval, citations, review-before-write, lint, eval, viewer와 MCP를 제공하는 제품화된 구현이다.

배울 점:

- 구조 validation과 semantic quality 검사를 분리한다.
- source hash로 실제 변경만 처리한다.
- 위험한 write를 candidate review로 보류한다.
- citation, provenance와 regression을 측정한다.

전략적 차이:

- provider, credentials, Node runtime, package, MCP, schema migration과 Releases를 유지해야 한다.
- `improvement-ai`는 실제 실패가 증명되기 전에는 이 runtime 비용을 중앙에서 부담하지 않는다.

### nashsu `llm_wiki`

원래 gist를 abstract design pattern으로, 자신의 구현을 desktop application으로 구분한다. App, graph, review, local MCP server와 별도 Agent Skill을 제공한다.

이 사례는 Blueprint와 제품의 교환 관계를 잘 보여준다. App은 즉시 사용성과 일관된 결과를 제공하지만 UI, backend, packaging, OS, provider와 data migration을 중앙에서 책임진다.

### Matt Pocock `skills`

작고 조합 가능한 완성 Skill을 제공하고 repo별 setup Skill이 issue tracker, labels와 문서 위치를 질문한다. 프로젝트가 복사본을 소유하는 방식과 자동 업데이트되는 managed plugin 방식을 모두 제공한다.

`improvement-ai`와 공유하는 흐름:

```text
공통 workflow
  → 프로젝트별 조사와 setup
  → tracker·경로·규칙 적응
```

차이는 Matt Pocock의 저장소가 공통 Skill 구현을 배포하고, `improvement-ai`는 AI가 Skill 자체를 프로젝트별로 생성하도록 의미 계약을 배포한다는 점이다.

### GitHub Spec Kit

여러 Agent에 Spec → Plan → Tasks → Implement workflow를 설치하고 project constitution과 artifact를 생성한다. 명확한 bootstrap, Agent integration, extension과 update mechanism을 제공한다.

배울 점:

- canonical intent와 생성 artifact의 관계를 명시한다.
- 프로젝트 초기화와 재적용 경로가 분명하다.
- Agent별 차이는 thin integration으로 분리한다.

차이와 비용:

- CLI, templates, Releases와 다수 Agent integration을 중앙에서 유지한다.
- `improvement-ai`는 target-project AI의 현지 생성으로 adapter 유지비를 줄이는 대신 생성 일관성을 Pilot에서 증명해야 한다.

### Anthropic Skills와 Superpowers

Anthropic Skills는 self-contained `SKILL.md`와 supporting resources를 installable unit으로 제공한다. Superpowers는 composable Skill과 bootstrap instructions로 전체 개발 방법론을 여러 Agent에 전달하며 Skill 본문과 harness adapter를 분리한다.

배울 점은 trigger 명확성, progressive disclosure, composability와 harness-independent instruction이다. 그러나 두 방식 모두 실행할 Skill 구현을 중앙에서 유지한다는 점에서 Blueprint-only 모델과 다르다.

## `improvement-ai` 전략 평가

### 강점

#### 성숙한 프로젝트의 기존 체계 적응

고정 Skill이나 template은 기존 Issue, ADR, README와 연구 기록을 복제할 수 있다. Blueprint의 읽기 전용 조사와 Integration/Migration 제안은 기존 source of truth를 유지하면서 부족한 capability만 생성할 수 있다.

#### 낮은 중앙 유지비

package, runtime, provider adapter, MCP, UI와 migration을 upstream에서 운영하지 않는다. 생성 결과와 프로젝트별 adaptation은 대상 프로젝트가 소유한다.

#### 권한과 source-of-truth 보호

Decision 승인, Work Item 완료, 외부 쓰기와 충돌 해결을 인간 권한으로 분리한다. 개인 wiki 자동 관리보다 software·research project의 governance에 적합하다.

#### exact provenance

Canonical Blueprint path의 마지막 변경 commit과 Installation Receipt로 실제 생성 계약을 재현한다. 다른 문서나 Blueprint 변경을 잘못된 update로 판정하지 않는다.

### 약점과 위험

#### 즉시 사용성

완제품보다 `프롬프트 복사 → 조사 → 설치안 검토 → 승인 → 생성 → 검증` 과정이 길다. Capability별 설치 README가 이 비용을 줄이지만 one-click Plugin과 같아질 수는 없다.

#### 생성 일관성 미검증

Karpathy의 원형은 세 계층과 세 operation으로 좁다. 현재 Blueprint는 기존 tracker, 권한, 여러 Agent와 migration까지 다루므로 자유도가 더 크다. 다른 AI가 같은 semantic Core를 가진 결과를 만드는지 실사용 evidence가 필요하다.

#### Blueprint 비대화

모든 edge case를 canonical 문서에 추가하면 핵심 operation을 흐릴 수 있다. 서로 다른 Pilot에서 실제로 반복된 실패를 방지하지 않는 설명은 reference나 research에 남기고 Blueprint invariant로 승격하지 않아야 한다.

#### portfolio 범위 제한

현재 전역 설치 금지는 project-owned state를 가진 Blueprint에 적합하다. 개인 cross-project knowledge vault나 무상태 bootstrap처럼 전역 배치가 자연스러운 capability는 별도 범위나 저장소가 필요할 수 있다.

## 비교 결론

현재 전략을 제품·Skill 배포로 되돌릴 이유는 확인되지 않았다. 시장의 대부분은 즉시 사용성을 위해 완성 구현으로 이동했고, 그 결과 adapter, runtime, migration과 Release 책임을 떠안았다. `improvement-ai`는 다음 위치를 선택한다.

| 비교 축 | 일반적인 유사 프로젝트 | `improvement-ai` |
|---|---|---|
| 배포 단위 | Skill, CLI, Plugin 또는 App | 생성 계약인 Blueprint |
| 현지 적응 주체 | setup script와 미리 구현한 adapter | 대상 프로젝트의 AI |
| 생성물 소유자 | upstream package 또는 설치 bundle | 대상 프로젝트 |
| 기존 기록 통합 | 제공된 adapter 범위 | 읽기 전용 조사 후 mapping |
| update | package 또는 Plugin upgrade | exact Blueprint semantic comparison과 migration proposal |
| 중앙 유지비 | 기능과 지원 범위에 따라 증가 | 의도적으로 낮음 |
| 즉시 사용성과 초기 일관성 | 높음 | 상대적으로 낮고 Pilot 필요 |

차별점은 “더 적은 기능” 자체가 아니라 **강한 의미·권한 계약을 제공하면서 구현과 상태를 프로젝트가 소유하게 하는 것**이다.

## Pilot benchmark

첫 두 Pilot은 다음 질문으로 평가한다.

### Karpathy test

Blueprint URL 하나와 설치 프롬프트만 받은 AI가 추가 설계 설명 없이 올바른 프로젝트 조사와 설치안을 제시하는가?

### Matt Pocock test

설치 과정이 짧고, 프로젝트별로 실제 선택이 필요한 source, authority와 path만 질문하는가?

### Spec Kit test

Canonical intent, generated artifact, source of truth와 update 경로가 명확하고 다른 Agent가 재개할 수 있는가?

### Atomic compiler test

중앙 runtime 없이도 provenance, structural validation, semantic Audit, conflict reporting과 review boundary가 충분한가?

### 성공 신호

- 서로 다른 Agent가 같은 Core 의미와 권한 경계를 가진 로컬 capability를 생성한다.
- 기존 프로젝트 기록과 중복 source of truth를 만들지 않는다.
- Installation Receipt만으로 생성 계약과 최신 여부를 복구한다.
- 사용자가 긴 교정 없이 설치안을 승인하거나 소수 항목만 수정한다.
- 유지 비용이 재설명과 재조사 비용보다 작다.

### 실패 시 다음 조치

- 구조가 지나치게 다르면 최소 project-local template 또는 schema contract를 검토한다.
- 설치 질문이 반복되면 README prompt와 proposal contract를 좁힌다.
- 같은 deterministic 오류가 반복되면 해당 검사만 수행하는 작은 helper를 검토한다.
- runtime, CLI, MCP와 중앙 package는 파일 기반 접근 실패가 반복될 때만 후보로 올린다.

## 주요 출처

- [Andrej Karpathy — llm-wiki.md](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [SamurAIGPT — llm-wiki-agent](https://github.com/SamurAIGPT/llm-wiki-agent)
- [Ar9av — obsidian-wiki](https://github.com/Ar9av/obsidian-wiki)
- [Atomic Strata — llm-wiki-compiler](https://github.com/atomicstrata/llm-wiki-compiler)
- [nashsu — llm_wiki](https://github.com/nashsu/llm_wiki)
- [Karpathy LLM Wiki Obsidian Plugin](https://community.obsidian.md/plugins/karpathywiki)
- [Nous Research Hermes — LLM Wiki Skill](https://github.com/NousResearch/hermes-agent/blob/main/skills/research/llm-wiki/SKILL.md)
- [praneybehl — llm-wiki-plugin](https://github.com/praneybehl/llm-wiki-plugin)
- [Matt Pocock — skills](https://github.com/mattpocock/skills)
- [Anthropic — skills](https://github.com/anthropics/skills)
- [GitHub — Spec Kit](https://github.com/github/spec-kit)
- [obra — Superpowers](https://github.com/obra/superpowers)
