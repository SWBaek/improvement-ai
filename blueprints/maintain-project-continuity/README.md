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

- 생성할 Skill의 이름, trigger, non-trigger, 책임과 프로젝트 로컬 경로
- 일반 질의에는 개입하지 않으면서 durable work 전에 Brief로 연결하는 최소한의
  always-on Agent instruction
- Project Brief, Work Item, Decision, Knowledge/Evidence와 Handoff 영역별 Integration 또는 Migration 선택
- Work Item을 프로젝트 로컬에서 관리할지, 기존 또는 선택한 GitHub Issues·Jira 같은 외부 tracker와 연동할지에 대한 나의 명시적 선택
- 기존 README, issue, ADR, tracker와 연구 기록의 source-of-truth 대응
- Candidate 보존 위치, Work Item 생성 전 중복·통합 검사와 프로젝트별 ready horizon
- 프로젝트 전역 lock이 아닌 세션별 Session Focus, 같은 브랜치의 병렬 Agent와
  working-tree overlap을 처리하는 방법
- 하나의 authoritative Handoff 위치, 명시적인 `no current checkpoint` 상태, bounded checkpoint와 새 세션의 freshness 검증 및 기능 검증 context mode
- 프로젝트 로컬 Profile, record와 Schema 구성
- 인간 승인과 외부 권한 경계
- Brief, durable-work entry, Decision, Handoff, Verification Context와 Audit의 검증 방법
- Blueprint Installation Receipt의 프로젝트 로컬 경로
- 생성하거나 변경할 파일

같은 정보를 기존 원본과 새 Continuity record에 중복 관리하지 마세요.
읽기 전용 조사 후 설치안을 작성하기 전에 Work Item 관리 위치를 반드시 질문하세요.
외부 tracker 선택은 계정 설정, 활성화, 인증 또는 쓰기 승인이 아닙니다.
다른 Agent가 재개·검증하기 위해 objective, 완료 조건, 현재 위치 또는 evidence가
필요한 변경, 재사용 가능한 조사·결론이나 의미 있는 다단계 작업은 durable work로
보고 변경 전에 Brief를 수행하세요. 일반 질의, 쉽게 다시 확인할 수 있는 읽기 전용
점검, 일시적 메모와 원자적인 의미 보존 수정은 제외하세요. 일치하는 committed Work
Item이 없으면 읽기 전용 조사와 update, Candidate, 통합 또는 생성안을 제시한 뒤
필요한 인간 승인과 외부 쓰기 승인을 기다리고, 그 전에는 프로젝트를 변경하지 마세요.
Session Focus는 각 Agent 세션에 속하며, 여러 세션이 같은 브랜치에서 서로 다른
Work Item을 선택할 수 있습니다. 전역 Focus나 Agent registry를 만들지 마세요.
Handoff checkpoint는 인계 대상으로 선택한 한 세션의 Focus만 담고 다른 active
Work Item이나 병렬 세션을 취소·대체하지 않게 하세요. 나머지 현재 위치는 각 Work
Item에서 복구하고 병렬 checkpoint나 세션 archive를 만들지 마세요.
canonical Handoff 위치에는 명시적인 빈 상태 또는 내가 확정한 checkpoint 하나만
두세요. 실제 빈 파일이나 placeholder를 빈 상태로 사용하거나 checkpoint 내용을
임의로 만들지 마세요. checkpoint의 생성·교체·제거는 내가 요청하거나 제안된
초안을 확정한 때에만 수행하고, 새 세션에서는 authoritative source와 대조하기
전에 checkpoint를 신뢰하지 마세요. 유효한 빈 상태는 `no current checkpoint`로
보고하고 authoritative Work Item과 Decision에서 다음 작업을 제안하세요. 최초
설치안에 명시한 빈 상태는 내가 그 설치안을 승인하면 생성할 수 있습니다.
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
Agent instruction, Skill trigger와 non-trigger, working tree, 기존 Focus 표현,
동시 Agent 사용 방식과 의도적인 local customization을 확인하세요.
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
- durable work와 제외 대상을 구분하고 변경 전에 Brief로 연결하는 최소 always-on
  Agent instruction 및 Skill trigger
- 프로젝트 전역 lock이 아닌 세션별 Focus, 같은 브랜치에서 서로 다른 Work Item을
  선택한 병렬 세션, 기존 dirty path 관찰과 overlap 처리
- 완료 조건 충족 시 completion review 절차
- 하나의 authoritative Handoff 위치와 실제 빈 파일·placeholder가 아닌 명시적인
  `no current checkpoint` 표현, 선택된 한 세션의 인계 범위와 checkpoint
  생성·교체·제거의 요청·확정 경계
- checkpoint에만 bounded content와 freshness watermark를 요구하고, 새 세션에서
  authoritative source를 대조해 `verified current`, `stale`, `unknown`을 판정하며
  빈 상태에서는 freshness label을 적용하지 않는 방법
- durable-event source, Focus divergence Audit와 canonical state 시각을
  projection 생성 시각과 구분하는 방법
- 빈 Handoff에서도 non-ignored tracked/untracked working tree와 unscoped durable
  work를 계속 검사하고, 의미 있는 Focus 없는 변경을 clean/`OK`가 아닌
  `needs attention`으로 보고하는 방법
- Candidate, Knowledge/Evidence와 Handoff의 요약 write authority가 세부 인간 승인
  정책보다 넓지 않음을 확인하는 방법
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

기존 Handoff를 다음과 같이 구분하고 각 처리안을 제시하세요.

- 사람이 확정한 실제 checkpoint는 보존하고 freshness를 검증합니다.
- template, placeholder 또는 임의 생성 요약은 명시적 빈 상태로 바꾸도록 제안합니다.
- 누적 이력형 record는 Work Item, Decision, Git 또는 tracker에서 고유 사실의
  권위 있는 원본을 모두 확인한 뒤 bounded checkpoint 또는 빈 상태를 제안합니다.
- 의도나 고유 사실을 판별할 수 없으면 unresolved로 보고하고 사람의 결정을 기다립니다.

승인 전에는 기존 Handoff를 변경하지 말고 자동으로 삭제·축약·clear하거나 현재
상태를 추측하지 마세요. Migration 제안에는 Handoff 표현, Skill trigger,
checkpoint에만 필수 필드를 요구하는 Schema 검증, Brief와 Audit 동작, clear 권한,
실패 처리와 rollback을 포함하세요.

기존의 프로젝트 전역 Focus 표현은 세션별 Focus로 바꾸는 안을 제시하되 Work Item,
Handoff 또는 dirty work를 자동으로 재귀속하지 마세요. 기존 dirty work, 누락된
Evidence나 Candidate는 unresolved migration input으로 보고 authoritative Work Item,
기록 또는 유지·통합안을 제시한 뒤 사람의 결정을 기다리세요. Agent/session registry나
세션별 Handoff archive를 새로 만들지 마세요.

Continuity를 언급하지 않은 durable research 요청과 non-trigger 대조군, Work Item
생성 gate, 서로 다른 Work Item을 선택한 같은 브랜치의 병렬 세션과 overlap 경고,
checkpoint 유지, 명시적 checkpoint 제거, 빈 상태에서 `no current checkpoint`를
보고하면서 working tree Audit을 계속하는 동작, 새 세션 freshness 검증 및
Verification Context를 확인하세요. 모든 승인된 변경과 로컬 검증이 성공한 뒤에만 Installation Receipt와
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
