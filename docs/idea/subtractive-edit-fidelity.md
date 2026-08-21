# Subtractive Edit Fidelity

## Status

- State: `Parked`
- Last reviewed: 2026-08-21
- Next trigger: 한 줄 결과 계약과 짧은 금지 카탈로그를, 대상 잔존(A)과 부재 서술(B)로 나눠 세는 대조 실험을 실제로 시작할 때 재개한다.

현재는 의도적으로 탐색을 중단했다. 아직 Capability Blueprint, 실행 도구, schema 또는 구현 사양이 아니다. 원인 조사는 [`docs/research/deletion-avoidance-and-rule-inversion.md`](../research/deletion-avoidance-and-rule-inversion.md)에 있다.

## 문제와 배경

범용 코딩 Agent에게 필요 없는 문장, 규칙, 경로를 지우거나 최적화하라고 하면, 대상을 없애기보다 기능하지 않도록 고쳐 남기는 일이 반복된다. 대상을 지운 뒤에도 제목·주석·PR·메모리에 “없음”을 다시 쓰는 일이 같이 반복된다.

이 저장소의 공개 커밋은 A처럼 보이는 치환을 남긴다. 대화 세션은 검증되지 않았다. 운영자는 2026-08-21에, 빼라는 지시를 실제로 하지 않았을 수 있다고 정정했다.

