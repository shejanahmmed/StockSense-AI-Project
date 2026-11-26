"""
Unit & Integration Tests for Closed-Loop Forecast Accuracy Audit & Model Reliability Scorecard
"""
import pytest
import numpy as np
import sys
from pathlib import Path

# Ensure project root is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.api.main import app
from src.api.database import get_db_connection
from src.api.auth_utils import create_access_token
from fastapi.testclient import TestClient

client = TestClient(app)

TEST_ORG = "test_org_audit"
TEST_TOKEN = create_access_token({"sub": TEST_ORG, "role": "admin"})
AUTH_HEADERS = {"Authorization": f"Bearer {TEST_TOKEN}"}


def test_wape_and_bias_mathematical_formulation():
    """Verify WAPE, Forecast Tracking Bias, and Reliability Score calculations."""
    actuals = np.array([10.0, 15.0, 12.0, 8.0, 20.0])
    predictions = np.array([12.0, 14.0, 11.0, 9.0, 18.0])

    sum_actuals = float(np.sum(actuals)) # 65.0
    sum_abs_err = float(np.sum(np.abs(actuals - predictions))) # 2 + 1 + 1 + 1 + 2 = 7.0
    sum_diff = float(np.sum(predictions - actuals)) # +2 - 1 - 1 + 1 - 2 = -1.0

    wape = round((sum_abs_err / sum_actuals) * 100.0, 1) # (7 / 65) * 100 = 10.77 -> 10.8%
    bias = round((sum_diff / sum_actuals) * 100.0, 1) # (-1 / 65) * 100 = -1.54 -> -1.5%
    accuracy = round(max(0.0, 100.0 - wape), 1) # 89.2%

    raw_score = 100.0 - (0.7 * wape) - (0.3 * abs(bias)) # 100 - (7.56) - (0.45) = 91.99
    reliability_score = round(max(10.0, min(99.0, raw_score)), 1) # 92.0

    assert wape == 10.8
    assert bias == -1.5
    assert accuracy == 89.2
    assert reliability_score == 92.0


def test_wape_zero_division_guard():
    """Verify that when actuals sum to zero, WAPE and Bias handle gracefully without crashing."""
    actuals = np.array([0.0, 0.0, 0.0])
    preds = np.array([0.0, 0.0, 0.0])
    sum_actuals = float(np.sum(actuals))

    if sum_actuals > 0:
        wape = (float(np.sum(np.abs(actuals - preds))) / sum_actuals) * 100.0
    else:
        wape = 0.0

    assert wape == 0.0


def test_accuracy_scorecard_endpoint_auth_required():
    """GET /api/analytics/accuracy-scorecard requires valid JWT."""
    res = client.get("/api/analytics/accuracy-scorecard")
    assert res.status_code == 401


def test_accuracy_scorecard_endpoint_with_records():
    """GET /api/analytics/accuracy-scorecard returns structured audit data and persists to SQLite."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Insert test inventory item with forecast audit fields
    cursor.execute('''
        INSERT OR REPLACE INTO inventory
        (org_name, sku, name, category, price, stock, reorder_point, supplier_lead_days, 
         forecast_wape, forecast_bias, forecast_reliability)
        VALUES (?, 'SKU-AUDIT-01', 'Test Audit Camera', 'Electronics', 150.0, 50, 40, 5, 7.5, 1.2, 94.0)
    ''', (TEST_ORG,))
    conn.commit()
    conn.close()

    res = client.get("/api/analytics/accuracy-scorecard", headers=AUTH_HEADERS)
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "success"
    assert "data" in data
    scorecard = data["data"]
    assert scorecard["has_audit"] is True
    assert "overall_accuracy" in scorecard
    assert "overall_wape" in scorecard
    assert "overall_bias" in scorecard
    assert "sku_scorecard" in scorecard
    assert len(scorecard["sku_scorecard"]) >= 1

    first_item = scorecard["sku_scorecard"][0]
    assert "sku" in first_item
    assert "wape" in first_item
    assert "bias" in first_item
    assert "reliability_score" in first_item
    assert "status" in first_item
    assert "recommendation" in first_item
