from content_analyzer_code import ContentAnalyzer

def test_content_analyzer_initialization():
    analyzer = ContentAnalyzer(["segment1", "segment2"])
    assert analyzer.content_segments == ["segment1", "segment2"]
    assert analyzer.sustainability_elements == []

def test_content_analyzer_empty_input():
    analyzer = ContentAnalyzer([])
    assert analyzer.content_segments == []
    assert analyzer.sustainability_elements == []


def test_detect_high_priority_keyword():
    analyzer = ContentAnalyzer(["This document ensures compliance with EU law"])
    results = analyzer.detect_keywords()

    # Must find "compliance" as high_priority
    assert ("compliance", "high_priority") in results
    assert len(results) == 1