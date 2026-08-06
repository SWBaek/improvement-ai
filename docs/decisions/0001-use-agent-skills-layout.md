# 0001. Agent Skills 구조를 기본 배포 단위로 사용

- 상태: Superseded by 0008
- 날짜: 2026-08-05

## 결정

재사용 가능한 AI 작업 방식은 `skills/<name>/SKILL.md` 구조로 작성한다. 초기 설치와 업데이트는 기존 Agent Skills 생태계를 활용하고 자체 package manager는 만들지 않는다.

## 이유

- 여러 AI 코딩 도구가 동일한 기본 구조를 읽을 수 있다.
- skill별 instruction, script, reference와 asset을 함께 묶을 수 있다.
- 저장소가 작을 때 불필요한 설치기 유지 비용을 피할 수 있다.

## 결과

도구별 고유 기능이 필요한 경우 adapter를 추가할 수 있지만 공통 skill을 복제하지 않는다. 자체 CLI는 반복되는 배포 문제가 확인된 뒤 별도 결정 기록과 함께 도입한다.
