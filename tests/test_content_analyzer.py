from content_analyzer.content_analyzer_code import ContentAnalyzer

def test_content_analyzer_initialization():
    # Creamos un ContentAnalyzer con segmentos de prueba
    analyzer = ContentAnalyzer(["segment1", "segment2"])
    
    # Comprobamos que se inicializa correctamente
    assert analyzer.content_segments == ["segment1", "segment2"]
    assert analyzer.sustainability_elements == []