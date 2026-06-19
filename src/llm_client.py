"""
ShelfEye Structured GenAI Synthesis Client
Handles deterministic JSON payload generation via OpenAI API for role-based briefs.
"""

import json
import logging
from typing import Dict, Any
from openai import OpenAI

# Initialize structured logging
logger = logging.getLogger("ShelfEye.LLMClient")

def generate_role_based_brief(company_name: str, daily_revenue: float) -> Dict[str, Any]:
    """
    Queries GPT-4o-mini using strict JSON mode to synthesize retail insights.
    
    Maps store-manager operational labor workflows to corporate buyer margin goals,
    leveraging ShelfEye's $45/mo pricing against the prospect's daily revenue exposure.
    """
    # Defensive programming: instantiate client securely via environment fallback
    try:
        client = OpenAI()
    except Exception as error:
        logger.error(f"Failed to initialize OpenAI client instance: {error}")
        return {
            "buyer_margin_pitch": "Configuration error. System tracking simulation fallback.",
            "manager_labor_pitch": "Configuration error. System tracking simulation fallback.",
            "outreach_hook": "Configuration error. System tracking simulation fallback."
        }

    # Enforce clear guardrails and data boundaries within the system prompt
    system_instruction = (
        "You are an expert B2B retail technology GTM strategist. Your output must be "
        "entirely metrics-driven, concise, free of corporate jargon, and formatted "
        "as a raw JSON object matching the requested schema exactly."
    )

    user_prompt = f"""
    Analyze the retail prospect '{company_name}', which is losing leakage margins 
    from an estimated daily aisle revenue of ${daily_revenue:,.2f} due to unaddressed shelf blind spots.
    
    Synthesize strategic messaging hooks for ShelfEye's $45/month SaaS product.
    
    You must return exactly this JSON structure and nothing else:
    {{
      "buyer_margin_pitch": "A hard financial justification contrasting the $45/mo cost against protecting ${daily_revenue}/day aisle revenue.",
      "manager_labor_pitch": "A workflow-focused pitch explaining how ShelfEye eliminates manual audit friction for store floor staff.",
      "outreach_hook": "A punchy, metric-focused sequence opener referencing the $1.77T global shelf leakage problem."
    }}
    """

    try:
        # Enforce structural schema compliance via JSON mode
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": system_instruction},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.2  # Low temperature to preserve structural determinism
        )
        
        raw_content = response.choices[0].message.content
        if not raw_content:
            raise ValueError("Received empty string response from LLM orchestration.")
            
        return json.loads(raw_content)

    except json.JSONDecodeError as json_error:
        logger.error(f"Failed to parse incoming LLM response string into valid JSON: {json_error}")
        raise ValueError("GenAI response failed structural validation.") from json_error
        
    except Exception as api_error:
        logger.error(f"OpenAI API transaction runtime failure: {api_error}")
        # Graceful degradation configuration for production stability
        return {
            "buyer_margin_pitch": f"Protecting ${daily_revenue}/day aisle revenue via automated monitoring.",
            "manager_labor_pitch": "Automating shelf blind spot detection to optimize localized labor force routines.",
            "outreach_hook": f"Mitigating a portion of the $1.77T global retail loss at {company_name}."
        }
