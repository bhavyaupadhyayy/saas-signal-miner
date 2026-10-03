"""Unit tests for response parsing, scoring and filtering. No network or API key needed."""

from main import SaaSSignalMiner
from utils import calculate_growth_score, get_fallback_data, parse_saas_startups_response


def test_parses_json_array_embedded_in_prose():
    response = 'Here are the startups:\n[{"name": "Acme", "sector": "Fintech"}]\nHope this helps.'
    startups = parse_saas_startups_response(response)
    assert [s["name"] for s in startups] == ["Acme"]
    assert startups[0]["sector"] == "Fintech"


def test_missing_fields_get_defaults():
    startup = parse_saas_startups_response('[{"name": "Acme"}]')[0]
    assert startup["description"] == "No description available"
    assert startup["funding_stage"] == "Early Stage"


def test_invalid_json_falls_back_to_dummy_data():
    startups = parse_saas_startups_response("[not valid json]")
    assert len(startups) == len(get_fallback_data())


def test_growth_score_adds_stage_signal_and_sector_bonuses():
    startup = {"funding_stage": "Series A", "signal_type": "Funding", "sector": "Cybersecurity"}
    assert calculate_growth_score(startup) == 50 + 15 + 15 + 10


def test_growth_score_base_when_no_signals_match():
    assert calculate_growth_score({}) == 50


def test_filter_by_sector_and_min_score():
    miner = SaaSSignalMiner.__new__(SaaSSignalMiner)  # skip API client setup
    startups = get_fallback_data()
    filtered = miner.filter_startups(startups, sector="healthcare", min_score=80)
    assert [s["name"] for s in filtered] == ["HealthAI Connect"]


def test_all_filter_keeps_everything():
    miner = SaaSSignalMiner.__new__(SaaSSignalMiner)
    startups = get_fallback_data()
    assert len(miner.filter_startups(startups, sector="All", funding_stage="All")) == len(startups)


def test_unique_values_are_sorted_and_deduplicated():
    miner = SaaSSignalMiner.__new__(SaaSSignalMiner)
    stages = miner.get_unique_values(get_fallback_data(), "funding_stage")
    assert stages == ["Early Stage", "Seed", "Series A"]
