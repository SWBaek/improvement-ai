# Private Remote Artifact Preview

## Status

- State: `Exploring`
- Last reviewed: 2026-08-07
- Next trigger: 실제 원격 작업 사례에서 공통 동작, 유지 상태와 안전한 종료 경계를 관찰한 뒤 Skill, Blueprint 또는 별도 제품 중 적합한 구현 형태를 판단한다.

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
- 이 불편은 프로젝트 내부 상태보다 사용자 장비와 원격 작업 방식에 가깝다.

실제 tailnet hostname, 개인 장비 이름, 프로젝트 경로와 접근 URL은 이 공개 Idea에 기록하지 않는다.

## 현재 가설

AI가 원격 작업 상황을 인식했을 때 시각적 결과물을 안전하게 게시하고 접근 URL과 종료 방법을 반환하는 공통 capability가 반복 지시를 줄일 수 있다.

가칭 `Private Remote Artifact Preview`는 해결하려는 사용자 경험을 나타낸다. Tailscale Serve는 현재 환경에서 유력한 adapter이지만 Idea의 정체성이나 최종 구현으로 확정하지 않는다. HTML 외에도 이미지, PDF, 정적 directory 또는 localhost 개발 서버가 같은 문제에 포함되는지는 실제 사례에서 확인한다.

## 미결정 구현 후보

| 후보 | 적합할 수 있는 조건 | 현재 불확실성 |
|---|---|---|
| 개인 지침 | 사용 빈도가 낮고 매번 요구가 다름 | 반복 설명을 충분히 줄일 수 있는가 |
| 전역 Agent Skill | 기존 CLI와 임시 server를 조율하는 절차만 필요함 | 전역 설치와 사용자 환경 권한을 안전하게 제한할 수 있는가 |
| Capability Blueprint | 사용자마다 Tailscale, SSH tunnel 등 다른 환경에 맞춘 생성이 필요함 | 두 프로젝트가 아니라 여러 사용자 환경에서 반복되는 문제인가 |
| 별도 CLI 또는 제품 저장소 | port, process, URL, 만료와 cleanup 상태를 지속 관리해야 함 | 실제로 runtime과 durable registry가 필요한가 |

현재 저장소의 Blueprint가 생성하는 capability는 프로젝트 로컬 설치가 원칙이다. 이 Idea는 여러 프로젝트를 가로지르는 사용자 환경용 전역 capability를 요구할 수 있으므로 기존 Blueprint의 전역 설치 예외로 간주하지 않는다. 필요성이 확인되면 사용자 환경 capability라는 별도 범주, 별도 Blueprint 또는 별도 구현 저장소 중 어느 경계가 적합한지 먼저 결정한다.

## 잠정적인 안전 경계

아직 공개 계약은 아니지만 다음 위험은 초기 관찰에서 반드시 검증한다.

- Tailscale Funnel처럼 공개 인터넷에 노출하는 기능을 자동 대안으로 사용하지 않는다.
- proxy backend는 가능한 경우 localhost에만 bind한다.
- 게시 전에 기존 Serve 상태와 관련 port 사용 여부를 확인한다.
- 저장소 전체, 상위 directory, 인증 정보와 의도하지 않은 파일을 directory listing으로 공개하지 않는다.
- background 또는 persistent 게시를 기본값으로 가정하지 않고 종료와 cleanup 방법을 항상 제시한다.
- 기존 Serve 구성을 전체 reset하거나 다른 프로젝트의 route를 덮어쓰지 않는다.
- 외부 쓰기, 장기 실행과 접근 범위에 필요한 인간 승인 경계를 구분한다.

## 기대 효과

- 프로젝트마다 원격 접속 조건과 호스팅 지시를 반복하지 않는다.
- AI가 터미널에 부적합한 결과물을 원격 검토 가능한 형태로 일관되게 제안한다.
- port와 기존 Serve route 충돌을 줄인다.
- 사용자가 현재 게시 중인 결과물, 접근 URL과 종료 방법을 알 수 있다.
- tailnet 내부 공개와 public exposure를 혼동하는 위험을 낮춘다.

