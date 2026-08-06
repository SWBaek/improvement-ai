# 0002. Framework를 최상위 capability로 관리

- 상태: Superseded by 0008
- 날짜: 2026-08-06

## 결정

여러 skill, tool과 adapter가 공유하는 규약, 스키마, 템플릿과 확장 체계는 `frameworks/<name>/`에서 독립적으로 관리한다. framework는 공통 계약의 canonical source이며 특정 소비자에 의존하지 않는다.

둘 이상의 최상위 영역에 영향을 주는 결정은 `docs/decisions/`에 기록하고, 하나의 framework에만 적용되는 결정은 해당 framework의 `decisions/`에 기록한다.

## 이유

- 공통 계약을 skill이나 package의 구현 세부사항과 분리할 수 있다.
- 여러 에이전트와 도구가 동일한 원본을 소비할 수 있다.
- framework별 규격, 버전, 예시와 검증을 응집된 단위로 발전시킬 수 있다.
- 저장소 전체 결정과 지역 결정을 구분해 ADR의 적용 범위를 명확히 할 수 있다.

## 결과

skill, tool과 adapter는 framework를 참조할 수 있지만 framework는 이들을 참조하지 않는다. 설치 단위가 self-contained해야 한다면 canonical framework에서 필요한 snapshot을 생성하고 drift를 자동 검증한다.
