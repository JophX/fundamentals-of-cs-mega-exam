#!/usr/bin/env bash
# Runs every checker. The build refuses to produce a PDF if any answer is wrong.
cd "$(dirname "$0")"
out=$( { python3 ch02_automata.py; python3 ch03_regex.py; python3 ch04_min.py; python3 ch07_cfg.py;
         python3 pl_exam_grammars.py; python3 pack_cnf.py --check; python3 pack_drill.py --check;
         python3 fcs_q4.py; python3 ch12_tm.py; python3 fcs_diamond.py; python3 practice_exams.py; } 2>&1 )
echo "$out" | grep -E "MISMATCH|NOT EQUAL|Traceback|BAD" && { echo "$out"; exit 1; }
echo "all checks passed ($(echo "$out" | grep -c '\[OK\]') grammar/automaton checks)"
