# Evaluation Session 001

- 상태: Awaiting human review
- 대상: Interaction Taxonomy v0.1 정보 구조

## 준비

먼저 Markdown baseline을 읽고 같은 사례의 저충실도 HTML을 엽니다.

| 사례 | Markdown | HTML |
|---|---|---|
| CASE-001 orient | [`case-001-orient.md`](../benchmarks/case-001-orient.md) | [`orient.html`](../prototypes/orient.html) |
| CASE-002 compare/decide | [`case-002-compare-decide.md`](../benchmarks/case-002-compare-decide.md) | [`compare-decide.html`](../prototypes/compare-decide.html) |
| CASE-003 revise/verify | [`case-003-revise-verify.md`](../benchmarks/case-003-revise-verify.md) | [`revise-verify.html`](../prototypes/revise-verify.html) |

Core 0.3의 최종 semantic 예시는 다음에서 확인합니다.

- [`orient-review.html`](../../examples/orient-review.html)
- [`compare-review.html`](../../examples/compare-review.html)
- [`decide-review.html`](../../examples/decide-review.html)
- [`revise-review.html`](../../examples/revise-review.html)
- [`verify-review.html`](../../examples/verify-review.html)
- [`artifact.html`](../../templates/artifact.html): 실제 Response 생성·복사·다운로드 runtime

## 수행 과제

1. CASE-001에서 목적, 범위, 성공 기준과 한계를 설명합니다.
2. CASE-002에서 세 대안의 선호 순위를 정하고 최종 선택 또는 보류를 표현합니다.
3. CASE-003에서 변경 반영 여부와 검증 결론을 각각 판단합니다.
4. 참조 template에서 select Response를 생성하고 JSON이 자신의 의사를 표현하는지 확인합니다.
5. 변경 요청 action을 선택해 comment 없이는 생성되지 않는지 확인합니다.

## 제출 형식

각 항목을 1점에서 5점으로 평가합니다.

```text
목적 이해도: /5
정보 탐색성: /5
행동 명확성: /5
target/revision 명확성: /5
응답 표현 충분성: /5

CASE-001 결과:
CASE-002 순위와 결정:
CASE-003 변경 판단과 검증 판단:
중대한 모호성:
개선 의견:
```

합격 기준은 각 항목 평균 4.0 이상, 2점 이하 없음, target/revision 혼동과 중대한 행동 모호성 없음입니다.
