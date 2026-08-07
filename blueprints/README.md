# Capability Blueprints

Capability Blueprint는 완성된 Skill이나 도구가 아니라, 대상 프로젝트의 AI가 그 프로젝트에 맞는 Agent Skills와 지원 자산을 설계하도록 만드는 canonical source다.

## 사용 방법

1. 최신 Blueprint는 `main` URL로, 재현 가능한 사용은 40자리 commit이 포함된 URL로 AI에게 전달한다.
2. AI는 대상 프로젝트의 지침, 기록 체계, Agent client와 기존 도구를 읽기 전용으로 조사한다.
3. AI는 필요한 Skill 수, 이름, trigger, source of truth, 표현 방식과 검증 방법을 제안한다.
4. 인간이 제안을 승인한 뒤에만 프로젝트 로컬 파일을 생성한다.
5. 생성된 Skill은 대상 프로젝트가 소유하며 Blueprint source와 정확한 Git revision을 기록한다.

예시 요청:

```text
다음 Capability Blueprint를 현재 프로젝트에 적용해 주세요.
먼저 프로젝트를 조사하고 필요한 로컬 Skill과 지원 자산의 구성을 제안하세요.
내가 승인하기 전에는 파일을 만들거나 수정하지 마세요.

https://github.com/SWBaek/improvement-ai/blob/main/blueprints/manage-focus-cycle/BLUEPRINT.md
```

Blueprint는 생성할 Skill의 개수를 고정하지 않는다. AI는 서로 다른 trigger와 책임이 있을 때만 나누며, 대상 Agent가 사용하는 프로젝트 로컬 경로를 따른다. 전역 설치와 upstream 자동 동기화는 기본 동작이 아니다.

## Lifecycle

| 상태 | 의미 |
|---|---|
| Candidate | 반복되는 문제가 issue에 기록됐지만 Blueprint가 아직 없다. |
| In Progress | Blueprint가 존재하며 실제 프로젝트에서 생성 결과를 Pilot 중이다. |
| Promoted | 서로 다른 두 프로젝트에서 생성·실사용되어 불변 조건과 trigger가 확인됐다. |
| Deprecated | 대체 Blueprint 또는 폐기 이유와 기존 소비자를 위한 안내가 기록됐다. |

## Registered Blueprints

| Blueprint | Status | Tracking |
|---|---|---|
| [manage-focus-cycle](manage-focus-cycle/BLUEPRINT.md) | In Progress | [#15](https://github.com/SWBaek/improvement-ai/issues/15) |
| [maintain-project-continuity](maintain-project-continuity/BLUEPRINT.md) | In Progress | [#21](https://github.com/SWBaek/improvement-ai/issues/21) |

## 작성 원칙

- 진입점은 `blueprints/<name>/BLUEPRINT.md`다.
- 이름은 소문자 kebab-case로 작성한다.
- Blueprint는 문제, 기대 결과, 불변 조건, 필수 operation, 적응 지점, 인간 권한, 생성 절차와 acceptance criteria를 포함한다.
- 필요한 경우 설명용 `references/`와 시나리오를 두되 실행 code, generator, formal schema나 복사 가능한 완제품을 두지 않는다.
- 프로젝트별 생성물과 Pilot 중 얻은 비공개 자료를 이 저장소로 가져오지 않는다. 반복 가능한 학습만 Blueprint에 반영한다.
