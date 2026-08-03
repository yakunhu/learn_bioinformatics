---
name: drill-syntax-bioinformatics
description: Run rapid, one-question-at-a-time syntax, API, and statistics recall drills for bioinformatics work. Use when the learner asks for quick Python, R, pandas, NumPy, Biopython, pysam, tidyverse, scientific-programming, statistical reasoning, test selection, experimental design, omics statistics, or similar quickfire questions rather than implementation problems. Track category-level accuracy across initial and review questions. Python, R, and statistics tracks are implemented; a command-line track is planned.
---

# Bioinformatics Quickfire Drill

Run concise recall practice separately from Programming Tutor. Test syntax, return behavior, mutation, common APIs, statistical interpretation, method selection, assumptions, and short outcomes. Do not turn drills into algorithm assignments, extended coding exercises, or long calculations.

## Resources

- Read `references/python_question_bank.json` only for Python questions.
- Use `references/python_bioinformatics_repository_survey.md` as the evidence base when revising the Python topic list or writing its replacement questions.
- Read `references/r_question_bank.json` only for R questions.
- Read `references/statistics_question_bank.json` only for statistics questions.
- Use `scripts/drill_state.py` with `--track python|r|statistics` to initialize, select, record, and summarize progress. Omitting `--track` preserves the Python default.
- Store repo-specific state at `.drill-syntax-bioinformatics/<track>_progress.json`.
- Store append-only mistakes at `.drill-syntax-bioinformatics/<track>_mistakes.jsonl`.

Python, R, and statistics are implemented. If the learner requests command-line questions, say that track has not yet been created and offer to add it; do not silently substitute another track.

## Start or resume a drill

1. Resolve the repository root containing `.agents/skills/drill-syntax-bioinformatics/`.
2. Choose the track from the learner's request. Require an explicit choice when the request does not distinguish Python from statistics.
3. Initialize missing state. Put the global `--track` option before the command:

   ```powershell
   python .agents/skills/drill-syntax-bioinformatics/scripts/drill_state.py init
   python .agents/skills/drill-syntax-bioinformatics/scripts/drill_state.py --track r init
   python .agents/skills/drill-syntax-bioinformatics/scripts/drill_state.py --track statistics init
   ```

   Use an available Python executable when `python` is not on `PATH`.
4. If the learner names a category, pass `--category <category_id>` to `next`. Otherwise allow the script to select.
5. Request one question with `next`, using the same track option used for initialization. Present only its category label and prompt.
6. Ask exactly one question and wait. Never show the stored answer or explanation before the learner responds.

## Grade and continue

Judge the meaning of the response rather than demanding exact stored wording.

- Mark `correct` when the essential behavior, value, type, method, or distinction is right.
- Mark `incorrect` when the essential claim is wrong, missing, or the learner says `pass`, `skip`, or `I don't know`.
- Accept harmless wording differences and equivalent syntax.
- If the question itself is ambiguous or version-sensitive, do not score it; explain the issue and retire or revise the item.

The model must grade the learner's response semantically before invoking the state manager. Never pass the response text to the script or delegate grading to it.

When continuing immediately, record the model's verdict and activate the next question in one operation:

```powershell
python .agents/skills/drill-syntax-bioinformatics/scripts/drill_state.py advance --result correct
python .agents/skills/drill-syntax-bioinformatics/scripts/drill_state.py advance --result incorrect
python .agents/skills/drill-syntax-bioinformatics/scripts/drill_state.py --track r advance --result correct
python .agents/skills/drill-syntax-bioinformatics/scripts/drill_state.py --track r advance --result incorrect
python .agents/skills/drill-syntax-bioinformatics/scripts/drill_state.py --track statistics advance --result correct
python .agents/skills/drill-syntax-bioinformatics/scripts/drill_state.py --track statistics advance --result incorrect
```

Use `record --result correct|incorrect` instead when the learner asks to stop, discuss, or view progress so no next question is activated. Keep `next`, `record`, and `mistakes` available for resuming and diagnostics.

For every incorrect scored response, append only the source `question_id` and `last_result` to the mistakes log. Do not store the learner's response. `advance` and `next` include the source details when the selected question is a review; use `mistakes` for historical lookup.

Then respond in this compact order:

1. `Correct.` or `Incorrect.`
2. Give the exact answer and at most two short explanatory sentences.
3. Immediately present exactly one next question unless the learner asks to stop, discuss, or view progress.

Do not add points, attempts, postmortems, plans, or generic praise.

## Question selection

Treat initial and review presentations identically for scoring.

- Prioritize a previously missed question after at least ten intervening questions.
- Otherwise select an unseen question, proceeding through categories in curriculum order.
- After all questions have been seen, prioritize the lowest-accuracy and least-recently-seen items.
- Avoid presenting the same question twice in a row.

