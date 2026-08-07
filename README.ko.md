# improvement-ai

> AI가 대상 프로젝트에 맞는 Skill과 workflow를 만들도록 안내하는 Capability Blueprint의 원본 저장소입니다.

[English](README.md)

`improvement-ai`는 애플리케이션, Skill catalog, package registry 또는 설치형 runtime 구현 저장소가 아닙니다. 반복 가능한 capability 설계를 간결한 Blueprint로 기록합니다. 사람은 Blueprint를 대상 프로젝트에서 작업 중인 AI에게 전달하고, AI는 프로젝트 관례를 조사해 로컬 설계를 제안한 뒤 승인 후에만 프로젝트 소유의 Skill을 생성합니다.

## 운영 원칙

- **제품보다 Blueprint:** 하나의 범용 구현 대신 문제, 불변 조건, operation, 적응 지점과 acceptance criteria를 보존합니다.
- **설계 전 조사:** 대상 프로젝트의 지침, 기록, 도구와 Agent client를 근거로 제안합니다.
- **작성 전 제안:** 파일 변경 전에 Skill 분해, 경로, 권한과 검증 방법을 보여줍니다.
- **프로젝트 소유:** 생성된 Skill과 지원 자산은 소비 프로젝트가 소유하며 upstream 변경을 자동 추적하지 않습니다.
- **전역 설치 금지:** 생성된 Skill, receipt, profile, schema, mapping과 상태 기록은 모두 대상 프로젝트 내부에 둡니다.
- **Revision provenance:** canonical Blueprint path를 마지막으로 변경한 commit을 버전으로 사용하고 프로젝트 로컬 Installation Receipt와 모든 생성 Skill에 기록합니다.
- **인간 권한:** 생성, 외부 쓰기, 활성화와 되돌리기 어려운 결정의 승인 경계를 명시합니다.
- **실사용 승격:** 서로 다른 두 프로젝트에서 생성·실사용된 뒤에만 Blueprint를 Promoted로 판단합니다.

## 제공 중인 Blueprint

| Blueprint | 상태 | 목적 | 사용 |
|---|---|---|---|
| `manage-focus-cycle` | In Progress | 전체 프로젝트의 가짜 종료점을 만들지 않고 하나의 제한된 Focus Cycle을 관리하는 프로젝트 로컬 capability를 생성합니다. | [설치](blueprints/manage-focus-cycle/README.md) · [계약](blueprints/manage-focus-cycle/BLUEPRINT.md) |
| `maintain-project-continuity` | In Progress | 세션·Agent·모델이 바뀌어도 작업, 결정, 근거와 인수인계를 보존하는 프로젝트 로컬 capability를 생성합니다. | [설치](blueprints/maintain-project-continuity/README.md) · [계약](blueprints/maintain-project-continuity/BLUEPRINT.md) |

[Blueprint index](blueprints/README.md)와 각 Blueprint의 tracking issue를 참고하세요.

## 사용 방법

원하는 capability의 **설치** 안내를 열고 준비된 프롬프트를 그대로 복사해 대상 프로젝트에서 작업 중인 AI에게 전달합니다. 설치 안내는 읽기 전용 조사와 설치안 제안부터 시작하며, 프로젝트 파일은 사람이 설치안을 승인한 뒤에만 생성됩니다.

최신 설계 탐색에는 `main` URL을 사용합니다. 생성 전 AI는 해당 canonical `BLUEPRINT.md`를 마지막으로 변경한 commit을 확인하고 exact URL에서 다시 읽은 뒤 대상 프로젝트에 40자리 revision을 기록합니다. 저장소의 무관한 commit은 설치를 오래된 것으로 만들지 않습니다.

생성 Skill은 대상 Agent의 프로젝트 로컬 탐색 경로를 따릅니다. 예를 들어 Codex는 일반적으로 `.agents/skills/<name>/`, Claude Code는 `.claude/skills/<name>/`을 사용합니다. 전역 Agent Skill directory와 프로젝트 밖 공유 경로는 금지합니다. 이 저장소는 생성물을 설치·업데이트·동기화하지 않습니다.

## Lifecycle

| 상태 | 의미 |
|---|---|
| Candidate | 반복되는 문제가 issue에 존재하지만 Blueprint는 아직 없습니다. |
| In Progress | Blueprint가 존재하며 실제 프로젝트에서 생성 결과를 Pilot 중입니다. |
| Promoted | 서로 다른 두 프로젝트에서 capability가 생성·실사용됐습니다. |
| Deprecated | 대체 또는 폐기 이유와 소비자 안내가 기록됐습니다. |

## 저장소 구조

```text
blueprints/    생성형 capability 설계와 평가 시나리오
docs/          아키텍처, 결정과 GitHub 운영 정책
scripts/       저장소 governance용 helper만 허용
.github/       Blueprint issue form, label, ownership와 PR 지침
```

프로젝트별 생성 Skill, runtime 구현, 인증 정보, session log와 비공개 Pilot 자료는 포함하지 않습니다.

## 과거 Snapshot

[`manage-focus-cycle-v0.1.0` GitHub Release](https://github.com/SWBaek/improvement-ai/releases/tag/manage-focus-cycle-v0.1.0)는 폐기된 설치형 Skill 접근의 변경하지 않는 역사적 snapshot입니다. 현재 배포 경로가 아니며 `main`에서 더 이상 업데이트되지 않습니다.

지원 SLA 없이 issue와 pull request를 받습니다. [기여 안내](CONTRIBUTING.md), [보안 정책](SECURITY.md), [아키텍처](docs/architecture.md)와 [MIT License](LICENSE)를 확인하세요.
