"""Generate a static HTML report from pipeline JSON outputs (no external packages required).

Usage:
  python tools/generate_static_report.py --input output/demo --output output/demo/report.html

Default input folder: output/demo
Default output file: output/demo/report.html

The script produces a simple, self-contained HTML file you can open in a browser
without installing Streamlit or Docker.
"""
import os
import sys
import json
from datetime import datetime


def load_records(folder):
    recs = []
    if not os.path.isdir(folder):
        print(f"Input folder not found: {folder}")
        return recs
    for fn in os.listdir(folder):
        if not fn.lower().endswith('.json'):
            continue
        path = os.path.join(folder, fn)
        try:
            with open(path, 'r', encoding='utf-8') as f:
                recs.append(json.load(f))
        except Exception as e:
            print(f"Failed to load {path}: {e}")
    return recs


def escape_html(s):
    return (str(s)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;'))


def render_report(records, out_path):
    now = datetime.utcnow().isoformat() + 'Z'
    rows = []
    details_html = []
    for r in records:
        tid = escape_html(r.get('task_id'))
        scores = r.get('scores', {})
        roi = r.get('roi', {})
        rca = r.get('rca', {})
        owner = r.get('owner', {})
        rec = r.get('recommendation', {})
        overall = scores.get('overall_score')
        roi_pct = roi.get('roi_percent')
        root = rca.get('root_cause')
        owner_name = owner.get('owner')
        rows.append(f"<tr><td><a href='#{tid}'>{tid}</a></td><td>{overall}</td><td>{roi_pct}</td><td>{root}</td><td>{owner_name}</td></tr>")

        # details
        details = f"<h2 id='{tid}'>{tid}</h2>\n"
        details += '<h3>Trace</h3>\n<pre>' + escape_html(json.dumps(r.get('trace', {}), indent=2)) + '</pre>\n'
        details += '<h3>Scores</h3>\n<pre>' + escape_html(json.dumps(scores, indent=2)) + '</pre>\n'
        details += '<h3>ROI</h3>\n<pre>' + escape_html(json.dumps(roi, indent=2)) + '</pre>\n'
        details += '<h3>RCA</h3>\n<pre>' + escape_html(json.dumps(rca, indent=2)) + '</pre>\n'
        details += '<h3>Owner</h3>\n<pre>' + escape_html(json.dumps(owner, indent=2)) + '</pre>\n'
        details += '<h3>Recommendation</h3>\n<pre>' + escape_html(json.dumps(rec, indent=2)) + '</pre>\n'
        details += "<p><a href='#top'>Back to top</a></p>\n"
        details_html.append(details)

    html = f"""<!doctype html>
<html>
<head>
  <meta charset='utf-8'>
  <title>AI Engineering ROI Report</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; }}
    table {{ border-collapse: collapse; width: 100%; margin-bottom: 24px; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
    th {{ background: #f4f4f4; }}
    pre {{ background: #fafafa; padding: 12px; border: 1px solid #eee; overflow: auto; }}
    h1 {{ margin-bottom: 4px; }}
    .meta {{ color: #666; margin-bottom: 16px; }}
  </style>
</head>
<body>
  <a id='top'></a>
  <h1>AI Engineering ROI Report (Demo)</h1>
  <div class='meta'>Generated: {now}</div>
  <h2>Summary</h2>
  <table>
    <thead><tr><th>Task ID</th><th>Overall Score</th><th>ROI %</th><th>Root Cause</th><th>Owner</th></tr></thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
  <hr/>
  {''.join(details_html)}
</body>
</html>
"""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Wrote report: {out_path}")


if __name__ == '__main__':
    inp = 'output/demo'
    out = os.path.join('output', 'demo', 'report.html')
    if len(sys.argv) >= 2:
        inp = sys.argv[1]
    if len(sys.argv) >= 3:
        out = sys.argv[2]
    records = load_records(inp)
    if not records:
        print(f"No records found in {inp}. Run python run_demo.py first.")
        sys.exit(1)
    render_report(records, out)
    # Attempt to open in default browser if possible
    try:
        import webbrowser
        webbrowser.open('file://' + os.path.abspath(out))
    except Exception:
        pass
