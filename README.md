# 🧬 learn_bioinformatics

## 🎯 Overview

learn_bioinformatics is a reusable Codex practice workspace for learning bioinformatics-oriented Python, R, and statistics. `.agents/skills/` contains the quickfire and programming-tutor skills, question banks, state-management script, and curriculum references; `.programming-tutor/fixtures/` contains small file-backed R datasets.

## 🚀 Getting started

Clone the repository and open its root as a Codex workspace, then ask Codex to use `drill-syntax-bioinformatics` for one-question-at-a-time Python, R, or statistics recall, or `programming-tutor` for full coding questions. Python 3 is required for the quickfire state script, R is required for the R examples, and individual exercises may name additional packages; learner progress, mistake records, session logs, temporary research clones, and local runtime files are intentionally excluded and will remain local when generated.

## 🗂️ Question banks

A **quickfire question** is a short prompt graded correct or incorrect, while a **full question** is a larger, multi-step assignment graded against detailed criteria.

To generate a new category, first decide whether you want quickfire or full questions, then ask Codex to extend the appropriate bank with `drill-syntax-bioinformatics` or the full-question curriculum with the `programming-tutor workflow`. 

Browse the complete 📚 [Python bank](.agents/skills/drill-syntax-bioinformatics/references/python_question_bank.json), [R bank](.agents/skills/drill-syntax-bioinformatics/references/r_question_bank.json), and [statistics bank](.agents/skills/drill-syntax-bioinformatics/references/statistics_question_bank.json) in the [question-bank folder](.agents/skills/drill-syntax-bioinformatics/references/).

## 💬 Question sessions

Name the track or category you want—for example, **“statistics”**—and the Skill selects that category and presents one question at a time.

It grades the meaning of each answer as correct or incorrect, gives concise feedback, and schedules missed material for later review so practice adapts to your needs.

For quickfire questions, the `drill-syntax-bioinformatics` Skill draws initial quickfire questions from curated Python, R, and statistics banks organized by practical categories, then generates review variants that test the same objective with changed details.

For full questions, //

