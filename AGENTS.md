# Improvement AI Agent Guide

## 저장소 정체성

`improvement-ai`는 AI가 대상 프로젝트에 맞는 Agent Skills와 workflow를 설계하도록 안내하는 **Capability Blueprint 전용 저장소**다. 이 저장소는 설치형 Skill, runtime 구현, CLI, package, framework 또는 프로젝트별 생성물을 배포하지 않는다.

## 핵심 원칙

- **Blueprint가 원본**: 문제, 기대 결과, 불변 조건, 필수 operation, 적응 지점과 acceptance criteria를 canonical source로 관리한다.
- **대상 프로젝트 우선**: Blueprint는 구현 형태와 Skill 수를 고정하지 않고 대상 프로젝트의 지침, 기록과 Agent client에 맞게 생성하도록 안내한다.
- **제안 후 생성**: AI는 프로젝트를 읽기 전용으로 조사하고 생성 구성을 제시하며 인간 승인 전에는 파일을 변경하지 않는다.
- **프로젝트 소유**: 생성된 Skill과 지원 자산은 대상 프로젝트가 소유한다. 이 저장소로 프로젝트별 변형을 가져오거나 자동 동기화하지 않는다.
- **전역 설치 금지**: Blueprint가 생성하는 Skill, Installation Receipt, Profile, schema, mapping과 상태 기록은 반드시 대상 프로젝트 내부에 둔다. 전역 Agent Skill이나 여러 프로젝트가 공유하는 새 상태 경로를 제안·생성하지 않는다. 기존 프로젝트 전용 외부 source의 Integration은 별도 권한 규칙을 따른다.
- **정확한 설치 revision**: Blueprint 버전은 canonical `BLUEPRINT.md` path를 마지막으로 변경한 40자리 Git commit이다. 생성 Skill provenance와 프로젝트 로컬 Installation Receipt가 같은 revision을 기록한다.
- **사람의 권한**: 외부 쓰기, 활성화, 종료와 파괴적 결정의 승인 경계를 Blueprint에 명시한다.
- **실사용 검증**: Blueprint는 서로 다른 두 프로젝트에서 생성·실사용된 뒤에만 Promoted로 승격한다.
- **낮은 운영비**: 실제 실패 근거 없이 schema, generator, validator, CI, Release automation이나 platform matrix를 추가하지 않는다.

## 저장소 범위

포함한다:

- `blueprints/`: canonical Capability Blueprints와 설명용 reference·평가 scenario
- `docs/idea/`: 아직 채택되지 않은 문제, 관찰과 capability 가설을 수집·구체화하는 Idea note
- `docs/`: Idea note 외의 아키텍처, ADR과 GitHub 운영 정책
- `.github/`: Blueprint proposal, label, ownership와 PR 지침
- `scripts/`: label 동기화처럼 저장소 governance에만 필요한 작은 helper

포함하지 않는다:

- `SKILL.md`를 포함한 설치 가능한 Agent Skill
- 실행 가능한 capability script, CLI, package, service, framework나 adapter
- 복사 가능한 완제품 template, runtime asset 또는 formal generation schema
- 특정 프로젝트의 생성 결과, 상태, 비공개 Pilot 자료와 session log
- 인증 정보, cache와 재생성 가능한 runtime 파일

## 기여 작업 규칙

- 모든 기여 작업은 먼저 `CONTRIBUTING.md`에서 유형, 시작 위치, issue 필요 여부, 언어와 검증 규칙을 확인한다.
- 오탈자, 링크, Research와 비규범 Idea는 저위험 직접 PR을 허용한다. 새 Blueprint, Blueprint 계약과 저장소 정책 변경은 issue-first로 진행한다.
- Canonical `BLUEPRINT.md`와 Pilot scenario는 영어로 작성한다. 최상위 영문·국문 README의 사용자 의미가 바뀌면 함께 갱신한다.
- Pilot evidence는 파일로 커밋하지 않고 기존 Blueprint tracking issue에 privacy-safe comment로 제출한다. `docs/github/pilot-evidence.md`의 형식을 따른다.
- Maintainer만 서로 다른 두 프로젝트 evidence를 확인하고 Blueprint를 Promoted로 확정한다.
- AI-assisted contribution의 내용, 출처, license, 민감 정보 제거와 검증 결과는 제출자가 책임진다.

## Blueprint 작성 규칙

