# Figure Render Audit

## Figure Checked

- Figure: Figure 3-1, "Research Design and Interpretation Route"
- Printed page number: 16
- Physical PDF page rendered: 17
- Rendered PNG inspected: `/Users/elgask0/REPOS/critical-minerals/05_draft/proposal/render_audit/figure_3_1_page-17.png`
- Render command: `pdftoppm -png -r 220 -f 17 -l 17 main.pdf render_audit/figure_3_1_page`

## Render Iterations

- Iteration 1: The fixed-grid redesign compiled and was rendered to PNG. Visual inspection showed that the grouped layout worked, but the group titles were still visually heavy and too close to the inner boxes.
- Iteration 2: The group-title style was reduced, and the inner box rows were lowered slightly inside the Foundations, Measurement and Empirical Design, and Interpretation containers. The render was accepted because the layout is symmetrical, the arrows are clean, labels are readable, and the group titles no longer crowd the boxes.

## Final Layout

The final diagram uses the same multidimensional logic as the older route figure while updating the content for the current thesis design. It has a top policy puzzle and research question row, a large nested Foundations group with four same-size inner boxes, a side Exposure and replacement framework box, a large nested Measurement and Empirical Design group with eight same-size inner boxes arranged as a 4 by 2 grid, a side Evidence pattern box, a large nested Interpretation group with four same-size inner boxes, a side Weak cases, nulls, and limits box, and a bottom Contribution box.

## Visual Checks

- No arrows cross other arrows.
- No arrows run through box text.
- Labels are readable in the rendered PNG, including the group titles.
- Group titles sit inside the containers without touching or overlapping the inner boxes.
- All inner boxes are same-size within their group.
- The Measurement and Empirical Design group contains eight boxes.
- The figure uses grouped and nested boxes rather than a flat stacked list.
- The figure contains no equations.
- The figure contains no internal workflow language.
- The caption states that the figure is a guide to the research design, not an additional estimator.
- The final layout resembles the old Figure 3-2 route style more than the previous stacked-band design.

## Remaining Visual Compromises

- The figure uses compact labels to preserve readability; detailed model notation remains in the surrounding text and equations rather than inside the diagram.
- The right-side boxes are slightly smaller than the main group containers, following the old route figure's side-output style.
