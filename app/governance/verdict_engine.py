def determine_verdict(run_state: dict) -> str:
    if not run_state.get("target_match_identified"):
        return "FAIL_TARGET_MATCH_IDENTIFICATION"

    if not run_state.get("teams_identified"):
        return "FAIL_TEAM_IDENTIFICATION"

    if run_state.get("blocking_missing_data"):
        return "FAIL_TEAM_AT_PLAY_SOURCE_COVERAGE"

    if not run_state.get("reconciliation_passed", True):
        return "FAIL_VALIDATION"

    if not run_state.get("leakage_passed"):
        return "FAIL_LEAKAGE_RISK"

    if not run_state.get("feature_vector_hash"):
        return "FAIL_VALIDATION"

    return "PASS_TEAM_AT_PLAY_OFFICIAL_RECONSTRUCTED"