1. `AGENTS.md`에 “GitHub 조회나 변경에는 인증된 `gh`만 사용한다”는 규칙이 있었다. 당시 GitHub connector가 동작하지 않아 생긴 우회였다.
2. connector가 다시 동작한 뒤, 1차 커밋([#42](https://github.com/SWBaek/improvement-ai/commit/de5bd09958129576ea7717f848b24661d9f4ca95))은 절을 지우지 않았다. 같은 절이 “connector를 우선한다. `gh` 전용 정책을 강제하지 않는다”로 남았다. 커밋 제목은 정책을 drop한다고 적었다.
3. 이후 커밋([#43](https://github.com/SWBaek/improvement-ai/commit/39bf2153f38fe467de0355364fd6737528e2b2fa))에서 GitHub 도구 절이 사라졌다.

출력 형태는 A다. 사람이 삭제를 요청했는지는 커밋만으로 단정하지 않는다. 정책 갱신 요청을 반전 문장으로 실현했을 수도 있다.

같은 형태의 치환은 이 예시만이 아니다. 죽은 코드, 쓰이지 않는 기능, 오래된 주석, 최적화 대상 경로에서도 “없애라”가 “끄거나 반대로 적어 남겨라”가 된다. 다만 그 일반화는 빼기 지시가 확인된 과제에만 적용한다.

핵심 불편은 모델이 게으르다는 인상이 아니다. 사람이 공백을 기대한 자리에, 반대 의미의 새 규칙이나 “이것을 빼 달라”는 서술 자체가 남아 이후 세션의 기본 동작까지 왜곡한다는 점이다.

## 현재 관찰

기제는 하나로 본다. 모델은 “없음”을 연산하지 않고 활성화된 주제를 부정형으로 재구성한다. 남는 위치는 둘로 나뉜다.

- **A. 대상 잔존.** 원 문장·경로가 극성 반전, 가드, 주석 처리, feature flag, fallback으로 파일에 남는다. 반전된 규칙은 원 규칙을 폐기하지 않는다. 같은 주제를 반대 방향으로 다시 계약한다.
- **B. 부재 서술 잔존.** 대상은 사라졌는데 제목, 커밋, PR, 주석, 메모리에 “X 없음”, “Y 제거”, “절대 넣지 말 것”이 남는다.

이 저장소 #42는 A 형태의 출력이지만, 빼기 지시가 대화로 확인되지 않아 A 확정이 아니다. 세션이 확인된 실패는 주로 B다. 공개 일화의 토마토 PR 제목과 하치와레 메모리, 아래 프로젝트 사례의 Grok 금지 문장과 `doc-extract-review` 이슈 #32다.

그 밖의 측정된 관찰은 조사 note를 따른다.

- 공개 코드 편집 측정에서도 통과한 패치가 개발자가 지운 줄을 상당 부분 남기고, 그중 다수가 가드로 우회한다.
- “workaround 하지 말라”는 문구만으로는 측정상 거의 나아지지 않는다.
- 정확한 삭제 구간을 알려 주면 미삭제는 줄지만, 그때는 경계를 넘기거나 코드를 추가하는 실패가 늘어난다.
- 실무 `AGENTS.md`에는 주석과 PR을 최종 상태로 쓰라는 긍정 문장이 있다. 확인한 원문은 [liby/dotfiles `AGENTS.md`](https://github.com/liby/dotfiles/blob/main/dot_codex/AGENTS.md)다. 주석은 non-obvious 이유만, PR은 최종 동작과 diff에서 못 읽는 취사만. 이는 B의 출력 표면을 겨눈 관례이지, A·B가 줄었다는 측정이 아니다.
- `never “without X”` 같은 금지 예시 목록, `Make the smallest change`를 삭제 충실도와 같이 두는 조언, 부재를 검사하는 테스트나 후처리 Agent는 공개 논의에서 해법으로 나오지만, 짧은 금지가 이 실패를 고친다는 1차 근거는 없다. “최소 수정”은 A를 더 쉽게 만들 수 있다. 한 줄을 반대로 바꾸는 편이 diff가 작아 보인다.

요청하지 않은 재료를 먼저 넣는 선행 추가는 이 Idea의 본 계약이 아니다. 그 추가가 주제를 활성화한 뒤, 빼라는 요청이 침묵이 아니라 A나 B로 남는 지점만 이 가설의 대상이다.

## 공개 일화

아래는 측정이 아니라 공개 게시물이다. A/B는 이 가설의 읽기이며 원저자의 분류가 아니다.

| 출처 | 관찰된 출력 | 읽기 |
|---|---|---|
| [@songkeys, 2026-08-20](https://x.com/songkeys/status/2090416137720999992) | 토마토계란볶음에 동파육을 넣은 뒤, 빼라는 지시에 PR 제목을 「番茄炒蛋（无东坡肉）」로 쓰고 왜 넣지 않았는지 주석에 장황히 설명 | B. 삭제 결과를 공백이 아니라 제목·주석의 부정문으로 구성한다. |
| [@YAYOFLAKE3, 2026-08-09](https://x.com/YAYOFLAKE3/status/2086275232118272186) | 라면에 계란과 파만 요청했는데 하치와레를 추가한 뒤, 지적받자 “절대 하치와레 넣으라고 지시한 적 없음”을 메모리에 저장 | B. 제거 대신 같은 주제에 대한 금지 계약을 새로 쓴다. |
| [@DrWhitePsyker, 2024-03-19](https://x.com/DrWhitePsyker/status/1769913485931028616) | 제목은 “Scrambled eggs without milk”, 본문 2단계는 우유를 넣음 | 인접하지만 다른 실패다. 제목의 부정이 본문의 부재로 이어지지 않는다. |
| 단일 원문 없이 반복 보고 | “X는 아직 출시되지 않았으니 언급하지 마라”는 지시가 결과물에 “X는 출시되지 않았으므로 다루지 않는다”는 문장으로 남음 | B. 금지 지시를 이행 증명으로 다시 쓴다. |
| 원글 답글 [@wladston](https://x.com/wladston/status/2090478510401855558), [@markizko](https://x.com/markizko/status/2090468464947261867) | 동파육이 없음을 보장하는 테스트와, 다른 요리의 기본 경로에 동파육을 남기는 fallback까지 추가한다는 지적 | 독립 세션 로그가 아니다. A와 같은 등급의 실패 형태를 유추한 확장이다. |

## 프로젝트 사례

2026-08-21에 열린 Paseo 워크스페이스의 git 산출물과, 확인된 한 Codex 세션을 읽었다. 비공개 경로와 vault 내용은 적지 않는다. A/B는 이 가설의 읽기다.

| 출처 | 관찰된 출력 | 읽기 |
|---|---|---|
| [sdoc-editor `c041cd5`](https://github.com/SWBaek/sdoc-editor/commit/c041cd57cb65ca2e3c76e0f457acada55264f174) → [`5565886`](https://github.com/SWBaek/sdoc-editor/commit/556588650b040c428d1b091a2f5dec96635d20e1) → [`4892442`](https://github.com/SWBaek/sdoc-editor/commit/4892442d32110916ace39581bc5ee19e06e78fac) | 2026-08-05 Grok advisor 규칙을 `AGENTS.md`에서 지운 뒤, 같은 날 다른 PR이 `Do not use Grok CLI… The project no longer maintains or requires them.`을 다시 넣었다. 이틀 뒤 orchestration 제거와 함께 그 문장도 사라졌다. | **B.** 대상은 이미 없는데 금지·“no longer” 계약으로 주제가 돌아온다. 공개 일화의 하치와레 메모리와 같은 형태다. 대화 세션은 이 데몬에 없다. 커밋 순서로만 읽는다. |
| [doc-extract-review #32](https://github.com/SWBaek/doc-extract-review/issues/32) (2026-08-21 Codex 세션) | 범위 밖 `mineru-local` 파일을 고친 뒤, 복구하라는 지적을 받고 되돌렸다. 이어서 기술 스택 이슈 본문에 그 폴더를 수정하지 않는다고 명시했다. 사람이 “이런 말은 넣지 마세요. 애초에 연관없던 거잖아요”라고 하자 본문에서 경로를 지웠다. | **B, 세션 확인.** 선행 추가는 별 가설이다. 이 Idea가 겨누는 지점은 복구 뒤에 무관한 이슈에 “수정하지 않는다”를 쓴 것이다. 두 번째 지적 뒤 현재 이슈 본문에는 경로가 없다. |
| [sdoc-editor `b83087d`](https://github.com/SWBaek/sdoc-editor/commit/b83087d68c468f1b17c8c0e5ed249b5a46183373) | 2026-08-13 `GitHub operations` 절을 통째로 삭제했다. PR 제목·본문은 CLI-only 제한을 drop하고 `no longer need to be restricted to authenticated gh`라고 적었다. 파일에는 반전 문장이 남지 않았다. | **정책 절 삭제.** 본 작업이 폐기로 읽히면 제목의 제거 서술은 잔여 동작이다. 이 저장소 #42와 “같은 빼기 요청”이라고 단정하지 않는다. |
| 제어 아키텍처 프로젝트 `5ce0b41` (2026-08-18) | Continuity·Focus 절과 프로젝트 로컬 Skill을 삭제하고, 폐기를 활성 Decision으로 기록했다. `AGENTS.md`에는 금지 대체 문장이 남지 않았다. | **삭제 + 정당한 결정 기록.** 운영 체계 폐기가 본 작업이고, 결정 로그가 그 잔여 동작이다. B가 아니다. |
| 개인 WorkOs `AGENTS.md` (2026-08-21 현재) | `gh` 전용 GitHub 규칙은 아직 현행이다. 버린 프로젝트 필드명을 새 기록에 쓰지 말라는 금지 목록은 남아 있다. | **`gh`는 A가 아니다.** 폐기 요청의 잔존이 확인되지 않았다. 필드 금지 목록은 마이그레이션이 끝났다면 **B 후보**, 아직이면 정당한 반전이다. |

질문방 워크스페이스는 빈 디렉터리였다. Tailscale 운영 저장소의 최근 산출물에서는 A/B를 보지 못했다.

## 현재 가설

가칭 `Subtractive Edit Fidelity`는 해결하려는 편집 결과다. 요청이 폐기·삭제·제거·거절한 추가의 철회이면, 대상과 그 부재에 대한 문장이 산출물 전체에서 없어야 한다. 산출물은 편집된 파일만이 아니다. 제목, 커밋, PR, 주석, 세션 메모리도 같은 잔존 표면이다. 요청이 동작을 끄되 흔적을 남기라는 것이면 그때만 가드나 반전 문장이 허용된다.

```text
학습 분포와 평가
  덧셈형 수정이 많고, 테스트는 제거를 잘 검사하지 않음
        ↓
내부 부정 연산
  “not Y”를 지움이 아니라 새 표현으로 구성함
        ↓
편집 도구와 Agent 지침
  치환이 기본이고, 최소 수정·비파괴가 보상됨
        ↓
남는 결과
  A: 반전, 가드, 주석, fallback
  B: 제목·PR·주석·메모리의 “없음” 서술
```

이 습관은 특정 제품의 버그라기보다, 여러 모델이 공유하는 편집 기본값으로 보는 편이 맞다. 사전학습 분포 자체는 이 저장소가 고치지 않는다.

“빼라”는 교정 지시 자체가 `Y`를 다시 활성화한다. 같은 가설의 조작 후보는 뺄셈 명령이 아니라 잔여 산출물의 재지정이다. 예: “동파육 빼고 PR 올려”가 아니라 “산출물은 토마토계란볶음이다.” 사람이 폐기를 반대 문장 작성과 구분하면, 상시 지침 없이도 B가 줄 수 있다.

전달 형태는 Skill보다 always-on 결과 기준에 가깝다. 트리거 있는 작업이 아니라 빼기·폐기·교정이 있는 세션에서 나타난다. 탐색 중인 문장은 금지 목록이 아니라 결과다.

```text
A deletion is complete when the target and any sentence
about its absence are both gone.
Titles, commits, and comments describe remaining behavior.
```

짧은 금지 카탈로그(`never “without X”`, 과정·제거 흔적 금지 예시)는 비교 팔이지 채택 후보가 아니다. 부정 예시는 바로 이 실패 모드를 재현할 수 있고, 코드 벤치마크에서 “workaround 하지 마라”는 거의 효과가 없었다.

`AGENTS.md` 운영 팁 카테고리는 이 Idea가 만들지 않는다. 한 줄이 측정되면 대상 프로젝트의 기존 always-on 파일에 넣는 Blueprint operation이거나 research 결과로 두는 편이, 팁 선반을 먼저 만드는 편보다 작다. 이 저장소 루트 `AGENTS.md`에 넣는 것은 전달 후보가 아니다.

## 기대 효과와 비목표

기대하는 결과는, 사람이 “이 규칙을 폐기해”, “이 경로를 지워”, “이것을 빼”, “이것을 최적화해”라고 했을 때 Agent가 다음을 구분하는 것이다.

- **삭제:** 대상 문장·경로와 그 부재 서술이 파일, 제목, 커밋, PR, 주석, 메모리에 없다.
- **비활성화:** 사람이 흔적 보존을 명시한 경우에만 가드, flag, 주석이 남는다.
- **반전:** 예전 규칙을 반대로 다시 쓰는 것은 폐기가 아니다. 새 계약이 필요할 때만 별도 문장으로 추가한다.
- **교정:** 거절한 추가를 철회할 때는 뺄셈을 서술하지 않고 잔여 산출물을 재지정한다.

비목표는 다음과 같다.

- 모델 가중치를 재학습하거나 특정 제품 runtime을 고치는 일
- 모든 최소 수정을 금지하는 일
- 삭제를 강제하는 schema, generator, validator, CI
- 전역 Agent Skill이나 사용자 홈에 편집 습관 교정기를 설치하는 일
- 최적화 요청을 무조건 삭제로 해석하는 일
- 효과 측정 없이 이 저장소 루트 `AGENTS.md`에 편집 습관 문단을 상시 추가하는 일
- 원인 논문을 더 모아 같은 결론을 반복하는 일
- `AGENTS.md` 운영 팁 카테고리나 팁 목록을 먼저 만드는 일
- 측정 전에 “이 한 줄을 넣으면 현상이 사라진다”고 홍보하는 일
- 짧은 금지 카탈로그를 검증된 해법으로 채택하는 일
- 부재를 검사하는 테스트나 후처리 Agent를 해법으로 두는 일
- 선행 추가를 같은 계약으로 묶는 일

## 위험과 반례

- 어떤 변경은 진짜로 반전 계약이 필요하다. “더 이상 `gh`를 강제하지 않는다”를 명시해야 다른 Agent의 기본값이 다시 `gh`만 쓰게 하는 경우가 있을 수 있다. 그때 공백은 의도가 아니다.
- 요청 자체가 공개 동작의 제거일 수 있다. 제목 `Remove legacy adapter`는 잔여 동작을 서술한다. `never “removed Y”`는 그 변경을 잘못된 잔존으로 오인한다. 이 가설이 겨누는 것은 범위 밖·거절된 요소의 부재 광고이지, 제거가 본 작업인 변경의 이름 붙이기 금지가 아니다.
- 정확한 줄을 강조하면 초과 삭제가 늘어난다는 측정이 있다. 삭제 충실도를 올리다가 관련 없는 인접 규칙을 지울 수 있다.
- “최소 수정”과 “대상 부재”는 충돌할 수 있다. 한 줄을 반대로 바꾸는 편이 diff는 작아 보인다.
- 정책 문장 반전(A)과 제목·PR·이슈의 “없음” 서술(B)을 같은 한 줄이 고친다는 것은 아직 가설이다. 금지 팔은 B만 줄이고 A는 안 줄거나, 금지 예시를 따라 쓸 수 있다.
- 반전 출력을 A로 읽으려면 빼기 지시가 대화로 확인돼야 한다. 커밋 제목의 drop만으로는 부족하다.
- 생성 지침이 길어지면 always-on 예산을 잠식한다. 이 습관을 루트 `AGENTS.md`에 장황히 복제하면 안 된다.

## 검증 기준 또는 실험 질문

다음 대조가 재개 조건이다. 같은 빼기 과제를 두 종류로 둔다. 정책 문장 삭제(A에 가깝다)와, 추가를 거절한 뒤의 PR(B에 가깝다).

| 팔 | 문장 |
|---|---|
| T0 | 추가 지침 없음 |
| T1 | 세션에 결과 계약. 대상과 부재 서술이 모두 없고, 서술은 잔여 동작만 |
| T2 | 세션에 짧은 금지 카탈로그. `without X`·과정·제거 흔적 금지 예시 |
| T3 | T1과 같은 문장을 대상 프로젝트 always-on에 둠 |
| T4 | 추가 지침 없이, 사람이 “빼라” 대신 잔여 산출물을 재지정 |

세는 항목은 분리한다.

1. A: 원 대상이 파일에 남아 있는가?
2. B: 부재 서술이 파일, 제목, 커밋, PR, 주석, 메모리에 남아 있는가?
3. 초과 삭제: 관련 없는 인접 문장·경로가 지워졌는가?

열린 질문:

1. T1이 T0보다 A와 B를 모두 줄이는가? 조사 note는 프롬프트만의 삭제는 비관적이다.
2. T2가 B만 줄이고 A는 안 줄거나, 금지 예시를 재현하는가?
3. T3의 always-on이 T1의 세션 한 줄과 다른가? 코드 CanItDelete의 비관적 결과가 여기에도 그대로인가?
4. T4만으로 B가 줄면, 상시 문장보다 교정 턴의 재지정이 작은 해법인가?
5. 같은 요청을 Codex, Grok, 다른 Agent에 반복하면 잔존 비율이 제품보다 과제 유형에 더 의존하는가?

아직 T0 밖의 팔은 이 저장소에서 측정하지 않았다. B는 sdoc-editor 커밋 순서와 `doc-extract-review` #32 세션으로 확인됐다. 이 저장소 #42는 A 형태 출력이며, 빼기 지시가 확인되지 않아 A 확정이 아니다.

## 향후 탐색

- 다음 조사는 문헌이 아니라 위의 대조 실험이다. 공개 일화, sdoc-editor Grok 줄, `doc-extract-review` #32는 B 과제 표면의 후보다. sdoc-editor `gh` 절 삭제와 아키텍처 Continuity 폐기는 절을 지운 대조다. 실무 `AGENTS.md` 문장은 T1의 긍정형 재료다. 짧은 금지가 검증됐다는 주장은 실험이 기각할 수 있는 비교 팔로만 둔다.
- 실험 문장은 “반전하지 마라”가 아니라 결과여야 한다.
- 효과가 있어도 이 저장소 `AGENTS.md`에는 정체성·불변·승인 경계만 둔다는 기존 예산을 깨지 않게, 한 줄 이내로만 검토한다. 대상 프로젝트의 기존 always-on 파일은 별 표면이다.
- 한 줄이 슬로건을 만족하면 그때 전달 형태를 고른다. 기본 후보는 새 카테고리가 아니라, 대상 프로젝트 always-on 파일에 그 문장을 넣는 Blueprint operation 또는 research 결과다.
- 효과가 없거나 초과 삭제가 늘면 Skill, 팁 목록, Blueprint로 올리지 않는다.
- 모델 재학습이나 제품 버그 신고로 범위를 넓히지 않는다.
- 선행 추가를 같은 계약으로 묶는 것은 별 가설이다.

## 관련 출처와 후속 링크

- 조사: [`docs/research/deletion-avoidance-and-rule-inversion.md`](../research/deletion-avoidance-and-rule-inversion.md)
- [sdoc-editor `c041cd5`](https://github.com/SWBaek/sdoc-editor/commit/c041cd57cb65ca2e3c76e0f457acada55264f174), [`5565886`](https://github.com/SWBaek/sdoc-editor/commit/556588650b040c428d1b091a2f5dec96635d20e1), [`4892442`](https://github.com/SWBaek/sdoc-editor/commit/4892442d32110916ace39581bc5ee19e06e78fac): B. Grok 규칙 삭제 후 금지 문장 재삽입
- [doc-extract-review #32](https://github.com/SWBaek/doc-extract-review/issues/32): B, 세션 확인. 복구 뒤 무관한 이슈에 “수정하지 않는다”를 명시
- [sdoc-editor `b83087d`](https://github.com/SWBaek/sdoc-editor/commit/b83087d68c468f1b17c8c0e5ed249b5a46183373): 정책 절 삭제. 빼기 지시와의 동일성은 단정하지 않음
- [liby/dotfiles `AGENTS.md`](https://github.com/liby/dotfiles/blob/main/dot_codex/AGENTS.md): 주석과 PR의 최종 상태 문장. B 표면의 실무 관례, 효과 측정 아님
- [@Nominatiivi, 2026. 토마토 원글에 그 파일을 가리킨 답글](https://x.com/Nominatiivi/status/2090464250573779338)
- [@songkeys, 2026. 番茄炒蛋와 东坡肉 PR 제목](https://x.com/songkeys/status/2090416137720999992)
- [@YAYOFLAKE3, 2026. 라면과 하치와레 메모리](https://x.com/YAYOFLAKE3/status/2086275232118272186)
- [@DrWhitePsyker, 2024. Scrambled eggs without milk](https://x.com/DrWhitePsyker/status/1769913485931028616)
- [Ebrahimi et al., 2026. *To Add Is Machine, To Delete Is Human*](https://arxiv.org/abs/2607.28887)
- [Santagata & De Nobili, 2024. *More is More: Addition Bias in Large Language Models*](https://arxiv.org/abs/2409.02569)
- [Zhou et al., 2026. *How Language Models Process Negation*](https://arxiv.org/abs/2605.03052)
- [Adams et al., 2021. *People systematically overlook subtractive changes*](https://doi.org/10.1038/s41586-021-03380-y)
