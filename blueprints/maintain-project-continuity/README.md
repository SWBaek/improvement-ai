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
- Work Item을 프로젝트 로컬에서 관리할지, 기존 또는 선택한 GitHub Issues·Jira 같은 외부 tracker와 연동할지에 대한 나의 명시적 선택
- 기존 README, issue, ADR, tracker와 연구 기록의 source-of-truth 대응
- Candidate 보존 위치, Work Item 생성 전 중복·통합 검사와 프로젝트별 ready horizon
- Handoff freshness evidence와 기능 검증 context mode
- 프로젝트 로컬 Profile, record와 Schema 구성
- 인간 승인과 외부 권한 경계
- Brief, Decision, Handoff, Verification Context와 Audit의 검증 방법
- Blueprint Installation Receipt의 프로젝트 로컬 경로
- 생성하거나 변경할 파일

같은 정보를 기존 원본과 새 Continuity record에 중복 관리하지 마세요.
읽기 전용 조사 후 설치안을 작성하기 전에 Work Item 관리 위치를 반드시 질문하세요.
외부 tracker 선택은 계정 설정, 활성화, 인증 또는 쓰기 승인이 아닙니다.
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

## 기존 설치 Migration

이미 이 Blueprint로 생성한 프로젝트 로컬 capability가 있다면 아래 프롬프트를 대상 프로젝트의 AI에게 그대로 전달한다. 이 프롬프트는 특정 과거 revision에 한정하지 않으며, 설치된 exact revision과 최신 exact revision을 비교해 필요한 변경만 제안한다.

```text
현재 프로젝트에 설치된 Maintain Project Continuity capability를 다음
Capability Blueprint의 최신 revision과 비교하고 Migration하세요.

먼저 현재 프로젝트를 읽기 전용으로 조사하세요. 기존 Installation Receipt,
모든 생성 Skill의 provenance, Profile, Schema, record, Handoff, tracker mapping,
Agent instruction과 의도적인 local customization을 확인하세요.
아직 파일, 외부 tracker 또는 다른 상태를 변경하지 마세요.

canonical BLUEPRINT.md path를 마지막으로 변경한 최신 40자리 commit을 확인하고,
설치 Receipt의 revision과 비교하세요. 두 exact-revision URL의 Blueprint를 다시 읽어
semantic difference를 분석하세요. 저장소 HEAD나 다른 경로의 변경을 update로
판정하지 마세요. Receipt가 없으면 기존 provenance와 프로젝트 기록을 근거로
Receipt 생성안부터 제안하고, 확인할 수 없는 revision을 추측하지 마세요.

Migration 제안에는 다음을 포함하세요.

- current, update available 또는 unknown 상태와 그 근거
- 보존할 local customization, stable ID, record history와 authority mapping
- Work Item을 프로젝트 로컬에서 관리할지, 기존 또는 선택한 외부 tracker와
  연동할지에 대한 나의 명시적 선택
- Candidate intake, 기존 Work Item 중복·통합 검사, 새 Work Item 생성 승인과
  프로젝트별 ready horizon
- 완료 조건 충족 시 completion review 절차
- Handoff freshness watermark, durable-event source, Focus divergence Audit와
  canonical state 시각을 projection 생성 시각과 구분하는 방법
- native Decision 상태를 rejected, superseded 또는 extension으로 손실 없이
  매핑하는 방법과 Handoff ownership의 일관성
- independent verification, change-informed regression verification과
  informed verification의 context 경계 및 evidence 기록 위치
- 사람이 읽고 diff하기 쉬운 YAML Profile과 frontmatter로의 영향
- 생성·수정·이전할 프로젝트 로컬 파일, 외부 쓰기, 인간 승인 경계,
  검증 방법, 실패 처리와 rollback

외부 tracker를 선택한 사실을 계정 설정, 활성화, 인증 또는 쓰기 승인으로
간주하지 마세요. 내가 구체적인 Migration 제안을 승인하기 전에는 아무것도
변경하지 마세요. 승인 후에도 승인된 프로젝트 로컬 파일과 별도로 승인된
외부 쓰기만 수행하세요. 사용자 홈, 전역 Agent Skill directory 또는 프로젝트
밖 공유 경로를 만들거나 사용하지 마세요.

대표 Brief, Work Item 생성 gate, Handoff freshness Audit와 Verification Context를
검증하세요. 모든 승인된 변경과 로컬 검증이 성공한 뒤에만 Installation Receipt와
모든 생성 Skill provenance를 최신 revision과 exact source로 함께 갱신하세요.
검증이 실패하거나 Migration이 일부만 적용되면 기존 revision을 유지하고,
부분 적용 상태와 rollback 방법을 보고하세요. 자동 재생성하거나 local
customization을 덮어쓰지 마세요.

Blueprint:
https://github.com/SWBaek/improvement-ai/blob/main/blueprints/maintain-project-continuity/BLUEPRINT.md
```

## 계약과 상태

- Canonical contract: [BLUEPRINT.md](BLUEPRINT.md)
- Status: In Progress
- Tracking: [issue #21](https://github.com/SWBaek/improvement-ai/issues/21)
