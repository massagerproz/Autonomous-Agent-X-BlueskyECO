# CLEAR Climate Copilot / CLEAR Climate OS

This is a proof-of-work AI application designed for climate, ESG, conservation, NGO, and donor-funded project teams. It helps users convert scattered project information into structured reporting evidence.

## Features & Workflow

The app follows a structured core workflow:
1. **Input Notes:** User pastes or uploads meeting notes, activity updates, etc.
2. **AI Extraction:** The system automatically extracts structured evidence (activities, risks, decisions).
3. **Review & Approve:** *Crucially*, AI output is treated as a draft. Human approval is required before evidence enters the tracker.
4. **Evidence Tracker:** A centralized store for approved, verified project facts.
5. **Report Generation:** Generates donor report drafts using *only* approved evidence to prevent inventing facts.
6. **QA Review:** Automatically flags any unsupported claims or overclaiming in the draft.
7. **Export:** Allows users to export the final verified report.

## How to Run

### Requirements
You will need Python installed along with the required libraries:
```bash
pip install streamlit
```

### Running the App
From the root of the repository, execute:
```bash
streamlit run clear_climate_os/app.py
```

### Testing the App
A file containing sample meeting notes is provided (`sample_data.txt`). You can copy its contents and paste them into the app to test the extraction and reporting workflow.

You can also run the automated tests via pytest:
```bash
pip install pytest
pytest clear_climate_os/test_app.py
```

## Engineering Principles Adherence
- Isolated module: App resides in the `clear_climate_os` feature folder.
- AI output is draft: Checkboxes require human approval before tracking.
- Grounded facts: The report draft strictly pulls from the evidence tracker.
- Included sample data and tests for easy demo execution.

## UI & UX Enhancements
- Includes custom CSS injecting Framer-like motion animations.
- Features microinteractions such as button hover scaling and subtle pulsing alerts for QA flagging, improving overall user experience.
