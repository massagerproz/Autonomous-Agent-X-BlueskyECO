# Agent Instructions for CLEAR Climate Copilot (`clear_climate_os/`)

This directory contains the proof-of-work application for CLEAR Climate Copilot. When working within this directory, AI agents must strictly adhere to the following principles:

1. **Isolation**: This is an isolated feature module. Do not modify files outside of `clear_climate_os/` unless explicitly requested. Do not attempt to integrate this prototype directly into the upstream autonomous agent code.
2. **AI Output as Draft**: A core domain constraint is that all AI-generated content (e.g., extracted evidence, generated reports) must be treated as a *draft*. Human approval is strictly required before evidence enters the tracker or is considered factual. Do not bypass or remove these approval gates.
3. **Fact Grounding**: Generated reports must only use facts from the approved evidence tracker. Do not invent or hallucinate data. The current mock QA system explicitly flags unsupported claims.
4. **Testing**: Maintain or expand testing (using `pytest`) when modifying core logic in `app.py` or `test_app.py`.
5. **Small Changes**: Keep changes small, surgical, and well-tested. Avoid overengineering the prototype.
