# Fundamentals of Computer Science (Datavetenskapens Grunder) - Mega Practice Exam Repository

This repository contains the syllabus, past exam context, course materials, and the prompt for generating a comprehensive university-level practice exam for **Fundamentals of Computer Science (Datavetenskapens Grunder)**.

---

## 📂 Repository Contents

- `PROMPT.md`: The complete prompt to give to Claude Code / AI.
- `pdfs/`: Original PDF files:
  - `exam2025-1.pdf`: Past exam for 5DV037 (Fundamentals of Computer Science) set by Martin Berglund.
  - `exam1.pdf` & `exam2.pdf`: Past exams.
  - `10-lecture.pdf`, `11-lecture.pdf`, `12-lecture.pdf`: Course lecture slides.
- `extracted_texts/`: Full plain-text extractions of all PDFs for rapid LLM processing without PDF parser overhead.

---

## 🎯 The Exam Generation Prompt

# Mega Practice Exam Generation Prompt

You are an expert Computer Science professor advising on the creation of a "mega practice exam" for a university course titled "Fundamentals of Computer Science (Datavetenskapens Grunder)". 
I need you to review the proposed structure of a practice exam and provide the actual LaTeX code for the questions. This exam must be incredibly comprehensive, starting from the basics and scaling up to the hardest exam-level questions. It must prepare the student for absolutely everything in the course.

Here is the exhaustive context of the course based on the student's lecture slides and a past exam:

## TEXTBOOKS:
- Peter Linz, "An Introduction to Formal Languages and Automata" (6th Edition)
- Michael Sipser, "Introduction to the Theory of Computation" (3rd Edition)

## SYLLABUS & LECTURE COVERAGE:
1. **Regular Languages**: DFA, NFA, NFA to DFA conversion (Subset Construction), DFA Minimization (Indistinguishable states/Marking algorithm).
2. **Regular Expressions & Closure**: Regex to NFA construction, Closure properties of regular languages (Union, Intersection, Complement, Set Difference), Decidability of Finiteness/Infiniteness. Pumping lemma for regular languages (pigeonhole principle).
3. **Context-Free Languages**: CFG design, Leftmost/Rightmost derivations, Derivation trees, Ambiguity.
4. **PDAs & Parsing**: NPDA and DPDA definitions, CFG to PDA conversion. Chomsky Normal Form (CNF) conversion (removing lambda and unit productions). CYK Algorithm. Pumping lemma for CFLs. Closure properties (Union, Concatenation, Star for CFLs. Complement, Intersection for DCFLs vs CFLs). 
5. **TM & Computability**: TM formal definition, Instantaneous descriptions. TM Variants (Stay-option, Semi-infinite tape, Offline, Multitape, Nondeterministic). Universal Turing Machine. Recursive vs Recursively Enumerable (Deciders vs Recognizers).
6. **Undecidability**: Countability (Cantor's diagonalization applied to powersets/TMs). The Halting Problem. Proving undecidability via Reductions (e.g., State Entry Problem).
7. **Complexity**: Time complexity, Big-O. Polynomial vs Exponential difference between DTM and NTM. The classes P and NP. NP-completeness, Cook-Levin Theorem (SAT is NP-complete). Polynomial-time reductions (SAT to 3SAT, 3SAT to CLIQUE).

## PAST EXAM CONTEXT (To gauge difficulty):
The actual 2022 exam included:
- True/False questions on regular/CFL closure, P vs NP, and TM decidability.
- Proofs of closure properties for Regular Languages.
- Filling out a Venn diagram of language classes with example languages and automata.
- Proving L = {w | |w|_a > 2|w|_b} U {w | 2|w|_a < |w|_b} is not context-free.
- Checking if a grammar is in CNF, and running the CYK algorithm on "abcab".
- Constructing a TM M_{gf} that computes g(f(v)) given TMs for f and g.
- Sketching why NTMs are not more computationally powerful than DTMs.
- Proving a custom boolean operator equation problem is NP-complete.
- Proving whether the infinite union of regular languages is regular.
- Defining NP and proving it is closed under union and intersection.

## MY PROPOSED MEGA-EXAM STRUCTURE (4 Modules, 15 massive questions):
- **Module 1**: Finite Automata & Regular Languages (Construction, MinDFA, Regex, Pumping Lemma, Closure).
- **Module 2**: CFLs & PDAs (CFG, PDA, CNF, CYK, CF-Pumping Lemma, Closure).
- **Module 3**: Computability (TM construction, Variants, Recursive/RE, Countability, Reductions/Undecidability).
- **Module 4**: Complexity (Big-O, P vs NP, Reductions, NP-completeness).

## YOUR TASK:
1. **Critique my proposed 15-question structure**: Is there anything missing from the syllabus or past exam?
2. **Write the ACTUAL LATEX CODE for this mega-exam**: Create specific, highly rigorous problem formulations. Do not just write generic placeholders. Write actual grammars to convert, actual strings to parse, actual TM functions to build, and a brand new custom NP-completeness reduction problem (similar to the past exam's operator question).
3. **Ensure the LaTeX is perfectly formatted**: Wrapped in a single document environment, and includes a section for the "Solutions/Answer Key" at the end.

