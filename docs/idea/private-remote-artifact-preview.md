# Private Remote Artifact Preview

## Status

- State: `Exploring`
- Last reviewed: 2026-08-10
- Next trigger: 단일 고정 Tailscale Serve port와 전용 Artifact Root를 사용하는 개인 전역 Skill Pilot에서 정적 게시, 충돌 방지, Dashboard와 cleanup을 검증하고, 동적 app의 subpath 호환 실패가 반복될 때 Hub runtime 또는 사전 할당 port pool의 필요성을 판단한다.

## 문제와 배경

주 작업은 집에 있는 컴퓨터에서 실행되지만, 사람은 외부에서 태블릿이나 휴대전화로 원격 접속해 AI와 협업한다. 현재는 터미널 중심 원격 접속 도구를 사용하며, 과거에는 `ttyd`와 `zellij` 조합도 사용했다.

AI가 생성한 HTML, 시각화, 디버깅 화면처럼 터미널에서 검토하기 어려운 중간 결과물은 Tailscale Serve로 임시 호스팅하고 tailnet 내부 URL에서 확인한다. 이 방식 자체는 유용하지만 프로젝트가 바뀔 때마다 사람은 AI에게 다음 사항을 반복해서 설명해야 한다.

- 현재 사용자는 외부 기기에서 터미널만 보고 있다는 점
- 시각적 결과는 원격에서 접근 가능한 형태로 제공해야 한다는 점
- Tailscale Serve를 사용하고 공개 인터넷에는 노출하지 않아야 한다는 점
- 이미 사용 중인 port와 Serve 구성을 확인해야 한다는 점
- 접근 URL, 실행 상태와 종료 방법을 알려줘야 한다는 점

핵심 불편은 특정 명령을 기억하는 것이 아니라, 여러 프로젝트에서 같은 원격 검토 환경과 안전 조건을 AI에게 계속 재설명해야 한다는 것이다.

## 현재 관찰

- 원격 터미널만으로는 복잡한 HTML과 대화형 결과물을 검토하기 어렵다.
- Tailscale Serve를 이용하면 같은 tailnet의 개인 기기에서 결과물을 확인할 수 있다.
- 프로젝트마다 AI의 기본 가정이 달라 호스팅 제안 여부와 방식이 일관되지 않다.
- 임의 port 선택은 기존 local listener 또는 Serve 설정과 충돌할 수 있다.
- background Serve와 local server가 남으면 어떤 결과물이 아직 노출 중인지 파악하기 어렵다.
- Windows의 일반 권한 터미널에서는 새 Serve 구성이 실패하여 사람이 원격으로 관리자 터미널을 열고 명령을 반복 실행해야 한다.
- 일반 권한에서도 `tailscale serve status --json`으로 기존 endpoint를 조회할 수 있으므로 조회와 Dashboard는 privileged mutation과 분리할 수 있다.
- 한 장비에서 여러 Serve endpoint가 실제로 병행되고 있어 port만으로 소유 프로젝트, artifact, 생성 시각과 안전한 종료 대상을 복구하기 어렵다.
- 이 불편은 프로젝트 내부 상태보다 사용자 장비와 원격 작업 방식에 가깝다.

실제 tailnet hostname, 개인 장비 이름, 프로젝트 경로와 접근 URL은 이 공개 Idea에 기록하지 않는다.

## 현재 가설

AI가 원격 작업 상황을 인식했을 때 시각적 결과물을 안전하게 게시하고 접근 URL과 종료 방법을 반환하는 **개인 전역 Skill**이 반복 지시를 줄일 수 있다. 전역 Skill은 Tailscale 전체를 관리하지 않고 private artifact preview lifecycle만 다룬다.

가칭 `Private Remote Artifact Preview`는 해결하려는 사용자 경험을 나타낸다. Tailscale Serve는 현재 환경의 transport adapter이고 Skill은 그 위에서 artifact 등록, 충돌 방지, inventory, URL 반환과 cleanup을 조율한다. HTML, 이미지, PDF와 정적 directory를 최초 범위로 삼고 localhost 개발 서버는 경로 호환성에 따라 후속 범위를 결정한다.

