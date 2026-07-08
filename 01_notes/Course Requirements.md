---
description: "Course requirements, grading, formatting, and submission details for the ZJU term paper"
created: 2026-06-04
modified: 2026-06-13
group: structure
tags: [project, critical-minerals, coursework, zju, term-paper]
status: active
created_by: opencode
---

# Course Requirements

## Course

**Introduction to China's Foreign Trade and Investment** — Zhejiang University

**Instructors**: Chen Liang (liang.chen@zju.edu.cn), Xie Enze (enzexie@zju.edu.cn)

**Schedule**: Thursday 8:50-12:25, Graduate Education Complex Room 404

## Term Paper Requirements

### Topic

Any topic related to:
- Chinese economy
- China's foreign trade
- FDI
- Your country's economy and foreign trade/FDI

Can also be based on Master Thesis.

### Format

| Element | Specification |
|---------|-------------|
| Paper title | 18pt, bold, centered |
| Level 1 headings | 18pt, bold |
| Level 2 headings | 14pt, bold |
| Level 3 headings | 12pt, bold |
| Abstract | 12pt serif (Times New Roman), non-bold, 300-600 words |
| Body text | 12pt, 1.5 line spacing, first-line indentation |

### Required sections

1. Abstract (300-600 words, 12pt serif, non-bold)
2. Keywords
3. Introduction
4. Body (with Level 1/2/3 headings)
5. Conclusion
6. References

### Length

- **Minimum 5,000 words** total
- **At least 10 references**

### Submission

- **Deadline**: June 25, 2026 (24:00 local time)
- **File naming**: FullName+StudentID
- Must also do a **20-minute PPT presentation** + Q&A
- Send PPT to instructor after presenting
- Include bibliographic references at end of PPT

### Grading

| Component | Weight |
|-----------|--------|
| Attendance | 10% |
| Discussion | 20% |
| Presentation + discussion | 20% |
| **Term paper** | **50%** |

### Textbooks

- Garnaut, Song, and Fang (eds.), *China's 40 Years of Reform and Development 1978-2018*, ANU Press, 2018
- Naughton, *The Chinese Economy: Transitions and Growth*, 2nd ed., MIT Press, 2018

## Course Schedule

| Lecture | Topic | Reading |
|---------|-------|---------|
| 1-2 | 40 years of Chinese economic reform | Ch. 1-3 (Garnaut) |
| 2-3 | China and the global trading system | Ch. 27 |
| 3 | China's foreign trade | Ch. 28 |
| 4 | FDI liberalization and impacts | Ch. 29 (Xie Enze) |
| 5 | OFDI stages | Ch. 30 (Xie Enze) |
| 6 | US perspective on China's external disputes | Ch. 31 |
| 7 | Discussion: Trade, Industrial, FDI Policy | — |
| 8 | Student Presentations | — |

## Our paper's fit

Our topic ("China's Critical-Mineral Export Controls and Foreign Trade
Policy") fits squarely under:
- **China's foreign trade** — export controls are trade policy instruments
- **Chinese economy** — mineral export controls affect industrial policy,
  resource allocation, and downstream supply chains
- Connects to course content on Ch. 27 (global trading system), Ch. 31 (US-China disputes), and Ch. 29-30 (FDI in both directions)

Xie Enze authored Chapters 29 and 30 (FDI), so the conclusion can briefly
mention how mineral controls may encourage outward and inward investment in
alternative mining, refining, and processing capacity. This should remain a
policy implication, not a main empirical claim.

## Current Term-Paper Plan

The active structure is `05_draft/TermPaper_Structure.md`.

The paper should be framed around this question:

> When does China's export licensing for critical minerals become a binding
> trade restriction rather than temporary administrative friction or strategic
> signaling?

The final numerical results should be filled only after:

1. finishing antimony bilateral data through March 2026;
2. extending the established treated and control products through March 2026;
3. rerunning `prepare_comtrade_thesis_panel.py`, `prepare_eurostat_cn8.py`,
   `prepare_geodist.py`, and `analysis_thesis.py`.

Sections 1-5 can be drafted before final results because the institutional
background, research question, theory, data description, and empirical design
are already settled.
