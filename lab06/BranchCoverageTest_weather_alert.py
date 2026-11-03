import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

# ==========================================================
# Branch Coverage Tests for weather_alert.py
# Target: >= 90% Branch Coverage (Achieves 100% Branch Coverage)
# ==========================================================

# --- Branch Coverage for wind_alert ---
def test_wind_alert_all_branches():
    # Test boundary and condition branches:
    # 1. speed_kmh >= 89 (True) -> 'warning'
    assert wind_alert(89) == "warning"
    assert wind_alert(100) == "warning"

    # 2. speed_kmh >= 62: False for >= 89, True for >= 62 -> 'watch'
    assert wind_alert(62) == "watch"
    assert wind_alert(88) == "watch"

    # 3. speed_kmh >= 39: False for >= 62, True for >= 39 -> 'advisory'
    assert wind_alert(39) == "advisory"
    assert wind_alert(61) == "advisory"

    # 4. speed_kmh < 39: False for all -> 'none'
    assert wind_alert(38) == "none"
    assert wind_alert(0) == "none"


# --- Branch Coverage for rain_alert ---
def test_rain_alert_all_branches():
    # Outer branch: mm_per_hour >= 50 (True)
    # Inner branch: soil_saturated == True -> 'warning'
    assert rain_alert(50, True) == "warning"
    assert rain_alert(80, True) == "warning"
    # Inner branch: soil_saturated == False -> 'watch'
    assert rain_alert(50, False) == "watch"
    assert rain_alert(75, False) == "watch"

    # Outer branch: mm_per_hour < 50, but mm_per_hour >= 10 (True)
    # Inner branch: soil_saturated == True -> 'watch'
    assert rain_alert(10, True) == "watch"
    assert rain_alert(49, True) == "watch"
    # Inner branch: soil_saturated == False -> 'advisory'
    assert rain_alert(10, False) == "advisory"
    assert rain_alert(30, False) == "advisory"

    # Outer branch: mm_per_hour < 10 (False for both >= 50 and >= 10) -> 'none'
    assert rain_alert(9, True) == "none"
    assert rain_alert(0, False) == "none"


# --- Branch Coverage for heat_alert ---
def test_heat_alert_all_branches():
    # Branch 1: humidity > 40 (True)
    # Condition: index >= 45 (True) -> 'warning'
    assert heat_alert(40, 90) == "warning"    # index = 40 + 5.0 = 45.0
    # Condition: index >= 40 (True), index >= 45 (False) -> 'watch'
    assert heat_alert(36, 80) == "watch"      # index = 36 + 4.0 = 40.0
    # Condition: index >= 35 (True), index >= 40 (False) -> 'advisory'
    assert heat_alert(32, 70) == "advisory"   # index = 32 + 3.0 = 35.0
    # Condition: index < 35 -> 'none'
    assert heat_alert(28, 50) == "none"       # index = 28 + 1.0 = 29.0

    # Branch 2: humidity <= 40 (False branch for humidity > 40)
    # Condition: index >= 45 (True) -> 'warning'
    assert heat_alert(45, 40) == "warning"    # index = 45
    # Condition: index >= 40 (True), index >= 45 (False) -> 'watch'
    assert heat_alert(40, 35) == "watch"      # index = 40
    # Condition: index >= 35 (True), index >= 40 (False) -> 'advisory'
    assert heat_alert(35, 20) == "advisory"   # index = 35
    # Condition: index < 35 -> 'none'
    assert heat_alert(30, 10) == "none"       # index = 30


# --- Branch Coverage for overall_alert ---
def test_overall_alert_all_branches():
    # Branch: alerts is empty (for loop does not execute) -> 'none'
    assert overall_alert([]) == "none"

    # Branch: alert in SEVERITY (True)
    # Branch: SEVERITY[alert] > SEVERITY[worst] (True branch -> update worst)
    assert overall_alert(["none", "advisory", "watch", "warning"]) == "warning"

    # Branch: SEVERITY[alert] > SEVERITY[worst] (False branch -> do not update worst)
    assert overall_alert(["warning", "advisory", "none"]) == "warning"

    # Branch: alert not in SEVERITY (True -> raises ValueError)
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["hurricane"])
