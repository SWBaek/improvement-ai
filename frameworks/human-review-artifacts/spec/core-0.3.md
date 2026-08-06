# Human Review Artifacts Core 0.3

- 상태: Released
- 규격 식별자: `human-review-artifacts/core@0.3`
- Manifest Schema: `urn:swbaek:human-review-artifacts:manifest:0.3`
- Review Response Schema: `urn:swbaek:human-review-artifacts:review-response:0.2`

이 문서의 MUST, MUST NOT, SHOULD, SHOULD NOT, MAY는 각각 필수, 금지, 권고, 비권고, 선택 요구사항을 뜻한다.

## 1. 목적과 권위 경계

Core는 AI가 생성한 복잡한 내용을 인간이 이해하고 행동한 결과를 다시 AI에게 전달하는 portable HTML Review Snapshot의 공통 계약이다. 특정 domain 데이터 모델이나 고정 화면을 정의하지 않는다.

외부 JSON/DSL은 프로젝트의 Authoring SSOT일 수 있다(MAY). Artifact의 semantic HTML은 해당 `id`와 `revision`에서 인간이 실제로 검토한 표현의 권위 있는 원본이다(MUST).

## 2. 전달 단위

- Artifact는 하나의 UTF-8 HTML5 파일이어야 한다(MUST).
- 핵심 내용, CSS, JavaScript와 시각 자산은 파일 안에 포함되어야 한다(MUST).
- JavaScript가 비활성화되어도 핵심 내용과 interaction 요청을 읽을 수 있어야 한다(MUST).
- 의미 있는 내용이 바뀌면 `revision`도 바뀌어야 한다(MUST).

## 3. 선언과 Manifest

`head`에는 다음 선언이 정확히 하나씩 있어야 한다(MUST).

```html
<meta name="human-review-artifact" content="core@0.3">
<script type="application/json" id="artifact-manifest">{...}</script>
```

Manifest는 `schemas/manifest-0.3.schema.json`을 따라야 한다(MUST). `html[lang]`, `title`, visible `h1`, status와 revision은 Manifest와 일치해야 한다(MUST).

## 4. Semantic HTML

Artifact는 `main[data-artifact-root]`를 하나 가져야 한다(MUST). 다음 section을 정확히 하나씩 제공한다.

| Section | 의미 |
|---|---|
| `summary` | 목적, 범위, 상태와 한계 |
| `content` | 판단에 필요한 주된 내용과 component |
| `interaction` | 인간에게 요청하는 행동과 response control |
| `provenance` | 입력, 생성 맥락과 출처 |

각 interaction target은 고유 ID와 `data-interaction-target`을 가져야 한다(MUST). 선택 가능한 option은 target 안에 있고 `data-interaction-option`과 고유한 `value`를 가져야 한다(MUST).

Representation Component는 `data-hra-component`로 선언한다(MAY). Core는 component 이름의 의미를 정의하지 않는다.

## 5. Interaction 계약

Manifest `interaction`은 정확히 하나의 pattern 이름·버전, 하나의 prompt와 하나 이상의 target을 선언해야 한다(MUST). 각 target은 `id`, `required`, 하나 이상의 `allowedActions`를 가진다.

표준 action은 다음과 같다.

```text
acknowledge, answer, comment, select, rank,
approve, reject, request-changes, defer, challenge
```

Core는 action의 구조와 target 연결을 정의한다. 알려진 pattern의 필수 component와 허용 action 조합은 Interaction Pattern 계약이 별도로 검증한다.

## 6. Review Response

Review Response는 `schemas/review-response-0.2.schema.json`을 따라야 한다(MUST). Response는 Artifact의 `id`, `spec`, `revision`, pattern과 target별 action을 기록한다.

- required target은 정확히 하나의 response를 가져야 한다(MUST).
- action은 target의 `allowedActions`에 포함되어야 한다(MUST).
- `answer`, `comment`, `request-changes`, `challenge`는 comment가 필요하다(MUST).
- `select`는 하나 이상의 `selectionIds`가 필요하다(MUST).
- `rank`는 두 개 이상의 중복 없는 `rankingIds`가 필요하다(MUST).
- selection과 ranking ID는 해당 target의 option이어야 한다(MUST).
- Artifact는 Response를 자동 저장하거나 외부로 전송해서는 안 된다(MUST NOT).

## 7. Runtime

Artifact는 정적 문서일 수 있다(MAY). 실행 script가 있으면 inline이어야 하고 Manifest `runtime.scripts`에 ID, owner, version과 digest를 선언해야 한다(MUST). CSP hash와 실제 body digest가 일치해야 한다(MUST).

Core runtime은 참조 runtime과 정확히 일치해야 한다. runtime은 canonical HTML 의미를 변경하지 않고 탐색과 로컬 Response 생성만 보강한다.

## 8. 보안, 접근성과 출력

- 자동 외부 요청, 외부 script/style/font/image를 사용해서는 안 된다(MUST NOT).
- inline event handler, `javascript:` URL, `iframe`, `object`, `embed`를 사용해서는 안 된다(MUST NOT).
- form은 `action`을 가져서는 안 된다(MUST NOT).
- CSP는 기본 차단과 선언 runtime hash를 강제해야 한다(MUST).
- semantic heading, accessible name, 키보드 동작과 visible focus를 제공해야 한다(MUST).
- 의미를 색상만으로 전달해서는 안 된다(MUST NOT).
- 인쇄 시 네 section이 모두 표시되어야 한다(MUST).

## 9. 확장과 적합성

Interaction Pattern은 `interactions/`, Representation Component는 `components/`, domain vocabulary는 `profiles/`에서 정의한다. Profile과 project extension은 Core 요구를 완화할 수 없다(MUST NOT).

Artifact는 Manifest Schema와 모든 Core MUST/MUST NOT 요구를 만족할 때 Core 0.3 적합이다. Pattern 적합성은 Core 적합성과 별도로 판정한다.
