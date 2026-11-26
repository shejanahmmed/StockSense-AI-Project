"""
Tests for Dynamic Safety Stock & Adaptive Reorder Point (ROP) Statistical Formulas
"""
import pytest
import math
import sys
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.api.routers.analytics import get_z_score

def test_get_z_score_exact_and_interpolated():
    """Verify normal inverse CDF z-score approximations."""
    # Standard benchmarks
    assert get_z_score(0.90) == 1.282
    assert get_z_score(0.95) == 1.645
    assert get_z_score(0.98) == 2.054
    assert get_z_score(0.99) == 2.326

    # Dynamic points
    assert get_z_score(0.80) == 0.842
    assert get_z_score(0.999) == 3.09

    # Midpoints
    z_mid = get_z_score(0.96)
    assert 1.645 < z_mid < 2.054


def test_dynamic_rop_formula_calculations():
    """Verify cycle demand, safety stock, and dynamic ROP match specifications."""
    # Scenario 1: Daily demand = 10, Lead time = 4 days, std = 3, service level = 95%
    forecasted_demand = 70.0
    forecast_horizon = 7
    d_daily = forecasted_demand / forecast_horizon # 10.0
    lead_days = 4 # sqrt(4) = 2.0
    demand_std = 3.0
    z = get_z_score(0.95) # 1.645

    cycle_demand = math.ceil(d_daily * lead_days) # ceil(10 * 4) = 40
    safety_stock = max(0, math.ceil(z * math.sqrt(lead_days) * demand_std)) # ceil(1.645 * 2 * 3) = ceil(9.87) = 10
    dynamic_rop = max(1, cycle_demand + safety_stock) # 40 + 10 = 50

    assert cycle_demand == 40
    assert safety_stock == 10
    assert dynamic_rop == 50


def test_zero_demand_std_safety_stock():
    """Verify that when standard deviation of demand is zero, safety stock is 0 but cycle demand persists."""
    d_daily = 5.0
    lead_days = 3
    demand_std = 0.0
    z = get_z_score(0.95)

    safety_stock = max(0, math.ceil(z * math.sqrt(lead_days) * demand_std))
    cycle_demand = math.ceil(d_daily * lead_days)
    dynamic_rop = max(1, cycle_demand + safety_stock)

    assert safety_stock == 0
    assert cycle_demand == 15
    assert dynamic_rop == 15
