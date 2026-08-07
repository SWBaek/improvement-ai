# Architecture

## 목적

`improvement-ai`는 대상 프로젝트의 AI가 project-owned Agent Skills와 workflow를 생성하도록 안내하는 Capability Blueprint의 canonical source다. 생성 결과와 프로젝트 상태는 소비 프로젝트가 소유한다.

## 흐름

```text
Capability Blueprint at the exact commit that last changed its canonical path
  └─ target-project AI inspects local policy and records
       └─ adaptation proposal
            └─ human approval
                 └─ project-owned Skills and supporting assets
                      └─ local verification and Pilot feedback
```

Blueprint는 생성 결과를 중앙에서 배포하거나 동기화하지 않는다. Pilot에서 확인된 반복 가능한 학습만 다음 Blueprint revision에 반영한다.

## 저장소 계층

1. **Idea incubation**: 아직 채택되지 않은 문제와 capability 가설을 탐색하는 `docs/idea/`
2. **Capability source**: `blueprints/`
3. **Evidence and decisions**: tracking issues와 `docs/decisions/`
4. **Repository governance**: `AGENTS.md`, `.github/`, `docs/github/`
5. **Governance helper**: `scripts/`의 작은 GitHub label 동기화 도구

설치형 Skill, capability runtime, package, framework, adapter와 프로젝트별 생성물은 계층에 포함하지 않는다.

Idea note는 canonical capability source가 아니다. 탐색 중인 문제와 가설을 보존하며, 반복 가능성과 검증 가치가 확인된 뒤에만 tracking issue를 가진 Candidate로 승격한다.

## Blueprint와 생성물 경계

- Blueprint는 문제, required outcomes, invariants와 operation을 규범적으로 정의한다.
- Skill 수, 파일 구조, 시각화 기술과 결정적인 helper는 대상 프로젝트의 근거에 따라 AI가 제안한다.
- AI는 승인 전까지 읽기 전용으로 동작하고, 승인된 프로젝트 로컬 경로만 변경한다.
- 생성 Skill, receipt, profile, schema, mapping과 상태 기록은 모두 대상 프로젝트 내부에 둔다. 전역 Agent 경로나 프로젝트 밖 공유 상태는 허용하지 않는다.
- 생성 Skill은 Agent Skills 호환 frontmatter와 Installation Receipt에 일치하는 exact-revision provenance를 가진다.
- 대상 프로젝트는 설치한 Blueprint마다 canonical path, path-scoped revision과 exact source를 담은 Installation Receipt 하나를 소유한다.
- 생성물은 upstream 변경을 자동 추적하지 않는다. canonical Blueprint path의 최신 변경 commit이 receipt와 다를 때만 새 revision 후보이며, 적용은 semantic comparison과 별도 승인 과정이다.
- 여러 프로젝트를 설치하는 편의를 위한 무상태 bootstrap capability는 별도 설계 대상이며 프로젝트별 생성물의 전역 설치 예외가 아니다.

## Lifecycle

- 채택 전 탐색은 `docs/idea/`의 Idea note에서 수행한다.
- Candidate는 GitHub issue에만 존재한다.
- 첫 Pilot을 시작할 때 `blueprints/<name>/BLUEPRINT.md`를 만들고 In Progress로 등록한다.
- 서로 다른 두 프로젝트에서 생성·실사용된 뒤 불변 조건과 trigger가 확인되면 Promoted로 변경한다.
- 대체나 폐기 시 같은 경로에 소비자 안내를 남기고 Deprecated로 변경한다.

## 배포와 검증

- 최신 소비 경로는 `main`의 Blueprint URL이다.
- 재현 가능한 소비 경로는 canonical `BLUEPRINT.md`를 마지막으로 변경한 40자리 commit이 포함된 GitHub URL이다. 저장소 HEAD의 무관한 변경은 Blueprint revision이 아니다.
- version catalog, tag, Release, changelog, installer, generator와 자동 update channel을 운영하지 않는다.
- 문서 링크, issue metadata와 `git diff --check`만 비례적으로 확인한다.
- Blueprint 품질은 자동 schema보다 실제 프로젝트 Pilot과 acceptance scenario로 판단한다.

`manage-focus-cycle-v0.1.0` Release는 이전 설치형 구조의 역사적 snapshot이며 현재 architecture의 소비 경로가 아니다.