- 각 Blueprint directory에는 사람용 설치 landing page인 `README.md`와 AI용 canonical 계약인 `BLUEPRINT.md`를 둔다.
- `blueprints/<name>/README.md`는 해결하는 문제, 적합한 사용 조건, 복사 가능한 설치 프롬프트, 설치 흐름, 최신·재현 가능 revision 사용법과 canonical Blueprint·tracking issue 링크만 간결하게 제공한다.
- 개별 README의 설치 프롬프트는 해당 Blueprint의 정확한 `main` URL을 포함하고 `읽기 전용 조사 → 설치안 제안 → 인간 승인 → 프로젝트 로컬 생성·검증` 경계를 명시한다. 사용자가 URL이나 capability 이름을 조립하게 하지 않는다.
- 개별 README는 Core 정보 모델, invariants, 상태 전이, operation과 acceptance criteria를 복제하지 않고 `BLUEPRINT.md`로 연결한다.
- 사람의 진입점은 `blueprints/<name>/README.md`, AI가 적용할 canonical 진입점은 `blueprints/<name>/BLUEPRINT.md`다. “설치”는 package 복사가 아니라 Blueprint 기반 프로젝트 로컬 capability 생성이라는 뜻임을 README에 설명한다.
- 이름은 소문자 kebab-case로 작성하고 `blueprints/README.md`에 정확히 한 번 등록한다.
- 본문은 문제, required outcomes, invariants, capability operations, project adaptation, instantiation protocol, human authority, non-goals와 acceptance criteria를 포함한다.
- Operation은 필요한 behavior를 정의하며 생성할 Skill의 이름이나 개수를 고정하지 않는다.
- 생성 절차는 `읽기 전용 조사 → 구체적 구성 제안 → 인간 승인 → 프로젝트 로컬 생성 → 대표 동작 확인` 순서를 따른다.
- 설치 제안의 모든 생성 경로가 대상 프로젝트 내부인지 확인한다. 사용자 홈, 전역 Skill directory, 공유 전역 config와 여러 프로젝트가 함께 쓰는 외부 상태 경로는 허용하지 않는다.
- 프로젝트별 상태를 소유하지 않는 별도 무상태 bootstrap capability는 새로운 Idea와 Blueprint로만 검토하며 현재 Blueprint의 전역 설치 예외로 취급하지 않는다.
- 생성 Skill의 YAML frontmatter는 Agent Skills 호환성을 위해 `name`과 trigger 중심 `description`만 사용하도록 지시한다.
- provenance는 frontmatter가 아닌 `SKILL.md` 본문의 HTML comment로 기록하도록 지시한다.
- `main`을 적용할 때 저장소 HEAD를 그대로 기록하지 않는다. 해당 canonical `BLUEPRINT.md`를 마지막으로 변경한 commit을 확인하고 exact-revision URL에서 다시 읽은 뒤 생성하도록 지시한다.
- 대상 프로젝트에는 Blueprint별 Installation Receipt를 정확히 하나 생성하도록 지시한다. 경로는 설치 제안에서 명시하고 `format`, `blueprint`, `repository`, `path`, 40자리 `revision`과 exact `source`를 기록한다.
- 최신 확인은 receipt의 canonical path를 마지막으로 변경한 최신 commit과 설치 revision을 비교한다. 다른 README나 Blueprint만 변경한 저장소 HEAD는 업데이트로 판정하지 않는다.
- 업데이트는 두 exact Blueprint의 semantic comparison, migration proposal과 인간 승인을 거친다. 로컬 검증 성공 후에만 receipt와 모든 생성 Skill provenance를 함께 갱신한다.
- 보조 `references/`는 직접 연결된 설명과 평가 scenario에만 사용한다. executable, generator, schema나 reference implementation을 포함하지 않는다.
- 외부 아이디어는 출처 링크와 사용 목적을 기록하고, 내용을 복사할 경우 license를 확인한다.

## Idea 작성 규칙

- 아직 반복 가능성, 범위 또는 해법이 확인되지 않은 아이디어는 `docs/idea/`에서 관리한다.
- `docs/idea/README.md`를 Idea index와 운영 안내의 진입점으로 유지한다.
- 각 Idea note는 문제, 배경 또는 관찰, 현재 가설, 비목표, 위험, 검증 질문과 관련 출처를 구분해 기록한다.
- Idea note는 채택된 결정, 공개 계약, Candidate issue 또는 Blueprint가 아니며 구현을 약속하지 않는다.
- Idea는 탐색 과정에서 자유롭게 수정할 수 있지만, Blueprint나 저장소 전체 방향을 규범적으로 변경하려면 issue와 필요한 ADR을 별도로 만든다.
- 반복되는 문제와 검증할 가치가 확인되면 GitHub issue를 만들어 Candidate로 승격하고 Idea note와 상호 연결한다.
- Blueprint를 만들거나 Idea를 폐기할 때는 note의 상태와 후속 링크를 갱신해 탐색 결과를 찾을 수 있게 한다.

## Lifecycle

