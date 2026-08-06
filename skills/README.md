# Skills

여러 프로젝트에서 재사용할 Agent Skills를 flat 구조로 관리합니다.

```text
skills/<skill-name>/
├── SKILL.md
├── scripts/       선택: 결정적인 실행 도우미
├── references/    선택: 필요할 때 읽는 상세 지침
└── assets/        선택: template과 정적 자산
```

`SKILL.md`의 YAML frontmatter에는 최소 `name`과 실제 trigger를 설명하는 `description`이 필요합니다. 이름은 소문자 kebab-case를 사용하고 디렉터리 이름과 일치시킵니다.

## 상태 관리

- Candidate는 GitHub issue로만 관리하며 Skill 디렉터리를 만들지 않습니다.
- Pilot을 시작하면 In Progress로 등록하고 `skills/<name>`을 만듭니다.
- 여러 사용에서 효과가 확인되면 경로를 바꾸지 않고 Promoted로 변경합니다.
- Deprecated는 대체 Skill 또는 폐기 이유를 tracking issue에 기록합니다.

## Registered Skills

모든 Skill은 아래 index에 정확히 한 번 등록합니다. 상태는 `In Progress`, `Promoted`, `Deprecated` 중 하나를 사용하고 Tracking에는 issue 링크 또는 폐기 기록을 둡니다.

<!-- skill-index:start -->
| Skill | Status | Tracking |
|---|---|---|
<!-- skill-index:end -->
