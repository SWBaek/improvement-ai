# Evidence-Grounded AGENTS.md Evolution

## Status

- State: `Exploring`
- Last reviewed: 2026-08-25
- Next trigger: `manage-workspace-agents-md`의 고정 revision을 기준 구현으로 삼아 성숙도가 다른 두 실제 저장소에서 read-only 감사를 시작하고, 발견사항의 채택·기각 사유와 최종 목적지를 비교할 때 갱신한다.

이 문서는 `AGENTS.md`를 한 번 잘 작성하는 방법보다, 프로젝트 변화와 실제 Agent 실패를 근거로 지속적으로 감사하고 개선하는 capability 가설을 탐색한다. 아직 Candidate issue, Capability Blueprint, 설치형 Skill, 구현 사양 또는 자동 수정 정책이 아니다.

공개 저장소 사례는 직접 연결한다. 비공개 저장소에서 얻은 관찰은 저장소명, 경로, 버전, 원문 지침과 업무 데이터를 공개하지 않고 일반화했다.

## 문제와 배경

AI-native 개발에서는 `AGENTS.md`가 단순한 안내 문서가 아니라 Agent의 탐색 순서, 변경 경계, 검증 방식과 인간 승인 지점을 결정하는 운영 제어면이 된다. 프로젝트가 진행되면서 사람과 Agent는 실패를 막기 위해 규칙을 계속 추가한다. 그러나 시간이 지나면 다음 문제가 생긴다.

- 실제 코드, CI, architecture, dependency와 지침이 달라진다.
- 동일한 사실이 `AGENTS.md`, README, CONTRIBUTING, architecture 문서와 도구별 instruction에 중복된다.
- lint나 test로 강제할 수 있는 규칙이 자연어에만 남는다.
- 한 세션의 실수나 일시적인 도구 장애가 영구 규칙으로 승격된다.
- 이미 사라진 대상이 “하지 말 것”이라는 부정형 규칙으로 계속 남는다.
- 범용 generator가 저장소 고유의 안전 경계와 domain rationale를 일반적인 짧은 템플릿으로 덮어쓴다.
- 반대로 보수적인 Agent는 stale 지침을 지우지 못하고 계속 덧붙인다.

따라서 핵심 질문은 다음과 같다.

> AI가 저장소 근거와 반복된 실패를 사용해 `AGENTS.md`를 개선하되, 근거 없는 규칙을 만들거나 중요한 경계를 삭제하거나 스스로 조용히 운영 정책을 바꾸지 않게 하려면 어떤 capability가 필요한가?

이 문제는 “좋은 템플릿”만으로 풀리지 않는다. 신규 저장소의 첫 작성, 이미 정리된 저장소의 정합성 감사, 세션 실패에서 개선 후보를 찾는 회고, 자연어 규칙을 실행 가능한 gate로 옮기는 작업은 서로 다른 작업이다.

## 현재 관찰

### 1. 품질 문제는 크기보다 정합성과 신호 밀도다

[`AGENTS.md` 크기 지침 조사](../research/agents-md-size-guidance.md)는 5KB, 60줄 같은 숫자가 공통 표준이 아니며, 제품의 잘림 한도와 품질 권장을 구분해야 한다고 정리한다. 항상 로드되는 파일은 작을수록 유리하지만, 길다는 이유만으로 domain invariant를 삭제할 수는 없다.

좋은 파일은 단순히 짧은 파일이 아니라 다음 특성을 가진다.

- 실제 존재하는 경로와 명령만 적는다.
- repository-wide invariant와 path-specific procedure를 구분한다.
- canonical source를 복제하지 않고 정확히 연결한다.
- 변경 시 함께 갱신해야 할 code, schema, fixture, docs와 test를 알려 준다.
- 기계적으로 강제 가능한 규칙은 lint, test, schema나 repository checker가 소유한다.
- 현재 작업에만 해당하는 사건을 영구 정책으로 만들지 않는다.

### 2. 개선 후보의 목적지는 `AGENTS.md` 하나가 아니다

세션에서 발견한 문제를 모두 `AGENTS.md`에 넣으면 파일은 실패 로그와 금지 목록이 된다. 같은 관찰이라도 권위와 지속성에 따라 목적지가 달라진다.

