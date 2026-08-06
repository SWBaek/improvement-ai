# Human Review Artifacts Charter

## 존재 이유

Human Review Artifacts는 AI가 생성한 복잡한 내용을 인간이 이해하고, 검토하고, 결정하며, 그 결과를 다시 AI에게 전달할 수 있는 상호작용 workflow를 제공한다.

Markdown 대화를 HTML로 단순 변환하는 것이 목적이 아니다. 대화 중 특정 시점의 맥락과 검토 대상을 사람이 다루기 좋은 표현으로 구성하고, 인간의 응답을 AI가 모호함 없이 후속 작업에 사용할 수 있도록 만드는 것이 목적이다.

## 핵심 명제

> 고정해야 하는 것은 HTML의 외형이 아니라 인간과 AI 사이의 상호작용 계약이다.

Artifact의 화면 구성은 설명, 질문, 비교, 비평, 결정, 수정, 검증과 계획 등 주된 상호작용 목적에 따라 달라질 수 있다. 그러나 식별, revision, provenance, review target, response, 접근성, 보안과 이식성의 공통 계약은 일관되어야 한다.

## 설계 원칙

1. **Interaction 중심**: 문서 주제나 업무 domain보다 인간이 수행해야 할 행동과 AI가 제공해야 할 맥락을 먼저 모델링한다.
2. **하나의 주된 목적**: Artifact 하나는 사람이 명확하게 인식할 수 있는 하나의 주된 검토 목적을 가져야 한다.
3. **적응형 구성**: 하나의 거대한 고정 템플릿 대신 제한된 interaction pattern, view component와 조합 규칙을 사용한다.
4. **사람을 위한 HTML**: HTML은 읽기, 탐색, 비교와 응답을 위한 표현 계층이다. 핵심 의미는 JavaScript 없이도 이해할 수 있어야 한다.
5. **기계를 위한 구조**: Manifest, Authoring Model과 Review Response는 생성, 검증, 교환과 자동화를 위한 구조화 계층이다.
6. **명시적인 의미 상태**: 사실, 근거, 가정, 제안, 질문, 위험과 결정을 가능한 한 구분한다.
7. **추적 가능한 변화**: 입력, 생성 과정, revision과 인간의 응답이 어떤 결과에 영향을 주었는지 추적할 수 있어야 한다.
8. **구조화된 왕복**: 인간의 응답은 다시 AI가 검증하고 후속 변경에 사용할 수 있는 형태로 표현한다.
9. **점진적인 일반화**: 한 프로젝트의 용어나 화면을 곧바로 표준으로 만들지 않는다. 여러 사례에서 반복되는 상호작용과 표현만 공통 기능으로 승격한다.
10. **인간의 통제**: Artifact는 판단을 돕지만 인간의 승인, 거부, 변경 요청이나 보류를 대신하지 않는다.

## 제공 범위

Framework는 다음을 제공한다.

- portable Review Artifact의 공통 계약
- 반복 가능한 AI-인간 interaction pattern
- 상황에 맞게 조합할 수 있는 view component
- pattern과 view의 조합 및 적합성 규칙
- 구조화된 Review Response
- 검증 도구, 참조 구현과 적용 사례

장기적인 개념 계층은 다음과 같다.

```text
Core
├─ Interaction Patterns
├─ Representation Components
└─ Domain Vocabulary / Project Extensions
```

- Core는 모든 Artifact의 공통 전달·검토 계약을 정의한다.
- Interaction Pattern은 인간에게 어떤 행동을 요청하는지 정의한다.
- Representation Component는 정보를 어떤 형태로 보여주는지 정의한다.
- Domain Vocabulary와 Project Extension은 논의 대상의 전문 용어와 프로젝트 고유 의미를 제공한다.

## 비목표

Framework는 다음을 목표로 하지 않는다.

- 모든 논의를 하나의 화면이나 문서 목차에 맞추기
- 모든 업무 domain을 하나의 거대한 데이터 모델로 통합하기
- 채팅과 자유로운 대화를 완전히 대체하기
- HTML 자체를 Authoring SSOT로 강제하기
- AI 산출물의 정확성이나 인간 결정의 타당성을 자동으로 보증하기
- 프로젝트 고유 규칙과 vocabulary를 Core에 포함하기

## 성공 기준

다음 질문에 지속적으로 긍정적으로 답할 수 있어야 한다.

- 인간이 긴 선형 텍스트보다 검토 대상과 현재 상태를 빠르게 파악할 수 있는가?
- 인간에게 요구되는 행동과 그 영향이 명확한가?
- 필요한 근거, 가정, 대안, 위험과 미결 사항을 찾을 수 있는가?
- 부분별 의견, 선택, 승인, 거부, 보류와 변경 요청을 표현할 수 있는가?
- 응답을 AI가 대상과 revision의 혼동 없이 처리할 수 있는가?
- 동일한 Core와 interaction pattern을 서로 다른 주제와 프로젝트에서 재사용할 수 있는가?
- Artifact가 오프라인, 접근성, 보안과 장기 보존 요구를 만족하는가?

## 변경 통제

이 Charter는 특정 Core 버전과 독립적인 장기 기준이다. 조사 문서, Profile, template과 개별 규격은 발전할 수 있지만 이 문서의 존재 이유, 핵심 명제, 설계 원칙 또는 비목표를 변경하려면 framework `decisions/`에 새로운 결정을 작성해야 한다.

새 결정은 변경 이유, 관찰된 사례, 대안, 기존 원칙과 규격에 미치는 영향을 설명하고 대체하는 결정을 명시해야 한다. 단순한 구현 편의만으로 Charter를 변경하지 않는다.
