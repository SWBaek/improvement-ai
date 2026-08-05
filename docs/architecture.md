# Architecture

## 목적

`improvement-ai`는 여러 프로젝트가 소비하는 개인 AI 역량의 canonical source다. 소비 프로젝트는 필요한 역량을 설치하거나 연결하지만 원본을 임의로 복제해 관리하지 않는다.

## 계층

1. **Shared contracts**: `frameworks/`
2. **Capability source**: `skills/`, `tools/`, `packages/`
3. **Configuration adapters**: `configs/`
4. **Distribution and maintenance**: `scripts/`
5. **Governance**: `AGENTS.md`, `.github/`, `docs/`
6. **Verification**: `tests/`, framework-local tests, CI workflow

## 설계 결정

- skill은 `skills/<name>/SKILL.md`를 단일 진입점으로 한다.
- framework는 특정 skill이나 에이전트에 의존하지 않는 공통 계약의 원본이다.
- 의존 방향은 framework에서 skill, tool과 adapter를 향하며 역방향 참조는 허용하지 않는다.
- 저장소 전역 결정과 framework 내부 결정을 각각 `docs/decisions/`와 framework의 `decisions/`에 분리한다.
- 에이전트별 파일은 공통 원본에서 파생할 수 있을 때 생성물로 취급한다.
- 초기 배포는 `npx skills` 같은 기존 생태계를 활용한다.
- 자체 CLI는 설정, hook, pack 또는 버전 고정까지 함께 관리해야 할 때 도입한다.
- 외부 자산은 vendoring보다 출처와 버전을 기록하는 방식을 우선한다.

## 향후 확장 조건

다음 요구가 반복되면 `packages/cli/`에 자체 CLI를 도입할 수 있다.

- skill 외에 전역 설정과 hook을 함께 설치해야 한다.
- 여러 capability를 profile 또는 pack으로 조합해야 한다.
- 설치 상태와 upstream drift를 검사해야 한다.
- Windows와 Unix에서 동일한 bootstrap 인터페이스가 필요하다.
