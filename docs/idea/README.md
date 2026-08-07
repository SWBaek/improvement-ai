# Ideas

`docs/idea/`는 아직 채택되지 않은 문제, 관찰과 capability 가설을 모으고 구체화하는 탐색 공간이다. Idea note는 결정 기록, 구현 사양, GitHub Candidate 또는 Capability Blueprint가 아니다.

## 운영 방식

1. 반복될 가능성이 있지만 범위와 해법이 불명확한 문제를 Idea note로 기록한다.
2. 조사 결과, 설계 가설, 반례와 열린 질문을 같은 note에서 갱신한다.
3. 실제로 검증할 가치와 반복 가능성이 확인되면 tracking issue를 만들고 Candidate로 승격한다.
4. 첫 Pilot을 시작할 준비가 되면 `blueprints/<name>/BLUEPRINT.md`로 구체화한다.
5. 채택하지 않기로 한 경우에도 이유와 상태를 남겨 같은 탐색을 반복하지 않게 한다.

Idea 단계에서는 실행 가능한 runtime, 설치형 Skill, formal schema나 speculative Blueprint directory를 만들지 않는다. 외부에서 얻은 개념은 출처와 이 Idea에 유용한 이유를 기록한다.

## 권장 구성

- 상태
- 문제와 배경
- 현재 개념 또는 설계 가설
- 기대 효과와 비목표
- 위험과 반례
- 검증 기준 또는 실험 질문
- 향후 탐색
- 관련 출처와 후속 링크

모든 항목이 처음부터 완전할 필요는 없다. 다만 추측을 확정된 사실처럼 기록하지 않고, Idea가 무엇을 아직 모르는지 드러내야 한다.

## Idea index

| Idea | 상태 | 요약 |
|---|---|---|
| [AI–Human Interactive Decision Workbench](ai-human-interactive-decision-workbench.md) | Idea note | 많은 인간 결정을 구조화된 시각적 Workbench에서 검토하고 AI에 전달하는 상호작용 방식 |
| [Local Project Continuity](local-project-continuity.md) | Idea note | 세션·Agent·모델이 바뀌어도 로컬 프로젝트의 상태와 축적 지식을 복구하는 프로젝트 소유 기억 체계 |
