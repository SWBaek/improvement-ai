# Skills

여러 프로젝트에서 재사용할 Agent Skills를 둡니다.

각 skill의 기본 구조는 다음과 같습니다.

```text
skills/<skill-name>/
├── SKILL.md
├── scripts/       선택: 실행 가능한 도우미
├── references/    선택: 필요할 때 읽는 상세 지침
└── assets/        선택: 템플릿과 정적 자산
```

`SKILL.md`의 YAML frontmatter에는 최소 `name`과 실제 trigger를 설명하는 `description`이 필요합니다. 이름은 소문자 kebab-case를 사용합니다.
