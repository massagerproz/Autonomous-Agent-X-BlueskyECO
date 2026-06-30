# Agent Instructions for CLEAR Climate Copilot (`clear_climate_os/`)

This directory contains the proof-of-work application for CLEAR Climate Copilot. When working within this directory, AI agents must strictly adhere to the following principles:

1. **Isolation**: This is an isolated feature module. Do not modify files outside of `clear_climate_os/` unless explicitly requested. Do not attempt to integrate this prototype directly into the upstream autonomous agent code.
2. **AI Output as Draft**: A core domain constraint is that all AI-generated content (e.g., extracted evidence, generated reports) must be treated as a *draft*. Human approval is strictly required before evidence enters the tracker or is considered factual. Do not bypass or remove these approval gates.
3. **Fact Grounding**: Generated reports must only use facts from the approved evidence tracker. Do not invent or hallucinate data. The current mock QA system explicitly flags unsupported claims.
4. **Testing**: Maintain or expand testing (using `pytest`) when modifying core logic in `app.py` or `test_app.py`.
5. **Small Changes**: Keep changes small, surgical, and well-tested. Avoid overengineering the prototype.

## Technical Implementations

### UI/UX: Glassmorphism and CSS Injection
The Streamlit frontend utilizes custom CSS injected via `st.markdown(..., unsafe_allow_html=True)` to break out of Streamlit's default constraints.
- **Glassmorphism**: Main content sections are wrapped in `<div class="glass-container">` to achieve a sleek UI with translucent backgrounds (`rgba(255, 255, 255, 0.6)`), backdrop-filters (`blur(10px)`), and delicate box-shadows.
- **Motion Design**: Staggered entrance animations are achieved by defining a `@keyframes staggerFadeInUp` and applying it to Streamlit's core classes (`.stMarkdown`, `.stTextArea`) and specifically targeting children of `div[data-testid="stForm"]` using `nth-child` selectors with incremental `animation-delay`s. This simulates a high-fidelity Framer Motion sequence.

### Simulated AI Features
To support advanced workflows without external dependencies, we use simulated modules and caching (`@st.cache_data`):
- **MockPGVector (`clear_climate_os/pgvector_mock.py`)**: Simulates a vector database for Retrieval-Augmented Generation (RAG). Allows users to search a mock historical knowledge base and export results as JSON.
- **Edge AI Enhancer (`clear_climate_os/api/edge_ai.py`)**: Simulates a serverless backend function that enhances the tone and formatting of draft reports.
- **Project Analytics**: Real-time dashboard metrics displaying total approved items and QA flags, dynamically updating based on session state.

### AI Payload Architecture
The extraction logic (`mock_ai_extract`) now produces a rich payload schema to improve traceability and trust. Future real LLM integrations must adhere to this schema per extracted item:
- `id` (int): Unique identifier.
- `category` (str): Domain-specific classification (e.g., Activity Update, Risk, Stakeholder Input, Deadline).
- `content` (str): The extracted claim or fact.
- `source` (str): Origin of the fact.
- `confidence` (float): AI certainty score (0.0 - 1.0) guiding color-coded UI badges.
- `reasoning` (str): Chain-of-thought explanation for *why* the AI extracted this specific piece of evidence, displayed to the user prior to human approval.
- `approved` (bool): Boolean flag enforcing the draft-to-verified lifecycle.
