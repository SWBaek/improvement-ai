# Ideas

`docs/idea/`는 아직 채택되지 않은 문제, 관찰과 capability 가설을 모으고 구체화하는 탐색 공간이다. Idea note는 결정 기록, 구현 사양, GitHub Candidate 또는 Capability Blueprint가 아니다.

## 운영 방식

1. 반복될 가능성이 있지만 범위와 해법이 불명확한 문제를 Idea note로 기록한다.
2. 조사 결과, 설계 가설, 반례와 열린 질문을 같은 note에서 갱신한다.
3. 실제로 검증할 가치와 반복 가능성이 확인되면 tracking issue를 만들고 Candidate로 승격한다.
4. 첫 Pilot을 시작할 준비가 되면 `blueprints/<name>/BLUEPRINT.md`로 구체화한다.
5. 채택하지 않기로 한 경우에도 이유와 상태를 남겨 같은 탐색을 반복하지 않게 한다.

Idea 단계에서는 실행 가능한 runtime, 설치형 Skill, formal schema나 speculative Blueprint directory를 만들지 않는다. 외부에서 얻은 개념은 출처와 이 Idea에 유용한 이유를 기록한다.

## 상태 관리

각 Idea note는 다음 상태 중 정확히 하나를 사용한다.

| 상태 | 의미 |
|---|---|
| `Exploring` | 현재 조사하거나 구체화하고 있다. |
| `Parked` | 명시한 재개 조건까지 의도적으로 중단한다. |
| `Promoted` | issue 또는 Blueprint로 승격되어 후속 위치에서 관리한다. |
| `Dropped` | 진행하지 않기로 결정했으며 그 이유를 보존한다. |

각 note의 첫 `Status` 섹션에는 `State`, `Last reviewed`, `Next trigger`를 기록하고 index에도 같은 값을 반영한다. `Parked`는 반드시 관찰 가능한 재개 조건을 가져야 하며, `Dropped`는 종료 이유를 `Next trigger`에 기록한다.

`Promoted`는 Idea의 lifecycle 상태일 뿐 Blueprint의 Pilot 진행률을 뜻하지 않는다. 승격 후의 계약과 실행 상태는 canonical Blueprint와 tracking issue에서 관리하며, Idea note에는 최초 문제와 탐색 근거, 후속 링크와 가설을 다시 검토할 조건만 남긴다.

## 권장 구성

- Status (`State`, `Last reviewed`, `Next trigger`, 필요한 후속 링크)
- 문제와 배경
- 현재 개념 또는 설계 가설
- 기대 효과와 비목표
- 위험과 반례
- 검증 기준 또는 실험 질문
- 향후 탐색
- 관련 출처와 후속 링크

모든 항목이 처음부터 완전할 필요는 없다. 다만 추측을 확정된 사실처럼 기록하지 않고, Idea가 무엇을 아직 모르는지 드러내야 한다.

## Idea index

| Idea | 상태 | 마지막 검토 | 다음 조건 |
|---|---|---|---|
| [AI–Human Interactive Decision Workbench](ai-human-interactive-decision-workbench.md) | `Parked` | 2026-08-07 | 실제 프로젝트에서 채팅 기반 다중 결정 검토의 반복 실패와 Pilot 후보가 확인되면 재개 |
| [Local Project Continuity](local-project-continuity.md) | `Promoted` | 2026-08-14 | 사용자 개입을 기본값으로 삼지 않는 더 작은 continuity 가설이 제안되면 최초 문제와 record-first 가정을 다시 비교 |
| [Private Remote Artifact Preview](private-remote-artifact-preview.md) | `Exploring` | 2026-08-10 | 단일 고정 Serve port와 전용 Artifact Root를 사용하는 개인 전역 Skill Pilot에서 정적 게시·Dashboard·cleanup을 검증하고 동적 app 실패 시 Hub 또는 port pool 필요성을 판단 |
| [Subtractive Edit Fidelity](subtractive-edit-fidelity.md) | `Parked` | 2026-08-21 | 한 줄 결과 계약과 짧은 금지 카탈로그를, 대상 잔존(A)과 부재 서술(B)로 나눠 세는 대조 실험을 실제로 시작할 때 재개 |
| [Newcomer Reverse Questioning](newcomer-reverse-questioning.md) | `Exploring` | 2026-08-14 | 빈 원장에서 지금 살아있는 일 몇 개만 신입 인터뷰로 페이지를 만든 뒤, 질문이 멈추는지와 운영 노동이 다시 붙는지 1주 관찰할 때 갱신 |
