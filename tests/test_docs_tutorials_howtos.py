"""Executable verification tests for grafana-tools CLI, transforms, Docker, and Diátaxis docs."""

from __future__ import annotations

import json
import py_compile
import re
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

try:
    import grafanalib  # noqa: F401
    import requests  # noqa: F401
    import yaml  # noqa: F401

    HAS_RUNTIME_DEPS = True
except ImportError:
    HAS_RUNTIME_DEPS = False

try:
    import yaml as yaml_only
except ImportError:
    yaml_only = None

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import grafana_transforms  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = REPO_ROOT / "docs"

LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)\n]+)\)")
FENCE_RE = re.compile(r"^(?P<indent>[ \t]*)(?P<ticks>`{3,}|~{3,})(?P<info>.*)$")
BOX_CHAR_RE = re.compile(r"[\u2500-\u257f▼▲◄►]")
FRENCH_DOC_MARKERS = re.compile(
    r"\b(?:procédure|tutoriel|démarrage|prérequis|vérification|"
    r"retour\s+arrière|utilisation|générateur|tableaux\s+de\s+bord)\b",
    re.IGNORECASE,
)
STE_BANNED = re.compile(
    r"(?:;|should\b|would\b|may\b|might\b|shall\b|"
    r"\b(?:don't|doesn't|isn't|aren't|won't|can't|let's)\b)",
    re.IGNORECASE,
)


def _iter_markdown() -> list[Path]:
    """Return all repository Markdown files outside .git."""
    return sorted(p for p in REPO_ROOT.rglob("*.md") if ".git/" not in p.as_posix())


def _extract_fenced_blocks(text: str) -> list[dict[str, object]]:
    """Extract fenced code blocks with indentation and language metadata."""
    blocks: list[dict[str, object]] = []
    open_fence: dict[str, object] | None = None
    for idx, line in enumerate(text.splitlines(), start=1):
        match = FENCE_RE.match(line)
        if open_fence is None:
            if match:
                ticks = match.group("ticks")
                open_fence = {
                    "char": ticks[0],
                    "len": len(ticks),
                    "indent": match.group("indent"),
                    "info": match.group("info").strip().lower(),
                    "start_line": idx,
                    "lines": [],
                }
        else:
            if match and match.group("ticks")[0] == open_fence["char"] and len(match.group("ticks")) >= int(open_fence["len"]):
                if not match.group("info").strip():
                    open_fence["code"] = "\n".join(open_fence["lines"])  # type: ignore[arg-type]
                    blocks.append(open_fence)
                    open_fence = None
                    continue
            open_fence["lines"].append(line)  # type: ignore[union-attr]
    if open_fence is not None:
        raise AssertionError(f"Unclosed fenced code block at line {open_fence['start_line']}")
    return blocks


def _strip_code(text: str) -> str:
    """Return Markdown text outside fenced and inline code spans."""
    lines: list[str] = []
    in_fence = False
    fence_char = ""
    fence_len = 0
    for line in text.splitlines():
        match = FENCE_RE.match(line)
        if not in_fence:
            if match:
                in_fence = True
                fence_char = match.group("ticks")[0]
                fence_len = len(match.group("ticks"))
            else:
                lines.append(re.sub(r"`[^`]+`", "", line))
        else:
            if match and match.group("ticks")[0] == fence_char and len(match.group("ticks")) >= fence_len and not match.group("info").strip():
                in_fence = False
    return "\n".join(lines)


def _heading_slugs(text: str) -> set[str]:
    """Build GitHub-style heading anchors from Markdown outside code blocks."""
    slugs: set[str] = set()
    counts: dict[str, int] = {}
    for line in _strip_code(text).splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*$", line)
        if not match:
            continue
        raw = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", match.group(1).strip())
        slug = re.sub(r"[^a-z0-9\- ]+", "", raw.lower()).strip().replace(" ", "-")
        slug = re.sub(r"-{2,}", "-", slug)
        if not slug:
            continue
        seen = counts.get(slug, 0)
        counts[slug] = seen + 1
        slugs.add(slug if seen == 0 else f"{slug}-{seen}")
    return slugs


class _MockGrafanaServer:
    """Ephemeral localhost HTTP server capturing /api/dashboards/db POST payloads."""

    def __init__(self) -> None:
        self.requests_seen: list[dict[str, object]] = []
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self) -> None:  # noqa: N802
                length = int(self.headers.get("Content-Length", "0"))
                body = self.rfile.read(length).decode("utf-8")
                outer.requests_seen.append(
                    {
                        "path": self.path,
                        "auth": self.headers.get("Authorization"),
                        "payload": json.loads(body),
                    }
                )
                resp = json.dumps({"id": 1, "slug": "linux-server-overview", "status": "success", "url": "/d/abc/linux-server-overview"}).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(resp)))
                self.end_headers()
                self.wfile.write(resp)

            def log_message(self, format: str, *args: object) -> None:  # noqa: A002
                return

        self._server = HTTPServer(("127.0.0.1", 0), Handler)
        self.port = self._server.server_port
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)

    def __enter__(self) -> "_MockGrafanaServer":
        self._thread.start()
        return self

    def __exit__(self, *args: object) -> None:
        self._server.shutdown()
        self._server.server_close()