| 관찰 유형 | 우선 검토할 목적지 |
|---|---|
| 실행 가능한 architecture boundary | lint, structural test, repository checker |
| persisted format 또는 public contract | schema, validator, contract test, canonical documentation |
| 장기 architecture 결정 | ADR 또는 architecture 문서 |
| 기여·릴리스·보안 절차 | CONTRIBUTING, SECURITY, focused workflow document |
| 특정 subtree에만 필요한 durable rule | nested `AGENTS.md` 또는 해당 Agent가 실제로 읽는 scoped instruction |
| 대부분의 작업에 필요한 Agent-only invariant | root `AGENTS.md` |
| 반복 가능한 특정 작업 절차 | project-local Skill 후보 |
| 일시적인 장애, 단일 실수, 현재 작업 상태 | 영구 기록하지 않음 |

핵심은 먼저 “어디에 쓸 것인가”가 아니라 “누가 이 진실을 소유해야 하는가”를 판단하는 것이다.

### 3. `AGENTS.md` 자기 수정은 영향 반경이 크다

일반 코드의 잘못된 한 줄은 일부 경로에만 영향을 줄 수 있지만, 잘못된 always-on 지침은 이후 모든 Agent 세션에 반복적으로 영향을 준다. Agent가 자신의 실패를 근거로 즉시 새 규칙을 추가하면 다음과 같은 순환이 가능하다.

```text
일회성 실패
  → 과도한 금지 규칙 추가
  → 이후 작업에서 불필요한 회피
  → 회피를 보정하는 새 규칙 추가
  → 지침 간 충돌과 context 증가
```

따라서 탐색과 제안은 자동화할 수 있어도, durable guidance의 materialization은 인간 승인 경계로 남겨야 한다는 가설이 강하다.

### 4. 삭제와 개선은 같은 문제가 될 수 있다

[`Subtractive Edit Fidelity`](subtractive-edit-fidelity.md)의 관찰처럼, 오래된 규칙을 제거하라는 요청이 반대 의미의 새 규칙이나 “이제 사용하지 않는다”는 부재 서술로 남을 수 있다. `AGENTS.md` 관리 capability는 추가뿐 아니라 다음을 검증해야 한다.

- 폐기 대상의 주제가 최종 파일에 다른 극성으로 남지 않았는가?
- 삭제 이유가 항상 로드되는 금지 문장으로 재등장하지 않았는가?
- historical context가 필요하다면 ADR이나 Git history로 이동했는가?

### 5. 저장소 성숙도에 따라 같은 요청의 답이 달라진다

#### 사례 A: domain-heavy 비공개 저장소

한 비공개 저장소의 root `AGENTS.md`는 비교적 길지만, 원본 evidence의 우선순위, immutable artifact, source identity, 지원 input contract, 선제적 abstraction 금지 같은 domain safety boundary를 담고 있었다. 일반적인 “60줄 이하” 재작성은 중복만 줄이는 것이 아니라 제품 위험 모델을 지울 가능성이 있었다.

이 사례에서 적합한 개입은 전체 재생성이 아니었다.

- repository truth와의 `Alignment` 감사
- exact version과 상세 rationale를 canonical contract로 보내는 최소 Patch
- path, command, decision ID, duplicated version처럼 결정적으로 검증 가능한 항목의 repository check
- 실제 반복 실패가 확인되기 전에는 새 prohibition을 추가하지 않음

#### 사례 B: 공개 `sdoc-editor`

