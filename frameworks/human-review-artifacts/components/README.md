# Representation Components 0.1

Component는 interaction에 필요한 정보를 semantic HTML로 표현하는 재사용 계약입니다. 각 component root는 고유 ID와 `data-hra-component`를 가집니다.

| Component | 필수 의미 |
|---|---|
| `context-overview` | 목적, 범위, 현재 상태, 한계 |
| `evidence-list` | 근거 식별자, 내용, 출처 또는 한계 |
| `option-comparison` | 둘 이상의 option과 동일한 비교 기준, trade-off, 불확실성 |
| `decision-panel` | 결정 질문, option, 영향, 보류 조건 |
| `change-diff` | 변경 전, 변경 후, 피드백 추적, 미반영 항목 |
| `verification-results` | 기준, 기대, 관찰 결과, 근거, 판정 |
| `response-panel` | prompt, target, 허용 action과 로컬 Response 출력 |

핵심 의미는 JavaScript 없이 읽을 수 있어야 하고 빈 상태는 누락이 아니라 `없음` 또는 `확인되지 않음`으로 명시합니다. 표는 caption과 header를, control은 label과 visible focus를 제공해야 합니다. 인쇄 시 내용과 현재 요청을 숨기지 않습니다.