| 단계 | 저장소 산출물 | 진입·종료 조건 |
|---|---|---|
| Idea | `docs/idea/<name>.md` | 문제나 가능성을 탐색 중이며 아직 capability 후보로 확정하지 않음 |
| Candidate | GitHub issue | 반복되는 문제가 식별됨 |
| In Progress | `blueprints/<name>/BLUEPRINT.md`와 tracking issue | 첫 프로젝트 Pilot 시작 |
| Promoted | 같은 Blueprint 경로 | 서로 다른 두 프로젝트에서 생성·실사용 성공 |
| Deprecated | 같은 경로의 폐기 안내와 issue | 대체 Blueprint 또는 폐기 이유 확인 |

Capability 상태와 issue 작업 상태를 혼동하지 않는다. 실제 Pilot evidence는 tracking issue에 기록하고 프로젝트의 비공개 내용은 요약된 재사용 학습만 남긴다.

## GitHub 명령 정책

- GitHub 서비스의 조회나 변경에는 **인증된 GitHub CLI(`gh`)만 사용한다**.
- GitHub API를 `curl`, 임의 HTTP client 또는 비인증 요청으로 직접 호출하지 않는다.
- issue, pull request, label, repository 설정을 다루기 전에 `gh auth status`가 성공하는지 확인한다.
- 로컬 버전 관리에는 `git`을 사용할 수 있다. `git push` 전에 `gh auth status`와 `git remote -v`로 계정과 대상 저장소를 확인한다.
- token을 명령행, 파일, log 또는 commit에 기록하지 않는다. `gh`가 관리하는 인증 정보를 사용한다.
- 파괴적이거나 되돌리기 어려운 GitHub 작업은 정확한 저장소와 대상을 먼저 출력해 확인한다.

## 기본 게시 정책

- 사용자가 이 저장소에서 간단한 수정이나 파일 변경을 요청하면, 요청 범위의 구현과 검증이 끝난 뒤 별도의 승인 질문 없이 항상 commit, push와 pull request merge까지 완료한다.
- 기본 branch에서 작업을 시작한 경우 작업 branch를 만들고 pull request를 통해 병합한다. 원격 기본 branch에 직접 push하지 않는다.
- commit 전 의도한 파일만 stage하고, push 전 `gh auth status`와 `git remote -v`로 인증 계정과 대상 저장소를 확인한다.
- 병합 후 로컬 기본 branch를 원격과 동기화하고 최종 branch, commit과 pull request를 보고한다.
- 관련 없는 사용자 변경, 충돌, 검증 실패, 파괴적 작업 또는 새로운 외부 권한이 필요한 상황은 자동 게시 범위에 포함하지 않는다. 안전하게 분리할 수 없으면 상태와 blocker를 보고하고 필요한 확인을 요청한다.

## 결정과 변경 절차

- 저장소 전체 정체성, lifecycle 또는 공개 Blueprint 계약을 바꾸는 결정은 `docs/decisions/`에 ADR로 남긴다.
- 기존 ADR을 삭제하거나 덮어쓰지 않고 새 ADR에서 supersede 관계를 기록한다.
- 미성숙한 아이디어는 `docs/idea/`에 두고, Candidate로 승격한 뒤의 작업 상태는 issue에서 관리한다. Idea를 speculative Blueprint directory로 만들지 않는다.
- 실제 프로젝트에서 관찰된 반복 문제를 가장 작은 Blueprint 변경으로 반영한다.
- 프로젝트별 구현을 일반 해법처럼 복사하지 않고, 반복 가능한 원칙과 acceptance evidence만 추출한다.
- 관련 링크와 issue form을 확인하고 `git diff --check`를 실행한다. 자동 validator나 CI는 반복 실패와 명확한 ROI가 생길 때만 추가한다.
- GitHub 작업은 인증된 `gh` 정책을 따른다. Blueprint는 path-scoped Git revision으로 소비하며 version catalog, tag, Release, changelog나 자동 update channel을 만들지 않는다.

## 완료 기준

- 저장소와 Blueprint index에서 각 capability의 사람용 설치 안내와 canonical 계약에 바로 접근할 수 있다.
- 개별 설치 안내의 프롬프트를 수정 없이 대상 프로젝트의 AI에게 전달해 읽기 전용 조사와 설치 제안을 시작할 수 있다.
- Blueprint만 읽은 AI가 대상 프로젝트 조사와 생성 제안을 시작할 수 있다.
- required behavior와 project adaptation의 자유도가 구분된다.
- 인간 승인 전 mutation 금지와 외부 권한 경계가 명확하다.
- 생성물의 프로젝트 소유권, 단일 Installation Receipt와 일치하는 exact-revision provenance가 명시된다.
- 모든 생성물 경로가 대상 프로젝트 내부이며 전역 설치나 프로젝트 밖 공유 상태가 없다.
- lifecycle index, tracking issue와 관련 문서가 일치한다.
- 설치형 Skill, runtime 구현, Release 경로나 과거 사용 명령을 현재 기능처럼 노출하지 않는다.
- 비밀 정보와 프로젝트별 runtime 상태가 포함되지 않는다.
