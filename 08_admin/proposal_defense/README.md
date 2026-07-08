# ZJU Economics Master Proposal Defense Admin

This folder keeps the official proposal-defense documents, screenshots, and working notes for Mario Diez Martinez's master thesis proposal defense.

## Current Interpretation

The deliverable is a master thesis proposal / opening report (开题报告), not the thesis itself. The proposal must show that the research idea is feasible, has a contribution, and can be defended before the committee.

The 2022 School of Economics requirement says the opening report and literature review are merged into one opening report. In practice, the proposal should contain a substantial literature-review section. A separate literature-review file should only be prepared if Ms Du or the committee explicitly asks for it.

## Official Files

- `official_docs/zju_econ_master_proposal_defense_review_form_2022.doc`
  - M1 opening-report review/audit form.
  - Must be printed double-sided and brought to the defense.
  - Contains the hard requirement: proposal plus literature review should be at least 10,000 Chinese characters/words.
- `official_docs/zju_thesis_review_defense_remuneration_form.doc`
  - Defense remuneration/signature form.
  - Must be filled with student name and committee members.
  - Committee chair goes in the 300 RMB row; other committee members stay at 250 RMB.
- `official_docs/zju_econ_master_proposal_requirements_2022.pdf`
  - School of Economics proposal requirements.
  - Opening report and literature review are merged.
  - Minimum length: at least 10,000.
  - Required content: research question and importance; literature review; structure and content; innovation; references.
- `official_docs/zju_econ_proposal_reference_outline_wyz_2023_06.pdf`
  - Detailed reference outline.
  - Recommends at least 30 references from good journals.
  - Asks for concrete model setup, variable measurement, data sources, and research roadmap.
- `official_docs/zju_econ_master_proposal_format_template_2019.docx`
  - Word formatting template for proposal text.
- `official_docs/zju_econ_master_literature_review_format_template_2019.docx`
  - Word formatting template for literature-review text.
- `zju_thesis_formatting_guidelines.md`
  - Clean project-local Markdown version of the ZJU thesis formatting rules.
  - This is the binding formatting authority for proposal drafting in `05_draft/proposal/main.tex`.

## Screenshots

- `screenshots/wechat_notice_required_documents_red_blue_boxes.png`
  - Red box: bring the review form and remuneration form.
  - Blue box: follow the writing requirements and format templates.
- `screenshots/proposal_defense_student_roster_mario_du_limin.png`
  - Mario's roster row: student number 22501254, major 中国经济, supervisor 杜立民.
- `screenshots/proposal_defense_deadlines_system_submission_notice.png`
  - Defense deadline reminder in the notice: opening defense by April 30 for that term.
  - After completion, student enters information in the graduate system and supervisor reviews.
  - 25级硕士 midterm-progress report reminder: before October 25 according to the notice. Confirm the applicable year if this matters.

## Proposal Content Requirements

All writing and generated LaTeX material should follow `zju_thesis_formatting_guidelines.md`.

Use the stricter interpretation of all available guidance:

1. Title.
2. Research background and research question(s).
3. Literature review and potential contribution.
4. Research method and thesis structure.
5. Regression equations, data, key variables, summary statistics, and possible results.
6. Innovation / contribution relative to prior work.
7. Research plan and time schedule.
8. References.

Minimum target:

- At least 10,000 Chinese characters/words for the merged proposal plus literature review.
- At least 30 references. The WeChat guidance said more than 20 papers, but the detailed School outline says at least 30, so the safer target is 30+.

## Defense Logistics

Before applying / defending:

- Get supervisor approval that the topic is feasible and ready for proposal defense.
- Message Ms Du to apply for defense if ready.
- Make sure the proposal title exactly matches the title entered in the Graduate Education Management New System.
- Ask for the committee member list and chair before filling the remuneration form.

Bring to the defense:

- Printed proposal copies: number should match the number of committee members. Earlier WeChat guidance mentioned 3 copies, but the official notice says to match committee size.
- `M1` proposal defense review form: one double-sided printed copy.
- Remuneration form: one printed copy.
- Slides for a 5-7 minute presentation.
- USB copy of slides if presenting in person.

During / after defense:

- Another student should record the committee questions and answers on the review form; reciprocate if needed.
- The committee chair signs the evaluation opinion.
- Each committee member signs the member table.
- Revise the proposal according to committee comments.
- Supervisor signs the guidance opinion after revision.
- Upload revised opening report PDF and related information to the Graduate Education Management New System:
  - 培养 -> 培养过程 -> 开题报告
- Ask supervisor to approve in the system.
- Submit signed paper materials as required by the current notice / class monitor / Econ 319 graduate office.

## Immediate Next Steps For This Project

1. Draft the proposal in a thesis-proposal format, not as a term-paper rewrite.
2. Use one document source for the proposal. The working project preference is LaTeX `main.tex`, but the final submitted file may need to be exported to Word/PDF formatting if the office requires it.
3. Build the proposal around a stronger theoretical framework:
   - why formally similar Chinese export-licensing controls bind differently across minerals;
   - how licensing credibility, outside options, self-cost, product specificity, and downstream exposure shape trade and price responses.
4. Expand the empirical plan beyond current preliminary results:
   - wave-specific DDD;
   - staggered DiD / event-study diagnostics;
   - product-placebo inference with the larger control pool;
   - domestic-vs-international price wedge analysis;
   - richer treatment/control/product classification.
5. Prepare a proposal figure/table package:
   - product-wave table;
   - data coverage table;
   - identification roadmap;
   - preliminary result table;
   - research schedule.
6. Prepare a 5-7 minute defense slide deck after the written proposal is stable.
