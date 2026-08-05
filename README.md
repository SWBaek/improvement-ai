# improvement-ai

여러 프로젝트에서 공통으로 사용할 개인 AI 역량을 개발하고 관리하는 저장소입니다. 반복 가능한 작업 방식을 Agent Skill, CLI, 자동화 도구와 설정으로 축적하는 것을 목표로 합니다.

## 원칙

- 공통 역량의 원본은 이 저장소에서 관리합니다.
- skill은 표준 `SKILL.md` 구조를 우선합니다.
- 기존 설치 도구로 충분한 동안 별도 CLI를 만들지 않습니다.
- Codex, Claude Code 등 에이전트별 차이는 adapter 계층으로 제한합니다.
- 모든 변경은 문서와 자동 검증을 동반합니다.

## 구조

```text
skills/        재사용 가능한 Agent Skills
tools/         독립 실행 자동화와 개발 도구
packages/      배포 가능한 CLI 및 npm 패키지
configs/       공통 설정과 에이전트별 adapter
external/      외부 skill·도구의 출처와 버전
scripts/       설치, 동기화와 검증 스크립트
tests/         저장소 계약 및 동작 검증
docs/          아키텍처와 의사결정 기록
```

자세한 설계는 [아키텍처](docs/architecture.md), 이슈 작성과 메타데이터 규칙은 [GitHub Issue 표준](docs/github/issues.md)을 참고하세요.

## 시작하기

저장소 계약을 검증합니다.

```powershell
python scripts/validate_repository.py
```

skill이 추가된 후에는 기존 Agent Skills CLI를 이용해 조회하거나 전역 설치할 수 있습니다.

```powershell
npx skills add SWBaek/improvement-ai --list
npx skills add SWBaek/improvement-ai -g -a codex
```

저장소의 표준 GitHub label을 동기화하려면 인증된 `gh` 세션에서 실행합니다.

```powershell
gh auth status
python scripts/sync_github_labels.py --repo SWBaek/improvement-ai
```

## 현재 단계

초기 기반을 구축하는 단계입니다. 첫 번째 실제 skill이나 도구가 추가되기 전까지 `packages/`와 `tools/`는 확장 지점만 정의합니다.
