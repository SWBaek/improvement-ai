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
- Blueprint Installation Receipt의 프로젝트 로컬 경로
- 생성하거나 변경할 파일

같은 정보를 기존 원본과 새 Continuity record에 중복 관리하지 마세요.
모든 Skill과 지원 자산은 대상 프로젝트 내부에만 설치하세요.
사용자 홈, 전역 Agent Skill directory 또는 프로젝트 밖 공유 경로를 제안하거나 사용하지 마세요.
내가 설치안을 승인하기 전에는 파일을 만들거나 수정하지 마세요.
설치 전 canonical BLUEPRINT.md를 마지막으로 변경한 40자리 commit을 확인하고,
그 exact-revision URL에서 Blueprint를 다시 읽으세요.
생성 결과에는 해당 revision과 exact source를 담은 Installation Receipt를 하나만 남기고,
모든 생성 Skill의 provenance를 그 receipt와 일치시키세요.

Blueprint:
https://github.com/SWBaek/improvement-ai/blob/main/blueprints/maintain-project-continuity/BLUEPRINT.md
```

## 설치 흐름

1. AI가 Blueprint와 대상 프로젝트를 읽기 전용으로 조사한다.
2. AI가 영역별 Integration/Migration과 프로젝트 로컬 설치안을 제안한다.
3. 사람이 설치안을 검토하고 승인한다.
4. AI가 승인된 파일만 생성·이전하고 대표 동작을 검증한다.

이 capability의 생성물은 전역으로 설치할 수 없다. 여러 프로젝트에 적용하려면 각 프로젝트에서 이 설치 흐름을 별도로 수행한다.

프롬프트의 `main` URL은 최신 설계를 찾는 진입점이다. AI는 저장소 HEAD가 아니라 canonical `BLUEPRINT.md`를 마지막으로 변경한 commit을 설치 revision으로 사용한다. 최신 확인도 이 path revision을 Installation Receipt와 비교하며, 다른 문서나 Blueprint 변경은 업데이트로 판정하지 않는다.

## 계약과 상태

- Canonical contract: [BLUEPRINT.md](BLUEPRINT.md)
- Status: In Progress
- Tracking: [issue #21](https://github.com/SWBaek/improvement-ai/issues/21)
