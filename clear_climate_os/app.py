import streamlit as st

def mock_ai_extract(text):
    """Mock AI extraction for demo purposes"""
    evidence = []

    # Simple keyword-based mock extraction
    if "solar" in text.lower() or "panels" in text.lower():
        evidence.append({
            "id": 1,
            "category": "Activity Update",
            "content": "Installed 50 solar panels at the community center.",
            "source": "Meeting Notes",
            "approved": False
        })
    if "delay" in text.lower() or "weather" in text.lower():
        evidence.append({
            "id": 2,
            "category": "Risk",
            "content": "Heavy rain causing delays in panel installation.",
            "source": "Meeting Notes",
            "approved": False
        })
    if "budget" in text.lower() or "approved" in text.lower() or "funding" in text.lower():
        evidence.append({
            "id": 3,
            "category": "Decision",
            "content": "Additional funding/budget of $5k approved for weatherproofing.",
            "source": "Meeting Notes",
            "approved": False
        })
    if "water" in text.lower():
         evidence.append({
            "id": 5,
            "category": "Activity Update",
            "content": "Installed new water filtration system.",
            "source": "Meeting Notes",
            "approved": False
         })

    # If no keywords match, just provide some generic parsed evidence
    if not evidence:
         evidence.append({
            "id": 4,
            "category": "Activity Update",
            "content": "Project kickoff meeting completed.",
            "source": "Meeting Notes",
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
    2. Extract Evidence
    3. Review & Approve
    4. Generate Draft Report
    5. QA Review
    6. Export
    """)

    # Initialize session state for evidence tracker
    if 'evidence_tracker' not in st.session_state:
        st.session_state['evidence_tracker'] = []
    if 'draft_report' not in st.session_state:
        st.session_state['draft_report'] = None
    if 'qa_flags' not in st.session_state:
         st.session_state['qa_flags'] = []

    st.header("Step 1: Input Meeting Notes or Updates")
    notes_input = st.text_area("Paste meeting notes, activity updates, or stakeholder inputs here:", height=150)

    if st.button("Process Notes"):
        if notes_input.strip() == "":
            st.warning("Please enter some notes to process.")
        else:
            st.session_state['notes_processed'] = True
            st.session_state['extracted_evidence'] = mock_ai_extract(notes_input)
            st.success("Notes processed! See extracted evidence below.")

    if st.session_state.get('notes_processed'):
        st.divider()
        st.header("Step 2 & 3: AI Extraction & Human Approval")
        st.markdown("Review the extracted evidence. **AI output must be treated as draft output, not truth.** Human approval is required before evidence enters the tracker.")

        extracted = st.session_state.get('extracted_evidence', [])

        if not extracted:
             st.info("No evidence extracted.")
        else:
            # Create a form for approval
            with st.form("approval_form"):
                approved_ids = []
                for item in extracted:
                    st.write(f"**{item['category']}**")
                    st.write(item['content'])

                    # Ensure unique keys for checkboxes based on item ID
                    is_approved = st.checkbox("Approve", key=f"approve_{item['id']}")
                    if is_approved:
                        approved_ids.append(item['id'])
                    st.markdown("---")

                submitted = st.form_submit_button("Save Approved Evidence to Tracker")

                if submitted:
                    # Update approval status
                    for item in extracted:
                        if item['id'] in approved_ids:
                            # Avoid duplicates in tracker (simple ID check)
                            if not any(e['id'] == item['id'] for e in st.session_state['evidence_tracker']):
                                item['approved'] = True
                                st.session_state['evidence_tracker'].append(item)

                    st.success(f"Saved {len(approved_ids)} items to Evidence Tracker!")

        st.divider()
        # Display Evidence Tracker
        if st.session_state['evidence_tracker']:
            st.header("Evidence Tracker")
            for e in st.session_state['evidence_tracker']:
                st.write(f"- [{e['category']}] {e['content']}")

            if st.button("Clear Evidence Tracker"):
                st.session_state['evidence_tracker'] = []
                st.session_state['draft_report'] = None
                st.rerun()

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
