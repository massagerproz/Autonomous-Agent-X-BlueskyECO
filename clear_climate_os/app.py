import streamlit as st
import json

def mock_ai_extract(text):
    """Mock AI extraction for demo purposes with confidence scores"""
    evidence = []

    if "solar" in text.lower() or "panels" in text.lower():
        evidence.append({
            "id": 1,
            "category": "Activity Update",
            "content": "Installed 50 solar panels at the community center.",
            "source": "Meeting Notes",
            "confidence": 0.95,
            "approved": False
        })
    if "delay" in text.lower() or "weather" in text.lower():
        evidence.append({
            "id": 2,
            "category": "Risk",
            "content": "Heavy rain causing delays in panel installation.",
            "source": "Meeting Notes",
            "confidence": 0.88,
            "approved": False
        })
    if "budget" in text.lower() or "approved" in text.lower() or "funding" in text.lower():
        evidence.append({
            "id": 3,
            "category": "Decision",
            "content": "Additional funding/budget of $5k approved for weatherproofing.",
            "source": "Meeting Notes",
            "confidence": 0.92,
            "approved": False
        })
    if "water" in text.lower():
         evidence.append({
            "id": 5,
            "category": "Activity Update",
            "content": "Installed new water filtration system.",
            "source": "Meeting Notes",
            "confidence": 0.85,
            "approved": False
         })

    if not evidence:
         evidence.append({
            "id": 4,
            "category": "Activity Update",
            "content": "Project kickoff meeting completed.",
            "source": "Meeting Notes",
            "confidence": 0.60,
            "approved": False
        })

    return evidence

def generate_report(evidence_tracker):
    """Generate a donor report draft based ONLY on approved evidence"""
    if not evidence_tracker:
        return "No evidence available to generate report."

    report = "### Donor Report Draft\n\n"
    report += "**Project Activities & Updates:**\n"
    i = 1
    for e in evidence_tracker:
        if e['category'] in ['Activity Update', 'Decision']:
             report += f"{i}. {e['content']}\n"
             i += 1

    report += "\n**Risks & Challenges:**\n"
    i = 1
    for e in evidence_tracker:
        if e['category'] == 'Risk':
             report += f"{i}. {e['content']}\n"
             i += 1

    # Inject a hallucinated claim to demonstrate QA flagging
    report += "\n**Impact:**\n"
    report += "1. Reduced carbon emissions by 500 tons this month. (UNSUPPORTED CLAIM)\n"

    return report

def qa_review(report):
    """Mock QA reviewer that flags unsupported claims"""
    flags = []
    if "UNSUPPORTED CLAIM" in report:
        flags.append({
            "type": "Unsupported Claim / Overclaiming",
            "description": "The claim 'Reduced carbon emissions by 500 tons this month' is not supported by the approved evidence tracker."
        })
    return flags

