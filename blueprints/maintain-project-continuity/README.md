# Maintain Project Continuity

세션, Agent 또는 모델이 바뀌어도 프로젝트의 열린 작업, 결정, 근거와 정확한 재개 지점을 프로젝트 소유 기록으로 복구하도록 로컬 capability를 생성한다.

이 README는 사람을 위한 설치 안내다. 규범적 계약은 [BLUEPRINT.md](BLUEPRINT.md)이며, 여기서 말하는 설치는 공통 package를 복사하는 것이 아니라 대상 프로젝트에 맞는 Skill, 기록과 Schema를 AI가 생성하는 과정이다.

## 이런 경우에 사용한다

- GitHub·GitLab issue 없이 로컬 또는 비공개 프로젝트를 운영한다.
- 장기 유지보수나 연구 작업을 여러 세션·Agent·모델 사이에서 이어가야 한다.
- 기존 README, issue, ADR과 연구 기록을 유지하거나 일부 영역만 새 체계로 이전하고 싶다.

## 설치

아래 프롬프트를 대상 프로젝트에서 작업 중인 AI에게 그대로 전달한다.

```text
현재 프로젝트에 다음 Capability Blueprint를 설치하세요.

먼저 Blueprint와 현재 프로젝트를 읽기 전용으로 조사하세요.
세션, Agent 또는 모델이 바뀌어도 작업을 이어갈 수 있는
프로젝트 로컬 continuity capability의 설치안을 제안하세요.

설치안에는 다음을 포함하세요.

- 생성할 Skill의 이름, trigger, 책임과 프로젝트 로컬 경로
- Project Brief, Work Item, Decision, Knowledge/Evidence와 Handoff 영역별 Integration 또는 Migration 선택
- 기존 README, issue, ADR, tracker와 연구 기록의 source-of-truth 대응
- 프로젝트 로컬 Profile, record와 Schema 구성
- 인간 승인과 외부 권한 경계
- Brief, Decision, Handoff와 Audit의 검증 방법
- 생성하거나 변경할 파일

같은 정보를 기존 원본과 새 Continuity record에 중복 관리하지 마세요.
내가 설치안을 승인하기 전에는 파일을 만들거나 수정하지 마세요.

Blueprint:
https://github.com/SWBaek/improvement-ai/blob/main/blueprints/maintain-project-continuity/BLUEPRINT.md
```

## 설치 흐름

1. AI가 Blueprint와 대상 프로젝트를 읽기 전용으로 조사한다.
2. AI가 영역별 Integration/Migration과 프로젝트 로컬 설치안을 제안한다.
3. 사람이 설치안을 검토하고 승인한다.
4. AI가 승인된 파일만 생성·이전하고 대표 동작을 검증한다.

최신 설계는 프롬프트의 `main` URL을 사용한다. 재현 가능한 설치에는 `main`을 정확한 40자리 commit으로 교체한다. `main`에서 시작해도 생성 Skill에는 실제 사용한 exact revision이 기록되어야 한다.

## 계약과 상태

- Canonical contract: [BLUEPRINT.md](BLUEPRINT.md)
- Status: In Progress
- Tracking: [issue #21](https://github.com/SWBaek/improvement-ai/issues/21)
