# ShelfEye: Retail Lead Prioritization & GenAI Insight Engine

ShelfEye is an enterprise-grade, architecture-focused GTM pipeline designed to ingest raw retail lead data, algorithmically rank high-yield prospects, and dynamically synthesize role-based sales intelligence. 

The engine directly targets accounts exposed to the **$1.77T global retail loss** driven by shelf blind spots discovered during retail manager field interviews. It programmatically sequences pipelines to secure Phase 1 pilots, accelerating the path toward a **$100k ARR milestone** while defending a target **>3:1 LTV:CAC ratio** by contrasting a **$45/month SaaS pricing model** against quantified **$500+/day retail aisle losses**.

## 🏗️ System Architecture

ShelfEye rejects loose script patterns in favor of a clean, decoupled, production-grade architecture. This ensures strict deterministic mathematical boundaries for lead scoring alongside structural flexibility for semantic analysis.

1. **Ingestion Layer (Streamlit Blueprint):** Designed to handle structured CSV uploads containing core account variables (daily revenue, labor friction status, and GTM pilot readiness).
2. **Deterministic Scoring Engine (Python/Pandas):** Eliminates subjective positioning by executing a rigid, weighted mathematical matrix to calculate a definitive Priority Score (0-100).
3. **Data Caching & Cost Defense Layer (SQLite Blueprint):** Implements a relational relational storage cache to intercept duplicate accounts, mitigating redundant LLM token expenditures to safeguard unit economics.
4. **Structured GenAI Synthesis Layer (OpenAI API / GPT-4o-mini):** Enforces strict JSON schemas to eliminate model drift, generating dual-persona sales briefs that map store-manager operational workflows directly onto corporate buyer margin goals.

---

## 🗂️ Repository Structure

```text
ShelfEye/
│
├── src/                         # Core Application Source
│   ├── app.py                   # Streamlit UI Layer Blueprint
│   ├── engine.py                # Deterministic Scoring Matrix
│   └── llm_client.py            # OpenAI Structured JSON Interface
│
├── .gitignore                   # Python Environment Hygiene
├── requirements.txt             # Dependency Manifest
└── README.md                    # System Documentation# ShelfEye
