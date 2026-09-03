# Establish Project Records

새 프로젝트의 Work Item 원본과 ADR 규약을 한 번 설정하고, 이후 사람과 Agent가 같은 프로젝트 로컬 기록 체계를 사용하도록 한다.

이 README는 사람을 위한 설치 안내다. 규범적 계약은 [BLUEPRINT.md](BLUEPRINT.md)이며, 설치 프롬프트 자체가 일회성 bootstrap이다. 설치 후에는 이 Blueprint나 별도의 bootstrap runtime 없이 대상 프로젝트의 `docs/project-records.md`, Agent instruction과 provider-native surface만으로 운영한다.

## 이런 경우에 사용한다

- 새 repository마다 Issue 위치, 종류, 상태와 label을 다시 정하는 비용을 줄이고 싶다.
- GitHub, GitLab, Jira 또는 Local을 사용하더라도 Work Item의 공통 의미를 유지하고 싶다.
- 중요한 architecture decision은 provider와 무관하게 프로젝트 Git repository의 ADR로 남기고 싶다.
- Agent가 Issue, board, local document와 ADR 중 어느 원본을 사용해야 하는지 추측하지 않게 하고 싶다.

이미 운영 중인 tracker나 ADR을 자동 migration하려는 경우에는 사용하지 않는다. 기존 체계와 충돌하면 설치 AI가 변경하지 않고 보존, 통합 또는 미설치 안을 제시해야 한다.

## 설치

아래 프롬프트를 초기화할 대상 프로젝트에서 작업 중인 AI에게 그대로 전달한다.

```text
현재 프로젝트에 다음 Capability Blueprint를 설치하세요.

먼저 Blueprint와 현재 프로젝트를 읽기 전용으로 조사하세요.
앞으로 할 repository work의 원본과 중요한 architecture decision의 기록 규약을
한 번 설정하고, 이후 이 Blueprint나 bootstrap runtime 없이 운영할 수 있는
프로젝트 로컬 설치안을 제안하세요.

설치안에는 다음을 포함하세요.

- 기존 Agent instruction, tracker, Issue form, board, label, local Issue, ADR과 Decision Log 조사 결과
- GitHub, GitLab, Jira, Local 또는 none 중 권장 Work Item provider와 근거
- idea, work, bug 종류 및 Inbox, Backlog, Ready, In progress, In review, Done lifecycle의 provider-native mapping
- content, progress, modifier, closure, dependency와 release scope 각각의 authoritative source
- docs/project-records.md와 이를 가리키는 최소 Agent instruction
- docs/adr/의 생성 기준, NNNN-kebab-case-title.md 이름, Proposed, Accepted, Rejected, Superseded 상태와 Context, Decision, Consequences 구성
- 생성하거나 변경할 모든 프로젝트 로컬 파일
- Project, board, label, field, workflow와 setting 등 별도 승인이 필요한 모든 외부 변경
- 지속적인 프로젝트 로컬 Skill이 정말 필요한지와 그 근거. 지침과 native surface로 충분하면 Skill을 만들지 마세요.
- Blueprint Installation Receipt의 프로젝트 로컬 경로
- 로컬 및 승인된 원격 상태의 검증 방법과 충돌 시 중단 조건

같은 진행 상태를 Project field, status label, local document와 수동 index에 중복 관리하지 마세요.
repository work, personal next action, completed Git history와 durable decision의 원본을 구분하세요.
중요한 실제 결정이 생기기 전에는 docs/adr/ directory나 placeholder ADR을 만들지 마세요.
예시 Work Item이나 가짜 lifecycle activity를 설치 검증용으로 만들지 마세요.
기존 기록 체계를 자동 migration, rename, renumber, normalize 또는 overwrite하지 마세요.

모든 생성 파일과 상태는 대상 프로젝트 내부에만 두세요.
사용자 홈, 전역 Agent Skill directory 또는 프로젝트 밖 공유 경로를 제안하거나 사용하지 마세요.
내가 project-local 설치안을 승인하기 전에는 파일을 만들거나 수정하지 마세요.
Work Item provider 선택은 인증, 활성화 또는 외부 쓰기 승인이 아닙니다.
원격 변경은 대상과 내용을 다시 보여 주고 project-local 변경과 별도로 승인받으세요.

설치 전 canonical BLUEPRINT.md를 마지막으로 변경한 40자리 commit을 확인하고,
그 exact-revision URL에서 Blueprint를 다시 읽으세요.
생성 결과에는 해당 revision과 exact source를 담은 Installation Receipt를 정확히 하나 남기세요.
생성 Skill이 실제로 필요하다면 provenance를 Receipt와 일치시키되,
이 일회성 bootstrap을 감싸기 위해 Skill을 만들지 마세요.

Blueprint:
https://github.com/SWBaek/improvement-ai/blob/main/blueprints/establish-project-records/BLUEPRINT.md
```

## 설치 흐름

1. AI가 Blueprint와 대상 프로젝트를 읽기 전용으로 조사한다.
2. AI가 Work Item provider, 공통 의미의 native mapping, ADR 규약, 생성 파일과 외부 변경을 제안한다.
3. 사람이 provider와 project-local 설치안을 승인한다.
4. AI가 승인된 로컬 파일만 생성하고 검증한다.
5. 외부 설정이 필요하면 AI가 정확한 변경을 다시 제시하고 별도 승인 뒤 적용·재검증한다.

이 설치는 신규 프로젝트를 우선한다. 기존 기록 체계가 있으면 자동으로 맞추지 않고 충돌과 선택지를 보고한다.

프롬프트의 `main` URL은 최신 설계를 찾는 진입점이다. 설치 AI는 저장소 HEAD가 아니라 canonical `BLUEPRINT.md`를 마지막으로 변경한 commit을 exact installation revision으로 사용한다. 이후 업데이트 확인도 그 path revision만 비교한다.

## 설치 후 기대 결과

모든 provider에서 공통으로 기대하는 진입점은 다음과 같다.

```text
AGENTS.md 또는 프로젝트의 기존 Agent instruction
docs/project-records.md
.agents/blueprints/establish-project-records.yaml
```

GitHub는 Issue Forms와 승인된 GitHub Project·label 구성을, Local은 `docs/issues/`와 Issue별 Markdown 파일을 사용할 수 있다. `docs/adr/`는 실제 중요한 결정이 처음 생길 때만 생성한다.

## 계약과 상태

- Canonical contract: [BLUEPRINT.md](BLUEPRINT.md)
- Pilot scenarios: [references/pilot-scenarios.md](references/pilot-scenarios.md)
- Status: In Progress
- Tracking: [issue #72](https://github.com/SWBaek/improvement-ai/issues/72)