### 현재 선도 가설: 한 번 Serve하고 이후에는 등록만 한다

관리자는 최초 한 번 전용 public Artifact Root 또는 일반 권한으로 실행되는 local Hub를 고정 Tailscale HTTPS port 하나에 연결한다. 이후 Agent는 `tailscale serve`를 다시 호출하지 않고 일반 권한 helper를 통해 artifact를 등록한다.

```text
one-time administrator setup
Tailscale Serve :<fixed-port>
        ↓
dedicated public Artifact Root or localhost Preview Hub
        ↓
global Skill + deterministic helper
        ├─ publish
        ├─ list / inspect
        ├─ unpublish / cleanup
        └─ render Dashboard
```

PowerShell script를 privileged broker로 만들거나 실행 때마다 UAC elevation을 요청하지 않는다. 최초 Tailscale 설정은 사람이 관리자 terminal에서 수행하고, 정상적인 게시 lifecycle은 일반 권한에서 끝나야 한다.

### 정적 Artifact v0.1

정적 HTML, PDF, 이미지와 directory는 외부 port 하나 아래의 고유 path로 게시할 수 있다.

```text
https://<tailnet-host>:<fixed-port>/
https://<tailnet-host>:<fixed-port>/previews/<preview-id>/
```

Skill의 deterministic helper는 artifact를 직접 원본 위치에서 노출하지 않고 전용 public root로 복사한다. registry와 내부 절대경로는 public root 밖에 둔다. Dashboard `index.html`은 공개 가능한 metadata만 사용해 현재 preview 목록, 상태, 생성 시각과 종료 방법을 보여주는 파생물이다.

### 동적 Artifact 적응 가설

일반 권한 local Hub가 reverse proxy를 소유하면 하나의 외부 port에서도 여러 backend를 path로 분리할 수 있다.

```text
/<preview-a>/ → 127.0.0.1:<local-port-a>
/<preview-b>/ → 127.0.0.1:<local-port-b>
```

그러나 absolute asset path, root redirect, Cookie `Path=/`, WebSocket, HMR, Service Worker, CSP와 OAuth callback을 고정한 app은 subpath에서 실패할 수 있다. v0.1에서 범용 rewriting proxy를 만들지 않는다. 실제 실패가 반복되면 관리자가 최초에 허용한 소수의 external/backend port slot을 fallback pool로 준비하고 Skill이 빈 slot만 할당하는 방식을 비교한다.

## 미결정 구현 후보

| 후보 | 적합할 수 있는 조건 | 현재 불확실성 |
|---|---|---|
| 개인 지침 | 사용 빈도가 낮고 매번 요구가 다름 | 반복 관리자 작업과 inventory 요구를 해결하지 못함 |
| 개인 전역 Agent Skill + helper | 정적 artifact를 한 고정 port와 전용 root로 관리 | 현재 가장 작은 Pilot 후보이며 동시 쓰기와 cleanup이 안전한가 |
| 일반 권한 Preview Hub | 동적 backend, healthcheck와 지속 Dashboard가 필요함 | 실제 subpath proxy 실패와 process ownership 요구가 반복되는가 |
| Capability Blueprint | 여러 사용자 환경과 transport에서 같은 contract가 반복됨 | 아직 개인 환경 외 evidence가 있는가 |
| 별도 제품 저장소 | daemon, durable registry, 여러 host 또는 adapter를 운영해야 함 | Skill bundled helper로 해결할 수 없는 lifecycle 실패가 확인되는가 |

현재 저장소의 Blueprint가 생성하는 capability는 프로젝트 로컬 설치가 원칙이다. 이 Idea의 개인 전역 Skill과 사용자 환경 registry는 프로젝트 상태를 소유하는 Blueprint 생성물의 전역 설치 예외가 아니다. 서로 다른 capability 범주이며, 이 저장소에는 Idea와 재사용 가능한 학습만 두고 실제 전역 Skill, helper와 runtime은 별도 사용자 환경에서 Pilot한다.

## 잠정적인 안전 경계

아직 공개 계약은 아니지만 다음 위험은 초기 관찰에서 반드시 검증한다.

