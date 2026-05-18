from datetime import UTC, datetime
from pathlib import Path

from subdominator.core.models import EnumerationSummary


class ReportGenerator:
    # ------------------------------------------------------------------ HTML --

    @staticmethod
    def to_html(target_file: Path, summary: EnumerationSummary) -> None:
        try:
            from jinja2 import Template
        except ImportError:
            raise ImportError(
                "HTML report dependencies are missing. "
                "Install them with: pip install subdominator[reports]"
            )

        # Build provider → count map for the breakdown section
        provider_counts: dict[str, int] = {}
        for f in summary.findings:
            provider_counts[f.resource] = provider_counts.get(f.resource, 0) + 1
        provider_rows = sorted(provider_counts.items(), key=lambda x: -x[1])

        started_str = (
            summary.started_at.strftime("%Y-%m-%d %H:%M:%S UTC")
            if summary.started_at
            else "N/A"
        )
        generated_str = datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC")
        duration_s = round(summary.duration_ms / 1000, 2) if summary.duration_ms else 0

        html_template = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Subdominator Report — {{ summary.root_domain }}</title>
    <style>
        :root {
            --bg:       #0d1117;
            --surface:  #161b22;
            --surface2: #1c2128;
            --primary:  #58a6ff;
            --success:  #3fb950;
            --warn:     #d29922;
            --text:     #c9d1d9;
            --text-dim: #8b949e;
            --border:   #30363d;
        }
        * { box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
                         Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.6;
            margin: 0;
            padding: 2rem;
        }
        .container { max-width: 1060px; margin: 0 auto; }
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 10px;
            padding: 1.5rem 2rem;
            margin-bottom: 1.5rem;
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            border-bottom: 2px solid var(--primary);
            padding-bottom: 1rem;
            margin-bottom: 2rem;
        }
        h1 { color: var(--primary); margin: 0 0 0.25rem; font-size: 1.7rem; }
        h2 { color: var(--primary); margin: 0 0 1rem; font-size: 1.2rem;
             border-bottom: 1px solid var(--border); padding-bottom: 0.4rem; }
        .meta { color: var(--text-dim); font-size: 0.85rem; margin: 0; }
        .badge {
            display: inline-block;
            padding: 0.2rem 0.65rem;
            border-radius: 20px;
            background: var(--surface2);
            border: 1px solid var(--border);
            font-size: 0.75rem;
            color: var(--primary);
            font-weight: 600;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 1rem;
        }
        .stat-item {
            text-align: center;
            padding: 1rem;
            background: var(--surface2);
            border-radius: 8px;
            border: 1px solid var(--border);
        }
        .stat-value { font-size: 1.6rem; font-weight: 700; color: var(--success); }
        .stat-label { font-size: 0.75rem; color: var(--text-dim);
                      text-transform: uppercase; letter-spacing: 0.05em; }
        table { width: 100%; border-collapse: collapse; margin-top: 0.5rem; }
        th, td { text-align: left; padding: 0.65rem 0.85rem;
                 border-bottom: 1px solid var(--border); font-size: 0.9rem; }
        th { background: var(--surface2); color: var(--primary);
             font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.04em; }
        tr:hover { background: rgba(88,166,255,0.04); }
        .tag {
            display: inline-block;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            background: var(--surface2);
            font-size: 0.8rem;
            border: 1px solid var(--border);
            color: var(--primary);
        }
        .bar-row { display: flex; align-items: center; gap: 0.6rem; margin: 0.4rem 0; }
        .bar-label { width: 160px; font-size: 0.85rem; white-space: nowrap;
                     overflow: hidden; text-overflow: ellipsis; color: var(--text); }
        .bar-track { flex: 1; background: var(--surface2); border-radius: 4px;
                     height: 10px; }
        .bar-fill { height: 100%; border-radius: 4px; background: var(--primary); }
        .bar-count { font-size: 0.8rem; color: var(--text-dim); min-width: 30px;
                     text-align: right; }
        .footer {
            text-align: center;
            margin-top: 3rem;
            color: var(--text-dim);
            font-size: 0.82rem;
        }
    </style>
