import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from database import _apply_limit
from report_generator import _remove_partial_duplicates, _normalize_headings, clean_text


# --- Query limit ---

def test_apply_limit_adds_limit():
    sql = "SELECT * FROM customers"
    result = _apply_limit(sql)
    assert "LIMIT 500" in result

def test_apply_limit_respects_existing():
    sql = "SELECT * FROM customers LIMIT 10"
    result = _apply_limit(sql)
    assert result == sql

def test_apply_limit_case_insensitive():
    sql = "SELECT * FROM customers limit 20"
    result = _apply_limit(sql)
    assert "LIMIT 500" not in result

def test_apply_limit_strips_semicolon():
    sql = "SELECT * FROM customers;"
    result = _apply_limit(sql)
    assert result.endswith("LIMIT 500;")
    assert ";;" not in result

def test_apply_limit_custom():
    sql = "SELECT * FROM customers"
    result = _apply_limit(sql, limit=100)
    assert "LIMIT 100" in result


# --- Partial duplicate removal ---

def test_removes_partial_duplicate():
    assert _remove_partial_duplicates("cont continue working") == "continue working"

def test_removes_short_partial():
    assert _remove_partial_duplicates("man many issues") == "many issues"

def test_removes_hyphenated_partial():
    assert _remove_partial_duplicates("engine-ove engine-overheating") == "engine-overheating"

def test_handles_double_space():
    assert _remove_partial_duplicates("and br  brake failure") == "and brake failure"

def test_preserves_normal_text():
    text = "The branch has high revenue."
    assert _remove_partial_duplicates(text) == text

def test_preserves_newlines():
    text = "first line\nsecond line"
    result = _remove_partial_duplicates(text)
    assert "\n" in result

def test_does_not_remove_number_formatting():
    # "8 800" is 8,800 in space-separated number format — should not be removed
    text = "over 8 800 incidents"
    assert _remove_partial_duplicates(text) == text


# --- Heading normalisation ---

def test_fixes_missing_space_in_heading():
    assert _normalize_headings("##SUMMARY") == "## SUMMARY"
    assert _normalize_headings("###FINDINGS") == "### FINDINGS"

def test_leaves_valid_heading_alone():
    assert _normalize_headings("## SUMMARY") == "## SUMMARY"

def test_converts_bold_heading():
    result = _normalize_headings("**SUMMARY**")
    assert result == "## Summary"

def test_converts_bold_recommendations():
    result = _normalize_headings("**RECOMMENDATIONS**")
    assert result == "## Recommendations"

def test_preserves_non_heading_bold():
    text = "The **branch** has high revenue."
    assert _normalize_headings(text) == text


# --- Full clean_text pipeline ---

def test_clean_text_exact_duplicate():
    result = clean_text("sometimes sometimes it works")
    assert result == "sometimes it works"

def test_clean_text_partial_duplicate():
    result = clean_text("repair to hand handle fuel leaks")
    assert result == "repair to handle fuel leaks"

def test_clean_text_heading_fix():
    result = clean_text("##SUMMARY\n- bullet point")
    assert result.startswith("## SUMMARY")

def test_clean_text_strips_ansi():
    result = clean_text("\x1b[32mgreen text\x1b[0m")
    assert "\x1b" not in result
    assert "green text" in result
