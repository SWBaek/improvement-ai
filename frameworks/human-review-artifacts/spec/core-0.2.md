# Human Review Artifacts Core 0.2

- 상태: Released
- 규격 식별자: `human-review-artifacts/core@0.2`
- Manifest Schema: `urn:swbaek:human-review-artifacts:manifest:0.2`
- Review Response Schema: `urn:swbaek:human-review-artifacts:review-response:0.1`

이 문서의 MUST, MUST NOT, SHOULD, SHOULD NOT, MAY는 각각 필수, 금지, 권고, 비권고, 선택 요구사항을 뜻한다.

## 1. 목적과 권위 경계

Core는 복잡한 AI 산출물을 사람이 탐색하고 검토하며 결정을 다시 전달할 수 있는 portable HTML Review Snapshot으로 표현하는 공통 계약이다. 특정 domain의 데이터 모델, 문서 목차, 표기법이나 정답을 정의하지 않는다.

Artifact는 선택적인 외부 Authoring Model에서 생성될 수 있다(MAY). 외부 모델은 프로젝트의 작업 SSOT가 될 수 있지만, Artifact의 semantic HTML은 해당 `id`와 `revision`에서 사람이 실제로 검토한 표현의 권위 있는 원본이다(MUST). 내장 데이터와 semantic HTML이 충돌하면 해당 검토에서는 semantic HTML을 우선한다(MUST).

## 2. 전달 단위와 Snapshot

- Artifact는 UTF-8로 인코딩된 하나의 HTML5 파일이어야 한다(MUST).
- 핵심 내용, CSS, JavaScript와 시각 자산은 파일 안에 포함되어야 한다(MUST).
- Manifest나 내장 데이터가 HTML 본문을 대체해서는 안 된다(MUST NOT).
- JavaScript가 비활성화되어도 핵심 내용과 review request를 읽을 수 있어야 한다(MUST).
- Artifact는 식별 가능한 immutable review snapshot이다. 의미 있는 내용이 바뀌면 `revision`도 바뀌어야 한다(MUST).
- 외부 데이터 모델이 필요한 경우 Domain Profile이 별도 파일 또는 내장 `application/json` 데이터를 정의할 수 있다(MAY).

## 3. 문서 선언과 Manifest

`head`에는 다음 선언이 정확히 하나씩 있어야 한다(MUST).

```html
<meta name="human-review-artifact" content="core@0.2">
<script type="application/json" id="artifact-manifest">{...}</script>
```

Manifest는 `schemas/manifest-0.2.schema.json`을 따라야 한다(MUST). `html[lang]`, `title`, 화면의 주 제목, 상태와 revision은 Manifest 값과 일치해야 한다(MUST). `updatedAt`은 `createdAt`보다 빠를 수 없다(MUST NOT).

`provenance.inputs`에 입력을 선언하면 각 입력은 stable `id`와 `sha256-<base64>` digest를 가져야 한다(MUST). 비밀이나 개인 절대 경로는 provenance에 기록해서는 안 된다(MUST NOT).

알 수 없는 Core 버전은 적합성 오류다. 알 수 없는 Profile은 Core 검증을 막지 않지만 소비자는 경고해야 한다(SHOULD).

## 4. Semantic contract

Artifact는 `main[data-artifact-root]`를 정확히 하나 가져야 한다(MUST). 다음 section을 `data-artifact-section` 값으로 제공한다.

| Section | 요구사항 | 의미 |
|---|---|---|
| `summary` | 필수 | 목적, 현재 결론과 검토 범위 |
| `content` | 필수 | Artifact의 주된 설명과 시각화 |
| `review-request` | 조건부 | 사용자가 검토하거나 결정할 항목 |
| `provenance` | 필수 | 생성 맥락, 근거와 출처 |

`review.mode`가 `comment`, `decide`, `approve`이면 `review-request`가 필수이고 `review.targets`는 하나 이상의 ID를 가져야 한다(MUST). 각 target은 문서 안에 같은 `id`를 가진 `data-review-item` 요소로 존재해야 한다(MUST). `inform`이면 target과 review request를 생략할 수 있다(MAY).

Review option은 `data-review-option`과 문서 안에서 고유한 비어 있지 않은 `value`를 가져야 한다(MUST). 주장과 검토 항목은 필요에 따라 `data-artifact-kind`로 `fact`, `assumption`, `proposal`, `decision`, `question`, `risk`, `evidence` 중 하나를 표시할 수 있다(MAY). 의미는 색상만으로 전달해서는 안 된다(MUST NOT).

