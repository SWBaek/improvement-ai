# Improvement AI Agent Guide

## 저장소 정체성

`improvement-ai`는 여러 프로젝트에서 재사용할 AI 협업 capability를 발견하고, 실제 작업에서 검증하고, 배포 가능한 형태로 발전시키는 개인 capability repository다. 하나의 애플리케이션이나 서비스가 저장소 전체의 목적이 되지 않는다.

## 목표와 원칙

- **Skill-first**: 새로운 capability는 가능한 한 작은 Agent Skill로 시작한다.
- **작고 조합 가능하게**: 하나의 거대한 workflow보다 책임과 trigger가 분명한 capability를 선호한다.
- **실사용 우선**: 추측한 범용성보다 실제 프로젝트에서 확인된 불편과 효과를 근거로 발전시킨다.
- **점진적 승격**: 반복성이 증명될 때만 tool, package, framework 또는 독립 서비스로 확장한다.
- **하나의 원본**: 공통 capability는 이 저장소에서 작성하고 agent별 파일은 가능한 한 생성하거나 얇게 연결한다.
- **도구 중립성**: 공통 지식과 workflow는 Codex, Claude Code 등 특정 agent의 인터페이스와 분리한다.
- **사람 중심 표현**: Markdown을 고정하지 않고 표, 도형, HTML 등 사람이 이해하기 좋은 표현을 선택한다.
- **비례하는 검증**: 실제 Skill 동작을 보호하는 작은 테스트만 유지하고 실패 근거 없이 platform matrix나 meta-validation을 추가하지 않는다.

## Capability lifecycle

| 단계 | 저장소 상태 | 진입 조건 |
|---|---|---|
| Candidate | GitHub issue와 짧은 설계 기록만 존재 | 반복되는 실제 문제가 식별됨 |
| In Progress | `skills/<name>/`과 tracking issue 존재 | 한 프로젝트에서 pilot을 시작함 |
| Promoted | 동일 경로의 검증된 Skill | 여러 사용에서 trigger와 효과가 확인됨 |
| Deprecated | 동일 경로에 대체 경로를 명시 | 더 나은 capability로 대체됐거나 유효하지 않음 |

Candidate 단계에서는 speculative 디렉터리, schema나 package를 만들지 않는다. 성숙도가 바뀌어도 Skill 경로는 이동하지 않으며 `skills/README.md`와 tracking issue의 상태만 갱신한다.

## 저장소 범위

포함한다:

- `skills/`: 여러 프로젝트에서 재사용할 Agent Skills
- `tools/`: Skill을 지원하는 독립 실행 자동화와 개발 도구
- `packages/`: 설치·배포 가능한 CLI와 package
- `frameworks/`: 둘 이상의 capability가 공유하는 검증된 계약
- `configs/`: 공통 설정과 agent별 adapter
- `templates/`: 새 capability를 시작하기 위한 최소 template
- `external/`: 외부 capability의 출처, 버전과 라이선스 metadata
- `scripts/`, `tests/`: 저장소 유지·검증 자동화
- `docs/`: 아키텍처, 운영 정책과 의사결정 기록

포함하지 않는다:

- 특정 프로젝트에만 유효한 구현, 상태와 생성 결과
- 비밀 정보, 세션 로그, 캐시와 재생성 가능한 runtime 파일
- 사용 사례 없이 먼저 만든 범용 schema와 추상화
- 독립 제품으로 운영돼야 하는 전체 서비스 코드

## GitHub 명령 정책

- GitHub 서비스의 조회나 변경에는 **인증된 GitHub CLI(`gh`)만 사용한다**.
- GitHub API를 `curl`, 임의 HTTP client 또는 비인증 요청으로 직접 호출하지 않는다.
- issue, pull request, label, release, workflow, repository 설정을 다루기 전에 `gh auth status`가 성공하는지 확인한다.
- 로컬 버전 관리에는 `git`을 사용할 수 있다. `git push` 전에 `gh auth status`와 `git remote -v`로 인증 계정과 대상 저장소를 확인한다.
- token을 명령행, 파일, 로그 또는 commit에 기록하지 않는다. `gh`가 관리하는 인증 정보를 사용한다.
- 파괴적이거나 되돌리기 어려운 GitHub 작업은 정확한 저장소와 대상을 먼저 출력해 확인한다.

## 작성 규칙

### Skills

