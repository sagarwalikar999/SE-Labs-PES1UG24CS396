import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

# ==========================================
# Code Coverage Tests for weather_alert.py
# Target: >= 90% Line Coverage (Achieves 100%)
# ==========================================

# --- Wind Alert Tests ---
def test_wind_warning():
    assert wind_alert(95) == "warning"

def test_wind_watch():
    assert wind_alert(70) == "watch"

def test_wind_advisory():
    assert wind_alert(45) == "advisory"

def test_wind_none():
    assert wind_alert(20) == "none"


# --- Rain Alert Tests ---
def test_rain_warning():
    assert rain_alert(60, True) == "warning"

def test_rain_watch_heavy_not_saturated():
    assert rain_alert(60, False) == "watch"

def test_rain_watch_moderate_saturated():
    assert rain_alert(25, True) == "watch"

def test_rain_advisory():
    assert rain_alert(25, False) == "advisory"

def test_rain_none():
    assert rain_alert(5, False) == "none"


# --- Heat Alert Tests ---
def test_heat_warning():
    assert heat_alert(42, 70) == "warning"

def test_heat_watch():
    assert heat_alert(38, 60) == "watch"

def test_heat_advisory():
    assert heat_alert(33, 60) == "advisory"

def test_heat_none():
    assert heat_alert(25, 40) == "none"


# --- Overall Alert Tests ---
def test_overall_alert_empty():
    assert overall_alert([]) == "none"

def test_overall_alert_worst_progression():
    assert overall_alert(["none", "advisory", "watch", "warning"]) == "warning"

def test_overall_alert_invalid():
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["invalid_alert"])
