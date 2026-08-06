# Human Review Artifacts

복잡한 AI 산출물을 사람이 이해하고, 검토하고, 결정하고, 다시 AI에게 전달할 수 있는 portable review surface로 표현하기 위한 framework입니다.

Core v0.3은 하나의 self-contained HTML Review Snapshot을 전달 단위로 사용하고, 하나의 주된 Interaction Pattern과 target별 허용 action을 선언합니다. 외부 JSON/DSL이 프로젝트의 Authoring SSOT일 수 있지만, 사람이 검토한 특정 revision의 표현은 정적 semantic HTML로 보존합니다.

장기 목표와 설계 원칙은 [`CHARTER.md`](CHARTER.md)를 따릅니다. 핵심 방향은 고정된 HTML 외형이 아니라 AI와 인간 사이의 상호작용 계약을 표준화하고, 목적에 맞는 interaction pattern과 representation component를 조합하는 것입니다.

## 구성

- [`spec/core-0.3.md`](spec/core-0.3.md): 규범적 Core 계약
- [`schemas/manifest-0.3.schema.json`](schemas/manifest-0.3.schema.json): 내장 Manifest Schema
- [`schemas/review-response-0.2.schema.json`](schemas/review-response-0.2.schema.json): 표준 Review Response Schema
- [`interactions/`](interactions/README.md): 범용 Interaction Pattern과 machine-readable catalog
- [`components/`](components/README.md): Representation Component 계약
- [`templates/artifact.html`](templates/artifact.html): 인터랙티브 참조 템플릿
- [`profiles/README.md`](profiles/README.md): Domain Profile 확장 계약
- [`research/`](research/README.md): AI-인간 interaction 사례와 pattern 연구
- `examples/`: Core만 사용하는 중립 예시
- `scripts/validate_artifact.py`: Core 적합성 validator
- `scripts/validate_interaction.py`: Interaction Pattern 적합성 validator
- `scripts/validate_review_response.py`: Review Response 및 Artifact 교차 validator
- `decisions/`: framework 내부 설계 결정

## 검증

```powershell
python frameworks/human-review-artifacts/scripts/validate_artifact.py <artifact.html>
python frameworks/human-review-artifacts/scripts/validate_artifact.py <artifact.html> --json
python frameworks/human-review-artifacts/scripts/validate_interaction.py <artifact.html>
python frameworks/human-review-artifacts/scripts/validate_review_response.py <response.json>
python frameworks/human-review-artifacts/scripts/validate_review_response.py <response.json> --artifact <artifact.html> --json
python -m unittest discover -s frameworks/human-review-artifacts/tests -p "test_*.py"
```

## 현재 상태

Core v0.3과 Interaction Taxonomy v0.1입니다. Core v0.2는 외부 적용 전에 interaction 중심 계약으로 교체했으며 호환 대상으로 유지하지 않습니다. 현재는 중립 사례의 직접 인간 검토와 외부 적용 가이드를 준비하고 있습니다.