</head>
<body>
<div class="container">
    <!-- ── Header ─────────────────────────────────────────────────────── -->
    <div class="header">
        <div>
            <h1>Subdominator Recon Report</h1>
            <p class="meta">Target: <strong style="color:var(--text)">{{ summary.root_domain }}</strong>
               &nbsp;·&nbsp; Generated: {{ generated_str }}</p>
        </div>
        <div><span class="badge">v3.0.0</span></div>
    </div>

    <!-- ── Executive Summary ──────────────────────────────────────────── -->
    <div class="card">
        <h2>Executive Summary</h2>
        <div class="stats-grid">
            <div class="stat-item">
                <div class="stat-value">{{ summary.total_unique_findings }}</div>
                <div class="stat-label">Unique Subdomains</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{ summary.targets_scanned | length }}</div>
                <div class="stat-label">Targets Scanned</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{ duration_s }}s</div>
                <div class="stat-label">Scan Duration</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">{{ provider_rows | length }}</div>
                <div class="stat-label">Active Providers</div>
            </div>
        </div>
    </div>

    <!-- ── Scan Metadata ──────────────────────────────────────────────── -->
    <div class="card">
        <h2>Scan Metadata</h2>
        <table>
            <tr><th>Property</th><th>Value</th></tr>
            <tr><td>Root Domain</td><td>{{ summary.root_domain }}</td></tr>
            <tr><td>Started At</td><td>{{ started_str }}</td></tr>
            <tr><td>Recursive Depth</td><td>{{ summary.recursive_depth }}</td></tr>
            <tr><td>Fresh Findings</td><td>{{ summary.fresh_findings_count }}</td></tr>
            <tr><td>Historical Findings</td><td>{{ summary.historical_findings_count }}</td></tr>
            <tr><td>New Since Last Scan</td><td>{{ summary.new_findings_count }}</td></tr>
            <tr><td>Total Providers Run</td><td>{{ summary.total_resource_executions }}</td></tr>
            <tr><td>Successful Providers</td><td>{{ summary.successful_resource_executions }}</td></tr>
            <tr><td>Failed Providers</td><td>{{ summary.failed_resource_executions }}</td></tr>
        </table>
    </div>

    <!-- ── Provider Breakdown ─────────────────────────────────────────── -->
    {% if provider_rows %}
    <div class="card">
        <h2>Provider Breakdown</h2>
        {% set max_count = provider_rows[0][1] %}
        {% for name, count in provider_rows %}
        <div class="bar-row">
            <div class="bar-label" title="{{ name }}">{{ name }}</div>
            <div class="bar-track">
                <div class="bar-fill"
                     style="width:{{ (count / max_count * 100) | round(1) }}%"></div>
            </div>
            <div class="bar-count">{{ count }}</div>
        </div>
        {% endfor %}
    </div>
    {% endif %}

    <!-- ── Discovery Results ──────────────────────────────────────────── -->
    <div class="card">
        <h2>Discovery Results ({{ summary.findings | length }} subdomains)</h2>
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>Subdomain</th>
                    <th>Source Provider</th>
                    <th>Depth</th>
                </tr>
            </thead>
            <tbody>
                {% for finding in summary.findings %}
                <tr>
                    <td style="color:var(--text-dim)">{{ loop.index }}</td>
                    <td>{{ finding.subdomain }}</td>
                    <td><span class="tag">{{ finding.resource }}</span></td>
                    <td>{{ finding.recursion_depth }}</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>

    <div class="footer">
        Generated with <strong>Subdominator v3.0.0</strong> &bullet;
        <a href="https://github.com/RevoltSecurities/Subdominator"
           style="color:var(--primary);text-decoration:none">RevoltSecurities</a>
    </div>
</div>
</body>
</html>
"""
        template = Template(html_template)
        content = template.render(
            summary=summary,
            provider_rows=provider_rows,
            started_str=started_str,
            generated_str=generated_str,
            duration_s=duration_s,
        )
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content, encoding="utf-8")

