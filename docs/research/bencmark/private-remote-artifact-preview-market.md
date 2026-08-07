# Private Remote Artifact Preview 시장 Benchmark

- 조사일: 2026-08-07
- 상태: Research note. 채택된 결정, 제품 요구사항 또는 Blueprint 계약이 아니다.
- 관련 Idea: [Private Remote Artifact Preview](../../idea/private-remote-artifact-preview.md)
- 목적: 로컬 컴퓨터에서 생성된 HTML·시각화·개발 화면을 외부 개인 기기에서 안전하게 검토하는 기존 제품을 비교하고, 전역 Skill·Capability Blueprint·별도 제품 중 어떤 형태를 추가 검증할 가치가 있는지 평가한다.

## 조사 질문

1. 기존 시장은 local service를 원격 browser에 전달하는 문제를 어떻게 해결하는가?
2. private-by-default 접근, URL 발급, port 발견, 상태 조회와 종료를 어디까지 제공하는가?
3. AI가 여러 프로젝트에서 artifact preview를 제안하고 lifecycle을 관리하는 문제까지 해결하는 제품이 있는가?
4. 현재 Idea는 기존 도구의 얇은 orchestration으로 충분한가, 별도 runtime이 필요한가?

## 비교 범위와 기준

공식 제품 문서에서 2026-08-07 현재 확인 가능한 behavior를 다음 기준으로 비교했다.

- **접근 경계**: 개인 또는 승인된 사용자만 접근하는지, public URL인지
- **host 위치**: 기존 local/home computer를 그대로 사용하는지, vendor workspace나 cloud deployment가 필요한지
- **artifact 범위**: 임의 HTTP service·정적 파일을 지원하는지, 특정 framework에 한정되는지
- **발견과 URL**: listening port 감지, URL 생성과 표시가 가능한지
- **lifecycle**: 현재 route 조회, foreground/background, 명시적 종료와 잔존 상태를 다루는지
- **AI workflow**: Agent가 결과물 유형과 원격 상황을 판단해 게시 여부, 안전 범위와 cleanup을 조율하는지

가격은 plan과 시점에 따라 자주 변하고 이번 문제의 핵심 판별 기준도 아니므로 정량 비교에서 제외했다. 실제 설치·성능·모바일 사용성은 시험하지 않았으며 공식 문서에 명시된 기능만 비교했다.

## 시장 지도

```text
기존 local/home computer 유지
├─ Private overlay network
│  └─ Tailscale Serve
├─ Internet ingress tunnel
│  ├─ Cloudflare Quick Tunnel / Cloudflare Tunnel
│  └─ ngrok
└─ IDE-integrated tunnel
   └─ Visual Studio Code Port Forwarding / Remote Tunnels

작업환경 자체를 vendor가 소유
├─ GitHub Codespaces
├─ Coder
└─ Ona

특정 application framework가 공유 기능 소유
├─ Gradio Share Links
└─ Streamlit Community Cloud
```

첫 그룹은 현재 home computer를 유지할 수 있어 Idea와 직접 경쟁하거나 기반 기술이 된다. 나머지는 preview UX의 benchmark이지만 작업환경 또는 application framework를 바꿔야 하므로 그대로 대체하지는 못한다.

## 제품 비교 요약

