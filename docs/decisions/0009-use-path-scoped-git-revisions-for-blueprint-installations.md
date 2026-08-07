# 0009. Blueprint 설치 버전으로 path-scoped Git revision을 사용

- 상태: Accepted
- 날짜: 2026-08-07

## 결정

Blueprint는 별도의 Semantic Version, tag, Release, version catalog 또는 알림 채널을 운영하지 않는다. AI가 사용하는 Blueprint의 버전은 canonical `blueprints/<name>/BLUEPRINT.md`를 마지막으로 변경한 40자리 Git commit이다. 저장소 전체 HEAD, 설치 README 또는 다른 Blueprint만 변경한 commit은 해당 Blueprint의 새 버전으로 간주하지 않는다.

AI는 `main` URL을 입력받아도 먼저 canonical Blueprint path의 최신 변경 commit을 확인하고, 그 commit이 포함된 불변 URL에서 문서를 다시 읽은 뒤 생성해야 한다. 대상 프로젝트에는 설치된 Blueprint마다 Installation Receipt를 정확히 하나 남긴다. 경로는 대상 프로젝트의 설치 제안에서 정하되 다음 정보를 포함한다.

```yaml
format: improvement-ai-blueprint-installation/v1
blueprint: <blueprint-name>
repository: https://github.com/SWBaek/improvement-ai
path: blueprints/<blueprint-name>/BLUEPRINT.md
revision: <40-character-commit>
source: https://github.com/SWBaek/improvement-ai/blob/<40-character-commit>/blueprints/<blueprint-name>/BLUEPRINT.md
```

모든 생성 `SKILL.md`의 provenance `source`와 `revision`은 Installation Receipt와 일치해야 한다. AI는 최신 여부를 확인할 때 receipt의 path를 마지막으로 변경한 최신 commit과 설치 revision을 비교한다. 같으면 최신, 다르면 업데이트 가능, 확인할 수 없으면 상태 확인 불가로 보고한다. 사람에게는 짧은 revision과 상태만 표시할 수 있지만 canonical receipt에는 40자리 값을 유지한다.

업데이트는 자동 적용하지 않는다. revision이 다르면 두 exact Blueprint 문서를 의미적으로 비교하고 로컬 customization과 생성물에 미치는 migration proposal을 제시한다. 인간 승인과 로컬 검증이 성공한 뒤에만 생성물 provenance와 Installation Receipt를 새 revision으로 함께 변경한다. 실패하거나 일부만 변경된 경우 기존 receipt revision을 유지한다.

## 이유

사람 중심 버전 번호는 bump 기준, changelog, 호환성 의미와 Release 운영을 추가하지만 AI는 exact Git revision만으로 원본 재현과 semantic comparison을 수행할 수 있다. 반대로 저장소 HEAD를 revision으로 사용하면 무관한 README나 다른 Blueprint 변경도 모든 설치를 오래된 것으로 오판한다. Canonical path의 마지막 변경 commit을 사용하면 Blueprint 계약이 실제로 바뀐 경우에만 업데이트 대상으로 판정할 수 있다.

Installation Receipt는 여러 생성 Skill과 지원 자산이 같은 Blueprint revision에서 만들어졌는지 확인할 대표 기록을 제공한다. 개별 Skill provenance는 파일 단위 출처를 유지하고 receipt는 설치 전체의 현재 revision을 제공한다.

## 결과

- Blueprint header에 별도 사람이 관리하는 version을 추가하지 않는다.
- Blueprint별 최신 revision은 canonical `BLUEPRINT.md` path의 Git history에서 계산한다.
- 모든 신규 설치는 프로젝트 로컬 Installation Receipt 하나를 가진다.
- 기존 설치를 업데이트할 때 receipt가 없으면 현재 Skill provenance와 로컬 파일을 조사해 receipt 생성안을 먼저 제시한다.
- README, references와 Pilot scenario만 변경해도 canonical Blueprint가 바뀌지 않으면 설치 업데이트가 필요하지 않다.
- tag, Release, changelog, registry, 자동 알림과 background update는 추가하지 않는다.