- Tailscale Funnel처럼 공개 인터넷에 노출하는 기능을 자동 대안으로 사용하지 않는다.
- proxy backend는 가능한 경우 localhost에만 bind한다.
- 게시 전에 기존 Serve 상태와 관련 port 사용 여부를 확인한다.
- Tailscale configuration mutation은 최초 setup 경계로 제한하고 정상 publish operation에서는 실행하지 않는다.
- 전용 public root 밖의 원본 프로젝트 directory를 직접 Serve하지 않는다.
- 저장소 전체, 상위 directory, 인증 정보, `.env`, Git metadata, source map과 의도하지 않은 파일을 복사하거나 directory listing으로 공개하지 않는다.
- path traversal, symlink와 junction을 통해 public root 밖으로 벗어나지 못하게 한다.
- background 또는 persistent route는 고정 Hub/root에만 사용하고 각 artifact의 종료와 cleanup 방법을 항상 제시한다.
- 기존 Serve 구성을 전체 reset하거나 다른 프로젝트의 route를 덮어쓰지 않는다.
- Dashboard에 실제 tailnet hostname, 개인 장비 이름과 원본 절대경로를 저장하지 않는다.
- privileged process가 임의 artifact path를 읽거나 Agent가 제공한 raw command를 실행하게 하지 않는다.
- 외부 쓰기, 장기 실행과 접근 범위에 필요한 인간 승인 경계를 구분한다.

## 기대 효과

- 프로젝트마다 원격 접속 조건과 호스팅 지시를 반복하지 않는다.
- AI가 터미널에 부적합한 결과물을 원격 검토 가능한 형태로 일관되게 제안한다.
- port와 기존 Serve route 충돌을 줄인다.
- 사용자가 현재 게시 중인 결과물, 접근 URL과 종료 방법을 알 수 있다.
- 일반 권한 Agent가 관리자 terminal과 UAC 상호작용 없이 정적 artifact lifecycle을 끝낼 수 있다.
- 하나의 고정 Tailnet URL과 Dashboard에서 여러 프로젝트의 preview를 찾을 수 있다.
- tailnet 내부 공개와 public exposure를 혼동하는 위험을 낮춘다.

## 비목표

- 지금 단계에서 공개 Tailscale 전용 Blueprint나 범용 제품을 확정하는 것
- 이 저장소에 runtime, CLI, server manager 또는 전역 Skill을 구현하는 것
- Tailscale node, account, ACL, DNS, exit node와 일반 VPN 설정 전체를 관리하는 것
- 공개 웹 호스팅 또는 Tailscale Funnel을 자동화하는 것
- production service 배포, 사용자 인증 체계 또는 장기 artifact 보관을 제공하는 것
- 프로젝트의 일반적인 개발 server와 deployment workflow를 대체하는 것
- 모든 동적 web framework를 HTML rewriting으로 하나의 subpath에 강제로 호환시키는 것

## 위험과 반례

### 개인 환경에 지나치게 특화될 가능성

문제가 한 사람의 장비 구성과 접속 습관에만 존재한다면 공개 Blueprint보다 개인 Skill이 더 적합하다. 유사한 원격 작업 사례나 환경 adapter의 반복성이 확인되기 전에는 일반 capability로 승격하지 않는다.

### 전역 capability의 권한 확대

여러 프로젝트에서 자동으로 동작하는 Skill은 잘못된 directory를 게시하거나 기존 Serve 설정을 변경할 수 있다. Skill은 원본 directory를 직접 노출하지 않고 전용 public root로 선택된 artifact만 복사해야 한다. 편의성만으로 프로젝트 경계와 명시적 승인 원칙을 약화해서는 안 된다.

### 작은 절차를 제품으로 과대 설계할 가능성

단일 고정 port, 전용 root, file registry와 정적 Dashboard만으로 문제가 해결된다면 daemon, database와 범용 reverse proxy는 불필요하다. 실제로 동적 backend health, process ownership, automatic expiry와 proxy 호환 실패가 반복될 때만 local Hub 또는 별도 제품을 검토한다.

### 임시 게시의 잔존

background mode나 재부팅 후 복구되는 설정은 의도보다 오래 남을 수 있다. 자동 만료가 필요한지, 사용자가 명시적으로 종료하면 충분한지는 사용 과정에서 확인한다.

