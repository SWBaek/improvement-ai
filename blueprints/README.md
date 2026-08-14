# Capability Blueprints

Capability Blueprint는 완성된 Skill이나 도구가 아니라, 대상 프로젝트의 AI가 그 프로젝트에 맞는 Agent Skills와 지원 자산을 설계하도록 만드는 canonical source다.

## 사용 방법

1. 아래 catalog에서 원하는 capability의 **설치 안내**를 연다.
2. 준비된 프롬프트를 수정 없이 대상 프로젝트에서 작업 중인 AI에게 전달한다.
3. AI는 프로젝트를 읽기 전용으로 조사하고 로컬 Skill과 지원 자산의 설치안을 제안한다.
4. 인간이 설치안을 승인한 뒤에만 프로젝트 로컬 파일을 생성한다.
5. AI는 canonical `BLUEPRINT.md`를 마지막으로 변경한 commit의 exact URL에서 다시 읽고, 대상 프로젝트의 Installation Receipt와 생성 Skill에 같은 40자리 revision을 기록한다.

Blueprint는 생성할 Skill의 개수를 고정하지 않는다. AI는 서로 다른 trigger와 책임이 있을 때만 나누며, 대상 Agent가 사용하는 프로젝트 로컬 경로를 따른다. 생성 Skill과 모든 지원 자산의 전역 설치 또는 프로젝트 밖 공유 경로 사용은 금지하며 upstream 자동 동기화도 하지 않는다.

Blueprint의 버전은 저장소 HEAD가 아니라 해당 canonical `BLUEPRINT.md` path를 마지막으로 변경한 commit이다. 대상 프로젝트는 설치한 Blueprint별 Installation Receipt 하나를 소유하며, AI는 이 revision을 최신 path revision과 비교해 `최신`, `업데이트 가능` 또는 `상태 확인 불가`로 보고한다. 별도 version number, tag, Release, changelog와 알림은 운영하지 않는다.

## Lifecycle

| 상태 | 의미 |
|---|---|
| Candidate | 반복되는 문제가 issue에 기록됐지만 Blueprint가 아직 없다. |
| In Progress | Blueprint가 존재하며 실제 프로젝트에서 생성 결과를 Pilot 중이다. |
| Paused | Blueprint는 보존하지만 기록된 재개 조건을 충족할 때까지 active Pilot과 신규 설치 권장을 중단한다. |
| Promoted | 서로 다른 두 프로젝트에서 생성·실사용되어 불변 조건과 trigger가 확인됐다. |
| Deprecated | 대체 Blueprint 또는 폐기 이유와 기존 소비자를 위한 안내가 기록됐다. |

## Registered Blueprints

| Blueprint | Status | Install | Contract | Tracking |
|---|---|---|---|---|
| `manage-focus-cycle` | In Progress | [설치 안내](manage-focus-cycle/README.md) | [Blueprint](manage-focus-cycle/BLUEPRINT.md) | [#15](https://github.com/SWBaek/improvement-ai/issues/15) |
| `maintain-project-continuity` | Paused | [설치 안내](maintain-project-continuity/README.md) | [Blueprint](maintain-project-continuity/BLUEPRINT.md) | [#21](https://github.com/SWBaek/improvement-ai/issues/21) |

## 작성 원칙

- 사람의 사용 진입점은 `blueprints/<name>/README.md`, AI가 적용할 canonical 계약은 `blueprints/<name>/BLUEPRINT.md`다.
- 개별 README는 capability 설명과 바로 복사할 설치 프롬프트를 제공하며 Blueprint 계약을 복제하지 않는다.
- Blueprint는 path-scoped Git revision, 단일 Installation Receipt, latest 비교와 승인 기반 migration 규약을 포함한다.
- Blueprint는 모든 생성 경로를 대상 프로젝트 내부로 제한하고 전역 설치를 명시적으로 금지한다.
- 이름은 소문자 kebab-case로 작성한다.
- Blueprint는 문제, 기대 결과, 불변 조건, 필수 operation, 적응 지점, 인간 권한, 생성 절차와 acceptance criteria를 포함한다.
- 필요한 경우 설명용 `references/`와 시나리오를 두되 실행 code, generator, formal schema나 복사 가능한 완제품을 두지 않는다.
- 프로젝트별 생성물과 Pilot 중 얻은 비공개 자료를 이 저장소로 가져오지 않는다. 반복 가능한 학습만 Blueprint에 반영한다.
