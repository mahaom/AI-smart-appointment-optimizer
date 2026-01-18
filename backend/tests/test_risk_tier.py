from app.services.scoring_service import assign_risk_tier

def test_assign_risk_tier_thresholds():
    assert assign_risk_tier(0.0) == "low"
    assert assign_risk_tier(0.29) == "low"
    assert assign_risk_tier(0.30) == "medium"
    assert assign_risk_tier(0.59) == "medium"
    assert assign_risk_tier(0.60) == "high"
    assert assign_risk_tier(0.99) == "high"
