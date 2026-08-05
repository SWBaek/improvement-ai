# Improvement AI Agent Guide

## 프로젝트 목표

이 저장소는 여러 프로젝트에서 반복해서 사용할 개인 AI 역량의 원본 저장소다. AI와 함께 일하며 발견한 개선 사항을 일회성 대화로 남기지 않고, 재사용 가능한 skill, CLI, 자동화 도구, 설정과 운영 규칙으로 축적한다.

## 핵심 컨셉

- **하나의 원본**: 공통 역량은 이 저장소에서 작성하고 각 AI 도구용 파일은 가능한 한 생성하거나 얇게 연결한다.
- **전역 재사용**: 특정 프로젝트에 종속되지 않는 skill과 도구를 우선 관리한다.
- **표준 우선**: skill은 Agent Skills의 `SKILL.md` 관례를 따르고 기존 설치 생태계를 먼저 활용한다.
- **점진적 확장**: 초기에는 단순한 디렉터리와 검증으로 시작하고, 실제 필요가 확인된 뒤 CLI, pack, registry를 추가한다.
- **검증 가능한 개선**: 새 역량에는 사용 조건, 기대 결과와 확인 방법을 함께 둔다.
- **안전한 배포**: 인증 정보와 로컬 런타임 상태는 저장하지 않으며 외부에서 가져온 자산의 출처와 라이선스를 기록한다.

## 저장소 범위

포함한다:

- `skills/`: 여러 프로젝트에서 재사용할 Agent Skills
- `frameworks/`: 여러 skill과 도구가 공유하는 규약, 스키마, 템플릿과 확장 체계
- `tools/`: 독립 실행 자동화 및 개발 도구
- `packages/`: 배포 가능한 CLI와 npm 패키지
- `configs/`: 공통 설정과 에이전트별 adapter
- `external/`: 외부 역량의 출처, 버전, 라이선스 메타데이터
- `scripts/`: 설치, 동기화, 검증 자동화
- `tests/`: 저장소 계약과 도구 동작 검증
- `docs/`: 아키텍처와 의사결정 기록

프로젝트 고유 구현, 비밀 정보, 세션 로그, 캐시와 내려받아 재생성할 수 있는 런타임 파일은 포함하지 않는다.

## GitHub 명령 정책

- GitHub 서비스의 조회나 변경에는 **인증된 GitHub CLI(`gh`)만 사용한다**.
- GitHub API를 `curl`, 임의 HTTP 클라이언트 또는 비인증 요청으로 직접 호출하지 않는다.
- issue, pull request, label, release, workflow, repository 설정을 다루기 전에 `gh auth status`가 성공하는지 확인한다.
- 로컬 버전 관리에는 `git`을 사용할 수 있다. `git push` 전에 `gh auth status`와 `git remote -v`로 인증 계정과 대상 저장소를 확인한다.
- 토큰을 명령행, 파일, 로그 또는 커밋에 기록하지 않는다. `gh`가 관리하는 인증 정보를 사용한다.
- 파괴적이거나 되돌리기 어려운 GitHub 작업은 정확한 저장소와 대상을 먼저 출력해 확인한다.

## 작성 규칙

### Skills

- 각 skill은 `skills/<skill-name>/SKILL.md`를 진입점으로 사용한다.
- 이름은 소문자 kebab-case로 작성한다.
- `SKILL.md` frontmatter에는 최소한 `name`과 구체적인 `description`을 둔다.
- 큰 참고자료와 실행 코드는 각각 `references/`, `scripts/`, `assets/`로 분리한다.
- 특정 에이전트 전용 동작은 명시하고, 공통 본문은 도구 중립적으로 유지한다.

### Frameworks

- 각 framework는 `frameworks/<framework-name>/README.md`를 진입점으로 사용한다.
- framework는 특정 skill이나 에이전트에 의존하지 않는 canonical source로 유지한다.
- skill, tool과 adapter는 framework를 소비할 수 있지만 framework가 이들을 참조하지 않는다.
- 둘 이상의 최상위 영역에 영향을 주는 결정은 `docs/decisions/`에, framework 내부 결정은 해당 framework의 `decisions/`에 기록한다.
- 규격과 스키마는 버전을 명시하며 이미 배포한 버전의 의미를 호환성 없이 변경하지 않는다.

### CLI와 도구

- 자체 CLI는 기존 도구로 해결할 수 없는 반복 작업이 확인된 뒤 추가한다.
- 사람이 읽는 출력과 자동화용 구조화 출력의 경계를 명확히 한다.
- 변경 작업에는 가능하면 `--dry-run` 또는 이에 준하는 읽기 전용 확인 경로를 제공한다.
- Windows와 Unix 지원 범위를 문서화하고, 지원한다고 명시한 환경에서 검증한다.

### 외부 자산

- 외부 skill이나 도구를 그대로 복사하지 말고 `external/catalog.yaml`에 출처와 사용 목적을 기록한다.
- 고정 재현이 필요하면 commit 또는 release tag를 기록한다.
- 라이선스가 불명확한 자산은 저장소에 포함하지 않는다.

## 변경 절차

1. 관련 문서와 기존 구현을 먼저 확인한다.
2. 가장 작은 재사용 가능한 단위로 구현한다.
3. 문서, 템플릿과 검증 코드를 함께 갱신한다.
4. `python scripts/validate_repository.py`를 실행한다.
5. 커밋 전에 diff에서 비밀 정보, 생성 파일과 불필요한 범위가 없는지 확인한다.
6. GitHub 작업은 위의 인증된 `gh` 정책을 따른다.

## 완료 기준

- 요청된 동작과 문서가 일치한다.
- 저장소 검증이 통과한다.
- 새 경로와 명령이 README 또는 관련 문서에서 발견 가능하다.
- 외부 의존성과 라이선스가 기록되어 있다.
- 비밀 정보와 개인 런타임 상태가 커밋에 포함되지 않는다.
