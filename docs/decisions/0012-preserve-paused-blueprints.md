# 0012. 실패한 Pilot의 Blueprint를 Paused로 보존

- 상태: Accepted
- 날짜: 2026-08-14

## 결정

Capability Blueprint lifecycle에 `Paused`를 추가한다. Paused Blueprint는 canonical 경로와 tracking issue를 유지하지만 active Pilot과 신규 설치 권장을 중단한다. 상태를 바꿀 때는 부정적 또는 불확정 Pilot evidence, 기존 설치 소비자 안내와 관찰 가능한 재개 조건을 함께 기록한다.

Paused는 외부 선행 조건 때문에 일시적으로 진행할 수 없는 `blocked` issue와 다르다. Maintainer가 현재 설계 가설을 더 이상 실험하지 않기로 명시적으로 판단한 상태다. 재개 조건을 충족하고 새 Pilot 설계를 승인하면 같은 Blueprint를 `In Progress`로 되돌릴 수 있다.

Paused 전환은 기존 설치를 자동으로 무효화, Migration 또는 제거하지 않는다. 대상 프로젝트가 소유한 생성물은 해당 프로젝트의 권한과 판단에 따라 유지·단순화·제거한다. 대체 또는 폐기를 결정한 경우에만 기존처럼 `Deprecated`로 전환하고 소비자 안내를 남긴다.

## 이유

기존 lifecycle의 `In Progress`는 실제 Pilot이 계속된다는 뜻이고, `Deprecated`는 대체 또는 폐기를 전제로 한다. 실제 사용에서 중요한 실패가 확인됐지만 계약, 실패 근거와 재설계 가능성을 보존할 가치가 있는 Blueprint에는 어느 상태도 정확하지 않다.

부정적 evidence를 받은 설계를 In Progress에 두면 신규 사용자가 검증 중인 권장안으로 오해할 수 있다. 반대로 즉시 Deprecated 처리하면 유효했던 문제 정의, authority boundary, 시나리오와 실패 학습을 성급히 버리거나 같은 탐색을 반복하게 된다. Paused는 추천 중단과 지식 보존을 분리한다.

## 결과

- Blueprint catalog와 canonical metadata는 Paused를 명시할 수 있다.
- Paused tracking issue는 열린 채 `status: paused` label을 사용한다.
- pause notice는 실패 근거, 기존 소비자 영향과 구체적인 재개 조건을 제공한다.
- Paused Blueprint의 설치 안내는 신규 설치를 권장하지 않으며 status-only revision 때문에 기존 설치를 Migration시키지 않는다.
- Paused는 Promotion evidence로 계산되지 않고 active Pilot이 아니다.
