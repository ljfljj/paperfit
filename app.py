# -*- coding: utf-8 -*-
"""PaperFit CLI：python app.py 论文.docx [--rules rules/dazuoye.json] [--out report.html]"""
import argparse, json, os, sys
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from paperfit.checker import check
from paperfit.report import render

def main():
    ap = argparse.ArgumentParser(description="PaperFit 论文格式体检官")
    ap.add_argument("docx", help="待检查的 .docx 文件")
    ap.add_argument("--rules", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "rules", "dazuoye.json"))
    ap.add_argument("--out", default="report.html")
    ap.add_argument("--json", default="")
    a = ap.parse_args()

    rules = json.load(io_open(a.rules))
    res = check(a.docx, rules)
    render(res, a.out)

    print("=" * 56)
    print(f"  文件：{res['file']}")
    print(f"  规则：{res['rules']}")
    print(f"  评分：{res['score']} / 100")
    print(f"  通过：{len(res['passed'])} 项    问题：{len(res['issues'])} 处")
    print("=" * 56)
    for i, it in enumerate(res["issues"], 1):
        print(f"  {i}. [{it['role']}] 要求 {it['expect']} → 实际 {it['actual']}  @ {it['where']}")
    if not res["issues"]:
        print("  [OK] 无问题，格式完全合规")
    print(f"\n  报告已生成：{os.path.abspath(a.out)}")
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump(res, f, ensure_ascii=False, indent=2)

def io_open(p):
    import io
    return io.open(p, "r", encoding="utf-8")

if __name__ == "__main__":
    main()
