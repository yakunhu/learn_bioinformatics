---
name: programming-tutor-setup
description: Initialize separate assignment-based R and Python programming curricula, progress summaries, logs, and fixture storage. Use when the Programming Tutor state is missing, when the learner explicitly requests a reset or rebuild, or before the first programming-tutor session in a workspace.
---

# Programming Tutor Setup

Initialize the durable state used by `$programming-tutor-curriculum` and `$programming-tutor`. Build a language curriculum, not a roadmap of existing project files.

## Required reference and state

Read [references/curricula.yaml](references/curricula.yaml) completely before writing state.

Use these project-root-relative paths:

- `.programming-tutor/python_progress.yaml`
- `.programming-tutor/python_session_log.yaml`
- `.programming-tutor/r_progress.yaml`
- `.programming-tutor/r_session_log.yaml`
- `.programming-tutor/fixtures/`

Keep R and Python evidence, scores, navigation, and logs separate. Never combine them in one progress or log file.

## Setup workflow

1. Locate the workspace root.
2. Read the curriculum reference.
3. Check all four state files.
   - If all exist, hand control to `$programming-tutor-curriculum` unless the learner explicitly requested a reset or rebuild.
   - If one is missing, create only the missing file and reconcile cross-references without deleting history.
   - Reset or replace existing state only when explicitly requested.
4. Create `.programming-tutor/fixtures/` if missing. Do not move or copy learner files into it unless explicitly authorized.
5. Initialize each progress file from only its language curriculum, preserving curriculum order and at most four assignment objectives per category.
6. Initialize each append-only log with metadata and `sessions: []`.
7. Parse all four YAML files and verify that every state-file reference resolves.
8. Hand the requested language to `$programming-tutor-curriculum`. If no language was specified, ask the learner to choose R or Python.

Do not scan existing code for baseline credit during ordinary setup. Perform a baseline scan only when separately requested; baseline evidence never earns points.

## Progress-file schema

Include:

- `schema_version`, `language`, `created`, and `last_updated`;
- `state_files`, `curriculum_source`, and `curriculum_order`;
- the scoring and review rules below;
- `selection` with `active_assignment`, `current_category`, and `next_new_category`;
- one record under `categories` for every curriculum category.

Each category record must include:

- `stage`, `importance`, `lifecycle`, and `lesson_required`;
- `objective_state`, keyed by the objective IDs in the curriculum reference, with `baseline_demonstrated`, `baseline_evidence`, `initial_assignment_required`, and `initial_assignment_completed`;
- `assignment_plan` with `max_initial_tasks: 4`, `completed_initial_tasks`, and `later_tasks_completed`;
- `points` with `earned`, `possible`, and `percent`;
- `review` with `successful_sessions`, `interval_stage`, `last_practiced`, and `next_review_after`;
- `strengths` and `needs_work`.

Use lifecycle labels only for navigation: `not_started`, `learning`, and `reviewing`. Do not store binary mastery.

Keep objective descriptions only in the curriculum reference; do not duplicate them into progress. Initialize every category with zero points. Initial tasks are generated later from the stored objectives; do not prewrite exact prompts.

## Fixed scoring and review configuration

Store these rules verbatim in both progress files:

- New-topic initial task: 5 possible points; successful attempt 1/2/3/4+ earns 5/4/3/2.
- Later task, whether scheduled review or requested deepening: 3 possible points; successful attempt 1/2/3+ earns 3/2/1.
- Mixed later task: exactly one scoring primary and one scoring secondary; allocate possible and earned points 2/3 to the primary and 1/3 to the secondary. Other applied topics receive no points.
- Compare categories using `points.percent = 100 * earned / possible`; use `null` when possible is zero.
- Initial coverage complete: schedule after 30 days.
- Successful later session: advance to 60 days, then 180 days, then repeat 180 days.
- Attempt 3+, substantial guidance, or incomplete work: follow up after 3 days without advancing the interval stage.
- A later review/deepening event has at most two sequential tasks. Never present two tasks at once.

## Log schema

Initialize `schema_version`, `language`, `progress_file`, and `sessions: []`.

Each future appended session records:

- session ID, date, category, mode, prompt summary, and objective IDs;
- scoring primary and optional scoring secondary;
- attempts, outcome, reasoning assessment, and tests performed;
- possible and earned point allocations;
- strengths, needs work, and any postmortem;
- review dates and interval stages before and after the session.

Never rewrite or delete an earlier log entry.

## Write boundary

During ordinary setup, write only within `.programming-tutor/`. Treat learner submissions and workspace files as read-only unless the learner explicitly authorizes a separate edit or move.