모든 section과 탐색 대상은 문서 안에서 유일한 `id`를 가져야 한다(MUST). 문서에는 하나의 visible `h1`이 있어야 한다(MUST).

## 5. Review Response

JSON Review Response는 `schemas/review-response-0.1.schema.json`을 따라야 한다(MUST). Response는 Artifact의 `id`, `spec`, `revision`과 target별 응답을 기록한다. JSON이 규범적 교환 형식이며 일반 텍스트 출력은 사람을 위한 편의 표현이다.

Response를 원 Artifact와 함께 검증할 때 다음이 일치해야 한다(MUST).

- `artifact.id`, `artifact.spec`, `artifact.revision`
- 모든 `targetId`와 Manifest의 `review.targets`
- 모든 `selectionIds`와 해당 Artifact의 `data-review-option` 값

Artifact는 Review Response를 자동 저장하거나 외부로 전송해서는 안 된다(MUST NOT). 복사와 로컬 다운로드는 사용자 동작으로만 수행한다(MUST).

## 6. Runtime 확장

Artifact는 실행 script가 없는 정적 문서일 수 있다(MAY). 실행 script가 있으면 다음을 모두 만족해야 한다(MUST).

- 모든 script는 inline이며 Manifest `runtime.scripts`에 `id`, owner, version과 digest가 선언된다.
- Core runtime은 해당 Core 버전의 참조 runtime과 정확히 일치한다.
- Profile runtime은 Manifest에 같은 이름과 버전의 Profile이 선언되어야 한다.
- 각 script의 digest와 CSP `script-src` hash가 실제 body와 일치한다.
- runtime은 canonical HTML을 생성하거나 의미를 바꾸지 않고 탐색, 표시와 로컬 응답 생성만 보강한다.

알 수 없는 Profile runtime은 Core 구조·digest·CSP 검증을 통과할 수 있지만 동작이 검증되지 않았다는 경고를 제공해야 한다(SHOULD).

Core 참조 runtime은 다음 기능을 제공한다(SHOULD).

- section 목차와 deep link
- section 접기와 펼치기
- `data-artifact-kind` 필터
- target별 Review Response를 JSON과 일반 텍스트로 복사 또는 다운로드
- 키보드 접근과 모바일 대응

## 7. 보안과 이식성

- 자동 외부 네트워크 요청과 외부 script, stylesheet, font, image를 사용해서는 안 된다(MUST NOT).
- inline event handler, `javascript:` URL, `iframe`, `object`, `embed`를 사용해서는 안 된다(MUST NOT).
- form은 로컬 검토 UI에 사용할 수 있지만 `action`을 가져서는 안 된다(MUST NOT).
- 사용자가 클릭하는 `https` 출처 링크는 허용한다(MAY). 새 창 링크에는 `rel="noopener noreferrer"`가 필요하다(MUST).
- CSP는 기본적으로 모든 기능을 차단하고 필요한 inline style, data image/font와 선언된 runtime hash만 허용해야 한다(MUST).

## 8. 접근성과 출력

- semantic HTML과 올바른 heading 순서를 사용해야 한다(MUST).
- 모든 control은 accessible name과 키보드 동작을 제공해야 한다(MUST).
- SVG와 image에는 동등한 텍스트 설명이 있어야 한다(MUST).
- 색상 대비와 focus indicator는 WCAG 2.2 AA를 목표로 한다(SHOULD).
- 인쇄 시 핵심 내용, review request와 provenance가 모두 표시되어야 한다(MUST).

## 9. Profile 확장

Profile은 Manifest의 `profiles`에 이름과 버전을 선언하고 데이터가 필요하면 `extensions.<profile-name>`을 사용한다. Profile은 새로운 section, kind, 데이터, 시각화, runtime과 검증을 추가할 수 있지만 Core 요구사항을 제거하거나 완화할 수 없다(MUST NOT).

Core와 Profile은 각각 `major.minor`로 버전 관리한다. 배포된 버전의 의미를 깨뜨리는 변경은 새 버전으로만 제공한다(MUST).

## 10. 적합성

Artifact는 Schema와 이 문서의 모든 MUST/MUST NOT 요구사항을 만족할 때 Core 0.2 적합으로 판정한다. Validator는 오류와 경고를 구분하고 자동화 가능한 JSON 결과를 제공해야 한다. Profile 적합성은 Core 적합성과 별도로 판정한다.
