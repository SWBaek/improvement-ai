# Manage Focus Cycle

끝이 없는 유지보수·연구·제품 프로젝트 안에서 지금 집중할 하나의 유한한 목표와 완료 조건을 관리하도록 프로젝트 로컬 capability를 생성한다.

이 README는 사람을 위한 설치 안내다. 규범적 계약은 [BLUEPRINT.md](BLUEPRINT.md)이며, 여기서 말하는 설치는 공통 package를 복사하는 것이 아니라 대상 프로젝트에 맞는 Skill과 지원 자산을 AI가 생성하는 과정이다.

## 이런 경우에 사용한다

- 프로젝트 전체에는 정직한 최종 완료 지점이 없지만 현재 작업에는 종료 조건이 필요하다.
- 연구가 끝없이 확장되거나 유지보수 작업의 완료 선언이 불명확하다.
- 현재 목표, 근거, blocker와 다음 인간 결정을 한정된 Focus Cycle로 관리하고 싶다.

## 설치

아래 프롬프트를 대상 프로젝트에서 작업 중인 AI에게 그대로 전달한다.

```text
현재 프로젝트에 다음 Capability Blueprint를 설치하세요.

먼저 Blueprint와 현재 프로젝트를 읽기 전용으로 조사하세요.
현재 프로젝트 안에서 하나의 제한된 Focus Cycle을 관리하기 위해 필요한
프로젝트 로컬 Skill과 지원 자산의 설치안을 제안하세요.

설치안에는 다음을 포함하세요.

- 생성할 Skill의 이름, trigger, 책임과 프로젝트 로컬 경로
- 기존 issue, plan 또는 연구 기록 중 사용할 source of truth
- Focus Cycle과 Completion Contract의 저장 위치
- 인간 승인과 외부 권한 경계
- 필요한 표현 방식과 검증 방법
- 생성하거나 변경할 파일

내가 설치안을 승인하기 전에는 파일을 만들거나 수정하지 마세요.

Blueprint:
https://github.com/SWBaek/improvement-ai/blob/main/blueprints/manage-focus-cycle/BLUEPRINT.md
```

## 설치 흐름

1. AI가 Blueprint와 대상 프로젝트를 읽기 전용으로 조사한다.
2. AI가 프로젝트 로컬 설치안을 제안한다.
3. 사람이 설치안을 검토하고 승인한다.
4. AI가 승인된 파일만 생성하고 대표 동작을 검증한다.

최신 설계는 프롬프트의 `main` URL을 사용한다. 재현 가능한 설치에는 `main`을 정확한 40자리 commit으로 교체한다. `main`에서 시작해도 생성 Skill에는 실제 사용한 exact revision이 기록되어야 한다.

## 계약과 상태

- Canonical contract: [BLUEPRINT.md](BLUEPRINT.md)
- Status: In Progress
- Tracking: [issue #15](https://github.com/SWBaek/improvement-ai/issues/15)
