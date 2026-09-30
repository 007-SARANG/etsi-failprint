import os


class ReportWriter:
    def __init__(self, segments, drift_map, clustered_segments,
                 output, log_path, total, failures, timestamp):
        self.segments = segments
        self.drift_map = drift_map
        self.clusters = clustered_segments
        self.output = output
        self.log_path = log_path
        self.total = total
        self.failures = failures
        self.timestamp = timestamp


    def generate_markdown(self):
        md = [f"# failprint Report",
              f"- Timestamp: {self.timestamp}",
              f"- Total Samples: {self.total}",
              f"- Failures: {self.failures} ({(self.failures/self.total)*100:.2f}%)",
              "\n## Contributing Feature Segments"]

        for feat, vals in self.segments.items():
            md.append(f"**{feat}**:")
            for val, fail_pct, delta in vals:
                md.append(f"- `{val}` → {fail_pct*100:.1f}% in failures (Δ +{delta*100:.1f}%)")
        return "\n".join(md)

    def write(self):
        markdown = self.generate_markdown()
        os.makedirs("reports", exist_ok=True)
        with open("reports/failprint_report.md", "w", encoding="utf-8") as f:
            f.write(markdown + "\n\n")
        if self.log_path:
            log_parent = os.path.dirname(self.log_path)
            if log_parent:
                os.makedirs(log_parent, exist_ok=True)
            with open(self.log_path, "a", encoding="utf-8") as log:
                log.write(f"[{self.timestamp}] Failures: {self.failures}/{self.total}\n")
        return markdown
