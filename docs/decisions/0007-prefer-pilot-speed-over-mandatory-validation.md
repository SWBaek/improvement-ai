# 0007. 강제 검증보다 Pilot 속도를 우선

- 상태: Partially superseded by 0008
- 날짜: 2026-08-06

## 결정

ADR 0006의 releasable-main, 모든 Skill 변경의 version 증가, 별도 changelog와 반복 CI 검증 정책을 폐기한다. `main`은 실제 프로젝트 feedback을 빠르게 반영하는 최신 개발 channel로 운영한다.

GitHub Actions 검증 workflow, OS matrix, main 재검증, 설치 smoke test, 저장소 구조 validator와 이를 다시 검증하는 meta-test를 제거한다. `manage-focus-cycle`의 renderer와 schema처럼 실제 사용자 결과를 직접 보호하는 작은 기능 테스트만 로컬에 유지한다.

독립 Skill version과 GitHub Release 개념은 유지하되 모든 변경에 적용하지 않는다. 정식 snapshot이 필요할 때만 `skills/catalog.json` version을 올리고, catalog 변경에만 반응하는 최소 Release workflow가 인증된 `gh`로 tag와 generated release notes를 만든다.

## 이유

이 저장소의 핵심 목적은 여러 AI capability를 실제 프로젝트에서 빠르게 실험하고 개선하는 것이다. 하나의 In Progress Skill 변경마다 Windows와 Ubuntu PR 검증, main 재검증, Release 재검증과 npm 설치를 반복하면 제품 runtime에 준하는 비용이 들지만 현재 위험과 사용 규모에 비례하지 않는다.

Repository metadata, index, changelog와 Release automation을 서로 검증하는 코드는 Skill 자체보다 큰 유지보수 대상이 됐다. 아직 Pilot 단계에서는 자동화된 형식 완전성보다 사용자가 실제로 느끼는 효용과 빠른 feedback loop가 더 중요하다.

Renderer의 escaping과 schema rejection 테스트는 실제 안전 동작을 보호하므로 유지할 가치가 있다. 반면 설치 도구, OS와 repository 구조 검증은 실제 실패가 보고될 때 추가해도 된다.

## 결과

- `.github/workflows/`에는 catalog 변경에만 실행되는 최소 Release workflow만 남는다.
- 일반 Skill 변경과 PR에는 GitHub Actions와 required status check가 실행되지 않는다.
- Catalog는 Skill 이름과 마지막 snapshot version만 보유한다.
- Release notes는 GitHub가 commit history에서 생성하며 별도 `docs/releases/`는 유지하지 않는다.
- Skill index와 lifecycle은 `skills/README.md`와 tracking issue에서 사람이 관리한다.
- 기존 `manage-focus-cycle-v0.1.0` tag와 Release는 변경하지 않는다.
- 새로운 검증은 반복되는 실제 실패와 명확한 ROI가 확인될 때만 추가한다.
