# Configs

여러 프로젝트에 공통으로 적용할 설정의 원본과 에이전트별 adapter를 둡니다.

- `shared/`: 도구에 독립적인 공통 규칙과 설정
- `codex/`: Codex에서만 필요한 adapter
- `claude/`: Claude Code에서만 필요한 adapter

공통 내용을 에이전트별 폴더에 복제하지 않습니다. 생성 과정이 필요해지면 `scripts/`에 생성기와 검증을 함께 추가합니다.
