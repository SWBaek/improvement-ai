# Decisions

저장소 전체에 영향을 주는 장기 결정을 번호 순서로 관리합니다. 새 결정은 기존 기록을 삭제하지 않고 상태와 대체 관계를 명시합니다.

| ADR | 상태 | 요약 |
|---|---|---|
| [0001](0001-use-agent-skills-layout.md) | Accepted | Agent Skills 구조를 기본 배포 단위로 사용 |
| [0002](0002-introduce-frameworks-as-first-class-capabilities.md) | Accepted, constrained by 0004 | 검증된 공통 계약을 `frameworks/`에서 관리 |
| [0003](0003-retire-human-review-artifacts.md) | Partially superseded by 0004 | 미사용 Human Review Artifacts 구현 폐기 |
| [0004](0004-adopt-capability-portfolio.md) | Accepted, candidate example superseded by 0005 | Capability 포트폴리오와 Skill-first lifecycle 채택 |
| [0005](0005-narrow-workspace-to-focus-cycle-management.md) | Accepted | 첫 capability를 Focus Cycle Management로 축소 |
| [0006](0006-release-skills-independently-from-releasable-main.md) | Accepted | Releasable main과 Skill별 독립 version·Release 채택 |
