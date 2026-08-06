# Human Review Artifacts

복잡한 AI 산출물을 사람이 이해하고, 검토하고, 결정하고, 다시 AI에게 전달할 수 있는 portable review surface로 표현하기 위한 framework입니다.

Core v0.2는 하나의 self-contained HTML Review Snapshot을 전달 단위로 사용합니다. 외부 JSON/DSL이 프로젝트의 Authoring SSOT일 수 있지만, 사람이 검토한 특정 revision의 표현은 정적 semantic HTML로 보존합니다.

## 구성

- [`spec/core-0.2.md`](spec/core-0.2.md): 규범적 Core 계약
- [`schemas/manifest-0.2.schema.json`](schemas/manifest-0.2.schema.json): 내장 Manifest Schema
- [`schemas/review-response-0.1.schema.json`](schemas/review-response-0.1.schema.json): 표준 Review Response Schema
- [`templates/artifact.html`](templates/artifact.html): 인터랙티브 참조 템플릿
- [`profiles/README.md`](profiles/README.md): Domain Profile 확장 계약
- `examples/`: Core만 사용하는 중립 예시
- `scripts/validate_artifact.py`: Core 적합성 validator
- `scripts/validate_review_response.py`: Review Response 및 Artifact 교차 validator
- `decisions/`: framework 내부 설계 결정

## 검증

```powershell
python frameworks/human-review-artifacts/scripts/validate_artifact.py <artifact.html>
python frameworks/human-review-artifacts/scripts/validate_artifact.py <artifact.html> --json
python frameworks/human-review-artifacts/scripts/validate_review_response.py <response.json>
python frameworks/human-review-artifacts/scripts/validate_review_response.py <response.json> --artifact <artifact.html> --json
python -m unittest discover -s frameworks/human-review-artifacts/tests -p "test_*.py"
```

## 현재 상태

Core v0.2입니다. 미사용 Core v0.1은 폐기했으며 호환 대상으로 유지하지 않습니다. 첫 Domain Profile은 Architecture 실사용 사례를 바탕으로 별도 설계합니다.
