# Improvement AI Agent Guide

`improvement-ai`는 대상 프로젝트에 Agent Skills와 workflow를 생성하도록 안내하는 **Capability Blueprint 전용 저장소**다. 설치형 Skill, runtime, CLI, package, framework나 프로젝트별 생성물을 배포하지 않는다.

이 파일은 매 세션 always-on 지침이다. 5KB 이하를 유지하고 세부는 정범 문서로 보낸다.

- 기여 유형, issue, 언어, 검증: [`CONTRIBUTING.md`](CONTRIBUTING.md)
- Idea 상태와 구성: [`docs/idea/README.md`](docs/idea/README.md)
- 크기 근거: [`docs/research/agents-md-size-guidance.md`](docs/research/agents-md-size-guidance.md)

## 불변 조건

- Blueprint가 원본이다. 문제, 결과, 불변 조건, operation, 적응 지점, acceptance를 계약으로 두고 구현 형태와 Skill 수를 고정하지 않는다.
- 대상 프로젝트는 읽기 전용으로 조사한 뒤 설치안을 제안한다. 인간 승인 전에는 파일을 변경하지 않는다.
- 생성 Skill과 지원 자산은 대상 프로젝트가 소유한다. 이 저장소로 가져오거나 자동 동기화하지 않는다.
- 생성 경로는 대상 프로젝트 내부만 허용한다. 전역 Agent Skill, 사용자 홈, 공유 전역 config, 여러 프로젝트가 쓰는 새 상태 경로는 금지한다.
- Blueprint 버전은 canonical `BLUEPRINT.md`를 마지막으로 변경한 40자리 commit이다. 저장소 HEAD를 설치 revision으로 쓰지 않는다.
- 대상 프로젝트에는 Blueprint별 Installation Receipt를 정확히 하나 둔다. 생성 Skill provenance와 같은 revision을 기록한다.
- 외부 쓰기, 활성화, 종료, 파괴적 결정은 인간 승인 경계다.
- Promoted는 서로 다른 두 프로젝트의 생성·실사용 뒤에만 확정한다. Maintainer가 판정한다.
- 실제 실패 근거 없이 schema, generator, validator, CI, Release, version catalog, tag, changelog를 추가하지 않는다.

## 이 저장소 작업

기여 전에 `CONTRIBUTING.md`를 확인한다. 오탈자, 링크, Research, 비규범 Idea는 직접 PR이다. 새 Blueprint, 계약 변경, 저장소 정책은 issue-first다.

- 이름은 kebab-case이고 `blueprints/README.md`에 한 번만 등록한다. 사람 진입점은 `blueprints/<name>/README.md`, AI 계약은 `BLUEPRINT.md`다. README에 정보 모델, invariant, operation, acceptance를 복제하지 않는다.
- 설치 프롬프트는 해당 Blueprint의 정확한 `main` URL과 `조사 → 제안 → 승인 → 프로젝트 로컬 생성` 경계를 포함한다.
- Canonical `BLUEPRINT.md`와 Pilot scenario는 영어다. 최상위 영문·국문 README 의미가 바뀌면 함께 갱신한다.
- 생성 Skill frontmatter는 `name`과 trigger 중심 `description`만 쓰도록 지시한다. provenance는 HTML comment다.
- Pilot evidence는 파일로 커밋하지 않고 tracking issue comment로 제출한다.
- `references/`는 설명과 평가 scenario만 둔다. 업데이트는 두 exact Blueprint 비교, migration 제안, 인간 승인 뒤에 receipt와 모든 생성 Skill provenance를 함께 갱신한다.
- Idea note는 결정이나 Blueprint가 아니다. 규범 변경은 issue와 필요한 ADR로 한다.

## GitHub와 게시

GitHub 조회와 변경은 연결된 GitHub connector를 우선한다. `gh` 전용 정책을 강제하지 않는다. GitHub API를 비인증 `curl`이나 임의 HTTP client로 직접 호출하지 않는다. token을 명령행, 파일, log, commit에 기록하지 않는다. 파괴적 작업은 대상 저장소와 객체를 먼저 확인한다.

사용자가 이 저장소의 간단한 수정을 요청하면 구현과 검증 후 승인 질문 없이 commit, PR, merge까지 완료한다. 기본 branch에 직접 push하지 않는다. 관련 없는 사용자 변경, 충돌, 검증 실패, 파괴적 작업, 새 외부 권한은 자동 게시에 넣지 않는다.

## 완료

설치 안내와 canonical 계약에 바로 닿고, 승인 전 mutation이 없으며, 생성 경로는 프로젝트 내부이고, 설치형 Skill·runtime·비밀·프로젝트 runtime 상태를 커밋하지 않았으면 완료다.
