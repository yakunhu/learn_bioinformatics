# Coding Practice Instructions

## Question vocabulary

- Use plain learner-facing language. Say "topic list and question counts" and "write all questions," not internal phrases such as "category allocation" or "full bank population."
- A **question** is any learner-facing prompt in either the quickfire or full-question format. **Problem** is synonymous with **question** and therefore also applies to both formats; do not use `problem` to mean only a full question.
- A **quickfire question** is a basic, often single-sentence question graded on a pass/fail basis and recorded as `correct` or `incorrect`.
- A **full question** is a larger, multi-step application question that requires a complete solution, such as code, analysis, or a worked response, and is graded against detailed criteria. Keep this definition independent of any specific language, method, or subject area.
- An **assignment** is synonymous with a **full question**; do not use `assignment` for a quickfire question.
- A **non-review question** is the first scored presentation of a question or its learning objective. It may be either quickfire (`mode: initial`) or full.
- A **review question** is a later question that revisits a previously scored question or learning objective. It may be either quickfire (`mode: review`) or full; apply the review and transfer rules of the relevant format.
- For quickfire questions, record correctness in progress for every scored question, whether review or non-review. Append a mistake entry whenever either type is answered incorrectly; do not describe the mistakes log as the complete question history.

## Quickfire question-bank creation

- For interview-focused quickfire banks intended for bioinformatics work, prioritize foundational syntax and recurring constructs demonstrated across representative, maintained bioinformatics repositories. Exclude contrived edge cases unless they recur in those repositories or explain a frequent bioinformatics failure mode. Review variants must preserve both the learning objective and its practical relevance to reading or debugging bioinformatics code.
- Unless the learner explicitly asks to continue without stopping, use two checkpoints when creating a new quickfire question bank:
  1. Propose the topic list and question counts, then pause for approval or adjustment.
  2. After approval, write all questions and connect the new track to the existing drill scripts.
- Test the implementation step by step, running the narrowest relevant check before proceeding:
  1. Validate the bank structure, expected total, unique question IDs and prompts, and per-topic counts.
  2. Run one isolated lifecycle test covering initialization, question selection, correct and incorrect recording, review spacing and recovery, minimal mistake logging, and progress metrics.
  3. Smoke-test question selection for existing tracks to detect regressions.
  4. Run the skill-package validator.
  5. Add targeted language, package, or runtime checks only when a failure or version-sensitive question provides a concrete reason.
- Stop testing once the required checks pass; do not add redundant validation merely for additional reassurance.

## Programming tutor progression

- Follow `.programming-tutor/r_progress.yaml` `curriculum_order` literally for the learner's user-facing R category progression. Do not skip ahead because a category has baseline evidence or an internal lifecycle tag unless the learner explicitly requests that.
- In this repo's study sequence, the first scored full question the learner undertakes in a category is an initial task scored out of 5. Earlier unscored baseline evidence may adjust lesson depth, but it must not silently reclassify that question as a review or requested-deepening task scored out of 3.
- If detailed progress state conflicts with the learner's stated records or the explicit curriculum order, reconcile the mismatch before issuing or scoring another full question.
- Before providing the learner with a full-question prompt, process the entire `## Assignment prompt` section of the programming-tutor skill.

## Correction handling

- When the learner corrects the assistant on a mistake, automatically draft a concise generalized amendment to the programming-tutor or curriculum Skills, or this repo-specific `AGENTS.md` and ask the learner for explicit approval before editing the file; avoid adding incident-specific history when an existing general rule already covers the correction.
