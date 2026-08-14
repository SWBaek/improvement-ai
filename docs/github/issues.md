# GitHub Issue 표준

## 목적

Issue는 Capability 후보, Blueprint 개선과 저장소 운영 작업의 이유·범위·완료 여부를 공유하는 durable record다. 프로젝트별 생성 결과나 비공개 Pilot 기록을 저장하는 장소가 아니다.

기여 유형과 issue 필요 여부의 진입점은 [`CONTRIBUTING.md`](../../CONTRIBUTING.md)다.

## Issue가 필요한 경우

| 변경 | 처리 방식 |
|---|---|
| 오탈자, 깨진 링크, 의미를 바꾸지 않는 설명 | issue 없이 직접 PR 가능 |
| Research와 비규범 Idea note | 직접 PR 가능, 논의가 필요하면 issue 선택 |
| 새 Capability Blueprint | Blueprint proposal issue 필수 |
| 기존 Blueprint의 invariant, operation, authority 또는 adaptation 계약 변경 | tracking 또는 feature issue 필수 |
| 저장소 정체성, lifecycle 또는 장기 정책 변경 | feature issue와 필요한 ADR 필수 |
| Pilot evidence | 새 issue를 만들지 않고 기존 tracking issue에 comment |
| 보안 취약점 | 공개 issue가 아닌 private vulnerability report |

직접 PR로 시작한 변경이 의미 계약을 바꾸는 것으로 확인되면 구현을 확대하지 않고 issue-first 흐름으로 전환한다.

## 제목과 유형

```text
[Blueprint] 프로젝트별 의사결정 검토 capability 생성
[Bug] Blueprint의 provenance 예제가 잘못된 commit 형식을 사용함
[Feature] Blueprint proposal form에 non-goal 입력 추가
```

새 Capability는 `type: blueprint`를 사용한다. `type: skill`과 `type: tool`은 과거 issue에만 남길 수 있으며 새 작업 유형으로 사용하지 않는다.

## 필수 정보

모든 issue는 해결하려는 문제, 영향을 받는 workflow, 원하는 결과, 범위 밖, 완료 증거와 권한·보안 위험을 설명한다.

Blueprint proposal은 추가로 다음을 포함한다.

- target contexts와 non-target contexts
- required outcomes와 invariants
- AI가 대상 프로젝트에서 확인해야 할 근거
- 인간 승인 지점
- 생성될 수 있는 프로젝트 로컬 artifact의 범위
- 서로 다른 두 프로젝트 Pilot 방법

## Labels

Label 정의의 원본은 `.github/issue-labels.json`이다.

| 차원 | 규칙 | 예시 |
|---|---|---|
| Type | 정확히 하나 | `type: blueprint`, `type: bug` |
| Area | 주 영역 하나, 필요하면 복수 | `area: blueprints`, `area: github` |
| Priority | triage 이후 정확히 하나 | `priority: p0` ~ `priority: p3` |
| Status | 열린 issue에 정확히 하나 | `status: triage`, `status: ready`, `status: paused` |

```text
status: triage → status: ready → status: in-progress → closed
                         ↘ status: blocked ↗

Blueprint tracking: status: in-progress ↔ status: paused
```

`status: blocked`는 외부 결정이나 선행 작업을 기다리는 상태다. `status: paused`는 Blueprint의 부정적·불확정 evidence를 보존하면서 명시한 재개 조건까지 Pilot을 의도적으로 중단한 상태다. 완료하거나 진행하지 않기로 한 issue는 닫고 status label을 제거한다. Catalog에서 제거된 legacy label은 역사적 issue 보존을 위해 remote에 남을 수 있다.

## Capability lifecycle

| Capability 단계 | Issue 상태 | 저장소 산출물 |
|---|---|---|
| Candidate | `triage` 또는 `ready` | 문제, target context, invariants와 Pilot 조건 |
| In Progress | `in-progress` | `blueprints/<name>/BLUEPRINT.md`와 index 등록 |
| Paused | `paused`인 열린 tracking issue | 같은 Blueprint, 실패 또는 불확정 evidence, 기존 소비자 안내와 관찰 가능한 재개 조건 |
| Promoted | Pilot 기준 충족 후 issue 종료 | 같은 Blueprint와 두 프로젝트의 비공개 정보 없는 evidence 요약 |
| Deprecated | 폐기 issue 종료 | 같은 경로의 대체 또는 폐기 안내 |

## Pilot evidence

Pilot은 [`Pilot evidence template`](pilot-evidence.md)을 사용해 해당 Blueprint tracking issue에 comment로 제출한다. 성공, 실패와 inconclusive 결과를 모두 기록할 수 있다.

- Blueprint 이름과 path-scoped 40자리 revision을 기록한다.
- 프로젝트 유형, 기존 관리 체계, Agent와 adaptation을 익명화해 설명한다.
- 실제 operation, 기대·관찰 결과, 검증, 유지 비용과 재사용 학습을 기록한다.
- 비공개 이름, 코드, 경로, 인증 정보와 원본 session log를 제거한다.
- 같은 프로젝트의 반복 사용은 한 Pilot을 강화하지만 두 번째 독립 Pilot로 계산하지 않는다.
- Maintainer가 두 evidence의 독립성과 Promoted 조건 충족 여부를 최종 판정한다.

## Triage와 동기화

1. 중복과 민감 정보 노출 여부를 확인한다.
2. required outcomes가 구현을 불필요하게 고정하지 않는지 확인한다.
3. type, area, priority와 status label을 지정한다.
4. 저장소 전체 계약에 영향을 주면 ADR을 추가한다.
5. 실제 Pilot 자료에서는 재사용 가능한 학습만 issue에 기록한다.

GitHub 서비스 변경은 인증된 GitHub connector 또는 인증된 `gh`를 사용한다. 아래는 `gh` 예시다.

```powershell
gh auth status
python scripts/sync_github_labels.py --repo SWBaek/improvement-ai --dry-run
python scripts/sync_github_labels.py --repo SWBaek/improvement-ai
```

동기화는 catalog label을 생성하거나 갱신하며 catalog 밖의 역사적 label을 삭제하지 않는다.
