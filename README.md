# PaperFit · 论文格式体检官

> 上传 Word 论文，自动对照模板逐条体检格式，输出评分、问题定位与整改清单。

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

## 解决的问题

写课程论文 / 大作业 / 期刊投稿时，最烦的不是内容写不出来，而是**格式被模板卡住**：

- 题目要三号黑体，我写成了宋体小四
- 一级标题要仿宋四号，我用了黑体
- 正文首行缩进 2 字符，我忘了缩进
- 参考文献要 10 篇、近 5 年占一半

这些规则写起来枯燥、查起来更枯燥，而且**人的肉眼很难判断字号到底是 10.5 磅还是 11 磅**。

PaperFit 把这些规则变成可执行的检查项，一次扫描给出：

```
✓ 得分（0-100）
✓ 问题清单（要求 vs 实际 vs 定位到第几段）
✓ 已通过项
✓ 段落级扫描统计
```

## 快速开始

```bash
pip install python-docx

# CLI：检查一篇论文
python app.py samples/thesis-bad.docx

# 输出 report.html，浏览器打开即可查看报告
```

实测输出：

```
========================================================
  文件：thesis-bad.docx
  规则：高校课程大作业通用模板
  评分：32 / 100
  通过：6 项    问题：13 处
========================================================
  1. [中文摘要] 要求 10.5pt → 实际 11.0pt  @ 第4段: 摘要：针对机械加工过程中...
  2. [一级标题] 要求 仿宋_GB2312、14.0pt → 实际 宋体、12.0pt  @ 第6段: 1  引言
  ...
```

同一份文件在**合规版本**上得分为 **100 / 100**，说明规则判定是收敛的、可复现的。

## Web 版

```bash
python serve.py
# 浏览器打开 http://127.0.0.1:8000
```

拖入 `.docx` → 点「开始体检」→ 直接看到 HTML 报告。

## 规则可配置

规则全部外置在 `rules/dazuoye.json`，换一套模板只改 JSON，不用改代码：

```json
{
  "name": "高校课程大作业通用模板",
  "roles": {
    "title":  { "cn_font": "黑体", "size_pt": 16.0, "bold": true, "align": "center" },
    "h1":     { "cn_font": "仿宋_GB2312", "size_pt": 14.0 },
    "body":   { "cn_font": "宋体", "size_pt": 10.5, "indent_chars": 2 },
    "ref":    { "cn_font": "宋体", "size_pt": 10.5 }
  },
  "reference": { "min_count": 10, "recent_years": 5, "recent_ratio": 0.5 }
}
```

## 工作原理

```
.docx ──python-docx──► 段落 XML ──► 角色识别 ──► 逐条比对规则 ──► 评分 + 问题定位 ──► HTML 报告
                                    (题名/作者/单位/
                                     摘要/关键词/标题/
                                     正文/参考文献)
```

核心在 `paperfit/checker.py`：
- **角色识别**：按位置与文本特征给每段打标签（第一个非空段 = 题名，`1  引言` = 一级标题，`[1]` = 参考文献……）
- **格式比对**：直接读 `w:rPr` 里的 `w:eastAsia`（中文字体）、`w:sz`（字号）、`w:b`（加粗）、`w:jc`（对齐）、`w:ind`（缩进）
- **评分**：通过项 /（通过项 + 问题项）

## 为什么用 python-docx 而不是 AI 直接判

格式合规是**确定性判断**：10.5pt 就是 10.5pt，不该靠概率模型猜。
所以 PaperFit 用规则引擎保证**可复现、可解释、零幻觉**——这也是它能做到"同一文件每次得分一致"的原因。

## 目录结构

```
paperfit/
├── app.py               CLI 入口
├── serve.py             Web 入口（标准库 http.server，零额外依赖）
├── paperfit/
│   ├── checker.py       规则引擎核心
│   └── report.py        HTML 报告渲染
├── rules/
│   └── dazuoye.json     模板规则（可替换）
├── samples/
│   ├── thesis-ok.docx   合规样例（100 分）
│   ├── thesis-bad.docx  问题样例（32 分）
│   ├── report-ok.html   报告样例（合规）
│   └── report-bad.html  报告样例（问题）
└── web/
    └── index.html       上传界面
```

## 后续规划

- [ ] **一键修复**：直接把不合规的 run 改成模板要求（python-docx 可写）
- [ ] **模板导入**：读取 `.doc` 模板本身，自动反推规则
- [ ] **批量检查**：整个文件夹一次扫完，输出 Excel 汇总
- [ ] **LLM 增强**：对规则无法覆盖的项（如"表述是否学术化"）给出建议

## License

MIT
