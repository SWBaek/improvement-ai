# improvement-ai

> 우리의 해법을 설치하지 마세요. 그 계약을 프로젝트 안의 AI에게 전달하세요.

[English](README.md)

`improvement-ai`는 범용 Skill 대신 **Capability Blueprint**를 배포합니다. Blueprint는 문제, 의미 계약, 필수 operation, 권한 경계와 acceptance evidence를 고정하고 실제 구현은 대상 프로젝트를 읽을 수 있는 AI에게 맡깁니다. AI는 기존 기록을 재사용하고 부족한 로컬 capability만 제안하며 인간 승인 후 생성합니다.

## 무엇이 다른가

일반적인 Skill·workflow 저장소는 하나의 구현을 배포하고 모든 프로젝트가 이를 설치·설정하게 합니다. 이 저장소는 capability의 핵심 의미를 잃지 않으면서 프로젝트마다 다른 구현을 생성할 수 있는 최소 계약을 배포합니다.

```text
일반적인 배포
upstream Skill / CLI / framework
  → 같은 구현을 여러 프로젝트에 복사
  → adapter와 설정 추가
  → upstream을 계속 추적

improvement-ai
exact-revision Blueprint
  → 대상 프로젝트의 AI가 실제 환경 조사
  → Integration, Migration, Skill 경계, 경로와 권한 제안
  → 인간 승인
  → 프로젝트가 생성 capability 소유
```

이 방식은 다음 경계를 의도적으로 만듭니다.

- **계약은 공유하지만 구현은 공유하지 않습니다.** 서로 다른 프로젝트가 다른 Skill과 파일을 생성해도 같은 invariant와 operation을 유지합니다.
- **기존 체계를 우선합니다.** 성숙한 issue, ADR, 연구 기록과 프로젝트 지침은 복제하지 않고 Integration하며 인간이 선택할 때만 Migration합니다.
- **프로젝트가 주권을 가집니다.** 생성 Skill, 상태, schema, mapping과 receipt는 대상 프로젝트 내부에만 존재하며 전역 설치와 upstream 동기화가 없습니다.
- **AI의 적응 과정을 검토할 수 있습니다.** 조사는 읽기 전용이고 전체 설치안이 mutation보다 먼저 나오며 중요한 결정은 인간 권한으로 남습니다.
- **모든 설치를 재현할 수 있습니다.** 하나의 Installation Receipt와 각 생성 Skill이 canonical Blueprint를 마지막으로 변경한 exact commit을 기록합니다.
- **설계는 실사용으로 안정성을 얻습니다.** 서로 다른 프로젝트에서 생성·운영에 성공한 뒤에만 Blueprint를 Promoted로 승격합니다.

이 접근은 Andrej Karpathy의 `llm-wiki.md`에서 동기를 얻었습니다. 강한 invariant와 operation을 가진 작은 Idea File은 고정 구현보다 재사용성이 높을 수 있습니다. `improvement-ai`는 이 패턴을 project-scoped capability portfolio로 일반화합니다. 자세한 비교는 [생태계 benchmark와 전략 검토](docs/research/bencmark/karpathy-llm-wiki-ecosystem.md)를 참고하세요.

## 세부 운영 원칙

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
| `maintain-project-continuity` | Paused | 실패한 Pilot에서 확인된 상호작용 비용을 재검토하는 동안 프로젝트 로컬 continuity 설계를 보존합니다. | [설치](blueprints/maintain-project-continuity/README.md) · [계약](blueprints/maintain-project-continuity/BLUEPRINT.md) |

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
| Paused | Blueprint는 보존하지만 기록된 재개 조건을 충족할 때까지 active Pilot과 신규 설치 권장을 중단합니다. |
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

## 기여하기

[기여 유형 선택표](CONTRIBUTING.md)에서 시작하세요. 작은 문서 수정, Research와 비규범 Idea는 직접 pull request로 제출할 수 있지만 새 Blueprint, 계약 변경과 저장소 정책 변경은 issue-first입니다. 실제 사용 결과는 [Pilot evidence template](docs/github/pilot-evidence.md)을 사용해 기존 tracking issue에 privacy-safe하게 제출합니다. Maintainer는 서로 다른 두 프로젝트 evidence를 확인한 뒤에만 Promotion을 확정합니다.

## 과거 Snapshot

[`manage-focus-cycle-v0.1.0` GitHub Release](https://github.com/SWBaek/improvement-ai/releases/tag/manage-focus-cycle-v0.1.0)는 폐기된 설치형 Skill 접근의 변경하지 않는 역사적 snapshot입니다. 현재 배포 경로가 아니며 `main`에서 더 이상 업데이트되지 않습니다.

지원 SLA 없이 issue와 pull request를 받습니다. [기여 안내](CONTRIBUTING.md), [보안 정책](SECURITY.md), [아키텍처](docs/architecture.md)와 [MIT License](LICENSE)를 확인하세요.