def main():
    st.set_page_config(page_title="CLEAR Climate Copilot", layout="wide")
    st.title("CLEAR Climate Copilot")
    st.subheader("Turn scattered project information into structured reporting evidence")

    st.sidebar.title("Workflow")
    st.sidebar.markdown("""
    1. Input Notes
    2. Extract & Edit Evidence
    3. Review & Approve
    4. Generate Draft Report
    5. QA Review
    6. Export
    """)

    # Initialize session state
    if 'evidence_tracker' not in st.session_state:
        st.session_state['evidence_tracker'] = []
    if 'draft_report' not in st.session_state:
        st.session_state['draft_report'] = None
    if 'qa_flags' not in st.session_state:
         st.session_state['qa_flags'] = []
    if 'extracted_evidence' not in st.session_state:
        st.session_state['extracted_evidence'] = []

    st.header("Step 1: Input Meeting Notes or Updates")
    notes_input = st.text_area("Paste meeting notes, activity updates, or stakeholder inputs here:", height=150)

    if st.button("Process Notes"):
        if notes_input.strip() == "":
            st.warning("Please enter some notes to process.")
        else:
            st.session_state['notes_processed'] = True
            # Load new evidence, resetting edits
            st.session_state['extracted_evidence'] = mock_ai_extract(notes_input)
            st.success("Notes processed! See extracted evidence below.")

    if st.session_state.get('notes_processed'):
        st.divider()
        st.header("Step 2 & 3: AI Extraction, Edit & Human Approval")
        st.markdown("Review and edit the extracted evidence. **AI output must be treated as draft output, not truth.** Human approval is required before evidence enters the tracker.")

        extracted = st.session_state.get('extracted_evidence', [])

        if not extracted:
             st.info("No evidence extracted.")
        else:
            with st.form("approval_form"):
                approved_ids = []
                # We need to keep track of edited content before submission
                edited_content_map = {}

                for i, item in enumerate(extracted):
                    col1, col2 = st.columns([1, 4])

                    with col1:
                        st.write(f"**{item['category']}**")
                        # Display confidence score with color coding
                        conf = item.get('confidence', 0)
                        color = "green" if conf > 0.8 else ("orange" if conf > 0.5 else "red")
                        st.markdown(f"AI Confidence: :{color}[{conf*100:.0f}%]")

                        is_approved = st.checkbox("Approve", key=f"approve_{item['id']}")
                        if is_approved:
                            approved_ids.append(item['id'])

                    with col2:
                        # Allow user to edit the AI's drafted content
                        edited_content = st.text_area(
                            "Edit Content:",
                            value=item['content'],
                            key=f"edit_content_{item['id']}",
                            height=68
                        )
                        edited_content_map[item['id']] = edited_content

                    st.markdown("---")

                submitted = st.form_submit_button("Save Approved Evidence to Tracker")

                if submitted:
                    for item in extracted:
                        # Update the item with whatever the user edited
                        item['content'] = edited_content_map[item['id']]

                        if item['id'] in approved_ids:
                            # Avoid duplicates in tracker
                            if not any(e['id'] == item['id'] for e in st.session_state['evidence_tracker']):
                                item['approved'] = True
                                # Add a copy to the tracker
                                st.session_state['evidence_tracker'].append(dict(item))

                    if approved_ids:
                        st.success(f"Saved {len(approved_ids)} items to Evidence Tracker!")
                    else:
                        st.warning("No items selected for approval.")

        st.divider()
        if st.session_state['evidence_tracker']:
            st.header("Evidence Tracker")
            for e in st.session_state['evidence_tracker']:
                st.write(f"- [{e['category']}] {e['content']}")

            col_clear, col_json = st.columns(2)
            with col_clear:
                if st.button("Clear Evidence Tracker"):
                    st.session_state['evidence_tracker'] = []
                    st.session_state['draft_report'] = None
                    st.rerun()
            with col_json:
                tracker_json = json.dumps(st.session_state['evidence_tracker'], indent=2)
                st.download_button(
                    label="Download Tracker Data (JSON)",
                    data=tracker_json,
                    file_name="evidence_tracker.json",
                    mime="application/json"
                )

            st.divider()
            st.header("Step 4 & 5: Report Generation & QA")
            if st.button("Generate Donor Report Draft"):
                report = generate_report(st.session_state['evidence_tracker'])
                flags = qa_review(report)

                st.session_state['draft_report'] = report
                st.session_state['qa_flags'] = flags

            if st.session_state.get('draft_report'):
                st.markdown(st.session_state['draft_report'])

                if st.session_state.get('qa_flags'):
                     st.error("### QA Review Alerts")
                     for flag in st.session_state['qa_flags']:
                         st.write(f"**{flag['type']}**: {flag['description']}")
                else:
                     st.success("QA Review Passed: No unsupported claims found.")

                st.divider()
                st.header("Step 6: Export")
                st.download_button(
                    label="Download Report as TXT",
                    data=st.session_state['draft_report'],
                    file_name="donor_report_draft.txt",
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()