[`sdoc-editor`의 현재 `AGENTS.md`](https://github.com/SWBaek/sdoc-editor/blob/main/AGENTS.md)는 repository map, global invariant와 workflow pointer에 집중한다. 세부 검증 계약은 [`CONTRIBUTING.md`](https://github.com/SWBaek/sdoc-editor/blob/main/CONTRIBUTING.md)에 있고, `package.json`의 `verify:*` script와 repository checker가 실행 가능한 진실을 소유한다.

이 구조는 처음부터 완성된 것이 아니다. [이슈 #209](https://github.com/SWBaek/sdoc-editor/issues/209)는 architecture 문서의 version drift, React runtime 설명의 drift, ADR ID 중복, prose rule과 ESLint 강도의 불일치, 분산된 검증 계약을 기록했다. [PR #211](https://github.com/SWBaek/sdoc-editor/pull/211)은 `AGENTS.md`를 더 늘리는 대신 다음 방향을 택했다.

- current-state 문서를 evergreen wording으로 변경
- enforceable invariant를 repository checker와 ESLint로 이동
- `verify:*` 명령을 canonical verification API로 통합
- root `AGENTS.md`를 map, invariant와 pointer로 축소
- Copilot-specific personal preference와 중복 guidance 제거

또한 [이슈 #164](https://github.com/SWBaek/sdoc-editor/issues/164)는 project-specific architect, reviewer, verifier orchestration이 단순 작업에도 delegation, 대기와 비용을 유발해 제거된 사례다. 따라서 이 저장소에 다시 복잡한 “AGENTS 개선 Agent 조직”을 넣는 것은 과거 실패를 반복할 수 있다.

이 사례에서 적합한 개입은 재생성이 아니라 audit-only와 기존 repository checker의 제한적 확장이다. 아무 변경도 권고하지 않는 결과도 성공일 수 있다.

두 사례의 대비는 capability가 하나의 스타일을 강제해서는 안 된다는 점을 보여 준다. 성숙한 저장소에는 보존과 정합성 확인이, 신규 또는 무질서한 저장소에는 bootstrap과 구조화가 필요하다.

## 기존 접근에서 얻을 수 있는 구성 요소

아래 도구는 경쟁 순위가 아니라 현재 공개된 접근의 서로 다른 부분을 보여 준다. 내용은 2026-08-25에 확인한 공개 문서를 요약한 것이며 템플릿이나 구현을 복사하지 않았다.

| 접근 | 강점 | 이 Idea에서 남는 질문 |
|---|---|---|
| [Sentry `agents-md`](https://github.com/getsentry/skills/blob/main/skills/agents-md/SKILL.md) | manifest, CI, docs를 먼저 조사하고 실제 경로·명령만 쓰며 작은 root/nested guide를 지향 | 60줄 목표와 기본 섹션이 domain-heavy 저장소에도 적합한가. 기존 safety rationale를 언제 보존해야 하는가. |
| [`manage-workspace-agents-md`](https://github.com/stayhydated/skills/blob/master/skills/manage-workspace-agents-md/SKILL.md) | Draft, Patch, Audit, Alignment를 분리하고 repository evidence와 최소 수정을 강조 | 세션 실패의 반복성 판단, rule destination routing과 실행 가능한 gate 승격까지 어디서 담당할 것인가. |
| [Netresearch `agent-rules`](https://github.com/netresearch/agent-rules-skill/blob/main/skills/agent-rules/SKILL.md) | project/scoped detection, command·CI·architecture extraction, freshness와 content verification을 script로 제공 | 지원 stack과 template가 저장소 구조를 과도하게 정규화하지 않는가. script/harness 유지비가 실제 실패 근거보다 커질 수 있는가. |
| [Netresearch `retro`](https://github.com/netresearch/retro-skill/blob/main/skills/retro/SKILL.md) | 세션 friction과 reusable learning을 찾아 여러 destination으로 분류하고 proposal별 승인을 요구 | Claude Code 중심의 session workflow를 Codex와 다른 Agent에 어떻게 일반화할 것인가. private transcript 없이 어떤 evidence로 반복성을 판단할 것인가. |

현재 가설은 이들 중 하나를 그대로 채택하는 것이 아니라 다음 조합이 필요하다는 것이다.

- generator의 repository inspection
- auditor의 evidence classification과 최소 Patch
- scripted checker의 deterministic verification
- retrospective의 destination routing과 인간 승인

### 첫 Pilot 기준 구현 선택

2026-08-25의 탐색 단계 운영 선택으로, 새 Skill을 먼저 만들지 않고
[`manage-workspace-agents-md`](https://github.com/stayhydated/skills/blob/a23fa326af472a5beedeec3e42a954037ee79222/skills/manage-workspace-agents-md/SKILL.md)를
첫 read-only 감사의 기준 구현으로 사용한다. 이 선택은 새 capability의 채택 결정,
Blueprint 계약 또는 이 저장소가 배포할 Skill을 뜻하지 않는다.

- 비교 가능한 결과를 위해 위 exact revision을 두 실제 저장소에서 동일하게 사용한다.
- Skill을 이 저장소로 복사하거나 설치하지 않고, Pilot 대상이 소유하는 프로젝트 로컬
  환경에서만 사용한다.
- 기존 Skill의 Draft, Patch, Audit, Alignment, evidence 분류와 최소 수정 절차를 먼저
  재사용한다.
- retrospective intake, `AGENTS.md` 밖의 durable destination routing, finding별 인간
  승인과 fresh-context 전후 평가가 실제로 부족한지 관찰한다.
- 기존 Skill만으로 required outcome이 충족되면 새 Skill을 만들지 않는다. 같은 공백이
  서로 다른 저장소에서 반복될 때만 upstream 기여, 작은 보완 Skill 또는 별도
  Capability Blueprint를 비교한다.

## 현재 capability 가설

가칭 **Evidence-Grounded AGENTS.md Evolution**은 `AGENTS.md` generator보다 repository guidance auditor에 가깝다. 한 번에 파일을 다시 쓰기보다 다음 폐루프를 수행한다.

```text
Repository truth + confirmed friction
  → maturity와 scope 판정
  → claim evidence 분류
  → durable destination 분류
  → read-only findings와 최소 변경안
  → 인간 승인
  → Patch 또는 executable gate 승격
  → repository-native verification
  → fresh-context 평가
```

### 1. 작업 모드를 먼저 선택한다

가능한 모드는 아직 확정 계약이 아니지만 최소한 다음 역할을 구분해야 한다.

- **Bootstrap:** 적절한 guide가 없는 신규·초기 저장소에서 첫 파일을 제안
- **Audit:** 기존 guide의 오류, 중복, 모호성, 과도한 범위를 보고
- **Alignment:** code, manifest, docs, CI, tests와 guide의 drift를 대조
- **Retrospective intake:** 반복 실패와 사용자 정정에서 개선 후보를 수집
- **Patch:** 승인된 finding만 최소 diff로 반영

기본값은 기존 파일이 있으면 Audit 또는 Alignment이며, 명시적인 요청 없이 full rewrite를 선택하지 않는 편이 안전하다.

### 2. 모든 claim에 근거 수준을 붙인다

- **Observed:** 파일, 명령, test, schema, CI, issue나 승인된 decision에서 직접 확인됨
- **Inferred:** 반복되는 구조와 ownership에서 강하게 추론되지만 명시 계약은 아님
- **Proposed:** 개선 가설이며 현재 repository truth가 아님

`AGENTS.md`에 자동으로 들어갈 수 있는 것은 Observed와 충분히 검토된 Inferred뿐이다. Proposed는 audit report나 issue에 남아야 한다.

### 3. 반복성보다 권위를 먼저 판단한다

같은 실패가 두 번 발생했다는 사실만으로 root rule이 되지는 않는다. 먼저 다음을 묻는다.

1. 이 사실의 canonical owner는 code, schema, test, ADR, CONTRIBUTING, Skill 중 무엇인가?
2. 대부분의 작업에서 항상 필요한가, 특정 path나 task에만 필요한가?
3. 기계적으로 검출할 수 있는가?
4. 지침이 없으면 실제로 잘못된 변경을 반복할 가능성이 있는가?
5. 이 규칙은 현재 존재하는 위험을 설명하는가, 이미 사라진 대상을 금지형으로 보존하는가?

반복 횟수 2회는 유용한 heuristic일 수 있지만 고정 계약으로 두기에는 근거가 부족하다. 승인된 ADR, PR review의 재발 방지 요구, canonical source와의 명백한 drift는 한 번만으로도 조치 근거가 될 수 있다.

### 4. 가능한 규칙은 실행 가능한 gate로 승격한다

다음은 natural-language rule보다 checker가 더 적합하다.

- 존재하지 않는 command와 path
- duplicate decision ID
- broken local link와 anchor
- configured dependency와 current-state 문서의 version drift
- forbidden import direction
- generated artifact 직접 수정
- CI와 local verification command의 불일치

반대로 제품 mission, 인간 승인 경계, evidence 우선순위, 선제적 abstraction 금지처럼 의미 판단이 필요한 원칙은 `AGENTS.md`나 canonical architecture 문서에 남을 수 있다.

### 5. 인간 승인은 변경 단위로 받는다

한 번의 “전체 개선 승인”보다 finding별 승인이 적절하다는 가설이다. 각 proposal은 최소한 다음을 보여 줘야 한다.

- 원문 claim과 적용 scope
- repository evidence
- 발견된 drift 또는 반복 실패
- 선택한 destination과 대안
- 삭제·이동·추가되는 최소 diff
- 실행할 validation
- 남는 불확실성

AI가 조용히 self-modify하거나 세션 종료 hook이 자동 commit하는 방식은 기본값으로 두지 않는다.

## 기대 효과

- `AGENTS.md`가 실패 로그와 금지 목록으로 비대해지는 것을 줄인다.
- repository truth와 지침의 drift를 조기에 찾는다.
- enforceable rule을 CI와 test로 옮겨 Agent 종류에 관계없이 적용한다.
- 신규 저장소와 성숙한 저장소에 다른 개입을 선택한다.
- domain-heavy safety boundary를 단순한 line budget 때문에 잃지 않는다.
- 일회성 도구 장애나 특정 Agent의 특이 실패가 영구 정책으로 굳는 것을 막는다.
- 변경하지 않는 것이 최선인 저장소를 정상적으로 판정한다.

## 비목표

- 모든 저장소에 동일한 5KB, 60줄 또는 section template를 강제하지 않는다.
- 매 세션 종료 시 `AGENTS.md`를 자동 수정하지 않는다.
- project-specific architect, reviewer, verifier orchestration을 기본 구성으로 만들지 않는다.
- 자연어 의미 비교를 required CI의 비결정적 LLM gate로 넣지 않는다.
- `AGENTS.md`, `CLAUDE.md`, Copilot instructions와 Cursor rules가 서로의 내용을 자동으로 읽는다고 가정하지 않는다.
- 다른 Agent platform의 파일을 무조건 symlink하거나 동일 내용으로 복제하지 않는다.
- architecture, CONTRIBUTING, ADR, schema와 test를 `AGENTS.md`로 대체하지 않는다.
- 사용자 홈이나 전역 memory에 project-specific rule을 자동 저장하지 않는다.
- 현재 Idea 단계에서 Skill, script, schema, generator 또는 Blueprint directory를 구현하지 않는다.

## 위험과 반례

### 과도한 축약

중복처럼 보이는 문장이 실제로는 다른 위험 경계에서 의도적으로 반복될 수 있다. safety-critical rationale나 negative constraint는 단순 text similarity로 삭제하면 안 된다.

### 과도한 기계화

저장소마다 bespoke checker를 추가하면 유지비가 커진다. 실제 재발 위험보다 checker code와 fixture가 더 복잡해질 수 있다. deterministic check는 작은 범위부터 시작해야 한다.

### retrospective 과적합

특정 모델, 도구 장애, 로컬 환경이나 한 사람의 작업 스타일에서만 발생한 실패가 일반 project invariant로 잘못 승격될 수 있다. raw transcript의 수집은 privacy와 보존 문제도 만든다.

### platform compatibility 오판

Codex, Claude Code, Copilot, Cursor는 instruction discovery와 precedence가 다를 수 있다. 한 platform의 scoped file을 다른 Agent가 읽을 것이라고 가정하면 중요한 규칙이 적용되지 않는다. 반대로 모든 파일에 복제하면 drift가 증가한다.

### 감사 결과의 권위 오판

코드가 현재 동작을 보여 주더라도 의도된 architecture를 항상 뜻하지는 않는다. 오래된 구현을 repository truth로 잘못 승격할 수 있으므로 accepted ADR, public contract와 maintainer 판단이 우선할 수 있다.

### 측정 지표의 왜곡

파일 크기 감소, rule 수 감소, finding 수 증가는 품질 자체가 아니다. 중요한 기준은 잘못된 변경, 재질문, 재시도와 false validation이 실제로 줄었는지다.

## 첫 검증 가설

### Phase 1: 동일한 read-only audit

성숙도가 다른 두 저장소에 같은 상위 절차를 적용한다.

1. top-level tree, root와 nested guidance, manifest, lockfile, CI, canonical docs, tests를 조사한다.
2. 현재 `AGENTS.md` claim을 evidence와 scope에 매핑한다.
3. 각 finding을 `keep`, `patch`, `move`, `mechanize`, `drop`, `not enough evidence`로 제안한다.
4. 실제 파일은 수정하지 않고 maintainer가 finding별로 채택·기각한다.

성공 신호는 두 저장소에 같은 결과를 강제하지 않는 것이다.

- domain-heavy 저장소에는 보존 중심의 Alignment와 작은 중복 제거를 권고한다.
- 이미 얇고 executable harness가 있는 저장소에는 Audit only 또는 checker의 제한적 개선을 권고한다.
- 존재하지 않는 path와 command를 만들지 않는다.
- private source의 원문과 식별 정보를 audit report 밖으로 유출하지 않는다.

### Phase 2: 승인된 최소 개선

각 저장소에서 승인된 finding만 반영하고 repository-native verification을 실행한다. 변경이 없는 저장소는 그대로 종료할 수 있다.

관찰할 항목:

- root guidance byte와 줄 수보다 canonical source duplication이 줄었는가
- broken path, stale command, duplicate version 같은 결정적 drift가 제거되었는가
- enforceable prose가 checker로 이동했는가
- 중요한 domain boundary가 유지되었는가
- Agent가 검증하지 않은 command를 통과했다고 쓰지 않았는가

### Phase 3: fresh-context task 비교

대표 작업을 새 context의 Agent에게 수정 전후로 수행하게 하고 다음을 비교한다.

- 잘못된 경로 또는 ownership 선택
- 필요한 canonical 문서 누락
- 사용자 재질문과 정정 횟수
- 실패한 command 재시도
- unrelated change와 overreach
- 완료 시 실제 validation과 보고의 일치

작은 표본에서 수치가 좋아졌다고 일반화하지 않고, 어떤 rule 또는 gate가 어떤 실패를 줄였는지 추적한다.

## 열린 질문

1. 오래된 prohibition residue와 여전히 필요한 safety constraint를 어떻게 구분할 것인가?
2. 세션 transcript를 저장하지 않고도 반복 실패를 privacy-safe하게 증명할 수 있는가?
3. root `AGENTS.md`, nested `AGENTS.md`, platform-specific scoped instruction과 project-local Skill의 분할 기준은 무엇인가?
4. branch마다 달라지는 command와 architecture를 어느 ref를 기준으로 감사할 것인가?
5. LLM audit의 false positive를 줄이기 위해 어떤 mechanical pre-pass가 최소한 필요한가?
6. “아무 변경도 필요 없음”을 quality result로 평가하는 benchmark를 어떻게 만들 것인가?
7. rule 준수 향상이 모델 성능 변화인지 guidance 변화인지 어떻게 분리할 것인가?
8. 한 저장소에서 여러 번 성공한 결과를 독립적인 capability evidence로 볼 수 있는가?

## Candidate 승격을 검토할 조건

다음 evidence가 쌓이면 Candidate issue를 검토한다.

- 성숙도가 다른 최소 두 저장소에서 read-only audit을 수행했다.
- 한 사례에서는 실제 drift 또는 잘못된 destination을 찾아 승인된 개선으로 연결했다.
- 다른 사례에서는 full rewrite를 거부하거나 변경 불필요를 정확히 판정했다.
- finding별 evidence와 human authority boundary가 반복해서 이해 가능했다.
- private repository와 session material을 공개하지 않고도 결과를 설명할 수 있었다.
- generator, auditor, retrospective, checker 중 어떤 부분이 Blueprint의 required outcome이고 어떤 부분이 프로젝트 적응 지점인지 구분할 수 있었다.

두 저장소에서 같은 템플릿을 만들었다는 사실만으로는 승격하지 않는다. 핵심 evidence는 서로 다른 저장소가 서로 다른 개입을 필요로 했는데도 공통 authority와 routing 원칙이 유지되는지다.

## 관련 출처와 후속 링크

### 이 저장소

- [`AGENTS.md` 크기 지침 조사](../research/agents-md-size-guidance.md)
- [`Subtractive Edit Fidelity`](subtractive-edit-fidelity.md)
- [`Ideas` 운영 방식](README.md)

### 공개 도구와 형식

- [AGENTS.md convention](https://agents.md/)
- [Sentry `agents-md`](https://github.com/getsentry/skills/blob/main/skills/agents-md/SKILL.md)
- [`manage-workspace-agents-md`](https://github.com/stayhydated/skills/blob/master/skills/manage-workspace-agents-md/SKILL.md)
- [Netresearch `agent-rules`](https://github.com/netresearch/agent-rules-skill/blob/main/skills/agent-rules/SKILL.md)
- [Netresearch `retro`](https://github.com/netresearch/retro-skill/blob/main/skills/retro/SKILL.md)

### 공개 프로젝트 사례

- [`sdoc-editor` Agent guide](https://github.com/SWBaek/sdoc-editor/blob/main/AGENTS.md)
- [`sdoc-editor` AI-native harness drift issue #209](https://github.com/SWBaek/sdoc-editor/issues/209)
- [`sdoc-editor` harness hardening PR #211](https://github.com/SWBaek/sdoc-editor/pull/211)
- [`sdoc-editor` project orchestration removal issue #164](https://github.com/SWBaek/sdoc-editor/issues/164)
- [`sdoc-editor` repository harness checker](https://github.com/SWBaek/sdoc-editor/blob/main/scripts/check-repository-harness.mjs)
