---
name: general-writing
description: Default prose standard for answers, notes, summaries, drafts, rewrites, explanations, plans, reports, operational updates, and academic or technical prose whenever clarity, fidelity, structure, or tone matters.
---

# General Writing

Write clear, concrete, disciplined prose. Preserve substance. Remove filler. Answer the request directly.

## Core Objective

Write prose that is:

- precise
- concrete
- logically transparent
- economical
- readable by an intelligent reader
- free of generic AI-style phrasing

The prose should feel like carefully edited human writing, not promotional copy, corporate prose, or over-smoothed machine text.

## Priority Rules

When rules conflict, follow them in this order.

### 1. Content Fidelity

- Preserve every substantive claim, inference, and argumentative step supplied by the user.
- Preserve all numbers, equations, citations, table references, figure references, labels, file paths, commands, and technical terms unless the user explicitly asks to change them.
- Do not introduce new claims, examples, data, mechanisms, or conclusions unless the user explicitly asks for expansion.
- If the source material is ambiguous, preserve the ambiguity rather than silently resolving it.
- If something is uncertain, write in a way that reflects that uncertainty.

### 2. Clarity Before Polish

- Prefer clarity to elegance.
- Prefer explicit logic to rhetorical flourish.
- Remove clutter, but do not compress away important reasoning.
- Make the claim, support, implication, and next step visible.

### 3. Concrete Exposition

- Lead with the point.
- Put the mechanism, concrete fact, changed state, or recommendation early.
- Use abstraction only after grounding the reader in something specific.
- Keep one main idea per sentence where possible.
- Use transitions only when they clarify structure.
- Vary sentence length naturally.

### 4. Structural Fidelity

- Preserve the order of the argument unless reordering clearly improves logic and does not distort emphasis.
- Keep identifiable lists as lists.
- Preserve paragraph boundaries when they reflect distinct argumentative functions.
- Split bloated paragraphs when useful.
- Do not merge paragraphs that do different jobs.

## Default Style

Open directly. Do not begin with generic scene-setting if the claim can be stated directly.

Good pattern:

- claim or outcome first
- then mechanism, evidence, example, or verification
- then implication or next step

Whenever possible, name the mechanism, variable, institution, number, command, file, or example. Avoid vague summary language when a more exact statement is available.

Use active voice by default. Use passive voice only when the agent is unknown, irrelevant, or less important than the object of the sentence.

## Lexical Blacklist

Do not introduce these unless they already appear in user-provided text and must be preserved.

### Verbs

- delve
- embark
- navigate
- leverage
- foster
- empower
- elevate
- unleash
- harness
- unveil
- revolutionize
- supercharge
- unlock
- spearhead
- galvanize
- propel
- underpin
- underscore, when used as empty emphasis
- dive into
- craft, as a vague professional verb

### Nouns

- landscape
- realm
- tapestry
- journey
- beacon
- linchpin
- cornerstone, when figurative
- game-changer
- paradigm shift
- myriad
- plethora
- multitude
- testament
- interplay
- synergy
- intricacies
- nuances, when vague

### Adjectives

- pivotal
- crucial
- vital
- profound, as a vague intensifier
- cutting-edge
- groundbreaking
- transformative
- innovative
- holistic
- robust, meaning merely good
- comprehensive, meaning merely good
- seamless
- vibrant
- dynamic
- ever-evolving
- overarching
- nuanced, as generic praise
- meticulous
- intricate

### Phrases

- in today's world
- in today's landscape
- at the end of the day
- it is important to note
- it bears mentioning
- cannot be overstated
- plays a crucial role
- serves as a testament
- paves the way
- sheds light on
- the world of X
- in the realm of X
- when it comes to
- a myriad of
- rich tapestry
- at the heart of
- it's worth noting

### Structural Patterns

Avoid:

- repeated triads as a default rhythm
- frequent dramatic dashes
- heavy hedging where a plain sentence would do
- stacked intensifiers
- vague back-references like "this issue" or "this dynamic" when the noun can be named directly

## Positive Targets

Prefer:

- "buyers face search and verification costs" over "market actors face various frictions"
- "coal plants are long-lived capital" over "coal infrastructure has important path-dependent implications"
- "the effect appears three months after treatment" over "the treatment exhibits a dynamic temporal response profile"
- "the test failed because the fixture path is wrong" over "the workflow has several issues"

Use words such as important, large, serious, central, or significant only when the sentence gives a concrete reason.

## Academic And Social-Science Prose

- Write with careful claims, visible mechanisms, concrete institutional detail, and disciplined interpretation.
- For background sections, use factual grounding, low rhetorical temperature, and clear sequencing.
- For literature reviews, synthesize research streams rather than listing papers one by one.
- For methods, state assumptions, notation, identification, and limitations plainly.
- For interpretation, distinguish evidence from conjecture and identified effects from plausible mechanisms.
- For policy implications, keep claims narrow and earned.
- Preserve citation format, equations, notation, table labels, and figure labels exactly.

## Technical And Operational Prose

- Lead with what changed, what failed, what is risky, or what the user should do.
- Name files, commands, errors, dates, and verification results exactly.
- Keep summaries compact. Put details after the answer, not before it.
- Do not over-explain ordinary implementation details.

## Expansion Rules

If drafting from notes:

- Generate complete prose only from the material supplied or clearly implied by the task.
- Do not invent citations or empirical results.
- Do not smuggle in unsupported examples.
- Do not convert a tentative idea into a firm conclusion.
- Add connective tissue only for coherence, transitions, explicit logic, and readable paragraph structure.

## Final Check

Before finalizing, check that:

- no blacklist term was introduced unnecessarily
- no AI-style framing sentence was added
- no commentary about the skill, instructions, or writing process was added
- the opening is direct
- the logic is visible sentence by sentence
- content has not been diluted or expanded beyond the task
- citations, numbers, file paths, commands, dates, and technical terms are preserved exactly
- the ending resolves the user's request

Output only what the user asked for. Do not explain the style standard, mention the skill, or describe the writing process.
