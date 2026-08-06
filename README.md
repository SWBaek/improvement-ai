# improvement-ai

> 여러 프로젝트에서 다시 사용할 AI 협업 역량을 발견하고, 실제 작업에서 검증하고, 배포 가능한 형태로 발전시키는 개인 capability repository.

`improvement-ai`는 하나의 애플리케이션이나 단일 서비스를 만드는 저장소가 아닙니다. AI와 함께 프로젝트를 수행하면서 반복해서 겪는 문제와 개선 방법을 **작고 조합 가능한 Skill과 보조 도구**로 축적하는 역량 포트폴리오입니다.

## 목표

이 저장소는 다음 순환을 지속 가능하게 만드는 것을 목표로 합니다.

1. 실제 프로젝트에서 AI 협업의 불편이나 반복 작업을 발견합니다.
2. 가장 작은 재사용 단위인 Agent Skill로 해결 방법을 실험합니다.
3. 다른 프로젝트에서도 효과와 사용 조건을 검증합니다.
4. 반복 실행이 필요한 부분만 script, tool 또는 package로 분리합니다.
5. 여러 capability가 실제로 공유하는 계약만 framework로 추출합니다.
6. 독립적인 제품이 된 capability는 별도 저장소로 분리하고 이곳에는 연결 Skill과 adapter를 남깁니다.

대화에서 한 번 얻은 개선을 프롬프트 조각으로 잃어버리지 않고, 언제 다시 사용해야 하는지와 제대로 작동했는지까지 확인할 수 있는 자산으로 만드는 것이 핵심입니다.

## Capability란 무엇인가

이 저장소에서 capability는 **AI와 인간이 반복해서 수행할 수 있는 하나의 검증 가능한 작업 방식**입니다.

좋은 capability에는 다음이 드러납니다.

- 언제 사용하고 언제 사용하지 않는가
- 인간과 AI가 각각 무엇을 해야 하는가
- 어떤 입력을 사용하고 어떤 결과를 만드는가
- 결과가 성공했는지 어떻게 확인하는가
- 특정 AI 제품에 종속되지 않고 어떻게 재사용하는가

Capability의 기본 전달 단위는 Agent Skill입니다. 필요하면 Skill 안에 reference, template, asset과 script를 포함할 수 있으므로, HTML 보고서나 자동화가 필요하다는 이유만으로 처음부터 서비스나 framework를 만들지 않습니다.

## 운영 원칙

- **Skill-first**: 새 아이디어는 가능한 한 작은 Skill로 시작합니다.
- **작고 조합 가능하게**: 하나의 거대한 workflow보다 분명한 책임을 가진 capability를 선호합니다.
- **실사용 우선**: 추측한 범용성보다 실제 프로젝트에서 확인된 불편과 효과를 근거로 발전시킵니다.
- **점진적 승격**: 반복성이 증명될 때만 tool, package, framework 또는 독립 서비스로 확장합니다.
- **하나의 원본**: 공통 capability의 canonical source는 이 저장소에서 관리하고 에이전트별 형식은 얇은 adapter로 둡니다.
- **도구 중립성**: 공통 지식과 workflow는 Codex, Claude Code 등 특정 agent의 인터페이스와 분리합니다.
- **사람 중심 표현**: 긴 Markdown이 항상 최선이라고 가정하지 않고, 표·도형·HTML 등 사람이 이해하기 좋은 표현을 선택합니다.
- **검증과 안전**: 사용 조건, 기대 결과, 검증 방법과 변경 안전장치를 capability의 일부로 취급합니다.

## Capability의 발전 단계

| 단계 | 의미 | 기본 산출물 |
|---|---|---|
| Candidate | 실제 문제는 있으나 재사용 방식이 아직 불명확함 | issue, 짧은 설계 기록 |
| In Progress | 한 프로젝트에서 사용하며 workflow를 조정 중 | 실험적 Skill과 필요한 asset/script |
| Promoted | 여러 사용에서 효과와 trigger가 확인됨 | 문서화·검증된 재사용 Skill |
| Deprecated | 더 나은 capability로 대체됐거나 더 이상 유효하지 않음 | 대체 경로와 폐기 이유 |

구현 규모는 다음 기준으로 확장합니다.

