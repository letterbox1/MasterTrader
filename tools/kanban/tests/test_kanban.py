"""End-to-end tests for tools/kanban/kanban.py, run against a throwaway repo (KANBAN_ROOT)."""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
TOOL = REPO / "tools" / "kanban" / "kanban.py"


class KanbanCase(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix="kanban-test-"))
        shutil.copytree(REPO / "tracking" / "templates", self.tmp / "tracking" / "templates")
        (self.tmp / "docs" / "roadmap").mkdir(parents=True)
        for n in range(9):
            (self.tmp / "docs" / "roadmap" / f"phase-{n}-x.md").write_text(
                f"# Phase {n} · Test phase {n}\n\n| R{n}.01 | req |\n- [ ] **T{n}.01** `BUILD` do it → R{n}.01\n- [ ] **T{n}.02** `USER` you do it → R{n}.01\n")
        (self.tmp / "docs" / "roadmap" / "README.md").write_text(
            "# Roadmap\n<!-- kanban:phase-status:start -->\nold\n<!-- kanban:phase-status:end -->\n"
            "<!-- kanban:roadmap-counts:start -->\n<!-- kanban:roadmap-counts:end -->\n"
            "<!-- kanban:user-register:start -->\n<!-- kanban:user-register:end -->\n")
        subprocess.run(["git", "init", "-q"], cwd=self.tmp, check=True)
        self.phase(0, opens_after="[]")
        self.phase(1, opens_after="[0]")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    # -- helpers
    def k(self, *args, ok=True, stdin=None):
        env = dict(os.environ, KANBAN_ROOT=str(self.tmp), CLAUDE_CODE_SESSION_ID="test-session")
        r = subprocess.run([sys.executable, str(TOOL), *args], cwd=self.tmp, env=env, capture_output=True, text=True, input=stdin)
        if ok and r.returncode:
            self.fail(f"kanban {' '.join(args)} failed:\n{r.stdout}\n{r.stderr}")
        return r

    def phase(self, n, opens_after="[]"):
        d = self.tmp / "tracking" / f"phase-{n}"
        (d / "tasks").mkdir(parents=True, exist_ok=True)
        (d / "bugs").mkdir(exist_ok=True)
        tpl = (self.tmp / "tracking" / "templates" / "phase.md").read_text()
        tpl = tpl.replace("phase: 0", f"phase: {n}").replace("opens_after: []", f"opens_after: {opens_after}")
        (d / "PHASE.md").write_text(tpl)

    def new(self, phase, title, *extra):
        out = self.k("new", "--phase", str(phase), "--title", title, *extra).stdout.strip().splitlines()[0]
        return self.tmp / out

    def meta(self, path):
        text = Path(path).read_text()
        fm = text.split("\n---", 1)[0]
        return {l.split(":", 1)[0].strip(): l.split(":", 1)[1].strip() for l in fm.splitlines()[1:] if ":" in l}

    def tick_all(self, path):
        p = Path(path)
        p.write_text(p.read_text().replace("- [ ]", "- [x]"))

    def item_id(self, path):
        return self.meta(path)["id"]

    # -- tests
    def test_new_item_validates_and_becomes_ready_in_open_phase(self):
        p = self.new(0, "Set up the stack")
        self.assertEqual(self.item_id(p), "P0-T001")
        self.k("validate")
        self.k("build")
        self.assertEqual(self.meta(p)["status"], "ready")

    def test_locked_phase_keeps_items_in_backlog_until_prerequisite_phase_done(self):
        p0 = self.new(0, "Only task of phase 0")
        p1 = self.new(1, "Phase 1 task")
        self.k("build")
        self.assertEqual(self.meta(p1)["status"], "backlog")
        # finish phase 0: task done + exit criteria ticked
        self.k("start", "P0-T001")
        self.tick_all(p0)
        self.k("done", "P0-T001", "--evidence", "unit tests passed")
        phase_file = self.tmp / "tracking" / "phase-0" / "PHASE.md"
        self.k("build")
        self.assertNotEqual(self.meta(phase_file)["status"], "done", "exit criteria not ticked yet")
        self.tick_all(phase_file)
        self.k("build")
        self.assertEqual(self.meta(phase_file)["status"], "done")
        self.assertEqual(self.meta(phase_file)["doc_sync_status"], "pending")
        self.k("build")  # second pass opens phase 1
        self.assertEqual(self.meta(p1)["status"], "ready")

    def test_dependencies_gate_ready(self):
        a = self.new(0, "First")
        b = self.new(0, "Second", "--depends", "P0-T001")
        self.k("build")
        self.assertEqual(self.meta(a)["status"], "ready")
        self.assertEqual(self.meta(b)["status"], "backlog")
        self.k("start", "P0-T002", ok=False)  # refuses: waits on P0-T001
        self.k("start", "P0-T001")
        self.tick_all(a)
        self.k("done", "P0-T001", "--evidence", "ok")
        self.assertEqual(self.meta(b)["status"], "ready")

    def test_done_gate_requires_ticks_and_evidence(self):
        p = self.new(0, "Gated")
        self.k("start", "P0-T001")
        r = self.k("done", "P0-T001", "--evidence", "x", ok=False)
        self.assertIn("unticked", r.stdout + r.stderr)
        self.tick_all(p)
        r = self.k("done", "P0-T001", ok=False)
        self.assertIn("evidence", r.stdout + r.stderr)
        self.k("done", "P0-T001", "--evidence", "pytest: 12 passed")
        m = self.meta(p)
        self.assertEqual(m["status"], "done")
        self.assertTrue(m["completed"])
        self.assertIn("verified: pytest: 12 passed", p.read_text())

    def test_doc_sync_queue_and_stop_hook_nudges_once(self):
        p = self.new(0, "Docs change")
        text = p.read_text().replace("doc_sync: []", "doc_sync: [docs/03-build-spec.md]")
        p.write_text(text)
        self.k("start", "P0-T001")
        self.tick_all(p)
        self.k("done", "P0-T001", "--evidence", "ok")
        self.assertEqual(self.meta(p)["doc_sync_status"], "pending")
        self.assertIn("P0-T001", (self.tmp / "tracking" / "DOC_SYNC.md").read_text())
        r1 = self.k("hook", "stop", stdin=json.dumps({"stop_hook_active": False}))
        self.assertEqual(json.loads(r1.stdout)["decision"], "block")
        r2 = self.k("hook", "stop", stdin=json.dumps({"stop_hook_active": False}))
        self.assertEqual(r2.stdout.strip(), "", "nudges only once per item")
        self.k("docsync", "P0-T001", "--done")
        self.assertEqual(self.meta(p)["doc_sync_status"], "done")
        self.assertIn("Nothing pending", (self.tmp / "tracking" / "DOC_SYNC.md").read_text())

    def test_stop_hook_respects_stop_hook_active(self):
        p = self.new(0, "Docs change")
        p.write_text(p.read_text().replace("doc_sync: []", "doc_sync: [SPEC.md]"))
        self.k("start", "P0-T001")
        self.tick_all(p)
        self.k("done", "P0-T001", "--evidence", "ok")
        r = self.k("hook", "stop", stdin=json.dumps({"stop_hook_active": True}))
        self.assertEqual(r.stdout.strip(), "")

    def test_open_s2_bug_blocks_phase_completion(self):
        t = self.new(0, "Task")
        self.k("new", "--phase", "0", "--kind", "bug", "--severity", "S2", "--title", "Broken thing")
        self.k("start", "P0-T001")
        self.tick_all(t)
        self.k("done", "P0-T001", "--evidence", "ok")
        phase_file = self.tmp / "tracking" / "phase-0" / "PHASE.md"
        self.tick_all(phase_file)
        self.k("build")
        self.assertNotEqual(self.meta(phase_file)["status"], "done")
        self.k("cancel", "P0-B001", "--reason", "duplicate")
        self.assertEqual(self.meta(phase_file)["status"], "done")

    def test_validate_catches_schema_errors(self):
        a = self.new(0, "A")
        b = self.new(0, "B", "--depends", "P0-T001")
        a.write_text(a.read_text().replace("depends_on: []", "depends_on: [P0-T002]"))  # cycle
        b.write_text(b.read_text().replace("status: backlog", "status: wip").replace("## Exceptions & edge cases", "## Exceptions"))
        dup = a.parent / "P0-T001-dup.md"
        dup.write_text(a.read_text())
        r = self.k("validate", ok=False)
        out = r.stdout
        self.assertIn("duplicate id", out)
        self.assertIn("cycle", out)
        self.assertIn("status='wip'", out)
        self.assertIn("missing heading", out)

    def test_checkpoint_resume_and_session_log(self):
        self.new(0, "Resumable")
        self.k("start", "P0-T001")
        self.k("checkpoint", "P0-T001", "schemas done, next: grants")
        r = self.k("resume")
        self.assertIn("schemas done, next: grants", r.stdout)
        r = self.k("hook", "session-start", stdin="{}")
        self.assertIn("resume brief", r.stdout)
        self.assertIn("session-start", (self.tmp / "tracking" / "SESSIONS.md").read_text())

    def test_session_start_installs_git_hooks_in_fresh_clone(self):
        self.new(0, "X")
        get = lambda: subprocess.run(["git", "config", "--get", "core.hooksPath"], cwd=self.tmp, capture_output=True, text=True).stdout.strip()
        self.assertEqual(get(), "")
        self.k("hook", "session-start", stdin="{}")
        self.assertEqual(get(), "tools/kanban/githooks")

    def test_pause_stops_cli_triage_but_build_forces(self):
        self.k("pause")
        p = self.new(0, "Pausable")
        self.assertEqual(self.meta(p)["status"], "backlog", "no triage while paused")
        self.k("build")
        self.assertEqual(self.meta(p)["status"], "ready", "explicit build still triages")

    def test_pause_silences_hooks(self):
        self.new(0, "X")
        self.k("pause")
        r = self.k("hook", "session-start", stdin="{}")
        self.assertEqual(r.stdout.strip(), "")
        self.k("pause", "--off")
        r = self.k("hook", "session-start", stdin="{}")
        self.assertIn("resume brief", r.stdout)

    def test_progress_bar_and_html_payload(self):
        p = self.new(0, "Half way")
        self.new(0, "Not started")
        self.k("start", "P0-T001")
        body = p.read_text()
        p.write_text(body.replace("- [ ] Step 1 …", "- [x] Step 1 …", 1))
        self.k("build")
        html = (self.tmp / "kanban.html").read_text()
        data = json.loads(re.search(r"const DATA = (\{.*?\});\n", html, re.S).group(1))
        ph0 = data["phases"][0]
        # 2 equal-size tasks; one in progress with 1/3 ToDo ticked → credit 0.1 + 0.7/3 ≈ 0.333 → 16.7%
        self.assertAlmostEqual(ph0["progress"]["pct"], 100 * (0.1 + 0.7 / 3) / 2, places=1)
        self.assertEqual(len(data["items"]), 2)
        board = (self.tmp / "tracking" / "phase-0" / "BOARD.md").read_text()
        self.assertIn("▒", board)
        root = (self.tmp / "KANBAN.md").read_text()
        self.assertIn("P0", root)
        roadmap = (self.tmp / "docs" / "roadmap" / "README.md").read_text()
        self.assertNotIn("\nold\n", roadmap)
        self.assertIn("| T0.02 | P0 | you do it |", roadmap)

    def test_build_is_idempotent(self):
        self.new(0, "Stable")
        self.k("build")
        before = (self.tmp / "KANBAN.md").read_text()
        r = self.k("build")
        self.assertIn("up to date", r.stdout)
        self.assertEqual(re.sub(r"_Updated.*_", "", before), re.sub(r"_Updated.*_", "", (self.tmp / "KANBAN.md").read_text()))


if __name__ == "__main__":
    unittest.main()
