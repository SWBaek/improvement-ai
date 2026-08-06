# GitHub Issue 표준

## 목적

Issue는 Capability 후보, Blueprint 개선과 저장소 운영 작업의 이유·범위·완료 여부를 공유하는 durable record다. 프로젝트별 생성 결과나 비공개 Pilot 기록을 저장하는 장소가 아니다.

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
| Status | 열린 issue에 정확히 하나 | `status: triage`, `status: ready` |

```text
status: triage → status: ready → status: in-progress → closed
                         ↘ status: blocked ↗
```

완료하거나 진행하지 않기로 한 issue는 닫고 status label을 제거한다. Catalog에서 제거된 legacy label은 역사적 issue 보존을 위해 remote에 남을 수 있다.

## Capability lifecycle

| Capability 단계 | Issue 상태 | 저장소 산출물 |
|---|---|---|
| Candidate | `triage` 또는 `ready` | 문제, target context, invariants와 Pilot 조건 |
| In Progress | `in-progress` | `blueprints/<name>/BLUEPRINT.md`와 index 등록 |
| Promoted | Pilot 기준 충족 후 issue 종료 | 같은 Blueprint와 두 프로젝트의 비공개 정보 없는 evidence 요약 |
| Deprecated | 폐기 issue 종료 | 같은 경로의 대체 또는 폐기 안내 |

## Triage와 동기화

1. 중복과 민감 정보 노출 여부를 확인한다.
2. required outcomes가 구현을 불필요하게 고정하지 않는지 확인한다.
3. type, area, priority와 status label을 지정한다.
4. 저장소 전체 계약에 영향을 주면 ADR을 추가한다.
5. 실제 Pilot 자료에서는 재사용 가능한 학습만 issue에 기록한다.

GitHub 서비스 변경은 인증된 `gh`만 사용한다.

```powershell
gh auth status
python scripts/sync_github_labels.py --repo SWBaek/improvement-ai --dry-run
python scripts/sync_github_labels.py --repo SWBaek/improvement-ai
```

동기화는 catalog label을 생성하거나 갱신하며 catalog 밖의 역사적 label을 삭제하지 않는다.
