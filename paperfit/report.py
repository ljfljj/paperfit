# -*- coding: utf-8 -*-
"""把体检结果渲染成 HTML 报告。"""
import html

TPL = """<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>PaperFit 格式体检报告 - {file}</title>
<style>
*{{box-sizing:border-box}}
body{{margin:0;font-family:-apple-system,"Segoe UI","Microsoft YaHei",sans-serif;background:#f5f6f8;color:#1f2329}}
.wrap{{max-width:920px;margin:0 auto;padding:32px 20px 60px}}
.head{{display:flex;align-items:center;gap:14px;margin-bottom:8px}}
.logo{{width:44px;height:44px;border-radius:12px;background:linear-gradient(135deg,#4f7cff,#22d3ee);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;font-size:18px}}
h1{{font-size:22px;margin:0}}
.sub{{color:#8a9099;font-size:13px;margin:4px 0 0 58px}}
.cards{{display:flex;gap:14px;margin:22px 0 26px}}
.card{{flex:1;background:#fff;border-radius:14px;padding:18px;box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.card .n{{font-size:30px;font-weight:700}}
.card .l{{color:#8a9099;font-size:12px;margin-top:2px}}
.good{{color:#12b76a}}.bad{{color:#f04438}}.mid{{color:#f79009}}
.sec{{background:#fff;border-radius:14px;padding:20px;margin-bottom:16px;box-shadow:0 1px 3px rgba(0,0,0,.06)}}
.sec h2{{font-size:15px;margin:0 0 14px;display:flex;align-items:center;gap:8px}}
.tag{{font-size:12px;padding:2px 8px;border-radius:20px;background:#eef2ff;color:#4f46e5}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{text-align:left;padding:9px 10px;border-bottom:1px solid #eef0f3}}
th{{color:#8a9099;font-weight:500;font-size:12px}}
.ok{{color:#12b76a}}.err{{color:#f04438}}
.pill{{display:inline-block;font-size:11px;padding:1px 7px;border-radius:10px}}
.pill.err{{background:#fef3f2;color:#f04438}}
.pill.ok{{background:#ecfdf3;color:#12b76a}}
.foot{{text-align:center;color:#b0b5bd;font-size:12px;margin-top:28px}}
</style></head><body><div class="wrap">
<div class="head"><div class="logo">PF</div>
<div><h1>论文格式体检报告</h1><div class="sub">{file} · 规则：{rules}</div></div></div>
<div class="cards">
  <div class="card"><div class="n {sc_cls}">{score}<span style="font-size:14px">分</span></div><div class="l">格式合规度</div></div>
  <div class="card"><div class="n bad">{n_issue}</div><div class="l">待修复问题</div></div>
  <div class="card"><div class="n good">{n_pass}</div><div class="l">已通过检查项</div></div>
  <div class="card"><div class="n">{n_para}</div><div class="l">扫描段落数</div></div>
</div>
<div class="sec"><h2>问题清单 <span class="tag">按严重程度排序</span></h2>
{issues_html}
</div>
<div class="sec"><h2>已通过的项目</h2>
<p>{passed_html}</p></div>
<div class="foot">PaperFit · 论文格式体检官 · 由规则引擎驱动，结果可复现</div>
</div></body></html>"""

def render(result, out_path):
    issues = result["issues"]
    rows = []
    for i, it in enumerate(issues, 1):
        rows.append(
            f"<tr><td>{i}</td><td><b>{html.escape(it['role'])}</b></td>"
            f"<td class='ok'>{html.escape(it['expect'])}</td>"
            f"<td class='err'>{html.escape(it['actual'])}</td>"
            f"<td>{html.escape(it['where'])}</td></tr>")
    issues_html = ("<table><tr><th>#</th><th>检查项</th><th>要求</th><th>实际问题</th><th>位置</th></tr>"
                   + "".join(rows) + "</table>") if rows else "<p class='ok'>🎉 没有发现问题，格式完全合规！</p>"
    passed_html = "　".join(f"<span class='pill ok'>✓ {html.escape(p)}</span>" for p in result["passed"]) or "<span class='mid'>暂无</span>"
    score = result["score"]
    sc_cls = "good" if score >= 90 else ("mid" if score >= 60 else "bad")
    doc = TPL.format(file=html.escape(result["file"]), rules=html.escape(result["rules"]),
                     score=score, sc_cls=sc_cls, n_issue=len(issues), n_pass=len(result["passed"]),
                     n_para=result["paragraphs"], issues_html=issues_html, passed_html=passed_html)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(doc)
    return out_path
