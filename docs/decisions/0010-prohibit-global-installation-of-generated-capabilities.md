# 0010. Blueprint 생성 capability의 전역 설치를 금지

- 상태: Accepted
- 날짜: 2026-08-07

## 결정

Capability Blueprint에서 생성한 Agent Skills, Installation Receipt, Profile, schema, mapping, 상태 기록과 기타 지원 자산은 반드시 대상 프로젝트 내부의 프로젝트 로컬 경로에 설치한다. 사용자 홈, Agent 전역 Skill directory, 공유 전역 config 또는 여러 프로젝트가 함께 사용하는 외부 경로에는 설치하지 않는다.

AI는 대상 Agent의 프로젝트 로컬 discovery convention을 우선 사용하고, convention이 없을 때만 Blueprint가 제시한 프로젝트 내부 fallback을 사용한다. 설치 제안에 전역 경로나 프로젝트 밖의 공유 상태가 포함되면 승인 가능한 adaptation으로 취급하지 않고 프로젝트 로컬 대안을 제시해야 한다. 사용자가 전역 설치를 요청해도 현재 Blueprint의 생성물로 수행하지 않는다.

여러 프로젝트의 상태·정책·mapping을 소유하지 않고 Blueprint 적용 절차만 시작하는 무상태 bootstrap capability는 향후 별도 Blueprint나 도구로 설계할 수 있다. 이는 현재 Blueprint 생성물의 전역 설치 예외가 아니며, 이 저장소는 그러한 bootstrap 구현을 제공하지 않는다.

## 이유

생성 capability는 대상 프로젝트의 source of truth, 승인자 역할, 기록 경로, 외부 쓰기 권한, schema extension과 exact Blueprint revision에 맞게 생성된다. 이를 전역으로 설치하면 한 프로젝트의 정책이 다른 프로젝트에 적용되고, 서로 다른 revision과 local customization이 충돌하며, 프로젝트 소유 continuity와 권한 경계가 무너질 수 있다.

프로젝트 로컬 설치는 생성물의 소유권, Git history, review, 제거 범위와 업데이트 대상을 프로젝트 경계 안에 유지한다. 설치 편의를 위한 bootstrap과 실제 프로젝트 상태를 운영하는 capability를 분리하면 전역 도구가 프로젝트별 canonical source가 되는 것을 막을 수 있다.

## 결과

- 모든 Blueprint는 전역 설치 금지를 invariant, 설치 절차, non-goal과 acceptance에 명시한다.
- 개별 설치 README의 복사 프롬프트도 전역 경로를 제안하거나 사용하지 말라고 지시한다.
- Pilot은 생성 파일이 모두 대상 프로젝트 내부에 있고 Agent가 프로젝트 로컬 Skill을 발견하는지 확인한다.
- 기존 전역 생성물이 발견되면 자동 이동하지 않고 프로젝트 로컬 migration proposal과 인간 승인을 요구한다.
- 별도 무상태 bootstrap capability가 필요해지면 새로운 Idea와 Blueprint 절차를 따른다.