## 비목표

- 지금 단계에서 Tailscale 전용 Blueprint나 설치형 Skill을 확정하는 것
- 이 저장소에 runtime, CLI, server manager 또는 전역 Skill을 구현하는 것
- 공개 웹 호스팅 또는 Tailscale Funnel을 자동화하는 것
- production service 배포, 사용자 인증 체계 또는 장기 artifact 보관을 제공하는 것
- 프로젝트의 일반적인 개발 server와 deployment workflow를 대체하는 것

## 위험과 반례

### 개인 환경에 지나치게 특화될 가능성

문제가 한 사람의 장비 구성과 접속 습관에만 존재한다면 공개 Blueprint보다 개인 Skill이 더 적합하다. 유사한 원격 작업 사례나 환경 adapter의 반복성이 확인되기 전에는 일반 capability로 승격하지 않는다.

### 전역 capability의 권한 확대

여러 프로젝트에서 자동으로 동작하는 Skill은 잘못된 directory를 게시하거나 기존 Serve 설정을 변경할 수 있다. 편의성만으로 프로젝트 경계와 명시적 승인 원칙을 약화해서는 안 된다.

### 작은 절차를 제품으로 과대 설계할 가능성

기존 `tailscale` 명령과 임시 static server 몇 단계만으로 문제가 해결된다면 daemon, database, port registry와 관리 UI는 불필요하다. 실제로 반복되는 lifecycle 실패가 관찰될 때만 runtime을 검토한다.

### 임시 게시의 잔존

background mode나 재부팅 후 복구되는 설정은 의도보다 오래 남을 수 있다. 자동 만료가 필요한지, 사용자가 명시적으로 종료하면 충분한지는 사용 과정에서 확인한다.

## 검증 질문

- 원격 작업에서 어떤 artifact 유형이 실제로 반복 게시되는가?
- AI가 단순한 공통 지침만 읽어도 안전하게 게시·보고·종료할 수 있는가?
- local backend port와 Tailscale HTTPS port를 각각 어떻게 선택하고 충돌을 확인해야 하는가?
- 한 번에 여러 프로젝트의 preview를 유지해야 하는가?
- 고정 URL path 재사용과 작업별 임시 port 중 어느 쪽이 관리하기 쉬운가?
- terminal 또는 Agent session 종료 시 preview도 종료해야 하는가?
- 현재 게시 상태를 기억하려면 파일이나 registry가 필요한가, `tailscale serve status`와 process 조사로 충분한가?
- 어떤 filesystem 범위와 server 유형은 자동 게시할 수 있고 무엇은 사람 승인이 필요한가?
- Tailscale이 없는 환경까지 적응해야 하는가?
- 다른 사용자에게도 반복되는 문제인가, 아니면 개인 전역 Skill로 충분한가?

## 다음 탐색

구현에 앞서 최소 세 번의 실제 원격 작업 사례를 관찰한다. 각 사례에서 artifact 유형, 수동 지시, 선택한 port와 route, 필요한 승인, 실행 시간, 종료 방식, 충돌과 잔존 상태를 민감 정보 없이 기록한다. 그 결과로 다음 중 가장 작은 해법을 선택한다.

1. 개인 운영 지침
2. 개인 전역 Skill
3. 환경별 생성을 안내하는 Capability Blueprint
4. lifecycle을 소유하는 별도 CLI 또는 제품

## 관련 출처

- [Tailscale Serve](https://tailscale.com/docs/features/tailscale-serve): tailnet 내부 공유, access control과 identity header의 보안 특성을 확인하기 위한 공식 설명
- [Tailscale Serve CLI](https://tailscale.com/docs/reference/tailscale-cli/serve): route, port, status, reset과 background 동작을 확인하기 위한 명령 명세
- [Tailscale Serve examples](https://tailscale.com/docs/reference/examples/serve): 정적 파일과 개발 server 게시, foreground/background lifecycle 사례
