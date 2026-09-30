import pandas as pd

from etsi.failprint import analyze


def test_analyze_writes_report_without_default_log(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    features = pd.DataFrame({"segment": ["a", "a", "b", "b"]})
    y_true = pd.Series([1, 1, 0, 0])
    y_pred = pd.Series([1, 0, 0, 1])

    report = analyze(features, y_true, y_pred, cluster=False)

    assert "Failures: 2 (50.00%)" in report
    assert (tmp_path / "reports" / "failprint_report.md").exists()
    assert not (tmp_path / "failprint.log").exists()
