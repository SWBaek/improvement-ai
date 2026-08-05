# Human Review Artifacts

복잡한 AI 산출물을 사람이 이해하고, 검토하고, 결정하고, 다시 AI에게 전달할 수 있는 portable review surface로 표현하기 위한 framework입니다.

Core v0.1은 하나의 self-contained HTML 파일을 전달 단위로 사용합니다. 문서 식별과 검증을 위한 JSON Manifest는 HTML 안에 포함하고 실제 논의 내용은 semantic HTML로 표현합니다.

## 구성

- [`spec/core-0.1.md`](spec/core-0.1.md): 규범적 Core 계약
- [`schemas/manifest-0.1.schema.json`](schemas/manifest-0.1.schema.json): 내장 Manifest Schema
- [`templates/artifact.html`](templates/artifact.html): 인터랙티브 참조 템플릿
- [`profiles/README.md`](profiles/README.md): Domain Profile 확장 계약
- `examples/`: Core만 사용하는 중립 예시
- `scripts/validate_artifact.py`: Core 적합성 validator
- `decisions/`: framework 내부 설계 결정

## 검증

```powershell
python frameworks/human-review-artifacts/scripts/validate_artifact.py <artifact.html>
python frameworks/human-review-artifacts/scripts/validate_artifact.py <artifact.html> --json
python -m unittest discover -s frameworks/human-review-artifacts/tests -p "test_*.py"
```

## 현재 상태

Core v0.1입니다. Architecture, Research 같은 Domain Profile과 생성 Skill은 실제 사용 결과를 바탕으로 별도 추가합니다.
