# Improvement AI Agent Guide

## 저장소 정체성

`improvement-ai`는 AI가 대상 프로젝트에 맞는 Agent Skills와 workflow를 설계하도록 안내하는 **Capability Blueprint 전용 저장소**다. 이 저장소는 설치형 Skill, runtime 구현, CLI, package, framework 또는 프로젝트별 생성물을 배포하지 않는다.

## 핵심 원칙

- **Blueprint가 원본**: 문제, 기대 결과, 불변 조건, 필수 operation, 적응 지점과 acceptance criteria를 canonical source로 관리한다.
- **대상 프로젝트 우선**: Blueprint는 구현 형태와 Skill 수를 고정하지 않고 대상 프로젝트의 지침, 기록과 Agent client에 맞게 생성하도록 안내한다.
- **제안 후 생성**: AI는 프로젝트를 읽기 전용으로 조사하고 생성 구성을 제시하며 인간 승인 전에는 파일을 변경하지 않는다.
- **프로젝트 소유**: 생성된 Skill과 지원 자산은 대상 프로젝트가 소유한다. 이 저장소로 프로젝트별 변형을 가져오거나 자동 동기화하지 않는다.
- **정확한 출처**: 생성 Skill은 Blueprint path와 40자리 Git commit을 본문 provenance comment로 기록한다.
- **사람의 권한**: 외부 쓰기, 활성화, 종료와 파괴적 결정의 승인 경계를 Blueprint에 명시한다.
- **실사용 검증**: Blueprint는 서로 다른 두 프로젝트에서 생성·실사용된 뒤에만 Promoted로 승격한다.
- **낮은 운영비**: 실제 실패 근거 없이 schema, generator, validator, CI, Release automation이나 platform matrix를 추가하지 않는다.

## 저장소 범위

포함한다:

- `blueprints/`: canonical Capability Blueprints와 설명용 reference·평가 scenario
- `docs/`: 아키텍처, ADR과 GitHub 운영 정책
- `.github/`: Blueprint proposal, label, ownership와 PR 지침
- `scripts/`: label 동기화처럼 저장소 governance에만 필요한 작은 helper

포함하지 않는다:

- `SKILL.md`를 포함한 설치 가능한 Agent Skill
- 실행 가능한 capability script, CLI, package, service, framework나 adapter
- 복사 가능한 완제품 template, runtime asset 또는 formal generation schema
- 특정 프로젝트의 생성 결과, 상태, 비공개 Pilot 자료와 session log
- 인증 정보, cache와 재생성 가능한 runtime 파일

## Blueprint 작성 규칙

- 각 Blueprint의 진입점은 `blueprints/<name>/BLUEPRINT.md`다.
- 이름은 소문자 kebab-case로 작성하고 `blueprints/README.md`에 정확히 한 번 등록한다.
- 본문은 문제, required outcomes, invariants, capability operations, project adaptation, instantiation protocol, human authority, non-goals와 acceptance criteria를 포함한다.
- Operation은 필요한 behavior를 정의하며 생성할 Skill의 이름이나 개수를 고정하지 않는다.
- 생성 절차는 `읽기 전용 조사 → 구체적 구성 제안 → 인간 승인 → 프로젝트 로컬 생성 → 대표 동작 확인` 순서를 따른다.
- 생성 Skill의 YAML frontmatter는 Agent Skills 호환성을 위해 `name`과 trigger 중심 `description`만 사용하도록 지시한다.
- provenance는 frontmatter가 아닌 `SKILL.md` 본문의 HTML comment로 기록하도록 지시한다.
- 보조 `references/`는 직접 연결된 설명과 평가 scenario에만 사용한다. executable, generator, schema나 reference implementation을 포함하지 않는다.
- 외부 아이디어는 출처 링크와 사용 목적을 기록하고, 내용을 복사할 경우 license를 확인한다.

## Lifecycle

| 단계 | 저장소 산출물 | 진입·종료 조건 |
|---|---|---|
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

## 결정과 변경 절차

- 저장소 전체 정체성, lifecycle 또는 공개 Blueprint 계약을 바꾸는 결정은 `docs/decisions/`에 ADR로 남긴다.
- 기존 ADR을 삭제하거나 덮어쓰지 않고 새 ADR에서 supersede 관계를 기록한다.
- Candidate는 issue에만 두고 speculative directory를 만들지 않는다.
- 실제 프로젝트에서 관찰된 반복 문제를 가장 작은 Blueprint 변경으로 반영한다.
- 프로젝트별 구현을 일반 해법처럼 복사하지 않고, 반복 가능한 원칙과 acceptance evidence만 추출한다.
- 관련 링크와 issue form을 확인하고 `git diff --check`를 실행한다. 자동 validator나 CI는 반복 실패와 명확한 ROI가 생길 때만 추가한다.
- GitHub 작업은 인증된 `gh` 정책을 따른다. Blueprint는 Git revision으로 소비하며 version catalog, tag나 Release를 만들지 않는다.

## 완료 기준

- Blueprint만 읽은 AI가 대상 프로젝트 조사와 생성 제안을 시작할 수 있다.
- required behavior와 project adaptation의 자유도가 구분된다.
- 인간 승인 전 mutation 금지와 외부 권한 경계가 명확하다.
- 생성물의 프로젝트 소유권과 exact-revision provenance가 명시된다.
- lifecycle index, tracking issue와 관련 문서가 일치한다.
- 설치형 Skill, runtime 구현, Release 경로나 과거 사용 명령을 현재 기능처럼 노출하지 않는다.
- 비밀 정보와 프로젝트별 runtime 상태가 포함되지 않는다.
