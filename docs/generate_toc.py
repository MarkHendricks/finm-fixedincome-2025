#!/usr/bin/env python3
"""
docs/generate_toc.py

Scans docs/discussions, docs/homework, and docs/exams for .ipynb files,
groups discussion/homework by week, and then adds an Exams section.
Writes docs/_toc.yml accordingly.
"""

import re
from pathlib import Path

def main():
    base = Path("docs")
    discuss_dir = base / "discussions"
    homework_dir = base / "homework"
    exams_dir = base / "exams"
    toc_path = base / "_toc.yml"

    # 1) Collect week-based entries
    weeks = {}
    # discussions: W.X. Title.ipynb
    for nb in sorted(discuss_dir.glob("W.*.ipynb")):
        m = re.match(r"W\.(\d+)\.\s*(.+)$", nb.stem)
        if not m:
            continue
        w = int(m.group(1))
        title = m.group(2)
        weeks.setdefault(w, []).append((f"discussions/{nb.stem}", title))

    # homework: Homework X.ipynb
    for nb in sorted(homework_dir.glob("Homework *.ipynb")):
        m = re.match(r"Homework\s+(\d+)$", nb.stem)
        if not m:
            continue
        w = int(m.group(1))
        weeks.setdefault(w, []).append((f"homework/{nb.stem}", f"Homework {w}"))

    # solutions: Solution X.ipynb
    for nb in sorted(homework_dir.glob("Solution *.ipynb")):
        m = re.match(r"Solution\s+(\d+)$", nb.stem)
        if not m:
            continue
        w = int(m.group(1))
        weeks.setdefault(w, []).append((f"homework/{nb.stem}", f"Solution {w}"))

    # 2) Start building the TOC YAML
    lines = [
        "format: jb-book",
        "root: index",
        "",
        "parts:",
    ]

    # Week parts
    for week in sorted(weeks):
        lines.append(f"  - caption: \"Week {week}\"")
        lines.append("    chapters:")
        for file, title in weeks[week]:
            lines.append(f"      - file: \"{file}\"")
            lines.append(f"        title: \"{title}\"")

    # 3) Exams part
    if exams_dir.exists():
        exam_nbs = sorted(exams_dir.glob("*.ipynb"))
        if exam_nbs:
            lines.append("")
            lines.append("  - caption: \"Exams\"")
            lines.append("    chapters:")
            for nb in exam_nbs:
                stem = nb.stem  # e.g. "Exam - Open" or "Solutions - Exam - Open"
                rel = f"exams/{stem}"
                title = stem.replace(" - ", " – ")
                lines.append(f"      - file: \"{rel}\"")
                lines.append(f"        title: \"{title}\"")

    # 4) Write out
    toc_path.write_text("\n".join(lines) + "\n")
    print(f"[generate_toc] Wrote {toc_path}")

if __name__ == "__main__":
    main()
