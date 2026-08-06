# Human Review Artifacts Adoption Guide

이 문서는 Core 0.3을 처음 외부 프로젝트에 적용하기 전에 사용하는 integration 계약입니다. Framework는 외부 프로젝트의 domain 모델이나 Authoring SSOT를 소유하지 않습니다.

## 권위 경계

```text
Project Authoring SSOT
        │
        ▼
Project-owned adapter
        │
        ▼
Core 0.3 HTML Review Snapshot
        │
        ▼
Review Response 0.2
        │
        ▼
Project model / decision / work item update
```

- 프로젝트는 JSON, DSL, 코드 또는 문서 등 자신의 Authoring SSOT를 유지합니다.
- adapter는 프로젝트가 소유하며 framework 계약을 소비합니다.
- 생성된 HTML의 semantic content는 해당 revision에서 사람이 검토한 표현입니다.
- Review Response는 자동으로 프로젝트 상태를 변경하지 않습니다. AI 또는 프로젝트 도구가 검증 후 명시적인 변경으로 반영합니다.

## 적용 절차

### 1. Artifact 필요 여부 판단

[`research/artifact-trigger.md`](research/artifact-trigger.md)의 생성 조건을 확인합니다. 하나의 human goal, target, context, allowed action과 완료 조건을 정할 수 없으면 대화를 계속합니다.

### 2. Interaction Pattern 선택

| 목표 | Pattern |
|---|---|
| 범위와 현재 상태 이해 | `orient@0.1` |
| 공통 기준으로 대안 평가 | `compare@0.1` |
| 채택·거부·보류·변경 요청 | `decide@0.1` |
| 피드백 반영 확인 | `revise@0.1` |
| 기준과 증거로 결과 판단 | `verify@0.1` |

한 Artifact에는 하나만 선택합니다. 여러 목표가 있으면 revision이나 별도 Artifact로 나눕니다.

### 3. Component 조합

[`components/README.md`](components/README.md)의 필수 component를 semantic HTML로 작성합니다. 프로젝트 vocabulary는 본문과 `profiles` 또는 `extensions`에 두고 Core나 Interaction 이름으로 만들지 않습니다.

### 4. Snapshot 생성

- `id`는 논의 대상의 수명 동안 안정적으로 유지합니다.
- 의미 있는 변경마다 `revision`을 증가시킵니다.
- 입력 파일은 secret이나 개인 절대 경로 없이 stable ID와 digest로 기록합니다.
- runtime을 사용할 경우 pinned framework checkout의 참조 runtime을 그대로 포함하고 digest와 CSP hash를 계산합니다.
- 외부 network 자원은 포함하지 않습니다.

첫 pilot에서는 framework source를 consumer 저장소에 복사해 독립 원본으로 만들지 않습니다. 프로젝트 adapter는 고정한 framework commit을 기록하고 checkout된 template, catalog와 validator를 사용합니다. 배포 결과인 self-contained HTML은 프로젝트에 보존할 수 있습니다.

### 5. Artifact 검증

```powershell
python <framework-root>/scripts/validate_artifact.py <artifact.html>
python <framework-root>/scripts/validate_interaction.py <artifact.html>
```

두 명령이 모두 성공해야 사람에게 전달합니다. warning은 의미를 이해하고 기록한 뒤에만 허용합니다.

### 6. Response 처리

사람이 복사하거나 다운로드한 Response를 원 Artifact와 함께 검증합니다.

```powershell
python <framework-root>/scripts/validate_review_response.py <response.json> --artifact <artifact.html>
```

검증 후 action을 프로젝트의 명시적인 후속 변경으로 변환합니다.

- `acknowledge`: 이해 상태만 기록
- `select`, `rank`: 선호 또는 선택 입력으로 사용
- `approve`, `reject`, `defer`: 상태 전환 후보
- `request-changes`, `challenge`, `comment`, `answer`: 모델 또는 작업 변경 입력

Response 자체를 결정으로 간주하지 않습니다. 프로젝트가 요구하는 Decision Log, issue 또는 Authoring SSOT 변경 절차를 따릅니다.

### 7. 새 revision 검토

변경된 내용은 기존 HTML을 덮어쓰는 대신 새 revision으로 생성합니다. 이전 Response는 revision 교차 검증에 실패해야 하며 새 Artifact에 재사용하지 않습니다.

## 첫 pilot에서 만들지 않는 것

- framework 소스의 project-local fork
- 범용 renderer CLI 또는 npm package
- project vocabulary를 포함한 Core 변경
- 자동 Response 전송이나 자동 승인
- 여러 interaction을 한 화면에 합친 dashboard

반복되는 adapter 코드가 두 번째 외부 프로젝트에서도 확인된 뒤 package 또는 Agent Skill 승격을 검토합니다.

## Pilot 준비 체크리스트

- framework commit을 고정했는가?
- Authoring SSOT와 generated HTML 경계가 문서화됐는가?
- 하나의 primary pattern을 선택했는가?
- target ID와 revision 정책이 있는가?
- Core와 Interaction validator가 통과하는가?
- Response를 반영할 프로젝트 절차가 있는가?
- 기존 구현의 정보 동등성과 rollback 경로가 있는가?
