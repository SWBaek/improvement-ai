# 0008. Blueprint 전용 생성형 Capability 저장소를 채택

- 상태: Accepted
- 날짜: 2026-08-07

## 결정

`improvement-ai`의 canonical artifact를 설치 가능한 Agent Skill에서 **Capability Blueprint**로 변경한다. Blueprint는 대상 프로젝트의 AI가 project-owned Skills와 지원 자산을 설계하도록 문제, required outcomes, invariants, capability operations, adaptation points, human authority와 acceptance criteria를 제공한다.

AI는 대상 프로젝트를 먼저 읽기 전용으로 조사하고, 생성할 Skill의 수·trigger·경로·권한·검증 방법을 인간에게 제안한다. 승인 후에만 프로젝트 로컬 파일을 생성한다. Skill 수는 Blueprint가 고정하지 않으며 서로 다른 trigger, permission 또는 context가 있을 때 프로젝트 근거에 따라 분해한다.

생성물은 소비 프로젝트가 소유하고 upstream을 자동 추적하지 않는다. 모든 생성 `SKILL.md`는 호환 가능한 `name`과 `description` frontmatter를 사용하고 본문 comment에 canonical Blueprint path와 정확한 40자리 Git commit을 기록한다. 새 Blueprint revision 적용도 자동 overwrite가 아니라 semantic comparison과 인간 승인을 거친다.

저장소는 `blueprints/<name>/BLUEPRINT.md`, 설명용 references, governance 문서와 작은 저장소 관리 helper만 유지한다. 설치형 Skill, capability runtime, CLI, package, framework, adapter, formal generation schema, generator, release catalog와 자동 Release workflow를 제공하지 않는다.

기존 `manage-focus-cycle` Skill, JSON schema, HTML renderer, asset과 기능 test는 main에서 제거한다. Focus Cycle의 문제와 불변 조건은 첫 `manage-focus-cycle` Blueprint로 다시 작성한다. `manage-focus-cycle-v0.1.0` tag와 Release는 변경하지 않는 역사적 snapshot으로 남긴다.

ADR 0001과 0002의 기본 배포 구조, ADR 0006의 Skill version·Release 모델은 이 결정으로 폐기한다. ADR 0004의 capability portfolio와 실사용 lifecycle, ADR 0005의 bounded Focus Cycle 개념, ADR 0007의 낮은 검증 비용 원칙은 유지하되 Skill source, renderer와 Release 관련 결과는 이 결정이 대체한다.

## 이유

설치형 공통 Skill은 즉시 실행할 수 있지만 대상 프로젝트의 기록 체계, Agent client, 권한과 표현 방식에 맞추려면 지속적인 adapter와 업데이트 책임이 생긴다. 반면 충분히 명확한 개념 계약과 operation을 제공하면 AI는 현지 맥락에서 적절한 Skill 경계를 스스로 만들 수 있다.

Andrej Karpathy의 [LLM Wiki idea file](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)은 라이브러리 없이도 immutable sources, AI-owned wiki, schema와 Ingest·Query·Lint operation을 고정해 여러 AI가 유사한 로컬 구현을 생성하도록 만든 사례다. 핵심 가치는 완제품을 복제하는 것이 아니라 AI가 반복해서 올바른 도구를 만들 수 있을 만큼 문제의 구조를 제시하는 데 있다.

이 방식은 프로젝트별 최적화, 도구 중립성, 낮은 중앙 유지보수 비용과 실제 맥락에 기반한 Skill 분해에 유리하다. 대신 생성 결과의 일관성과 안전성을 보장하기 위해 invariants, 승인 경계, acceptance scenario와 exact-revision provenance가 필요하다.

## 결과

- 저장소 README, architecture와 AGENTS는 Blueprint-only 정체성을 사용한다.
- Candidate는 issue에만 존재하고 In Progress부터 Blueprint 경로를 만든다.
- Promoted는 서로 다른 두 프로젝트에서 생성·실사용된 evidence를 요구한다.
- `skills/`, `tools/`, `packages/`, `frameworks/`, `configs/`, `templates/`, capability tests와 Release workflow를 제거한다.
- GitHub Issue Form과 label은 Blueprint proposal 중심으로 바뀐다.
- 프로젝트별 Skill과 도구는 이 저장소에 수집하거나 배포하지 않는다.
- 문서 link와 governance metadata만 비례적으로 확인하며 generator나 conformance CI를 만들지 않는다.