| 제품군 | 대표 제품 | 기본 접근 경계 | 기존 home computer | 임의 local HTTP | 상태·종료 primitive | AI가 artifact lifecycle 조율 |
|---|---|---|---|---|---|---|
| Private overlay | Tailscale Serve | tailnet과 access policy | 가능 | 가능 | status, config, foreground/background, off | 없음 |
| Public ingress tunnel | Cloudflare Quick Tunnel | public Internet | 가능 | 가능 | foreground process 중심 | 없음 |
| Policy-controlled ingress | ngrok | Internet endpoint, policy로 제한 | 가능 | 가능 | Agent와 endpoint 관리 | 없음 |
| IDE tunnel | VS Code Port Forwarding | 기본 private account 인증 | 가능 | 가능 | Ports UI와 tunnel lifecycle | IDE 내부 자동 감지 일부 |
| Cloud dev environment | GitHub Codespaces | 기본 private | 불가, Codespace 안에서 실행 | 가능 | Ports UI/CLI, visibility | localhost URL 자동 감지 |
| Remote workspace platform | Coder | owner 기본, 배포 policy | 별도 workspace 필요 | 가능 | port 감지, dashboard, app healthcheck | workspace template 중심 |
| Cloud dev environment | Ona | 배포·runner별 access level | local environment 미지원 | 가능 | listening port 조회, CLI open | Agent output에 preview URL 연결 |
| Framework share/deploy | Gradio / Streamlit | Gradio share는 public, Streamlit은 배포 정책 | framework별 상이 | 범용 아님 | framework process/deployment | framework가 생성한 app에 한정 |

`AI가 artifact lifecycle 조율` 열은 공식 문서에서 확인된 범위를 기준으로 한다. 제품이 API나 CLI를 제공한다고 해서 AI가 안전한 게시 판단과 cleanup policy를 내장한다고 추론하지 않았다.

## 직접 경쟁·기반 기술

### Tailscale Serve

[Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve)는 local port, file 또는 directory를 같은 tailnet에 제공하고 tailnet access control을 그대로 적용한다. Funnel과 달리 public Internet 공유를 목적으로 하지 않으며, 같은 port를 Serve와 Funnel에 동시에 사용할 수 없다.

