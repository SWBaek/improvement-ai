# improvement-ai

> 여러 프로젝트에서 다시 사용할 AI 협업 역량을 실제 작업으로 검증하고, 독립 버전의 Agent Skill로 배포하는 개인 capability 저장소입니다.

[English](README.md)

`improvement-ai`는 하나의 애플리케이션이나 서비스가 아닙니다. AI와 일하며 발견한 반복 문제를 작고 조합 가능한 Skill로 시작하고, 실사용 근거가 확인될 때만 결정적 script, package, framework 또는 별도 서비스로 확장하는 역량 포트폴리오입니다.

## 운영 원칙

- **Skill-first:** 가장 작은 재사용 단위인 Agent Skill로 시작합니다.
- **실사용 우선:** 추측한 범용성보다 실제 프로젝트에서 확인된 효과를 근거로 발전시킵니다.
- **하나의 원본:** 공통 capability는 이 저장소에서 관리하고 client별 adapter는 얇게 유지합니다.
- **사람 중심 표현:** 결정에 따라 간결한 텍스트, 표, 도형 또는 HTML을 사용합니다.
- **안전하고 검증 가능한 배포:** trigger, non-trigger, 기대 결과, version, 의존성과 검증 방법을 함께 관리합니다.

## Capability lifecycle

| 상태 | 의미 |
|---|---|
| Candidate | 실제 문제는 있지만 재사용 workflow가 아직 불명확합니다. |
| In Progress | 실제 작업에서 Skill을 Pilot하며 조정합니다. |
| Promoted | 반복 사용으로 효과, trigger와 안전장치가 확인됐습니다. |
| Deprecated | 대체 capability 또는 폐기 이유가 기록됐습니다. |

Release 성숙도와 Capability 성숙도는 별개입니다. 공개 `0.x` Release도 Pilot 근거가 확보될 때까지 `In Progress`로 유지할 수 있습니다.

## 제공 중인 Skill

| Skill | Version | 상태 | 지원 client | 목적 |
|---|---:|---|---|---|
| [`manage-focus-cycle`](skills/manage-focus-cycle/SKILL.md) | 0.1.0 | In Progress | Codex | 유한·장기 유지보수·연구 프로젝트 안에서 하나의 제한된 Focus Cycle을 관리합니다. |

`manage-focus-cycle`은 Completion Contract와 하나의 Primary Focus Cycle을 관리하고, 안전한 임시 HTML Workspace를 생성하며, 전체 프로젝트 완료율이나 가짜 최종 종료점을 만들지 않고 현재 작업을 닫도록 돕습니다. [변경 이력](docs/releases/manage-focus-cycle.md)과 [tracking issue #10](https://github.com/SWBaek/improvement-ai/issues/10)을 참고하세요.

## 설치와 사용

검증된 `skills` installer는 Node.js 22.20 이상이 필요하고 Workspace renderer는 Python 3.13을 사용합니다. Codex가 공식 검증 대상이며 다른 Agent Skills client는 아직 미검증입니다.

프로젝트에서 Skill을 조회하고 설치합니다.

```powershell
npx skills@latest add SWBaek/improvement-ai --list
npx skills@latest add SWBaek/improvement-ai --skill manage-focus-cycle --agent codex -y
```

새 Codex session에서 명시적으로 호출합니다.

```text
$manage-focus-cycle 현재의 제한된 목표와 완료 계약을 설정하고 시각적 Workspace를 열어 주세요.
```

기존 프로젝트 또는 전역 설치를 갱신합니다.

```powershell
npx skills@latest update manage-focus-cycle --project -y
npx skills@latest update manage-focus-cycle --global -y
```

Installer는 처음 설치한 Git ref의 폴더 변경을 추적합니다. 기본 설치는 `main`을 따르고 version tag는 재현 가능한 설치와 rollback 지점입니다. Release 알림은 GitHub의 Releases 구독으로 받을 수 있습니다.

## 저장소 구조

```text
skills/        Agent Skills와 실행에 필요한 bundled resource
tools/         Capability를 지원하는 독립 자동화
packages/      설치 가능한 CLI와 package source
frameworks/    여러 capability가 실제로 공유하는 versioned contract
configs/       공통 설정과 client adapter
external/      외부 자산의 출처, version과 license
scripts/       저장소 검증과 Release 자동화
tests/         계약과 동작 검증
docs/          아키텍처, 결정, issue 정책과 변경 이력
```

특정 프로젝트의 구현과 상태, 인증 정보, session log, cache와 재생성 가능한 runtime 출력은 포함하지 않습니다.

## 검증과 기여

```powershell
python scripts/validate_repository.py
python -m unittest discover -s tests -p "test_*.py" -v
```

지원 SLA 없이 issue와 pull request를 받습니다. [기여 안내](CONTRIBUTING.md), [보안 정책](SECURITY.md), [MIT license](LICENSE)를 확인하세요.

## 운영 문서

- [Agent 운영 규칙](AGENTS.md)
- [저장소 아키텍처](docs/architecture.md)
- [Skill Release 정책](docs/releases/README.md)
- [아키텍처 결정](docs/decisions/)
- [GitHub Issue 표준](docs/github/issues.md)
- [GitHub 저장소 설정](docs/github/repository-settings.md)
