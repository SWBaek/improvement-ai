# 0006. Releasable main에서 Skill을 독립 version으로 배포

- 상태: Accepted
- 날짜: 2026-08-06

## 결정

각 Skill을 저장소 전체와 분리된 Semantic Version으로 관리하고 `skills/catalog.json`을 현재 version과 lifecycle 상태의 canonical source로 사용한다. Tag는 `<skill-name>-v<version>` 형식이며, 배포된 Skill의 폴더가 바뀌면 같은 pull request에서 version과 `docs/releases/`의 변경 이력을 갱신한다.

`main`은 외부 사용자가 `skills update`로 소비하는 항상 배포 가능한 channel로 유지한다. Version 증가가 `main`에 병합되면 GitHub Actions가 전체 검증 후 인증된 `gh`로 tag와 Release를 자동 생성한다. Release와 In Progress/Promoted/Deprecated lifecycle은 독립적으로 판단한다.

`manage-focus-cycle` v0.1.0은 MIT로 배포하고 Codex를 첫 검증 client로 선언한다. 다른 Agent Skills client는 표준 구조를 소비할 수 있지만 검증 완료 전까지 지원을 약속하지 않는다.

ADR 0005에서 보류했던 독립 renderer의 필요성이 공개 배포 준비에서 확인됐다. 프로젝트 text를 AI가 HTML에 직접 치환하면 escaping과 schema drift를 결정적으로 검증할 수 없으므로, versioned JSON input을 검증하고 안전한 HTML을 생성하는 표준 라이브러리 script를 Skill 안에 bundle한다. 이는 별도 CLI, Framework 또는 Service로 승격하지 않는다.

## 이유

하나의 저장소에는 서로 다른 속도로 발전하는 여러 Skill이 존재하므로 저장소 단일 version은 무관한 capability를 함께 release하게 만든다. 반대로 version과 changelog를 Skill 내부에 넣으면 실행 시 agent context와 설치 artifact가 운영 문서로 불필요하게 커진다.

`skills` installer는 Semantic Version을 해석하지 않고 설치한 Git ref의 폴더 변경을 추적한다. 따라서 기본 소비 channel인 `main`에 미완성 변경을 허용하지 않고, tag와 GitHub Release를 공지·감사·rollback 지점으로 사용하는 운영이 적합하다.

결정적 renderer는 HTML의 유연성을 없애지 않으면서도 raw HTML injection, 잘못된 placeholder, unsafe URL과 부분 file write를 자동으로 차단한다. 반복 가능한 외부 배포에서 이 안전성은 수동 template 치환보다 우선한다.

## 결과

- `skills/catalog.json`, Skill별 외부 release history와 자동 Release workflow를 유지한다.
- `main`의 Skill 변경은 version 증가와 release note 없이 병합할 수 없다.
- `manage-focus-cycle-v0.1.0`은 일반 GitHub Release이며 Capability는 Pilot 완료 전까지 In Progress다.
- 설치 artifact에는 root MIT license와 동일한 `LICENSE.txt`가 포함된다.
- `manage-focus-cycle` Workspace input schema v1과 bundled renderer가 공개 계약이 된다.
- Breaking change는 0.x minor 또는 1.0 이후 major version과 migration·rollback 안내를 요구한다.
- 자체 registry, package, 범용 Framework와 별도 Service는 여전히 실사용 근거가 생길 때까지 추가하지 않는다.
