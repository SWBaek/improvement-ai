# Project Records Bootstrap

## Status

- State: `Promoted`
- Last reviewed: 2026-09-03
- Next trigger: [Candidate #72](https://github.com/SWBaek/improvement-ai/issues/72)의 계약이나 [Establish Project Records Blueprint](../../blueprints/establish-project-records/BLUEPRINT.md)의 Pilot evidence가 최초 가설을 좁히거나 반증할 때 재검토한다.

## 승격 결과

이 Idea는 [Candidate #72](https://github.com/SWBaek/improvement-ai/issues/72)와 [Establish Project Records Blueprint](../../blueprints/establish-project-records/BLUEPRINT.md)로 승격됐다. 아래 내용은 문제를 발견하고 범위를 좁힌 탐색 맥락이며, 현재 계약과 Pilot 상태의 원본은 Blueprint와 tracking issue다.

## 문제와 배경

한 사람이 여러 프로젝트를 오가더라도 앞으로 할 일과 오래 남길 결정의 위치와 형식이 같다면 매번 운영 방식을 다시 학습하거나 Agent에게 설명하는 비용을 줄일 수 있다. 현재 프로젝트들은 GitHub Issues, GitHub Project, 로컬 Markdown, 개인 업무 시스템과 별도 Work Item 구조를 서로 다르게 사용한다. 중요한 결정도 ADR, Decision Log, Issue 본문과 대화에 흩어진다. 일부 프로젝트는 실제 Issue가 있지만 원본 위치를 프로젝트 지침에 선언하지 않고, 다른 프로젝트는 tracker가 없는데도 지속 작업과 일시적 실험을 구분할 기준이 없다.

문제는 모든 프로젝트가 같은 서비스를 사용하지 않는다는 사실 자체가 아니다. 같은 사람이 소유한 신규 프로젝트에서도 다음이 매번 달라지는 점이다.

- 계획 작업과 버그를 어디에 기록하는가
- 제안, 구현 작업과 버그를 어떤 구조로 작성하는가
- 준비, 진행, 검토와 완료를 어떤 상태로 표현하는가
- 상태, label과 board 중 무엇이 원본인가
- 개인의 다음 행동, repository work, 완료 이력과 architecture decision의 경계는 어디인가
- 장기적으로 유효한 결정을 어디에 어떤 최소 형식으로 보존하는가
- Agent가 외부 Issue를 읽거나 변경할 때 어떤 권한이 필요한가

이 차이는 프로젝트 전환 때 사람의 context switching을 늘리고, 새로운 Agent가 잘못된 tracker에 기록하거나 로컬과 원격에 같은 상태를 복제할 가능성을 만든다.

## 현재 관찰

2026-09-03에 Paseo에 등록된 15개 로컬 프로젝트를 읽기 전용으로 조사했다. 비공개 프로젝트의 이름, 경로와 Issue 내용은 이 공개 Idea에 기록하지 않고 재사용 가능한 패턴만 남긴다.

- 실제 운영 방식은 GitHub Issues, `docs/issues/`의 로컬 Markdown, 개인 업무 시스템의 Project action, 별도 project-local Work Item, 명시적 tracker 없음으로 나뉘었다.
- GitHub를 사용하는 프로젝트도 Project field가 상태를 소유하는 경우, status label이 상태를 소유하는 경우와 Issue만 비정형으로 사용하는 경우가 섞여 있었다.
- 두 local-only 도구 프로젝트는 `docs/issues/` 아래에 Issue별 파일과 README index를 두었지만 ID와 상태 어휘가 서로 달랐다. 개별 파일과 index 표가 같은 상태를 중복 소유해 함께 갱신해야 했다.
- 일부 프로젝트는 repository work를 GitHub나 로컬 Work Item에 두면서 개인의 다음 행동을 별도 업무 시스템에도 기록했다. 두 범위가 명시되지 않으면 정당한 개인 reminder와 중복 backlog를 구분하기 어렵다.
- tracker가 없는 짧은 실험 directory도 있었다. 모든 폴더에 Issue system을 강제하는 것보다 `none`을 명시하고 다시 검토할 조건을 두는 편이 작을 수 있다.
- 별도 project-local Continuity 구조는 Work Item, Profile, Handoff, schema, 검증과 Skill을 함께 도입했다. 강한 추적성은 제공했지만 단순한 Issue source 선언보다 상호작용과 유지 비용이 컸다.
- 공개 `Paseo-Plugin` 저장소는 GitHub Issue Forms, 자동 label과 Project 등록, 하나의 Project Status 원본, parent/child와 dependency, PR close 연결을 함께 사용했다. 조사 시점의 23개 Issue가 모두 label과 Project에 연결되어 있었고 22개가 닫혀 있어 현재 개인 프로젝트 중 가장 일관된 GitHub 사례였다. 다만 닫힌 두 Issue의 Project Status가 `In review`에 남아 remote lifecycle도 drift할 수 있음을 보였다.
- 공개 `sdoc-editor` 저장소는 계획 작업을 GitHub Issues, 완료 작업을 Git history, 장기 architecture rationale를 ADR로 분리하고 Issue Form과 AI 작성 지침을 제공했다. 이는 하나의 Issue system이 모든 기록을 소유할 필요가 없다는 근거다.

이 조사는 bootstrap 방식의 효과를 검증한 Pilot이 아니다. 기존 프로젝트의 단면에서 불일치와 선례를 확인한 관찰이다.

## 현재 가설

초기 가설은 **Project Records Bootstrap**을 프로젝트 시작 직후 사람이 명시적으로 한 번 실행하는 개인 전역 Agent Skill로 두는 것이었다. Candidate 승격에서는 전역 Skill 대신 Blueprint 설치 프롬프트 자체를 일회성 bootstrap으로 사용하고, 선택과 승인 뒤 모든 사람과 Agent가 읽을 수 있는 프로젝트 로컬 기록 계약을 생성하는 방향을 택했다. 계약은 앞으로 할 일을 위한 Work Item 원본과 오래 남길 결정을 위한 ADR 원본을 구분하며, 설치 후 지속적인 bootstrap Skill을 요구하지 않는다.

```text
explicit one-time Blueprint installation
  → read-only project inspection
  → Work Item provider and record scope proposal
  → human approval
  → fixed record core + one Work Item provider profile
  → project-local policy, Work Item templates and Agent pointer
  → local and approved remote verification
  → no runtime dependency on the Blueprint or bootstrap Skill
```

이 접근은 기존 프로젝트를 일반화해 다시 쓰는 migration Skill이 아니라 greenfield bootstrap을 우선한다. 이미 Issue나 tracker가 있는 프로젝트에서는 자동 정규화하지 않고 기존 원본과 충돌을 보고한다.

### 일관성의 두 층

모든 provider에서 같은 의미를 사용하되 물리적 표현은 provider의 native surface에 고정 mapping한다.

1. **공통 기록 계약**: Work Item과 ADR의 역할, 원본, 연결, authority와 중복 금지
2. **Work Item provider profile**: GitHub, GitLab, Jira, Local 또는 다른 선택지에서 Issue 의미를 표현하는 정확한 위치와 기능

같은 provider를 선택한 신규 프로젝트는 같은 파일 경로, template, label과 field를 사용한다. 서로 다른 provider도 Agent가 같은 의미와 순서로 탐색할 수 있어야 한다.

### Work Item 공통 의미의 선도 가설

Issue 종류는 아직 확정 계약이 아니지만 첫 Pilot에서는 다음 세 가지를 비교한다.

- `idea`: 구현 승인 전 제안
- `work`: 구현하기로 결정한 하나의 검증 가능한 결과
- `bug`: 재현 가능한 오동작

모든 Issue는 문제 또는 배경, 원하는 결과, 범위, 비목표, 검증 가능한 완료 조건, 의존성과 위험, 관련 근거를 가진다. Bug는 환경, 재현 절차, 기대 동작과 실제 동작을 추가한다.

첫 lifecycle 후보는 다음과 같다.

```text
Inbox → Backlog → Ready → In progress → In review → Done
```

`blocked`와 `needs-triage`는 상태 전이를 보조하는 표식이며 별도 진행 상태로 중복하지 않는다. 진행하지 않는 항목은 이유를 남기고 닫는다. Milestone은 진행 상태가 아니라 release 범위가 실제로 필요할 때만 사용한다.

### 범위별 하나의 원본

프로젝트 전체의 모든 할 일을 한 시스템에 강제로 모으지 않는다. 같은 범위에는 하나의 authoritative source만 허용한다.

```text
repository work       → selected Issue provider
personal next action  → personal work system, when used
completed work        → Git and merged change history
durable decision      → project repository의 docs/adr/
```

개인 reminder는 repository backlog를 대체하거나 같은 Issue의 진행 상태를 복제하지 않는다. 외부 제품에서 발견한 문제를 upstream에 보고하는 경로도 현재 프로젝트의 internal backlog와 구분한다.

Work Item provider와 ADR 사용 여부는 논리적으로 독립적이다. 일반적인 장기 프로젝트는 둘 다 사용할 수 있고, 짧은 실험은 둘 다 만들지 않을 수 있다. Architecture 원칙이나 표준을 보존하는 repository는 Work Item provider를 `none`으로 선언하면서 ADR만 사용할 수도 있다. ADR 규칙은 항상 선언하지만 실제 파일은 중요한 결정이 생겼을 때만 만든다.

| Work Item 원본 | ADR 파일 | 예상 맥락 |
|---|---|---|
| GitHub, GitLab, Jira 또는 Local | 있음 | 일반적인 장기 프로젝트 |
| GitHub, GitLab, Jira 또는 Local | 아직 없음 | 작거나 초기 단계인 프로젝트 |
| `none` | 있음 | Architecture, 표준 또는 결정 기록 repository |
| `none` | 없음 | 일회성 실험 |

### 프로젝트 로컬 진입점과 ADR 규약

모든 profile은 사람과 Agent가 두 기록 체계를 한곳에서 발견하도록 `docs/project-records.md`를 공통 진입점으로 둔다. `AGENTS.md`에는 이 문서를 가리키는 짧은 pointer만 추가한다. 진입점은 Work Item provider, 종류와 lifecycle, 상태 원본, ADR 위치와 생성 기준, Issue-ADR-PR 연결, 외부 mutation authority를 선언한다.

ADR provider를 별도로 선택하지 않는다. ADR은 provider와 무관하게 프로젝트 Git repository의 `docs/adr/` 아래에 Markdown으로 보존한다. 첫 Pilot의 최소 규약 후보는 다음과 같다.

```text
location: docs/adr/
filename: NNNN-kebab-case-title.md
status: Proposed | Accepted | Rejected | Superseded
sections: Context | Decision | Consequences
```

ADR은 이후 작업을 제약하고, 여러 대안 사이의 선택을 설명하며, 되돌리기 어렵거나 미래 작업자가 이유를 다시 물을 가능성이 높은 결정에만 사용한다. 단순한 작업 순서, 일시적 조사와 구현 세부사항은 Work Item에 남긴다. 중요한 결정이 생기기 전에는 빈 directory나 placeholder ADR을 만들지 않는다.

Accepted 또는 Rejected ADR의 역사적 의미는 다시 쓰지 않는다. 결정이 바뀌면 새 ADR을 만들고 이전 ADR을 `Superseded`로 표시한다. 관련 Work Item과 구현 PR이 있으면 상호 link하되, ADR status를 Issue label이나 수동 index에 복제하지 않는다.

### GitHub profile 후보

GitHub를 선택하면 Issue가 내용을, repository별 GitHub Project의 `Status` field가 진행 상태를 소유한다. Type과 area, `blocked`, `needs-triage`만 label로 표현하고 status label을 함께 만들지 않는다.

프로젝트 로컬 결과 후보는 다음과 같다.

```text
AGENTS.md                              concise entry point or pointer
docs/project-records.md               Work Item and ADR policy and binding
.github/ISSUE_TEMPLATE/01-idea.yml
.github/ISSUE_TEMPLATE/02-work.yml
.github/ISSUE_TEMPLATE/03-bug.yml
.github/ISSUE_TEMPLATE/config.yml
```

GitHub Project, label과 remote setting의 생성은 로컬 template 생성 승인과 별개의 외부 mutation이다. Skill은 변경 대상을 먼저 보여 주고 명시적 승인을 받은 뒤 실행하며, 생성 후 원격 상태를 다시 읽어 검증한다. GitHub remote가 있다는 이유만으로 GitHub Issues 사용을 확정하지 않는다.

### Local profile 후보

Local을 선택하면 첫 경로 후보는 `docs/issues/`다. `.agents/`는 Agent Skill과 discovery를 위한 공간으로 남기고 사람과 여러 Agent가 함께 읽는 운영 record와 섞지 않는 가설을 우선한다.

```text
AGENTS.md
docs/project-records.md
docs/issues/README.md
docs/issues/_templates/idea.md
docs/issues/_templates/work.md
docs/issues/_templates/bug.md
docs/issues/ISSUE-0001-short-title.md
```

각 Issue 파일이 상태의 유일한 원본이어야 한다. README의 수동 index 표에 상태를 복제하지 않고 directory scan이나 필요할 때 생성하는 projection으로 목록을 얻는 방식을 비교한다. Local profile이 별도 runtime이나 database를 요구하지 않아야 한다.

GitHub와 Local profile 모두 `docs/adr/` 규약은 같다. 첫 중요한 결정이 생겼을 때만 directory와 첫 ADR을 만들며, Work Item provider 차이가 ADR 경로나 형식을 바꾸지 않는다.

### 다른 provider

GitLab과 Jira는 Work Item 공통 의미를 native Issue type, board, workflow와 field에 mapping할 수 있다. 그러나 현재 개인 프로젝트에서 실사용 evidence가 없으므로 첫 Pilot에서 전용 adapter, schema나 remote automation을 완성하지 않는다. 사람이 선택했을 때 프로젝트와 tool surface를 조사해 mapping proposal을 만드는 경로만 열어 두고, 실제 반복 사용 뒤 고정 profile로 승격할지 판단한다. 어느 provider를 선택해도 ADR은 project-local Git 문서로 유지한다.

`none`도 정식 선택지다. 지속 backlog가 필요 없는 실험 프로젝트라면 tracker를 만들지 않고, 여러 세션에 걸친 미완료 작업이나 반복 누락이 생길 때 다시 bootstrap을 검토할 조건만 기록할 수 있다.

## 기대 효과

- 같은 provider를 쓰는 신규 프로젝트 사이에서 Issue 생성, 탐색과 상태 변경의 muscle memory가 유지된다.
- Agent가 새 프로젝트에 들어와 Issue source와 lifecycle을 다시 질문하거나 추측하는 빈도가 줄어든다.
- GitHub, Local과 이후 provider가 달라도 `idea`, `work`, `bug`와 상태 의미가 유지된다.
- status label, board와 로컬 문서가 같은 진행 상태를 중복 소유하지 않는다.
- 개인 next action과 repository backlog의 역할을 분리한다.
- 앞으로 할 일과 오래 남길 결정을 구분하고 Issue, ADR과 PR 사이의 탐색 경로를 유지한다.
- Work Item provider가 달라도 ADR의 경로와 최소 형식은 같다.
- bootstrap Skill을 일상 workflow의 runtime dependency로 만들지 않는다.
- project-local policy가 사람과 여러 Agent client의 공통 진입점이 된다.

## 비목표

- 이 저장소에 설치형 Skill, template bundle, helper, runtime 또는 프로젝트별 생성물을 커밋하는 것
- 기존 프로젝트의 Issue를 자동 migration하거나 현재 운영 체계를 덮어쓰는 것
- 일상적인 Issue 생성, triage, 구현, review와 close를 bootstrap Skill이 계속 수행하는 것
- 여러 tracker 사이에 Issue나 상태를 양방향 동기화하는 것
- 모든 개인 task, meeting, research note, Decision과 completed history를 하나의 system으로 통합하는 것
- GitHub Project, label, Jira workflow, 인증 또는 외부 계정을 사람 승인 없이 생성·변경하는 것
- GitLab과 Jira의 실사용 근거 없는 adapter를 첫 버전에 완성하는 것
- 짧은 실험 directory에도 무조건 tracker를 생성하는 것
- 모든 기술적 선택에 ADR을 강제하거나 중요한 결정을 자동 판정하는 것
- 일상적인 ADR 작성, review와 acceptance를 bootstrap Skill이 계속 수행하는 것
- ADR을 Wiki, GitHub Discussions, Issue provider 또는 별도 database와 동기화하는 것
- ADR index, generator, validator와 migration 도구를 실제 실패 근거 없이 만드는 것
- 기존 ADR을 자동 이전하거나 번호를 다시 매기는 것
- 프로젝트 거버넌스와 문서 체계 전반을 설계하는 것
- 현재 Idea 단계에서 공통 의미를 formal schema나 고정 Blueprint contract로 확정하는 것

## 위험과 반례

### 일관성이 project fit보다 우선될 위험

작고 일시적인 프로젝트는 Issue system 없이도 충분할 수 있다. 반대로 공개 community 프로젝트와 비공개 개인 프로젝트는 intake, privacy와 권한 요구가 다르다. 공통 core는 유지하되 `none`과 project-specific policy pointer를 허용하지 않으면 표준이 불필요한 운영 노동을 만든다.

### provider 의미가 완전히 같지 않음

GitHub Project Status, GitLab scoped label, Jira workflow와 Markdown frontmatter는 권한, transition과 query 능력이 다르다. 이름만 같고 행동이 다르면 context switching이 줄었다는 착시가 생긴다. 각 mapping의 실제 operation과 failure를 검증해야 한다.

### 생성 시점의 remote 과잉 변경

새 repository라는 이유로 Project, label, field와 automation을 한 번에 만들면 외부 mutation 범위가 커진다. 로컬 정책 생성, remote setup, 인증과 조직 설정을 하나의 포괄 승인으로 묶지 않는다.

### template와 실제 운영의 drift

초기 구조가 같아도 종료된 Issue의 Project Status가 남거나, Issue Form label과 remote label이 달라질 수 있다. bootstrap 성공은 파일 생성만이 아니라 실제 Issue lifecycle 뒤의 일관성으로 판단해야 한다.

### 표준 업데이트가 새 migration 체계를 요구할 위험

개인 표준의 새 버전을 모든 기존 프로젝트에 강제하면 bootstrap이 updater와 framework로 커진다. 첫 Pilot에서는 생성된 프로젝트가 자기 운영 파일을 소유하고 자동 update를 받지 않는다. 반복되는 migration 필요가 확인되기 전에는 updater를 만들지 않는다.

### ADR의 과잉 작성 또는 결정 유실

모든 구현 선택을 ADR로 만들면 짧게 유지하려던 기록 체계가 review 부담과 잡음으로 커진다. 반대로 ADR을 선택 사항이라는 이유로 중요한 결정을 Issue comment나 대화에만 남기면 장기 맥락을 잃는다. 첫 Pilot은 정확한 판정 자동화가 아니라, 짧은 생성 기준만으로 사람이 납득할 만한 경계를 반복해서 적용할 수 있는지 본다.

### 아직 ADR이 없는 프로젝트의 빈 구조

모든 신규 프로젝트에 빈 `docs/adr/`나 사용 선언용 ADR을 만들면 일회성 실험에도 불필요한 파일이 생긴다. 정책에서 경로와 기준만 선언하고 실제 중요한 결정이 생길 때 첫 파일을 만드는 방식이 발견 가능성을 유지하는지 검증한다.

### 개인 취향을 공개 Blueprint invariant로 오인할 위험

정확한 label, 상태와 경로의 통일은 한 사용자의 portfolio에서는 가치가 크지만 다른 팀에는 맞지 않을 수 있다. 개인 Skill Pilot이 성공해도 곧바로 범용 Blueprint의 고정 구현으로 승격하지 않는다. 여러 사용자에게 반복되는 핵심 문제와 adaptation boundary가 확인되어야 한다.

## 검증 질문

- 신규 프로젝트에서 사람이 기억해야 하는 선택을 provider 하나와 최소 project metadata로 줄일 수 있는가?
- 같은 provider의 두 프로젝트가 실제로 같은 경로, template, label과 field를 갖는가?
- GitHub와 Local에서 같은 Issue 종류와 lifecycle 의미가 유지되는가?
- fresh-context Agent가 추가 설명 없이 Issue source, 현재 상태와 허용된 mutation을 찾는가?
- Agent가 local mirror나 status label을 새로 만들어 상태를 중복하지 않는가?
- 개인 next action과 repository work가 같은 backlog로 오인되지 않는가?
- Local Issue file만으로 목록 탐색과 상태 변경이 충분한가, 아니면 deterministic projection이 필요한가?
- Project Status와 closed Issue의 drift를 어떤 최소 검증으로 발견할 수 있는가?
- bootstrap Skill을 사용할 수 없는 Agent도 생성된 프로젝트 로컬 문서만으로 같은 workflow를 따르는가?
- `none`을 선택한 프로젝트에서 Issue system을 만들지 않은 것이 실제 누락을 낳는가?
- fresh-context Agent가 Work Item과 durable decision을 구분하고 각각의 원본을 찾는가?
- 사소한 구현 선택에 ADR을 남발하지 않으면서 중요한 결정은 대화나 Issue 본문에만 묻히지 않는가?
- `none` Work Item provider에서도 ADR을 독립적으로 사용할 수 있는가?
- ADR이 아직 없는 프로젝트에 빈 구조나 지속적인 유지 비용이 생기지 않는가?
- Issue-ADR-PR link가 탐색을 돕되 내용이나 status의 두 번째 원본을 만들지 않는가?
- 고정 표준이 줄인 context switching이 template와 remote 설정 유지 비용보다 큰가?
- 이 capability가 다른 사용자에게도 반복되는가, 아니면 개인 전역 Skill로 충분한가?

## 승격 당시 Pilot 가설

정식 Pilot은 exact Blueprint revision으로 생성된 프로젝트 로컬 결과를 대상으로 하며 tracking issue에 evidence를 제출한다. 기존 프로젝트 migration이 아닌 서로 다른 신규 프로젝트를 우선한다.

1. GitHub 기반 신규 프로젝트 하나에 명시적으로 bootstrap을 실행한다.
2. local-only 신규 프로젝트 하나에 같은 공통 의미와 Local profile을 생성한다.
3. 각 프로젝트에서 `idea`, `work`, `bug` 중 필요한 실제 Issue를 만들고 하나 이상의 Issue를 `Ready → In progress → In review → Done`으로 이동한다.
4. 실제로 중요한 결정이 발생한 프로젝트에서만 ADR 하나를 작성하고, 다른 프로젝트에는 검증만을 위한 ADR이나 빈 directory를 만들지 않는다.
5. 새 context의 Agent에게 Work Item 조회, 새 작업 제안, 중요한 결정의 기록 위치 판단과 완료 확인을 요청한다.
6. source 재질문, 잘못된 위치, 역할 혼동, 필수 정보 누락, 중복 상태, remote drift, ADR 과잉 작성과 사용자 정정 횟수를 기록한다.
7. Blueprint나 bootstrap Skill을 호출하지 않은 후속 세션에서도 프로젝트 로컬 계약만으로 운영되는지 확인한다.
8. 실제 후보가 생기면 `Work Item: none`과 ADR만 사용하는 repository를 후속 반례로 검증한다.

성공 신호는 구조가 생성되었다는 사실이 아니라, 두 프로젝트에서 Agent와 사람이 Work Item과 durable decision의 의미를 재학습하지 않고 구분하며 각 상태 원본이 하나로 유지되는 것이다. GitHub와 Local의 차이가 반복적으로 방해되거나 개인 표준 밖에서 같은 요구가 확인되면 Candidate issue와 Capability Blueprint의 adaptation boundary를 검토한다.

## 관련 출처와 후속 링크

### 이 저장소

- [`Local Project Continuity`](local-project-continuity.md): 기존 tracker integration과 project-local Work Item을 함께 다룬 더 넓은 초기 가설
- [`maintain-project-continuity` Blueprint](../../blueprints/maintain-project-continuity/BLUEPRINT.md): tracker 선택, authority와 중복 금지를 포함했지만 실제 Pilot에서 상호작용 비용이 확인된 계약
- [Matt Pocock ecosystem 비교](../research/bencmark/karpathy-llm-wiki-ecosystem.md#matt-pocock-skills): 고정 Skill 구현과 repository별 setup의 관계를 비교한 기존 조사

### 공개 사례

- [Paseo-Plugin Issue 관리 규칙](https://github.com/SWBaek/Paseo-Plugin/blob/main/.github/ISSUE_MANAGEMENT.md): GitHub Issues, Project field, label, dependency와 PR close를 분리한 현재 개인 표준의 가장 일관된 사례
- [Paseo-Plugin Issue Forms](https://github.com/SWBaek/Paseo-Plugin/tree/main/.github/ISSUE_TEMPLATE): idea, development plan과 bug의 입력 구조 및 자동 Project 연결 사례
- [sdoc-editor Agent guide](https://github.com/SWBaek/sdoc-editor/blob/main/AGENTS.md): planned work, completed history와 durable decision의 원본 분리 사례
- [sdoc-editor AI issue-reporting guide](https://github.com/SWBaek/sdoc-editor/blob/main/.github/AI_ISSUE_REPORTING.md): template 선택, evidence, privacy와 remote mutation 검증 사례
- [Matt Pocock `setup-matt-pocock-skills`](https://github.com/mattpocock/skills/blob/main/skills/engineering/setup-matt-pocock-skills/SKILL.md): repository별 tracker와 문서 위치를 설정하지만 downstream Skill set의 configuration 역할을 하는 비교 사례
- [Michael Nygard, Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions): 작은 text record를 project repository에 보존하고 새 결정으로 이전 결정을 supersede하는 ADR 원형
- [AWS Prescriptive Guidance, Architectural decision record process](https://docs.aws.amazon.com/prescriptive-guidance/latest/architectural-decision-records/adr-process.html): 결정의 context, decision, consequences와 accepted record의 불변성 및 superseding lifecycle에 대한 참고
