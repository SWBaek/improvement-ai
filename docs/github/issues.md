# GitHub Issue 표준

## 목적

Issue는 아이디어 메모가 아니라 작업의 이유, 범위와 완료 여부를 공유하는 durable record다. 구현을 시작할 수 있을 만큼 구체적으로 작성하되 해결 방법을 불필요하게 고정하지 않는다.

## 제목

Issue Form이 제공하는 prefix 뒤에 결과 중심의 짧은 제목을 작성한다.

```text
[Bug] Windows에서 전역 skill 경로를 찾지 못함
[Feature] 외부 skill 버전 drift를 검사함
[Skill] 반복 가능한 저장소 초기화 workflow 제공
[Tool] label catalog를 인증된 gh로 동기화
```

`문제`, `개선`, `테스트`처럼 맥락 없는 제목은 사용하지 않는다.

## 본문 필수 정보

모든 issue는 다음 질문에 답해야 한다.

1. 현재 어떤 문제가 있는가?
2. 누가 또는 어떤 workflow가 영향을 받는가?
3. 원하는 결과는 무엇인가?
4. 범위 밖으로 둘 것은 무엇인가?
5. 완료를 증명할 수 있는 조건은 무엇인가?
6. 권한, 보안, 호환성과 파괴적 동작 위험은 무엇인가?

Bug는 재현 절차, 기대 동작, 실제 동작과 환경을 추가한다. Skill은 trigger와 non-trigger, 대상 agent와 필요한 도구를 추가한다. CLI와 도구는 인터페이스, 지원 플랫폼, 기존 대안과 상태 변경 안전장치를 추가한다.

## Attributes

GitHub에서 추적 가능한 표준 attribute는 label로 표현한다. label 정의의 원본은 `.github/issue-labels.json`이다.

| 차원 | 규칙 | 예시 |
|---|---|---|
| Type | 정확히 하나 | `type: bug`, `type: skill` |
| Area | 주 영역 하나, 필요하면 복수 | `area: skills`, `area: github` |
| Priority | triage 이후 정확히 하나 | `priority: p0` ~ `priority: p3` |
| Status | 열린 issue에 정확히 하나 | `status: triage`, `status: ready` |

### Priority

- `priority: p0`: 데이터 손실, 자격 증명 노출 또는 핵심 배포 중단. 즉시 대응한다.
- `priority: p1`: 핵심 workflow를 막거나 다음 milestone 전에 처리해야 한다.
- `priority: p2`: 기본 우선순위. 계획된 작업에서 처리한다.
- `priority: p3`: 편의 개선이나 장기 후보로, 시간이 허용될 때 처리한다.

### Status lifecycle

```text
status: triage → status: ready → status: in-progress → closed
                         ↘ status: blocked ↗
```

- `triage`: 정보, 중복 여부, type, area와 priority를 검토한다.
- `ready`: 범위와 acceptance criteria가 명확해 구현할 수 있다.
- `in-progress`: 담당자가 실제 작업을 시작했다.
- `blocked`: 구체적인 선행 조건을 issue 본문이나 comment에 기록한다.
- 완료 또는 하지 않기로 결정한 issue는 닫고 status label은 제거한다.

## Triage 절차

1. 중복과 민감 정보 노출 여부를 확인한다.
2. 누락된 재현 정보 또는 완료 조건을 보완한다.
3. type, area, priority와 status label을 지정한다.
4. 범위가 크면 독립적으로 검증 가능한 하위 issue로 나눈다.
5. 구현 결정이 장기 구조에 영향을 주면 `docs/decisions/`에 ADR을 추가한다.

## Capability lifecycle과 issue

Capability의 성숙도와 issue 작업 상태는 다음과 같이 연결합니다.

| Capability 단계 | Issue 상태 | 저장소 산출물 |
|---|---|---|
| Candidate | `status: triage` 또는 `status: ready` | 문제, trigger, 기대 결과와 pilot 조건 |
| In Progress | `status: in-progress` | `skills/<name>/SKILL.md`, `skills/README.md` index 등록 |
| Promoted | acceptance criteria 충족 후 issue 종료 | 동일한 Skill 경로와 검증 근거 |
| Deprecated | 별도 폐기 issue를 종료 | index 상태, 대체 경로 또는 폐기 이유 |

Candidate는 실제 pilot이 시작되기 전까지 Skill 디렉터리를 만들지 않습니다. Promoted와 Deprecated 전환도 경로를 이동하지 않고 `skills/README.md`와 issue 기록만 갱신합니다.

## Label 동기화

GitHub 서비스 변경은 `AGENTS.md` 정책에 따라 인증된 `gh`만 사용한다.

```powershell
gh auth status
python scripts/sync_github_labels.py --repo SWBaek/improvement-ai --dry-run
python scripts/sync_github_labels.py --repo SWBaek/improvement-ai
```

동기화는 catalog에 있는 label을 생성하거나 갱신하며, catalog 밖의 label은 삭제하지 않는다.
