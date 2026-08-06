# 0004. Capability 포트폴리오와 Skill-first lifecycle을 채택

- 상태: Accepted; Candidate example superseded by 0005
- 날짜: 2026-08-06

## 결정

`improvement-ai`를 하나의 제품이나 서비스 저장소가 아니라 여러 프로젝트에서 재사용할 AI 협업 capability를 발견하고 검증하며 배포하는 포트폴리오로 운영한다.

Capability의 기본 전달 단위는 `skills/<name>/SKILL.md`다. Candidate는 GitHub issue로만 관리하고, 실제 pilot을 시작하는 In Progress 단계부터 flat Skill 디렉터리를 만든다. Skill의 성숙도는 경로를 이동하지 않고 `skills/README.md`와 tracking issue에 기록한다.

결정적인 변환이나 검증이 반복되면 companion script 또는 tool을, 여러 프로젝트가 설치 가능한 실행 기능을 공유하면 package를 추가한다. Framework는 둘 이상의 capability가 동일한 versioned contract를 실제로 공유할 때만 추출한다. 독립 배포, 인증, 원격 동기화 또는 자체 release lifecycle이 필요한 capability는 별도 저장소로 분리하고 이 저장소에는 연결 Skill과 adapter를 남긴다.

ADR 0002의 framework 저장 위치와 의존성 원칙은 유지하지만 framework 생성의 우선순위는 이 결정의 실사용 조건을 따른다. ADR 0003의 `human-review-artifacts` 폐기 결정은 유지하고, Project Workspace를 다음 중심 제품으로 삼는 미래 방향은 이 결정으로 대체한다.

## 이유

이 저장소의 원래 목적은 AI와 함께 일하면서 발견한 다양한 개선 사항을 전역 재사용 가능한 역량으로 축적하는 것이었다. 하나의 미검증 아이디어를 저장소 전체의 제품 목표로 올리면 다른 capability의 진입점이 흐려지고, schema와 framework를 사용 경험보다 먼저 설계하게 된다.

Agent Skill은 instruction뿐 아니라 reference, asset과 script를 포함할 수 있으므로 대부분의 새로운 workflow를 검증하기에 충분하다. 작은 Skill로 시작하면 실제 사용 결과를 얻기 전까지 tool, package와 service의 운영 비용을 피할 수 있다.

## 결과

- 저장소의 첫 질문은 무엇을 만들 것인가가 아니라 어떤 반복 가능한 capability를 검증할 것인가가 된다.
- Human-AI Project Workspace는 저장소의 정체성이 아니라 첫 Candidate 중 하나로 관리한다.
- Skill은 상태와 무관하게 `skills/<name>` 경로를 유지하며 상태는 index와 issue에서 관리한다.
- 구현이 없는 placeholder 하위 디렉터리는 만들지 않는다.
- Framework와 독립 서비스는 명시된 승격 조건을 만족할 때 별도 결정으로 도입한다.
