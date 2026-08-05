# 0001. Self-contained HTML을 Artifact 전달 단위로 사용

- 상태: Accepted
- 날짜: 2026-08-06

## 결정

Core Artifact는 하나의 HTML 파일로 전달한다. 실제 내용은 semantic HTML을 원본으로 삼고, 식별과 검증을 위한 최소 JSON Manifest를 실행되지 않는 `application/json` script로 포함한다.

## 이유

- 브라우저만 있으면 별도 build 없이 열고 공유할 수 있다.
- 사람용 표현과 기계 판독 메타데이터를 한 파일에 유지할 수 있다.
- 모든 domain을 미리 하나의 거대한 JSON 데이터 모델로 고정하지 않는다.
- HTML 본문 전체를 JSON에 복제할 때 생기는 두 원본의 drift를 피한다.

## 결과

Manifest는 문서 식별, 수명주기, 검토 모드, profile과 provenance만 담당한다. 실제 주장, 근거와 결정 내용은 HTML에만 기록한다. 별도 JSON이나 DSL이 필요한 domain은 Profile에서 추가할 수 있다.
