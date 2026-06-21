from app import mock_ai_extract, generate_report, qa_review

def test_mock_ai_extract_with_matches():
    text = "We installed 50 solar panels, but heavy rain is causing a delay. Also, a budget was approved. The mayor set a deadline for next week."
    evidence = mock_ai_extract(text)
    assert len(evidence) == 5
    categories = [e['category'] for e in evidence]
    assert 'Activity Update' in categories
    assert 'Risk' in categories
    assert 'Decision' in categories
    assert 'Stakeholder Input' in categories
    assert 'Deadline' in categories

    # Check for presence of new fields
    for e in evidence:
        assert 'confidence' in e
        assert isinstance(e['confidence'], float)
        assert 'reasoning' in e
        assert isinstance(e['reasoning'], str)

def test_mock_ai_extract_no_matches():
    text = "Just a regular meeting with nothing specific."
    evidence = mock_ai_extract(text)
    assert len(evidence) == 1
    assert evidence[0]['category'] == 'Activity Update'
    assert 'confidence' in evidence[0]
    assert 'reasoning' in evidence[0]

def test_generate_report_empty():
    report = generate_report([])
    assert report == "No evidence available to generate report."

def test_generate_report_with_evidence():
    evidence = [
        {"id": 1, "category": "Activity Update", "content": "Test activity", "approved": True},
        {"id": 2, "category": "Risk", "content": "Test risk", "approved": True},
        {"id": 3, "category": "Deadline", "content": "Test deadline", "approved": True}
    ]
    report = generate_report(evidence)
    assert "Test activity" in report
    assert "Test risk" in report
    assert "Test deadline" in report
    assert "UNSUPPORTED CLAIM" in report

def test_qa_review():
    report_with_claim = "Some text. Reduced carbon emissions by 500 tons this month. (UNSUPPORTED CLAIM)"
    flags = qa_review(report_with_claim)
    assert len(flags) == 1
    assert flags[0]['type'] == 'Unsupported Claim / Overclaiming'

    report_without_claim = "Just regular text."
    flags = qa_review(report_without_claim)
    assert len(flags) == 0
