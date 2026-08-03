---
name: programming-tutor-curriculum
description: Select the next R or Python programming assignment, prioritize due and low-scoring reviews, calculate attempt-based points, schedule 30/60/180-day reviews, and persist assignment evidence. Use at the beginning and end of every Programming Tutor assignment or when the learner asks what to practice or review next.
---

# Programming Tutor Curriculum

Manage topic order, scoring, reviews, and durable state for `$programming-tutor`. Treat the language-specific progress file as compact decision state and its session log as append-only evidence.

## Language and files

Require the learner to select R or Python for each session. If omitted, ask and wait.

Resolve only the selected language pair:

- Python: `.programming-tutor/python_progress.yaml` and `.programming-tutor/python_session_log.yaml`
- R: `.programming-tutor/r_progress.yaml` and `.programming-tutor/r_session_log.yaml`

If either selected-language file is missing, invoke `$programming-tutor-setup`. Never mix evidence or scores across languages.

## Selection order

Read the selected progress file before every selection. Choose exactly one active programming task using this order:

1. a topic or assignment explicitly requested by the learner;
2. an unfinished active assignment;
3. a scheduled review due today or earlier;
4. the next objective whose `initial_assignment_completed` value is false;
5. after initial coverage, a later-deepening task for the lowest-scoring category.

When several reviews are due, choose the lowest `points.percent`; treat `null` as lower than any numeric score. Break further ties by oldest `last_practiced`, then curriculum order.

For lowest-score deepening, use the same tie rules. Do not select a secondary topic whose prerequisites have not been introduced or demonstrated.

Read the selected objective descriptions from the `curriculum_source` reference. Return to the Tutor:

- language, category, objective IDs, stage, importance, and lifecycle;
- session mode: `initial`, `scheduled_review`, or `requested_deepening`;
- whether a short concept lesson is required;
- relevant strengths, needs work, and baseline evidence;
- one scoring primary and, only for a mixed later task, one scoring secondary;
- remaining initial-task or later-event allowance;
- current points and review dates.

When issuing an initial problem, write `selection.active_assignment` as a mapping containing exactly `category`, `objective_id`, and `mode`. Do not write any other state at task selection.

## Assignment limits

- Assign exactly one initial problem to each `objective_state`. Each problem is scored out of 5 and has one scoring objective; incidental overlap with other objectives is non-scoring. Move to later-task scoring only after every objective has received its initial problem, unless the learner explicitly moves on early.
- Give one programming task at a time.
- A scheduled review or requested-deepening event contains at most two sequential tasks. Stop after one when it supplies enough evidence.
- Never expose two task prompts simultaneously.
- Use mixed-topic assignments only after every applied topic has been introduced or demonstrated.

## Points

A materially incorrect response to a relevant interpretation question keeps the assignment incomplete and counts as a failed attempt; do not assign a separate interpretation grade.

### Initial task

An initial task belongs to one category and has 5 possible points. On successful completion, award:

- attempt 1: 5;
- attempt 2: 4;
- attempt 3: 3;
- attempt 4 or later: 2.

An incomplete task earns 0. Count each combined revision responding to a reported batch of core failures as one attempt; do not count clarifying messages.

Classify revisions by interview relevance before incrementing attempts. Core failures reflect substantive problems in the algorithm, transformation, data relationships, analytical reasoning, or scoring objective. Secondary details—such as an isolated missing negation when the intended condition is clear, exact empty-vector types, integer-versus-double outputs, class-versus-storage-type distinctions when the validation intent is correct, naming or quoting slips, and defensive missing/zero-length guards—do not increment attempts or keep an assignment incomplete once the scoring objective and required reasoning are sound. Treat an apparently small syntax or type issue as core only when it demonstrates a substantive misunderstanding or is itself the scoring objective.

### Later task

Every post-initial task uses the same scoring whether it is a scheduled review or requested deepening. It has 3 possible points. On successful completion, award:

- attempt 1: 3;
- attempt 2: 2;
- attempt 3 or later: 1.

An incomplete task earns 0.

For a single-topic later task, allocate all possible and earned points to its category.

For a mixed later task:

- designate exactly one scoring primary and one scoring secondary;
- allocate possible and earned points proportionally: 2/3 to the primary and 1/3 to the secondary;
- round stored values to two decimal places;
- tag any other applied topics as non-scoring evidence only.

After every scored task, set each affected category's percent to `round(100 * earned / possible, 1)`. Keep it `null` when possible is zero. Existing-code baseline evidence always adds 0 earned and 0 possible points.

## Review schedule

Use category-level interval stages:

- completed initial coverage, `waiting_30`, due 30 days later;
- first successful later event: `waiting_60`, due 60 days later;
- second successful later event: `waiting_180`, due 180 days later;
- later successful events: remain `waiting_180`, due 180 days later.

A requested-deepening event counts like a scheduled review and resets the next date from the current session.

Advance the interval stage only when all tasks used for the event are completed on attempt 1 or 2 with sound reasoning. If any task takes attempt 3+, requires substantial guidance, or remains incomplete, keep the long-interval stage unchanged and set `next_review_after` to 3 days later.

## Lifecycle and coverage

Use lifecycle only for routing:

- `not_started`: no objective introduced or demonstrated;
- `learning`: one or more objectives lack an initial completed problem;
- `reviewing`: every objective has an initial completed problem

Do not record binary mastery. 

When the last objective's initial problem is completed, set the category to `reviewing`, set `interval_stage: waiting_30`, and schedule 30 days from the evidence date.

## End-of-task persistence

After grading and any required postmortem:

1. Reread the selected progress and log files.
2. Build one append-only session entry with the fields defined by Setup.
3. Append it automatically after the outcome is settled. Ask for confirmation only if grading or topic attribution remains ambiguous.
4. If `outcome` is `completed` and `active_assignment.mode` is `initial`, set `categories[active_assignment.category].objective_state[active_assignment.objective_id].initial_assignment_completed` to `true`.
5. Update only affected objectives, category aggregates, navigation fields, and review fields.
6. Clear `active_assignment` only when the task is complete or the learner explicitly abandons it.
7. Set `last_updated` and recompute `current_category` and `next_new_category`.
8. Parse both YAML files and verify point arithmetic and file references.
9. Return a one-line point and scheduling delta to the Tutor.

Never edit an earlier log entry. Corrections must be appended as a new correction record and reflected in the summary.

## Write boundary

Write only the selected language's progress and log files. Assignment fixtures belong under `.programming-tutor/fixtures/<assignment_id>/`. Treat learner code as read-only unless the learner explicitly asks for an edit.
