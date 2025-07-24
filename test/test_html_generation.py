import pandas as pd
import os
from etsi.failprint.core import analyze


def test_html_output():
    """Test that HTML output is generated correctly with all expected components."""
    # Sample data
    X = pd.DataFrame({
        "feature1": [1, 2, 2, 3, 3, 3, 4],
        "feature2": [10, 15, 14, 13, 12, 13, 20],
        "category": ["A", "B", "B", "B", "C", "C", "A"]
    })
    y_true = pd.Series([1, 1, 1, 0, 0, 1, 0])
    y_pred = pd.Series([1, 1, 0, 0, 0, 1, 1])
    
    # Generate HTML report
    html_report = analyze(X, y_true, y_pred, output="html", cluster=True)
    
    # Verify HTML file was created
    assert os.path.exists("reports/failprint_report.html"), "HTML report file not created"
    
    # Read the generated HTML
    with open("reports/failprint_report.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Verify essential HTML components are present
    assert "<!DOCTYPE html>" in html_content, "Missing DOCTYPE"
    assert "<title>Failprint HTML Report</title>" in html_content, "Missing title"
    assert "Failprint HTML Report" in html_content, "Missing main heading"
    
    # Verify summary section
    assert "<b>Total Samples:</b> 7" in html_content, "Missing total samples"
    assert "Failures: 2" in html_content, "Missing failure count"
    assert "28.57%" in html_content, "Missing failure percentage"
    
    # Verify plotly chart components
    assert "plotly" in html_content.lower(), "Missing Plotly chart"
    assert "Top Features Influencing Failures" in html_content, "Missing chart title"
    
    # Verify cluster sections
    assert "Cluster-wise Feature Stats" in html_content, "Missing cluster section"
    assert "Cluster 1" in html_content, "Missing cluster data"
    
    # Verify failure segments
    assert "Failure Segments" in html_content, "Missing failure segments section"
    assert "feature1" in html_content, "Missing feature data"
    
    # Verify CSS styling is present
    assert "<style>" in html_content, "Missing CSS styling"
    assert "font-family: Arial" in html_content, "Missing font styling"
    
    print("✅ HTML output test passed - all components verified")


def test_html_vs_markdown():
    """Test that both HTML and markdown outputs work."""
    X = pd.DataFrame({
        "feature1": [1, 2, 3],
        "feature2": [10, 20, 30]
    })
    y_true = pd.Series([1, 0, 1])
    y_pred = pd.Series([1, 1, 0])
    
    # Test HTML output
    html_report = analyze(X, y_true, y_pred, output="html")
    assert "<!DOCTYPE html>" in html_report, "HTML output not generated"
    
    # Test markdown output (default)
    md_report = analyze(X, y_true, y_pred, output="markdown")
    assert "# failprint Report" in md_report, "Markdown output not generated"
    
    print("✅ Both HTML and markdown outputs work correctly")


if __name__ == "__main__":
    test_html_output()
    test_html_vs_markdown()
    print("✅ All HTML generation tests passed!")