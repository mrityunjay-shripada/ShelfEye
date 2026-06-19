"""
ShelfEye UI Application Layer Blueprint
Streamlit controller orchestration handling ingestion pipelines and visual rendering.
"""

import logging
import streamlit as st
import pandas as pd
from src.engine import compute_priority_score
from src.llm_client import generate_role_based_brief

# Setup logging context
logger = logging.getLogger("ShelfEye.App")

def run_application() -> None:
    """
    Orchestrates the user interface layout and pipeline data flow for ShelfEye.
    Handles CSV ingestion, data frame transformation, and sales brief visualization.
    """
    st.set_page_config(page_title="ShelfEye GTM Engine", layout="wide")
    
    st.title("🎯 ShelfEye: Retail Lead Prioritization Command Center")
    st.caption("Targeting the $1.77T global shelf blind spot loss with automated account intelligence.")

    # 1. Ingestion Interface Components
    uploaded_file = st.file_uploader(
        "Upload Raw Retail Leads Dataset (CSV Format)", 
        type=["csv"],
        help="Expected columns: Company Name, Est Daily Aisle Revenue, Shelf Blind Spots Detected, Labor Friction High, Pilot Pack Readiness, Market Fit Score"
    )

    if not uploaded_file:
        st.info("💡 Awaiting CSV ingestion to initialize the prioritization matrix pipeline.")
        return

    try:
        # 2. Ingestion & Core Data Transformation Pipeline
        raw_dataframe = pd.read_csv(uploaded_file)
        
        # Guardrail check for expected structural columns
        required_fields = {"Company Name", "Est Daily Aisle Revenue"}
        if not required_fields.issubset(raw_dataframe.columns):
            st.error("🚨 Missing critical fields. Verify 'Company Name' and 'Est Daily Aisle Revenue' exist in the CSV.")
            return

        with st.spinner("Processing deterministic scoring matrices..."):
            # Map row payloads through the scoring logic module
            raw_dataframe["Priority Score"] = raw_dataframe.apply(
                lambda row: compute_priority_score(row.to_dict()), axis=1
            )
            
            # Re-index dataframe sorted by highest algorithmic impact score
            processed_df = raw_dataframe.sort_values(by="Priority Score", ascending=False).reset_index(drop=True)

        # 3. Data Presentation Layer
        st.subheader("📋 Ranked High-Yield Retail Prospects")
        st.dataframe(
            processed_df, 
            use_container_width=True,
            column_config={
                "Priority Score": st.column_config.NumberColumn("Priority Score (0-100)", format="%.2f"),
                "Est Daily Aisle Revenue": st.column_config.NumberColumn("Est Daily Aisle Revenue", format="$%.2f")
            }
        )

        # 4. GenAI Semantic Briefing Interface
        st.divider()
        st.subheader("⚡ GenAI Dual-Persona Action Cards")
        st.markdown("Select a prioritized account to compile structured role-based pitches.")

        # Account picker dropdown configuration
        target_index = st.selectbox(
            "Select Account for Live Sales Briefing:",
            options=processed_df.index,
            format_func=lambda idx: f"[{processed_df.loc[idx, 'Priority Score']:.1f}] {processed_df.loc[idx, 'Company Name']}"
        )

        if st.button("Synthesize Account Strategy", type="primary"):
            target_lead = processed_df.loc[target_index]
            company_name = str(target_lead["Company Name"])
            daily_rev = float(target_lead["Est Daily Aisle Revenue"])

            with st.spinner(f"Querying structured schema hooks for {company_name}..."):
                # Delegate text generation to the decoupled LLM client
                insights = generate_role_based_brief(company_name, daily_rev)
                
                # Render multi-column, role-specific strategic dashboard widgets
                meta_col, hook_col = st.columns([1, 2])
                with meta_col:
                    st.metric(label="Calculated Priority Score", value=f"{target_lead['Priority Score']}/100")
                with hook_col:
                    st.info(f"**⚡ Outreach Hook Sequence Opener:**\n\n{insights.get('outreach_hook')}")

                pitch_col1, pitch_col2 = st.columns(2)
                with pitch_col1:
                    st.success(f"**💼 Corporate Buyer Margin Pitch ($45/mo vs ${daily_rev:,.2f}/day ROI):**\n\n{insights.get('buyer_margin_pitch')}")
                with pitch_col2:
                    st.warning(f"**🏬 Store Manager Floor Labor Pitch:**\n\n{insights.get('manager_labor_pitch')}")

    except Exception as error:
        logger.critical(f"Application interface crashed during rendering loop: {error}")
        st.error("An unhandled exception occurred while rendering the data pipelines. Review logs for details.")

if __name__ == "__main__":
    run_application()
