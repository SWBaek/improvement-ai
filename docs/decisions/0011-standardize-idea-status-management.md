# 0011. Idea 상태 관리를 표준화

- 상태: Accepted
- 날짜: 2026-08-07
- 관련 issue: [#29](https://github.com/SWBaek/improvement-ai/issues/29)

## 결정

모든 Idea note는 `Exploring`, `Parked`, `Promoted`, `Dropped` 중 정확히 하나의 상태를 사용하고 `Last reviewed`와 `Next trigger`를 함께 기록한다. `docs/idea/README.md`의 index에도 같은 세 정보를 표시한다.

- `Exploring`은 현재 조사하거나 구체화하는 Idea다.
- `Parked`는 관찰 가능한 재개 조건까지 의도적으로 중단한 Idea다.
- `Promoted`는 issue 또는 Blueprint로 승격되어 후속 위치에서 관리하는 Idea다.
- `Dropped`는 더 진행하지 않기로 결정하고 이유를 보존한 Idea다.

`Promoted` 이후의 Blueprint 계약과 Pilot 실행 상태는 canonical Blueprint와 tracking issue에서만 관리한다. Idea note는 최초 문제와 탐색 근거를 보존하고, 후속 링크와 핵심 가설을 다시 검토할 조건만 유지한다.

## 이유

자유 형식의 상태 문구만으로는 활발히 탐색하는 Idea와 의도적으로 멈춘 Idea를 구분하기 어렵다. 상태만 추가해도 무엇을 기다리는지 알 수 없으므로 마지막 검토일과 다음 조건이 함께 필요하다.

반면 승격된 Idea에 Blueprint와 Pilot의 상태를 계속 복제하면 두 원본이 생기고 시간이 지나며 서로 어긋난다. Idea lifecycle과 Blueprint lifecycle을 분리하면 index에서는 전체 포트폴리오의 정체 상태를 확인하면서도 규범적 계약과 실행 evidence의 원본을 유지할 수 있다.

## 결과

- 새 Idea와 기존 Idea는 네 가지 상태만 사용한다.
- `Parked`는 재개 조건 없이 사용할 수 없다.
- `Dropped`는 종료 이유를 보존한다.
- Idea index만 보고 마지막 검토 시점과 다음 행동 조건을 파악할 수 있다.
- 승격 후 세부 진행률은 Idea note가 아니라 연결된 issue와 Blueprint에서 확인한다.
- 상태나 다음 조건이 달라질 때 note와 index를 함께 갱신한다.
