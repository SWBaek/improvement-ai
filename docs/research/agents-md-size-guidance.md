# AGENTS.md 크기 지침 조사

- 조사일: 2026-08-13
- 상태: Research note. 채택된 ADR이나 Blueprint 계약이 아니다.
- 목적: `AGENTS.md`를 5KB 이하로 관리하는 제안이 공식·공신 자료와 맞는지 확인하고, 이 저장소의 always-on 지침 예산을 정할 근거를 남긴다.

## 조사 질문

1. 공식 AGENTS.md 형식이나 주요 Agent 제품이 5KB 상한을 규정하는가?
2. 제품이 정한 것은 권장 크기인가, 잘림 한도인가?
3. 현재 `improvement-ai` `AGENTS.md`(약 14KB)는 그 기준에서 어디에 있는가?
4. 이 저장소가 5KB를 채택한다면 어떤 의미로 채택해야 하는가?

## 비교 기준

- 1차 출처: 형식 관리 주체와 Agent 제품 문서
- 2차 출처: 제품 문서를 인용한 해설. 공식 숫자와 다를 때만 참고
- 구분: 잘림 한도(넘으면 잘리거나 이후 파일을 읽지 않음)와 품질 권장(넘으면 준수가 떨어진다고 안내)

## 1차 출처

| 출처 | 종류 | 숫자 | 의미 |
|---|---|---|---|
| [AGENTS.md 형식](https://agents.md/) (AAIF / Linux Foundation) | 형식 명세 | 없음 | 필수 필드 없음. README는 사람용, AGENTS.md는 Agent용. 큰 monorepo는 중첩 파일 사용 |
| [OpenAI Codex — Custom instructions with AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | 제품 문서 | 기본 `project_doc_max_bytes` = 32 KiB | 전역+프로젝트 지침 **합산** 한도. 넘으면 이후 파일을 더하지 않음. 설정으로 올릴 수 있음 |
| [Anthropic Claude Code — Memory](https://code.claude.com/docs/en/memory) | 제품 문서 | CLAUDE.md **200줄 미만** 권장. Auto memory `MEMORY.md`는 200줄 또는 25KB 중 먼저 오는 쪽 | CLAUDE.md는 길어도 전부 로드. 길면 context를 쓰고 준수가 떨어질 수 있음 |
| [Cursor — Rules](https://cursor.com/docs/rules) | 제품 문서 | Rule 파일 **500줄 미만** | `.cursor/rules` best practice. AGENTS.md에는 별도 바이트 한도가 없음 |
| [Anthropic — Effective context engineering](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | 공학 안내 | 바이트 숫자 없음 | context는 유한한 attention budget. 원하는 결과를 내는 **가장 작은 high-signal token 집합**을 고른다 |

Codex 문서는 잘림 한도를 명시한다. Claude와 Cursor 문서는 품질 권장이다. 어느 쪽도 5KB를 표준으로 적지 않는다.

## 관찰

조사 시점의 `AGENTS.md`는 13,922바이트, 133줄이다.

- Claude의 200줄 권장보다는 짧다.
- Codex 기본 합산 한도 32 KiB의 약 43%다.
- Cursor 500줄 권장보다 훨씬 짧다.
- 기여 유형, Blueprint/Idea 작성, lifecycle 표를 `CONTRIBUTING.md`와 다른 정범 문서와 복제한다.

커뮤니티 글은 60–300줄, 500–2,000 token, 150줄 같은 더 작은 목표를 말하지만, 이는 제품 명세가 아니다. 2,000 token은 영어 기준으로 대략 8KB 전후이며 5KB와 같은 숫자가 아니다.

한국어 UTF-8는 한글 1자당 3바이트라, 같은 5KB에 영어보다 적은 문장이 들어간다. 바이트 예산은 언어에 따라 실제 지침 수가 달라진다.

## 추론

5KB는 공식 업계 표준이 아니다. Codex 32 KiB와 Claude 25KB는 **잘림 방지 천장**이고, Claude 200줄과 Cursor 500줄은 **준수 품질 권장**이다.

다만 always-on 파일은 매 세션에 올라가므로, 공식 천장까지 채우는 것은 제품 문서와 Anthropic의 high-signal 원칙에 어긋난다. 현재 14KB의 문제는 천장 초과가 아니라 정범 문서 복제로 신호 밀도가 낮다는 점이다.

이 저장소에서 5KB는 “공식 표준”이 아니라 **루트 always-on 지침의 로컬 예산**으로 쓰는 것이 맞다. 세부 작성 규칙은 `CONTRIBUTING.md`, `docs/idea/README.md`, 각 `BLUEPRINT.md`에 두고, `AGENTS.md`에는 정체성, 불변 조건, 승인·게시 경계만 남긴다.

## 이 저장소에 대한 함의

- 5KB를 ADR이나 공개 Blueprint 계약으로 승격하지 않는다.
- 루트 `AGENTS.md`는 5KB 이하를 목표로 유지한다. 넘으면 복제를 줄이고 정범 문서로 연결한다.
- 중첩 `AGENTS.md`나 작업별 문서로 나눌 필요는 아직 없다. 이 저장소는 Blueprint 전용이고 루트 지침 하나로 충분하다.
- 줄 수 200 또는 합산 32 KiB를 이 저장소의 목표로 쓰지 않는다. 전자는 현재 파일보다 느슨하고, 후자는 잘림 한도다.

## 한계

- xAI / Grok Build 공개 문서는 `AGENTS.md` 바이트 한도를 확인하지 못했다.
- 제품 한도는 설정과 버전에 따라 바뀐다. 이 note의 숫자는 2026-08-13 문서 기준이다.
- 짧은 파일이 항상 더 잘 지켜진다는 인과는 이 조사가 측정하지 않았다. 제품 문서의 권장과 context rot 설명을 근거로 한 운영 판단이다.
