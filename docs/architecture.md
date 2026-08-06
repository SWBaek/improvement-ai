# Architecture

## 목적

`improvement-ai`는 여러 프로젝트가 소비하는 개인 AI capability의 canonical source다. 소비 프로젝트는 필요한 capability를 설치하거나 연결하고, 프로젝트 고유 상태와 결과물은 자체 저장소에서 소유한다.

## 계층

1. **Capability source**: `skills/`
2. **Companion execution**: `tools/`, `packages/`
3. **Shared contracts**: `frameworks/`
4. **Configuration adapters**: `configs/`
5. **Distribution and maintenance**: `scripts/`, `templates/`, `external/`
6. **Governance and verification**: `AGENTS.md`, `.github/`, `docs/`, `tests/`

Skill이 기본 진입점이며 나머지 계층은 실제 capability가 요구할 때만 추가한다. 디렉터리가 존재한다는 사실이 해당 형태의 구현을 미리 만들어야 한다는 뜻은 아니다.

## 의존 방향

```text
consumer project
  └─ installed Skill
       ├─ bundled references/assets/scripts
       ├─ companion tool or package
       └─ shared framework contract
```

- Skill은 자체 asset과 script를 포함하거나 독립 tool, package와 framework를 소비할 수 있다.
- Tool과 package는 agent에 독립적인 실행 인터페이스를 제공한다.
- Framework는 소비자인 Skill, tool, package와 agent adapter를 참조하지 않는다.
- Agent별 설정은 공통 원본을 복제하지 않고 adapter 또는 생성물로 유지한다.
- 소비 프로젝트의 코드, 상태와 생성 결과를 이 저장소로 역수입하지 않는다.

## Lifecycle과 저장 위치

- Candidate는 GitHub issue에만 존재하며 아직 source directory를 갖지 않는다.
- In Progress부터 `skills/<name>/SKILL.md`를 만들고 실제 프로젝트에서 pilot한다.
- Promoted와 Deprecated도 같은 flat 경로를 유지하고 `skills/README.md`의 상태를 바꾼다.
- 결정적인 반복 실행이 확인되면 companion tool을 추가하고, 공유 설치가 필요해지면 package로 승격한다.
- 둘 이상의 capability가 같은 contract를 공유할 때만 `frameworks/<name>/`으로 추출한다.

## 독립 저장소 분리 조건

다음 중 하나가 capability의 핵심 운영 요구가 되면 별도 제품 또는 서비스 저장소로 분리하는 결정을 검토한다.

- 항상 실행되는 runtime이나 server
- 독립적인 배포와 release lifecycle
- 사용자 인증, 원격 저장 또는 동기화
- 다중 사용자 협업과 운영 monitoring
- Agent Skill 없이도 성립하는 독립 사용자 경험

분리 후에도 AI가 해당 제품을 사용하는 반복 workflow는 이 저장소의 Skill 또는 adapter로 유지할 수 있다.

## 배포와 검증

- Skill 설치는 가능한 동안 기존 Agent Skills 생태계를 사용한다.
- 자체 CLI는 Skill 외 설정, hook, pack 또는 version 고정까지 함께 관리해야 할 때만 도입한다.
- 외부 자산은 vendoring보다 출처와 version을 기록하는 방식을 우선한다.
- 저장소 전역 계약은 `scripts/validate_repository.py`, capability 고유 동작은 해당 Skill 또는 tool의 테스트가 검증한다.
- 저장소 전역 결정은 `docs/decisions/`, Framework 내부 결정은 해당 Framework의 `decisions/`에 기록한다.
