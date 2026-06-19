"""
ShelfEye Core Deterministic Scoring Engine
Translates qualitative retail GTM signals into a quantitative priority score.
"""

import logging
from typing import Dict, Any

# Configure structured logging for production traceability
logger = logging.getLogger("ShelfEye.Engine")

def compute_priority_score(lead_data: Dict[str, Any]) -> float:
    """
    Calculates a weighted priority score (0.0 to 100.0) for a retail prospect.
    
    Weights applied:
    - Market Fit & Roadmap Readiness: 30%
    - Revenue Exposure ($500+/day target): 25%
    - Inventory Pain Signals (Shelf Blind Spots): 25%
    - Workforce Labor Friction: 20%
    """
    try:
        # 1. Market Fit & Roadmap Phase Alignment (30% Weight)
        # Phase 1 pilots get immediate prioritization to accelerate the $100k ARR milestone
        roadmap_matrix = {"Phase 1": 100.0, "Phase 2": 60.0, "Phase 3": 30.0}
        
        market_fit = float(lead_data.get("Market Fit Score", 0)) * 10.0
        phase_score = roadmap_matrix.get(lead_data.get("Pilot Pack Readiness"), 20.0)
        fit_component = (market_fit * 0.5) + (phase_score * 0.5)
        
        # 2. Daily Aisle Revenue Exposure (25% Weight)
        # Strategic threshold to anchor against the $45/mo SaaS pricing model
        daily_revenue = float(lead_data.get("Est Daily Aisle Revenue", 0))
        revenue_component = 100.0 if daily_revenue >= 500.0 else 50.0
        
        # 3. Inventory Pain Signals / Shelf Blind Spots (25% Weight)
        # Targets the operational root cause of the $1.77T global retail loss
        has_blind_spots = str(lead_data.get("Shelf Blind Spots Detected")).strip().lower() == "yes"
        pain_component = 100.0 if has_blind_spots else 20.0
        
        # 4. Workforce/Labor Force Friction (20% Weight)
        # Aligns product positioning with store-manager operational bandwidth constraints
        labor_friction = str(lead_data.get("Labor Friction High")).strip().lower() == "true"
        labor_component = 100.0 if labor_friction else 40.0
        
        # Compute final aggregate weighted metric
        final_priority_score = (
            (fit_component * 0.30) + 
            (revenue_component * 0.25) + 
            (pain_component * 0.25) + 
            (labor_component * 0.20)
        )
        
        return round(final_priority_score, 2)
        
    except (ValueError, TypeError) as error:
        logger.error(f"Execution failed due to malformed metrics payload: {error}")
        raise ValueError("Lead data parsing failed. Ensure numeric inputs are formatted correctly.") from error