### 한 port의 동적 app 호환성

정적 artifact에는 path namespace가 충분하지만 임의의 동적 app은 자신이 URL root를 소유한다고 가정할 수 있다. 한 port만 지원한다는 목표 때문에 범용 proxy rewriting을 과도하게 구현하지 않는다. 먼저 base path를 지원하는 app만 Hub mode로 처리하고 실패 evidence가 있을 때 port pool fallback을 검토한다.

### 공유 registry 동시성

여러 Agent가 동시에 publish 또는 cleanup하면 ID, registry와 Dashboard가 충돌할 수 있다. 자연어 절차만으로 관리하지 않고 atomic write, lock과 owner 확인을 수행하는 작은 deterministic helper가 필요한지 Pilot에서 검증한다.

## 검증 질문

- 원격 작업에서 어떤 artifact 유형이 실제로 반복 게시되는가?
- AI가 전역 Skill과 deterministic helper만으로 안전하게 게시·보고·종료할 수 있는가?
- 정적 artifact를 전용 public root로 복사하는 비용과 원본 갱신 지연이 허용 가능한가?
- 하나의 고정 Tailscale HTTPS port와 path namespace로 실제 정적 사례를 모두 처리할 수 있는가?
- 한 번에 여러 프로젝트의 preview를 유지해야 하는가?
- 고유 Preview ID, 프로젝트 별칭과 display name 중 Dashboard 탐색에 필요한 최소 metadata는 무엇인가?
- terminal 또는 Agent session 종료 시 preview도 종료해야 하는가?
- cleanup은 명시적 unpublish, 다음 Skill 실행 시 만료 정리 또는 지속 Hub 중 어디까지 필요한가?
- registry는 단일 JSON과 atomic lock으로 충분한가?
- 어떤 filesystem 범위와 server 유형은 자동 게시할 수 있고 무엇은 사람 승인이 필요한가?
- 어떤 동적 app이 subpath reverse proxy에서 실제로 실패하며 소수의 pre-served port pool이 필요한가?
- Tailscale이 없는 환경까지 적응해야 하는가?
- 다른 사용자에게도 반복되는 문제인가, 아니면 개인 전역 Skill로 충분한가?

## 다음 탐색

첫 Pilot은 개인 전역 Skill과 bundled deterministic helper를 사용한다. 관리자가 고정 port 하나와 전용 public root를 최초 한 번 Serve한 뒤 다음을 최소 세 사례에서 관찰한다.

1. 정적 HTML directory, PDF 또는 이미지 publish
2. 고유 path와 Dashboard 등록 및 다른 프로젝트와의 충돌 방지
3. 일반 권한 list, inspect, unpublish와 cleanup
4. 원본 외 파일, 절대경로와 비밀정보가 공개되지 않는지 확인
5. 동적 app 하나를 base-path 방식으로 시험하고 실패 원인을 분류

정적 root 방식이 충분하면 전역 Skill 범위에 머문다. 지속 process와 health 관리가 필요하면 일반 권한 Preview Hub를 검토한다. root-bound 동적 app 실패가 반복되면 관리자가 최초에 Serve한 작은 port pool을 fallback으로 검토한다. 여러 사용자·transport에서 같은 문제와 invariant가 확인될 때만 Candidate issue와 Blueprint 승격을 검토한다.

## 관련 출처

- [시장과 인접 제품 benchmark](../research/bencmark/private-remote-artifact-preview-market.md): private network, public tunnel, IDE forwarding, remote workspace와 framework별 공유 기능 비교
- [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve): tailnet 내부 공유, access control과 identity header의 보안 특성을 확인하기 위한 공식 설명
- [Tailscale Serve CLI](https://tailscale.com/docs/reference/tailscale-cli/serve): route, port, status, reset과 background 동작을 확인하기 위한 명령 명세
- [Tailscale Serve examples](https://tailscale.com/docs/reference/examples/serve): 정적 파일과 개발 server 게시, foreground/background lifecycle 사례
- [Tailscale security bulletins](https://tailscale.com/security-bulletins): privileged daemon과 local operator가 file serving boundary를 잘못 구성할 때의 위험을 확인하기 위한 보안 근거
