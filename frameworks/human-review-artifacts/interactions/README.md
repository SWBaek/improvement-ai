# Interaction Patterns

Interaction Pattern은 Artifact에서 인간이 달성할 하나의 주된 목표, 필요한 맥락, 허용 response action과 완료 조건을 정의합니다. Core 0.3 Artifact는 pattern 이름과 버전을 하나만 선언합니다.

v0.1은 `orient`, `compare`, `decide`, `revise`, `verify`를 제공합니다. 세부 계약과 machine-readable catalog는 [`catalog-0.1.json`](catalog-0.1.json)에 있습니다.

알려진 pattern의 의미 적합성은 `scripts/validate_interaction.py`로 Core 적합성과 별도로 검증합니다.