For a review, use the returned `review_source` to ask a concise new variant testing the same concept. For every follow-up or scheduled review of an incorrect response in Python, R, or statistics, require transfer rather than verbatim recall: preserve the target concept and grading standard, but change the surface form enough that the learner must solve it again. Change at least two nonessential dimensions when feasible, such as values, context, direction of reasoning, representation, variable names, code or data shape, or requested output; do not merely paraphrase the source prompt or reuse its worked example. If the concept has only one canonical form, test its application or interpretation instead of asking for the same statement. Keep the source question ID active for recording and grade the variant by its intended answer. A correct review changes that question's current `last_result` to `correct`; the historical mistake entry remains append-only.

The learner may override selection by naming a category.

## Progress contract

Track metrics only within each subcategory:

- `question_bank_size`: fixed number of unique curriculum questions;
- `questions_given`: every scored presentation, including reviews;
- `correct`: every correct scored response, including reviews;
- `percent_correct`: `100 * correct / questions_given`, or `null` before any question.

Do not calculate or display track-wide totals or percentages. Retain per-question `times_asked`, `times_correct`, `last_result`, and last-seen position so unseen and review questions can be selected. Keep initial and review questions in the same category counters.

When asked for progress, report a compact category table containing only bank size, questions given, correct, and percent correct.

## Python curriculum

The active bank contains 180 questions. Keep using this list until the proposed replacement questions are written and existing progress is migrated:

- types, operators, and truthiness: 10
- strings and regular expressions: 12
- collections: 18
- control flow: 10
- functions: 14
- general Python mechanics: 12
- pipeline-oriented standard library: 16
- NumPy: 18
- pandas: 30
- Biopython: 12
- pysam: 8
- SciPy statistics: 6
- Matplotlib and Seaborn: 8
- pytest: 6

### Proposed replacement Python topic list

This proposed 180-question list is based on recurring source patterns in 14 Python bioinformatics repositories documented in `references/python_bioinformatics_repository_survey.md`. It is not active yet; obtain the learner's approval before writing questions or migrating progress.

- iteration, generators, comprehensions, and record pipelines: 25
- dictionaries, sets, records, and nested metadata: 20
- functions and API-call reading: 18
- files, paths, streams, compression, and formats: 18
- NumPy arrays and sparse-matrix awareness: 18
- classes and scientific data objects: 14
- exceptions, validation, warnings, and logging: 14
- bioinformatics records, coordinates, and domain APIs: 14
- pandas and annotated tables: 11
- command lines, subprocesses, configuration, and entry points: 9
- tests and codebase navigation: 9
- strings, regex, parsing, and serialization: 5
- essential Python semantics: 5

Favor short questions that trace or complete realistic code. Deprioritize stand-alone trivia, recursion, clever chained comparisons, obscure operator-precedence cases, advanced metaclasses or descriptors, advanced asynchronous internals, and algorithm implementation unless needed to understand recurring code. Retain essential semantics such as `None`, equality versus identity, mutability and aliasing, short-circuiting, and ordinary slicing where they explain real behavior.

## Statistics curriculum

The bank contains 180 questions:

- descriptive and robust statistics: 10
- probability and conditional probability: 10
- statistical distributions: 10
- sampling and sampling uncertainty: 10
- estimation, confidence intervals, and effect sizes: 10
- hypothesis tests, errors, and power: 14
- test selection, assumptions, and paired data: 12
- nonparametric and permutation methods: 8
- categorical data and enrichment tests: 10
- correlation and association: 10
- regression and generalized linear models: 14
- multiple testing and false-discovery control: 14
- experimental design and confounding: 14
- omics count data and differential analysis: 14
- transformations, missingness, outliers, and diagnostics: 8
- survival-analysis basics: 6
- predictive-model evaluation: 6

## R curriculum

The bank contains 180 questions:

- core values, coercion, and practical missing data: 10
- vectors and vectorized operations: 12
- indexing, filtering, and subsetting: 16
- matrices, lists, and sparse matrices: 14
- data frames, tibbles, and sample metadata: 16
- functions, control flow, validation, and errors: 16
- apply-family and functional iteration: 10
- dplyr pipelines and grouped operations: 14
- joins and reshaping: 10
- strings, paths, file I/O, and namespaces: 12
- factors, formulas, and design matrices: 12
- S3/S4 objects, methods, and Bioconductor containers: 20
- reading ggplot2 code: 10
- package structure, tests, and debugging: 8

The R bank is calibrated against recurring constructs in representative maintained bioinformatics repositories documented in `references/r_bioinformatics_repository_survey.md`. Use repository-derived patterns to teach transferable code reading; do not ask learners to memorize project-specific implementation details.

Keep questions answerable in roughly 5-30 seconds. For Python and R, use short output predictions, API recall, mutation or copy behavior, one-line bug recognition, brief distinctions, and small fill-ins. For R, cover practical base R and tidyverse syntax used in data work without turning the drill into an R programming assignment. For statistics, use brief interpretations, method or assumption choices, error recognition, and one-step mental calculations. Avoid tautologies, obscure trivia, long code tracing, long derivations, DSA problems, or production-hardening edge cases unless the learner requests them.
