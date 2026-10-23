---
name: tcx-persona
description: "Choose an investor persona, adapt it to the user's trading method, or improve a personal persona from selected trade reviews. Use for investor-style templates, personal trading principles, strengths and weaknesses, or review-driven persona learning. Reuse Brain, Strategy, and Decision Memory ownership; never change the specialist roster."
---

# TCX Persona

Help the user develop a personal investment approach while the existing Head
Manager and nine specialists keep their roles. A persona is an Investment
Brain overlay, not a new employee, model, specialist, or permission.

## Choose and personalize

1. Read [catalog.md](references/catalog.md) to offer the 13 bundled lenses.
   Load only the chosen [persona reference](references/personas/).
   Names mean inspired perspectives, not identity or endorsement.
2. Identify the user's timeframe, research approach, entry/exit criteria,
   sizing constraints, avoid conditions, and examples of good and bad decisions.
   Use information already supplied; ask only for material missing choices.
   Do not invent the user's trading method or pretend an unfinished draft is
   ready. Clearly mark unknowns.
3. Read the existing `tcx-brain` skill and its bundle contract for source
   authoring. Use a new user-owned `investment-brain-*` id. State the chosen
   lens, abstraction, id, version, publisher, license, destination, and excluded
   private information before writing. Preserve upstream attribution.
4. For an initial source, run the standard-library helper from the workspace:

   ```text
   python .agents/skills/tcx-persona/scripts/create_persona.py --template warren-buffett --id investment-brain-my-quality --name "My Quality Lens" --publisher "Workspace owner" --license MIT
   ```

   Use an available ordinary Python interpreter; do not reopen the denied
   application runtime. If none is available, author the same strict source
   bundle with native file tools using the selected reference and the Brain
   contract. The helper only creates a source under `investment-brains/`;
   it cannot install, activate, overwrite, or call services.
5. Edit `skill/references/method.md` and the source skill to express the
   user's general inquiry priorities, falsifiers, scope, and abstention rules.
   Explicit user adaptations take precedence over the starting lens; explain
   material conflicts and never average incompatible styles. Keep exact
   entry/exit, sizing, stops, and portfolio rules in a separate conversational
   Strategy draft using `tcx-strategy`'s content contract. Without a fresh
   explicit Strategy turn, do not write Strategy files or call its lifecycle
   service. Report the Brain source and conversational rules draft when the
   method needs both, with the exact next `$tcx-strategy` request.
   Personal account details belong in Investor Context. Raw trades and review
   evidence remain in Decision Memory, outside the portable Brain.
6. Validate through proof-free `manage_investment_brain action=validate`.
   Follow `tcx-brain` for versioning, privacy review, and source/lifecycle
   separation. Stop source authoring after validation and a concise change
   summary. For managed install, update, activation, or rollback, return the
   exact next `$tcx-brain` request required by that existing contract.

## Use in analysis

`$tcx-persona`, a template name, or a prior selection does not select a Brain.
A run requires one exact active `$investment-brain-*` invocation. Inspect
installation status before claiming readiness. A Strategy, when needed, must
be selected through its existing contract too. Preserve separate run bindings
for persona/version comparisons. Current evidence can falsify the persona.

Head Manager translates the selected lens into compact research questions for
the existing specialists through `tcx-workflow`. Do not distribute all persona
files to every child or add a persona vote, specialist, or mandatory debate.

## Learn from review

Read [learning.md](references/learning.md) when the user asks to review trades,
learn from mistakes, preserve strengths, or improve a named personal persona.
Use `tcx-memory` for canonical retrieval, review, and lesson handling. Produce
an evidence-linked improvement proposal; when the user requests a concrete
source revision, apply it using `tcx-brain` source rules and validate it.
Learning here means explicit, versioned instructions and evidence-backed
lessons, not model-weight training or an automatically proven trading edge.

Do not silently edit installed Brains, Strategies, roles, risk limits, or
execution settings. A review alone does not authorize managed activation.
Native children inherit MCP credentials: their critique is research-only,
not independent reviewer authentication or authority to promote a lesson.

## Return

Give the personal Brain id/version and source path, template provenance,
customizations and unresolved choices, any separate Strategy draft, validation
result, and exact next step. For a review also give what to preserve, what to
change, contrary evidence, lesson status, and the proposed validation test.
Never claim improved returns or completed learning without evidence.
