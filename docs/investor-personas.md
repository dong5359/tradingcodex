# Investor Personas

`tcx-persona` is the Head Manager skill for selecting an investor-inspired
lens, adapting it to a personal trading approach, and proposing improvements
from selected reviews. The nine fixed specialists retain their roles.

## Ownership and native coverage

Native Codex owns template selection, interpretation, source authoring, and
review reasoning. The standard-library scaffold helper only materializes a
new user-owned source. The existing [Brain service](investment-brain-plugins.md)
owns validation, installation, immutable versions, activation, rollback, and
run provenance. [Decision Memory](decision-memory.md) owns review evidence and
lessons. [Strategy](user-facing-skills.md) owns explicit trading decision rules.

No new registry, MCP endpoint, database model, lifecycle marker, scheduler,
debate round, or persona agent is introduced. This avoids duplicating Brain
selection and versioning, Memory records, and specialist routing. Browsing or
scaffolding needs no service call; source validation uses the existing call.
Research adds no mandatory child or tool call. Only one selected lens and its
method are loaded, not all 13 references. Review costs depend on selected
evidence, with no claim of measured latency or return improvement.

## Templates and personal sources

The 13 templates are Aswath Damodaran, Ben Graham, Bill Ackman, Cathie Wood,
Charlie Munger, Michael Burry, Mohnish Pabrai, Nassim Taleb, Peter Lynch, Phil
Fisher, Rakesh Jhunjhunwala, Stanley Druckenmiller, and Warren Buffett. These are
interpretations of investment approaches, not the people or their endorsement.

References are vendored from
[vibe-investing](https://github.com/dong5359/vibe-investing/tree/15954a68fcf9c5368955f935a899e9c80ad48d5c/skills/investor-personas)
at that pinned commit. The MIT notice accompanies the references and every
derived source. Catalog data and reference Markdown are inert resources, not
13 automatically discovered skills.

A source lives at `investment-brains/<investment-brain-id>`. The scaffold
requires a template, new id, display name, publisher, and license; it refuses
overwrites and path traversal. It creates the strict Brain manifest, explicit
skill metadata, starting lens, personal-method draft, learning principles,
and attribution. It performs no network access or lifecycle mutation.

The personal method overrides the starting lens where explicitly adapted.
Unspecified methods remain marked as drafts; unresolved conflicts remain
visible. General evidence priorities, competence limits, causal questions,
falsifiers, and abstention rules belong in the Brain. Exact entry/exit,
position sizing, stops, and portfolio rules belong in a separate Strategy.
Account facts remain in Investor Context. Private cases remain outside the
portable source.

Source authoring and managed installation follow `tcx-brain` without an
alternative admission path. `$tcx-persona` and template names do not select
an analysis overlay. Each run selects one exact active `$investment-brain-*`
id, sealing its version and content digests. Compare distinct personas or
versions in distinct runs.

## Review-driven learning

Learning is an explicit change to instructions supported by recorded cases;
it does not train model weights or prove an investment edge.

1. Identify the personal source and the versions/Strategies actually used in
   the user-selected decisions. Preserve cohorts, cutoff, and contrary cases.
2. Evaluate decision-time process before outcome. If the outcome is already
   known, disclose hindsight exposure; never backdate a blind process lock.
3. Separate evidence defects, reasoning defects, rule adherence,
   implementation/costs, and ordinary uncertainty.
4. Preserve strengths as repeatable behaviors with applicability limits.
   Address weaknesses with the smallest bounded change and competing
   explanations. A profitable trade does not justify raising risk.
5. Return before/proposed principles, supporting and contrary case references,
   scope, uncertainty, and a preregistered baseline/test/failure condition.
6. Keep lessons as candidates until their canonical evidence supports a
   stronger state. Separate replay, unseen holdout, and live-forward evidence;
   account for costs, exposure, drawdown, turnover, and attempted variations.
7. When the user requests a concrete source revision, abstract the selected
   lessons, publish a higher source version, and validate it. Managed update
   and activation retain their existing explicit lifecycle boundary. Historical
   runs retain their original binding; rollback uses an installed prior version.

Memory adoption and postmortem recording retain their terminal handoffs.
Inherited-MCP children can critique a candidate as research-only but cannot
impersonate an authenticated independent reviewer to promote lessons.
A workspace proposal note, if requested, is only a noncanonical draft linking
existing records, not a second ledger.

## Validation

`tests/test_persona_skill.py` exercises all 13 templates against the real
Brain validator, source creation without application imports, root-only
projection, unchanged specialist count, invalid inputs and overwrite
rejection, explicit selection, immutable revision provenance, and rollback.
Skill behavior additionally needs generated-workspace native Codex checks for
personalization, review with contrary cases, incomplete methods, and separation
of review proposals from managed activation. Passing structural tests alone
does not establish native review behavior or profitability.