class TestGrafanaToolsDocsAndCli(unittest.TestCase):
    """Validate Diátaxis docs, Mermaid diagrams, Docker/Makefile, transforms, and CLI."""

    def test_diataxis_structure_links_and_ste_rules(self) -> None:
        required_docs = [
            REPO_ROOT / "README.md",
            DOCS_DIR / "index.md",
            DOCS_DIR / "01-tutorials" / "index.md",
            DOCS_DIR / "01-tutorials" / "01-generate-and-export-first-dashboard.md",
            DOCS_DIR / "01-tutorials" / "02-customize-variables-transformations-and-container.md",
            DOCS_DIR / "02-how-to-guides" / "index.md",
            DOCS_DIR / "02-how-to-guides" / "export-and-publish-dashboards.md",
            DOCS_DIR / "02-how-to-guides" / "run-docker-and-extend-panels.md",
            DOCS_DIR / "03-reference" / "index.md",
            DOCS_DIR / "03-reference" / "cli-yaml-schema-and-transformations.md",
            DOCS_DIR / "04-explanation" / "index.md",
            DOCS_DIR / "04-explanation" / "architecture-yaml-pipeline-and-api-design.md",
        ]
        for path in required_docs:
            self.assertTrue(path.is_file(), f"Missing Diátaxis doc: {path}")

        md_files = _iter_markdown()
        self.assertGreaterEqual(len(md_files), 12)
        for md_file in md_files:
            content = md_file.read_text(encoding="utf-8")
            plain = _strip_code(content)
            self.assertNotIn("grafana-training", content, f"Stale cross-repo link in {md_file}")
            self.assertNotIn("ansible/", content, f"Removed non-existent ansible reference in {md_file}")
            self.assertIsNone(FRENCH_DOC_MARKERS.search(plain), f"French marker found in {md_file}")

            for link in LINK_RE.findall(plain):
                if link.startswith(("http://", "https://", "mailto:")):
                    continue
                target_str, _, anchor = link.partition("#")
                target_path = md_file if not target_str else (md_file.parent / target_str).resolve()
                self.assertTrue(target_path.exists(), f"Broken link '{link}' in {md_file}")
                if anchor and target_path.is_file() and target_path.suffix == ".md":
                    slugs = _heading_slugs(target_path.read_text(encoding="utf-8"))
                    self.assertIn(anchor, slugs, f"Broken anchor '#{anchor}' in {md_file} -> {target_path}")

        for howto in sorted((DOCS_DIR / "02-how-to-guides").glob("*.md")):
            plain = _strip_code(howto.read_text(encoding="utf-8"))
            self.assertIsNone(STE_BANNED.search(plain), f"ASD-STE100 banned token in {howto}")

    def test_mermaid_diagrams_and_zero_ascii_art(self) -> None:
        mermaid_total = 0
        for md_file in _iter_markdown():
            content = md_file.read_text(encoding="utf-8")
            for block in _extract_fenced_blocks(content):
                code = str(block["code"])
                info = str(block["info"])
                if info == "mermaid":
                    mermaid_total += 1
                    self.assertEqual(block["indent"], "", f"Indented mermaid fence in {md_file}")
                    first_line = next((ln.strip() for ln in code.splitlines() if ln.strip()), "")
                    self.assertTrue(
                        first_line.startswith(("flowchart ", "graph ", "sequenceDiagram")),
                        f"Unsupported mermaid diagram header '{first_line}' in {md_file}",
                    )
                elif info in {"", "text", "plaintext", "ascii"}:
                    self.assertNotIn("-->", code, f"ASCII flow arrow found in {md_file}")
                    self.assertNotIn("graph ", code, f"Untagged mermaid diagram in {md_file}")
                    self.assertIsNone(BOX_CHAR_RE.search(code), f"Box-drawing art in {md_file}")

        self.assertGreaterEqual(mermaid_total, 4)

    def test_dockerfile_makefile_english_code_and_transforms(self) -> None:
        dockerfile_text = (REPO_ROOT / "Dockerfile").read_text(encoding="utf-8")
        self.assertIn("grafana_helper.py", dockerfile_text)
        self.assertIn("grafana_transforms.py", dockerfile_text)

        helper_text = (REPO_ROOT / "grafana_helper.py").read_text(encoding="utf-8")
        transforms_text = (REPO_ROOT / "grafana_transforms.py").read_text(encoding="utf-8")

        # Keep exact Makefile / CI workflow grep contract for __version__ = "1.0.1".
        version_lines = [ln for ln in helper_text.splitlines() if "__version__" in ln]
        self.assertEqual(version_lines, ['__version__ = "1.0.1"'])

        for name, source_text in [("grafana_helper.py", helper_text), ("grafana_transforms.py", transforms_text)]:
            non_ascii = [ch for ch in source_text if ord(ch) > 127]
            self.assertEqual(non_ascii, [], f"Unexpected non-ASCII characters in {name}: {non_ascii}")

        with tempfile.TemporaryDirectory() as tmpdir:
            py_compile.compile(str(REPO_ROOT / "grafana_helper.py"), cfile=str(Path(tmpdir) / "h.pyc"), doraise=True)
            py_compile.compile(str(REPO_ROOT / "grafana_transforms.py"), cfile=str(Path(tmpdir) / "t.pyc"), doraise=True)

        # Verify all 17 transformation builders and documented reference entries.
        self.assertEqual(len(grafana_transforms.TRANSFORMATIONS_MAP), 17)
        ref_doc = (DOCS_DIR / "03-reference" / "cli-yaml-schema-and-transformations.md").read_text(encoding="utf-8")
        sample_args = {
            "filterByName": {"include": ["Time", "Value"]},
            "filterByValue": {"field": "Value", "operator": "greater", "value": 10},
            "filterByQuery": {"refIds": ["A"]},
            "merge": {},
            "outerJoin": {"field": "instance"},
            "addFieldFromCalculation": {"mode": "binary", "reducer": "sum", "expression": "A + B"},
            "reduce": {"reducer": "mean"},
            "groupBy": {"fields": {"instance": "groupby"}, "aggregations": ["mean"]},
            "organize": {"renameByName": {"Value": "CPU"}},
            "labelsToFields": {"labels": ["instance"]},
            "seriesToRows": {},
            "convertFieldType": {"field": "Time", "targetType": "time"},
            "groupToNestedTable": {"key": "instance"},
            "sortBy": {"field": "Value", "reverse": True},
            "limit": {"limit": 10},
            "extractFields": {"source": "Message", "regex": ".*"},
            "debug": {},
        }
        self.assertEqual(set(sample_args), set(grafana_transforms.TRANSFORMATIONS_MAP))
        for t_name, kwargs in sample_args.items():
            self.assertIn(f"`{t_name}`", ref_doc)
            payload = grafana_transforms.TRANSFORMATIONS_MAP[t_name](**kwargs).to_json_data()
            self.assertIn("id", payload)
            self.assertIn("options", payload)

        if yaml_only is not None:
            examples = sorted((REPO_ROOT / "examples").glob("*.yaml"))
            self.assertEqual(len(examples), 21)
            for ex in examples:
                self.assertIn(ex.name, ref_doc)
                cfg = yaml_only.safe_load(ex.read_text(encoding="utf-8"))
                self.assertIsInstance(cfg, dict, f"Invalid root in {ex}")
                self.assertIn("dashboard", cfg)
                self.assertIn("panels", cfg)
                for panel in cfg["panels"]:
                    self.assertIn(panel["type"], {"timeseries", "stat", "gauge"})
                    self.assertIsInstance(panel["gridPos"], dict)
                    for tr in panel.get("transformations", []):
                        self.assertIn(tr["type"], grafana_transforms.TRANSFORMATIONS_MAP)

    @unittest.skipUnless(HAS_RUNTIME_DEPS, "grafanalib, PyYAML, and requests required")
    def test_cli_examples_export_push_and_error_handling(self) -> None:
        ver = subprocess.run(
            [sys.executable, "grafana_helper.py", "--version"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(ver.returncode, 0, ver.stderr)
        self.assertEqual(ver.stdout.strip(), "grafana_helper.py 1.0.1")

        help_res = subprocess.run(
            [sys.executable, "grafana_helper.py", "--help"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=15,
        )
        self.assertEqual(help_res.returncode, 0, help_res.stderr)
        for flag in ("--file", "--output", "--push", "--version"):
            self.assertIn(flag, help_res.stdout)

        import grafana_helper  # noqa: E402
        from grafanalib._gen import DashboardEncoder  # noqa: E402

        examples = sorted((REPO_ROOT / "examples").glob("*.yaml"))
        self.assertEqual(len(examples), 21)
        for ex in examples:
            cfg = yaml_only.safe_load(ex.read_text(encoding="utf-8"))
            dash = grafana_helper.generate_dashboard(cfg)
            encoded = json.loads(json.dumps(dash.to_json_data(), cls=DashboardEncoder))
            self.assertEqual(encoded["title"], cfg["dashboard"]["title"])
            self.assertGreaterEqual(len(encoded["panels"]), 2)

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp = Path(tmpdir)

            # Tutorial 1 export check
            out_json = tmp / "linux-overview.json"
            res = subprocess.run(
                [sys.executable, "grafana_helper.py", "--file", "examples/linux-overview.yaml", "--output", str(out_json)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(res.returncode, 0, res.stderr)
            exported = json.loads(out_json.read_text(encoding="utf-8"))
            self.assertTrue(exported["overwrite"])
            self.assertEqual(exported["dashboard"]["title"], "Linux Server Overview")
            self.assertEqual(len(exported["dashboard"]["panels"]), 6)
            self.assertEqual([t["id"] for t in exported["dashboard"]["panels"][4]["transformations"]], ["merge", "filterFieldsByName"])

            # Tutorial 2 custom YAML check
            custom_yaml = tmp / "service-health.yaml"
            custom_yaml.write_text(
                "\n".join(
                    [
                        "dashboard:",
                        '  title: "Service Health Lab"',
                        "variables:",
                        '  - name: "job"',
                        '    datasource: "Prometheus"',
                        '    query: "label_values(up, job)"',
                        "panels:",
                        '  - title: "Targets Up"',
                        '    type: "stat"',
                        '    datasource: "Prometheus"',
                        "    gridPos: { h: 4, w: 6, x: 0, y: 0 }",
                        '    targets: [{ expr: "sum(up)" }]',
                        '  - title: "Request Latency"',
                        '    type: "timeseries"',
                        '    datasource: "Prometheus"',
                        "    gridPos: { h: 8, w: 18, x: 6, y: 0 }",
                        '    options: { unit: "seconds" }',
                        '    targets: [{ expr: "up" }]',
                        "    transformations:",
                        '      - type: "sortBy"',
                        '        options: { field: "Value", reverse: true }',
                        '      - type: "limit"',
                        "        options: { limit: 10 }",
                        '  - title: "Memory Usage"',
                        '    type: "gauge"',
                        '    datasource: "Prometheus"',
                        "    gridPos: { h: 6, w: 12, x: 0, y: 8 }",
                        '    options: { unit: "percent" }',
                        '    targets: [{ expr: "up" }]',
                    ]
                ),
                encoding="utf-8",
            )
            custom_out = tmp / "service-health.json"
            res2 = subprocess.run(
                [sys.executable, "grafana_helper.py", "--file", str(custom_yaml), "--output", str(custom_out)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertEqual(res2.returncode, 0, res2.stderr)
            custom_data = json.loads(custom_out.read_text(encoding="utf-8"))["dashboard"]
            self.assertEqual([p["type"] for p in custom_data["panels"]], ["stat", "timeseries", "gauge"])
            self.assertEqual([t["id"] for t in custom_data["panels"][1]["transformations"]], ["sortBy", "limit"])

            # End-to-end --push HTTP check verifying unwrapped dashboard payload
            with _MockGrafanaServer() as srv:
                env = dict(**__import__("os").environ)
                env["GRAFANA_URL"] = f"http://127.0.0.1:{srv.port}"
                env["GRAFANA_API_KEY"] = "test-api-token"
                push_res = subprocess.run(
                    [sys.executable, "grafana_helper.py", "--file", "examples/linux-overview.yaml", "--push"],
                    cwd=REPO_ROOT,
                    env=env,
                    capture_output=True,
                    text=True,
                    timeout=15,
                )
                self.assertEqual(push_res.returncode, 0, push_res.stderr)
                self.assertEqual(len(srv.requests_seen), 1)
                req = srv.requests_seen[0]
                self.assertEqual(req["path"], "/api/dashboards/db")
                self.assertEqual(req["auth"], "Bearer test-api-token")
                payload = req["payload"]
                self.assertIsInstance(payload, dict)
                self.assertEqual(payload["folderId"], 0)
                self.assertTrue(payload["overwrite"])
                self.assertEqual(payload["dashboard"]["title"], "Linux Server Overview")
                self.assertNotIn("dashboard", payload["dashboard"])

            # Boundary error tests
            empty_yaml = tmp / "empty.yaml"
            empty_yaml.write_text("", encoding="utf-8")
            bad_res = subprocess.run(
                [sys.executable, "grafana_helper.py", "--file", str(empty_yaml)],
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
                timeout=15,
            )
            self.assertNotEqual(bad_res.returncode, 0)
            self.assertIn("Dashboard YAML root must be a mapping", bad_res.stderr)


if __name__ == "__main__":
    unittest.main()
