from content_analyzer.content_analyzer_code import ContentAnalyzer

def test_content_analyzer_initialization():
    analyzer = ContentAnalyzer(["segment1", "segment2"])
    assert analyzer.content_segments == ["segment1", "segment2"]
    assert analyzer.sustainability_elements == []

def test_content_analyzer_empty_input():
    analyzer = ContentAnalyzer([])
    assert analyzer.content_segments == []
    assert analyzer.sustainability_elements == []