- 각 Skill은 flat 경로 `skills/<skill-name>/SKILL.md`를 진입점으로 사용한다.
- 이름은 소문자 kebab-case로 작성하고 frontmatter의 `name`과 디렉터리 이름을 일치시킨다.
- `description`은 실제 trigger와 non-trigger를 구분할 수 있을 만큼 구체적으로 작성한다.
- 큰 참고자료, 실행 코드와 정적 자산은 각각 `references/`, `scripts/`, `assets/`로 분리한다.
- 특정 agent 전용 동작은 명시하고 공통 본문은 도구 중립적으로 유지한다.
- 모든 Skill은 `skills/README.md` index에 정확히 한 번 등록하고 상태와 tracking issue를 기록한다.

### Tools와 packages

- 같은 변환, 검증 또는 rendering을 결정적으로 반복해야 할 때 companion script나 tool을 추가한다.
- 여러 Skill이나 프로젝트가 설치 가능한 실행 기능을 공유할 때만 package 또는 CLI를 추가한다.
- 사람이 읽는 출력과 자동화용 구조화 출력의 경계를 명확히 한다.
- 변경 작업에는 가능한 경우 `--dry-run` 또는 이에 준하는 읽기 전용 확인 경로를 제공한다.
- 지원하는 Windows와 Unix 환경을 문서화하고 해당 환경에서 검증한다.

### Frameworks

- Framework는 둘 이상의 capability가 동일한 versioned contract를 실제로 공유할 때만 만든다.
- 각 Framework는 `frameworks/<framework-name>/README.md`를 진입점으로 사용한다.
- Framework는 특정 Skill, agent나 소비 도구에 의존하지 않는 canonical source로 유지한다.
- Skill, tool과 adapter는 Framework를 소비할 수 있지만 Framework는 이들을 참조하지 않는다.
- 공개한 규격과 schema는 version을 명시하며 배포된 의미를 호환성 없이 변경하지 않는다.

### 독립 서비스

- 독립 실행 환경, 배포, 인증, 원격 동기화 또는 자체 release lifecycle이 필요하면 별도 저장소로 분리한다.
- 이 저장소에는 분리된 서비스를 호출하거나 설치하는 Skill과 adapter만 남긴다.

### 외부 자산과 결정

- 외부 Skill이나 도구를 그대로 복사하지 않고 `external/catalog.yaml`에 출처, version, license와 사용 목적을 기록한다.
- 고정 재현이 필요하면 commit 또는 release tag를 기록한다.
- license가 불명확한 자산은 포함하지 않는다.
- 둘 이상의 최상위 영역에 영향을 주는 결정은 `docs/decisions/`에, Framework 내부 결정은 해당 Framework의 `decisions/`에 기록한다.
- 기존 ADR을 지우거나 의미를 덮어쓰지 않고 새 ADR에서 대체 관계를 기록한다.

## 변경 절차

1. 관련 문서와 기존 구현을 먼저 확인한다.
2. 실제 사용 근거와 현재 lifecycle 단계를 확인한다.
3. 가장 작은 재사용 가능한 단위로 구현한다.
4. 동작 계약이 바뀌면 관련 문서와 직접적인 capability 테스트만 갱신한다.
5. 정식 snapshot을 배포하라는 명시적 요청이 있을 때만 `skills/catalog.json`의 version을 올린다.
6. 관련 테스트가 있으면 해당 테스트만 실행한다. 저장소 전체 build, OS matrix와 설치 smoke test를 기본 완료 조건으로 요구하지 않는다.
7. commit 전에 diff에서 비밀 정보, 생성 파일과 불필요한 범위가 없는지 확인한다.
8. GitHub 작업은 인증된 `gh` 정책을 따른다. Catalog version이 바뀐 경우에만 최소 workflow가 인증된 `gh`로 tag와 Release를 생성한다.

## 완료 기준

- 요청된 동작과 문서가 일치한다.
- Capability의 trigger, non-trigger, 기대 결과와 검증 방법이 명확하다.
- 상태와 tracking 정보가 `skills/README.md` 또는 GitHub issue에 반영된다.
- 변경한 capability에 직접 관련된 테스트가 있으면 통과한다.
- 새 경로와 명령이 README 또는 관련 문서에서 발견 가능하다.
- 외부 의존성과 license가 기록되어 있다.
- 명시적으로 Release하는 변경에는 catalog version이 있다.
- 비밀 정보와 개인 runtime 상태가 commit에 포함되지 않는다.