| 형태 | 선택 기준 |
|---|---|
| Skill | AI의 판단, 조사, 생성 또는 작업 순서를 재사용하면 충분할 때 |
| Companion script/tool | 같은 변환·검증·렌더링을 결정적으로 반복해야 할 때 |
| Package/CLI | 여러 Skill이나 프로젝트가 설치 가능한 실행 기능을 공유할 때 |
| Framework | 둘 이상의 capability가 버전 관리되는 동일 계약을 실제로 공유할 때 |
| 별도 서비스 저장소 | 독립 실행 환경, 배포, 인증, 원격 동기화 또는 자체 릴리스 주기가 필요할 때 |

Framework와 서비스는 목표가 아니라 검증된 capability가 필요에 따라 도달하는 구현 형태입니다.

## 저장소 범위

```text
skills/        재사용 가능한 Agent Skills
tools/         Skill을 지원하는 독립 실행 자동화와 개발 도구
packages/      설치·배포 가능한 CLI와 package
frameworks/    여러 capability가 공유하는 검증된 계약
configs/       공통 설정과 agent별 adapter
templates/     새 capability를 시작하기 위한 최소 template
external/      외부 capability의 출처, 버전과 라이선스
scripts/       저장소 설치, 동기화, 검증과 배포 자동화
tests/         저장소 계약과 공통 동작 검증
docs/          아키텍처, 운영 정책과 의사결정 기록
```

포함하는 것:

- 여러 프로젝트에서 다시 사용할 Skill과 workflow
- Skill이 직접 사용하는 reference, template, asset과 script
- capability의 설치·검증·배포를 지원하는 공통 도구
- 실사용으로 공유 필요성이 확인된 package와 framework
- 출처, 호환성, 안전성과 운영 결정을 설명하는 문서

포함하지 않는 것:

- 특정 프로젝트에만 유효한 구현과 프로젝트 상태
- 세션 로그, 캐시, 인증 정보와 개인 런타임 데이터
- 사용 사례 없이 먼저 만든 범용 schema와 추상화
- 독립 제품으로 운영돼야 하는 전체 서비스 코드
- 다른 곳에서 재생성할 수 있는 다운로드·빌드 결과물

## 첫 번째 주요 Candidate

**Human-AI Project Workspace**는 이 저장소 전체의 정체성이 아니라, 여기서 발전시킬 capability 중 하나입니다.

이 capability는 AI가 프로젝트를 조사한 뒤 인간에게 다음을 시각적으로 보여주는 workflow를 목표로 합니다.

1. 프로젝트 전체 진행 상황
2. 현재 단계, Focus와 필요한 결정
3. 현재 문제에 적합한 표, 흐름, architecture diagram 또는 기타 시각 자료

GM 프로젝트에서 pilot을 시작할 때 flat Skill과 필요한 HTML asset/script를 만들고 In Progress로 전환합니다. 인간의 응답은 기존 채팅을 사용합니다. 독립 Engine, Framework 또는 서버형 서비스는 Skill만으로 해결하기 어려운 요구가 실제로 확인된 뒤 검토합니다.

## 현재 상태

| 영역 | 상태 |
|---|---|
| 저장소 운영 기반 | 구축됨 |
| Promoted capability | 아직 없음 |
| Human-AI Project Workspace | Candidate, Skill 기반 pilot 준비 전 |
| 자체 CLI와 Framework | 실사용 근거가 생길 때까지 보류 |

## 시작하기

저장소의 구조와 metadata 계약을 검증합니다.

```powershell
python scripts/validate_repository.py
```

Promoted Skill이 추가되면 기존 Agent Skills 생태계를 우선 사용해 조회하고 설치합니다.

```powershell
npx skills add SWBaek/improvement-ai --list
npx skills add SWBaek/improvement-ai -g -a codex
```

GitHub label을 동기화할 때는 인증된 GitHub CLI를 사용합니다.

```powershell
gh auth status
python scripts/sync_github_labels.py --repo SWBaek/improvement-ai
```

## 운영 문서

- [Agent 운영 규칙](AGENTS.md)
- [저장소 아키텍처](docs/architecture.md)
- [의사결정 기록](docs/decisions/)
- [GitHub Issue 표준](docs/github/issues.md)