[Serve CLI](https://tailscale.com/docs/reference/tailscale-cli/serve)는 다음 primitive를 이미 제공한다.

- local HTTP reverse proxy와 file/directory serving
- HTTPS 또는 HTTP listener port와 URL path 지정
- `tailscale serve status --json`과 전체 config 조회
- foreground 실행과 `--bg` persistent 실행
- route 비활성화와 전체 reset

Idea와의 적합성:

- 이미 설치된 private identity와 network를 재사용하므로 개인 원격 preview의 transport로 가장 직접적이다.
- home computer에서 실행 중인 결과물을 다른 개인 기기에서 열 수 있다.
- access control과 MagicDNS·TLS를 별도 preview 제품이 다시 구현할 필요가 없다.

남는 문제:

- 어떤 artifact를 게시할지, static file server와 application server 중 무엇을 시작할지 결정하지 않는다.
- local listener와 Serve route의 소유 프로젝트를 연결하지 않는다.
- 빈 port 선택, filesystem 범위 검사, 기존 route 비간섭과 작업별 cleanup을 하나의 workflow로 제공하지 않는다.
- `--bg`는 재부팅이나 Tailscale 재시작 후에도 복구되므로 임시 preview가 의도보다 오래 남을 수 있다.
- 공식 문서상 `status`와 `status --json`의 반환 정보가 완전히 같지 않아 자동화가 한 표현만 신뢰하면 누락될 수 있다.

판정: **새 network 제품보다 Tailscale primitive를 안전하게 조율하는 얇은 계층을 먼저 시험할 근거가 강하다.**

### Cloudflare Quick Tunnels와 Cloudflare Tunnel

[Cloudflare Quick Tunnels](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/)는 account나 domain 설정 없이 `cloudflared` process 하나로 localhost service에 임의 `trycloudflare.com` URL을 만든다. 개발·시험 전용이며 URL은 public Internet에서 접근 가능하다. 공식 제한에는 SLA 부재, 최대 200 concurrent request와 SSE 미지원이 포함된다.

강점:

- random URL 발급까지 한 명령으로 끝난다.
- client device가 별도 VPN에 참여하지 않아도 된다.
- 임시 개발 결과를 빠르게 공유하는 UX가 단순하다.

Idea와의 차이:

- 사용 목적은 개인 private preview인데 Quick Tunnel은 public exposure다.
- URL의 추측 난이도는 인증이나 private network 경계가 아니다.
- 지속형 Cloudflare Tunnel과 Access를 조합하면 접근 제어가 가능하지만 account, hostname과 policy 운영 범위가 커진다.

판정: public sharing이 필요한 다른 profile에는 후보지만, 현재 개인 tailnet 요구의 자동 fallback으로 사용해서는 안 된다.

### ngrok

[ngrok Authentication](https://ngrok.com/docs/guides/share-localhost/auth)은 local app 앞에 OAuth를 추가할 수 있고, [Network Security](https://ngrok.com/docs/guides/share-localhost/security)는 IP restriction과 mTLS 같은 Traffic Policy를 제공한다. public ingress이지만 인증과 edge policy를 결합해 허용 사용자를 제한할 수 있다.

강점:

- URL 발급, TLS, OAuth/OIDC/SAML·IP·mTLS policy와 traffic 관찰을 하나의 제품에서 제공한다.
- tailnet client를 설치하지 않은 reviewer와 공유해야 할 때 범용성이 높다.
- endpoint policy와 session duration을 세밀하게 설정할 수 있다.

Idea와의 차이:

- 개인 기기만 접근하는 현재 상황에는 tailnet보다 identity와 cloud policy 구성이 무겁다.
- transport와 access control은 제공하지만 어떤 local artifact를 안전하게 게시하고 언제 정리할지는 호출자가 결정한다.
- plan별 endpoint, traffic identity와 관찰 기능 차이를 운영 시 고려해야 한다.

판정: 외부 reviewer가 필요한 profile의 강한 benchmark이지만 현재 문제의 최소 해법은 아니다.

## IDE와 개발환경의 preview UX

### Visual Studio Code Port Forwarding과 Remote Tunnels

[VS Code Port Forwarding](https://code.visualstudio.com/docs/debugtest/port-forwarding)은 Microsoft dev tunnels를 사용하며 기본 visibility가 `Private`다. 같은 GitHub 또는 Microsoft account 인증을 요구하고, UI에서 URL 복사·browser 열기·editor preview와 public 전환을 지원한다. public 전환 시 URL을 아는 누구나 접근할 수 있다고 명시한다.

[Remote Tunnels](https://code.visualstudio.com/docs/remote/tunnels)는 home computer나 VM에 VS Code Server를 설치하고 외부 VS Code client 또는 browser에서 연결하는 bring-your-own-compute 흐름을 제공한다.

배울 점:

- 기본 private와 명시적 public 전환이 올바른 기본값이다.
- 발견된 port, 접근 URL, visibility와 open action을 같은 UI에 보여준다.
- 개발 server가 URL을 출력하면 사람이 다시 tunnel 명령을 조립하지 않도록 editor가 연결한다.

한계:

- VS Code session과 account 생태계가 workflow 경계다.
- AI가 생성한 임의 static artifact의 server 시작, 안전한 root 선택과 종료 조건까지 일반화하지 않는다.
- 현재 사용자가 terminal 중심 client를 유지하려는 경우 editor 교체 비용이 발생한다.

### GitHub Codespaces

[Codespaces port forwarding](https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace)는 terminal에 출력된 localhost URL을 감지해 자동 forwarding하고 clickable URL로 바꾼다. 기본 visibility는 `private`이며 `org`와 `public`으로 바꿀 수 있고, CLI와 Ports UI에서 관리한다.

배울 점:

- application output 감지부터 URL 제공까지 연결하면 사용자의 반복 지시가 크게 줄어든다.
- private·organization·public visibility를 명시적으로 표현한다.
- port label과 repository configuration을 통해 반복 workspace의 intent를 보존한다.

한계:

- compute가 Codespace에 있어야 하므로 기존 home computer를 그대로 사용하는 요구와 다르다.
- private remote URL을 비browser client에서 호출할 때 token 인증이 필요할 수 있다.

### Coder

[Coder port forwarding](https://coder.com/docs/user-guides/workspace-access/port-forwarding)은 workspace의 listening port를 감지하고 owner, organization, authenticated, public 공유 수준을 제공한다. Coder Desktop은 VPN 연결 후 workspace의 모든 port를 별도 명령 없이 같은 hostname과 port로 접근하게 하고, dashboard app은 URL과 healthcheck를 template에 선언할 수 있다.

배울 점:

- listening port discovery와 owner-only 기본 접근은 원하는 운영 경험에 가깝다.
- URL, app 이름, icon, healthcheck와 공유 수준을 하나의 관리 화면에 모은다.
- 상태를 소유하는 제품이라면 “현재 열려 있는 preview” 목록이 핵심 기능임을 보여준다.

한계:

- Coder deployment와 workspace agent가 전제다.
- 기존 임의 home project에 작은 기능만 추가하는 것보다 훨씬 큰 운영 체계다.

### Ona

[Ona port sharing](https://ona.com/docs/ona/integrations/ports)은 environment port를 HTTPS URL로 열고 creator 또는 organization access를 적용할 수 있으며 CLI에서 URL을 반환한다. listening port 조사와 browser preview 흐름을 제공하지만 local environment에는 사용할 수 없다. 문서에는 runner가 access control을 지원하지 않으면 공유 port가 `everyone`처럼 동작할 수 있다는 주의도 있다. [Ona changelog](https://ona.com/docs/changelog)는 Agent session의 PR link와 preview URL을 clickable output으로 제공한다고 기록한다.

배울 점:

- Agent 작업 결과에서 preview URL을 clickable output으로 제공하는 경험이 중요하다.
- 기능 이름보다 실제 runner의 access-control capability를 확인해야 한다.
- port open과 browser launch를 하나의 operation으로 묶을 수 있다.

한계:

- vendor environment가 필요하고 현재 home computer에는 적용되지 않는다.

## Framework별 공유 기능

### Gradio Share Links

[Gradio Share Links](https://gradio.app/guides/understanding-gradio-share-links)는 locally running Gradio application에 tunnel을 만들고 `gradio.live` URL을 제공한다. 공식 설명상 이 URL은 public하게 접근 가능하며 share server는 app을 host하지 않고 local app으로 traffic을 연결한다.

장점은 application 생성과 share URL 발급이 하나의 API option으로 결합된다는 것이다. 그러나 Gradio application에 한정되고 private-by-default 요구와 맞지 않는다.

### Streamlit Community Cloud

[Streamlit Community Cloud sharing](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app)은 Streamlit app을 cloud에 deploy하고 초대 기반으로 공유할 수 있다. 이는 local preview tunnel보다는 framework-specific deployment에 가깝다.

두 사례의 시사점은 결과물 framework가 runtime을 이미 소유하면 preview lifecycle을 가장 매끄럽게 통합할 수 있다는 점이다. 반대로 범용 capability가 HTML, PDF, static directory와 임의 dev server를 모두 다루려면 각 runtime의 시작·준비 확인·종료 차이를 흡수해야 한다.

## 확인된 공통 패턴

### 1. transport는 이미 상품화되어 있다

private mesh, public tunnel, authenticated ingress, IDE tunnel과 workspace proxy가 모두 존재한다. 새로운 protocol이나 tunnel service를 만드는 것은 현재 Idea의 확인된 필요가 아니다.

### 2. 좋은 제품은 private를 기본값으로 둔다

Tailscale Serve, VS Code forwarding과 Codespaces는 승인된 network 또는 account를 기본 경계로 둔다. Public 전환은 별도 동작이다. Quick Tunnel과 Gradio처럼 public URL을 기본 제공하는 제품은 사용성은 높지만 현재 보안 요구와 다르다.

### 3. URL 반환만으로는 lifecycle이 끝나지 않는다

성숙한 workspace 제품은 port 목록, visibility, label, healthcheck와 종료 상태를 함께 보여준다. 임시 preview도 최소한 무엇이 열렸고 누가 소유하며 어떻게 닫는지 복구할 수 있어야 한다.

### 4. 자동화 가능한 primitive와 안전한 workflow 사이에 간격이 있다

CLI와 API는 port·route·policy를 생성할 수 있지만, 다음 판단은 대부분 호출자에게 남는다.

- artifact가 terminal 표현보다 browser preview에 적합한가
- 어느 directory 또는 process만 노출해도 되는가
- 기존 route가 다른 작업 소유인지 덮어써도 되는가
- foreground와 persistent 중 무엇이 맞는가
- 사용자가 검토를 끝냈을 때 어떤 process와 route를 정리해야 하는가

### 5. 가장 가까운 UX는 IDE와 remote workspace 안에 있다

Codespaces, VS Code, Coder와 Ona는 listening port 발견, private URL, open action과 visibility를 한 흐름으로 제공한다. 그러나 이 UX는 해당 workspace를 채택한 경우에만 작동한다. 기존 home computer와 terminal 중심 AI client를 유지하면서 같은 경험을 제공하는 독립적인 Agent workflow는 조사 범위에서 확인하지 못했다.

## 시장 공백에 대한 추론

다음은 공식 제품 기능에서 직접 확인한 사실이 아니라 비교를 통해 얻은 추론이다.

시장 공백은 새로운 hosting backend가 아니라 **Agent-facing preview orchestration**일 가능성이 높다.

```text
AI가 결과물과 사용자 상황 판단
  → 허용된 transport 선택
  → artifact 전용 local server 준비
  → 기존 listener와 route 충돌 검사
  → private access와 filesystem 범위 확인
  → 접근 URL 반환
  → owner, 생성 시각과 종료 방법 보고
  → 검토 종료 시 자신이 만든 자원만 cleanup
```

이 계층은 Tailscale, ngrok 또는 IDE tunnel을 대체하지 않고 adapter로 사용한다. 현재 개인 환경에서는 Tailscale-only adapter 하나로 시작할 수 있으며, 다른 transport를 처음부터 추상화할 시장 근거는 없다.

## Idea에 대한 전략적 시사점

### 지금 Blueprint로 승격하지 않는다

다른 제품에서도 반복되는 UX 패턴은 확인했지만, 다른 사용자와 Agent가 같은 문제를 겪는다는 evidence는 아직 없다. 개인 환경의 얇은 Skill로 충분한지 먼저 확인해야 한다.

### 제품 저장소도 아직 필요하지 않다

Tailscale은 status와 config 조회, file serving, proxy, foreground/background와 off primitive를 이미 제공한다. 먼저 Agent instruction이 이를 안전하게 조합할 수 있는지 시험해야 한다. durable registry, daemon, UI 또는 cross-process recovery 실패가 반복될 때만 별도 CLI를 검토한다.

### 전역 Skill 가설이 가장 작은 첫 실험이다

문제는 여러 project를 가로지르는 사용자 환경에 있고 프로젝트 source of truth를 소유하지 않는다. 따라서 실제 Pilot은 이 저장소의 설치형 산출물이 아니라 별도 개인 전역 Skill로 수행할 가능성이 높다. 이는 현재 Blueprint의 전역 설치 금지에 대한 예외가 아니라 아직 Blueprint가 아닌 사용자 환경 실험이다.

### 최초 범위는 Tailscale-only가 적합하다

transport abstraction은 구현을 늘리고 private/public 의미를 흐릴 수 있다. 현재 요구에서는 다음 contract만 시험하는 편이 작다.

- Serve만 허용하고 Funnel과 public tunnel은 사용하지 않음
- 기존 status와 listener를 읽고 충돌하지 않는 route 제안
- 명시적으로 선택한 artifact 또는 localhost service만 게시
- URL, 접근 범위, foreground/background와 종료 명령 보고
- 다른 route를 reset하지 않고 자신이 만든 자원만 종료

## 경쟁 제품 대비 성공 기준

첫 실험은 network 성능이 아니라 반복 지시 제거와 안전성으로 평가한다.

| 기준 | 최소 성공 신호 |
|---|---|
| 상황 인식 | 사용자가 원격 terminal 환경임을 매번 다시 설명하지 않아도 적절한 preview를 제안 |
| private 기본값 | public endpoint를 만들지 않고 tailnet access만 사용 |
| 충돌 방지 | existing listener와 Serve config를 조사하고 타 작업 route를 보존 |
| 범위 제한 | 의도한 artifact 또는 localhost service만 접근 가능 |
| 사용자 결과 | 열 수 있는 URL, 접근 범위와 종료 방법을 한 번에 제공 |
| lifecycle | 자신이 만든 server와 route를 식별하고 선택적으로 종료 |
| 낮은 유지비 | 별도 daemon이나 database 없이 반복 사례를 처리 |

### 별도 제품으로 전환할 신호

- 여러 Agent session이 같은 preview를 안정적으로 조회·종료하지 못한다.
- process와 Serve config만으로 artifact owner를 복구할 수 없다.
- port와 path route 충돌이 반복된다.
- 자동 만료, healthcheck와 orphan cleanup이 없어서 노출이 누적된다.
- 여러 transport adapter 또는 여러 host를 실제로 동시에 관리해야 한다.
- 사람이 현재 preview 목록과 보안 상태를 볼 관리 화면을 반복해서 요구한다.

### Blueprint 후보로 전환할 신호

- 둘 이상의 사용자 환경에서 같은 문제와 operation이 반복된다.
- Tailscale 외의 transport에서도 공통 invariant와 authority 경계가 유지된다.
- AI가 환경을 조사해 서로 다른 project/client에 맞는 Skill을 생성해야 하는 차이가 확인된다.
- 구현보다 문제·안전 계약·적응 지점의 공유가 더 큰 가치를 만든다.

## 결론

기존 시장은 secure transport와 remote workspace preview를 이미 잘 해결한다. 현재 Idea가 새롭게 제공할 수 있는 가치는 tunnel 자체가 아니라 **터미널 중심 AI 작업에서 preview 필요성 판단부터 private publication, URL 전달과 cleanup까지 연결하는 사용자 환경 workflow**다.

현재 evidence가 지지하는 가장 작은 다음 단계는 Tailscale Serve를 그대로 활용하는 개인 전역 Skill Pilot이다. Blueprint 승격이나 별도 제품 저장소는 그 Pilot에서 orchestration의 반복성과 stateful lifecycle 실패가 확인된 뒤 판단한다.

## 주요 출처

- [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve)
- [Tailscale Serve CLI](https://tailscale.com/docs/reference/tailscale-cli/serve)
- [Tailscale Serve examples](https://tailscale.com/docs/reference/examples/serve)
- [Cloudflare Quick Tunnels](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/)
- [ngrok Authentication](https://ngrok.com/docs/guides/share-localhost/auth)
- [ngrok Network Security](https://ngrok.com/docs/guides/share-localhost/security)
- [Visual Studio Code Port Forwarding](https://code.visualstudio.com/docs/debugtest/port-forwarding)
- [Visual Studio Code Remote Tunnels](https://code.visualstudio.com/docs/remote/tunnels)
- [GitHub Codespaces port forwarding](https://docs.github.com/en/codespaces/developing-in-a-codespace/forwarding-ports-in-your-codespace)
- [Coder port forwarding](https://coder.com/docs/user-guides/workspace-access/port-forwarding)
- [Ona port sharing](https://ona.com/docs/ona/integrations/ports)
- [Ona changelog](https://ona.com/docs/changelog)
- [Gradio Share Links](https://gradio.app/guides/understanding-gradio-share-links)
- [Streamlit Community Cloud sharing](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app)
