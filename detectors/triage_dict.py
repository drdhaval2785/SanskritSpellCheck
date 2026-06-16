#!/usr/bin/env python3
"""triage_dict.py -- one entry point for the body-grounded triage of a dictionary.

Runs the four deterministic steps in order, then prints the exact arguments to launch
the (single, shared) body-aware LLM workflow. After that workflow finishes, run with
--finish to synthesize the review package.

    cd detectors
    python triage_dict.py PWG            # package -> enrich -> bodies -> body_batches; prints workflow args
    #  ... launch detectors/bodyaware_workflow.js with the printed args (the body-aware LLM step) ...
    python triage_dict.py PWG --finish   # synthesize PWG_triaged.txt + file_first + wrong_readings

The body-aware workflow batch count is discovered at runtime by the workflow itself, so
nothing about batch counts is ever passed by hand.
"""
import sys
import os
import json
import subprocess

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

import triage_lang

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
GITHUB = os.path.dirname(ROOT)


def run(script, dict_code):
    print("\n=== %s %s ===" % (script, dict_code))
    subprocess.run([sys.executable, os.path.join(HERE, script), dict_code], check=True)


def main():
    if len(sys.argv) < 2:
        print("usage: python triage_dict.py <DICT> [--finish]")
        sys.exit(1)
    dict_code = sys.argv[1]
    finish = '--finish' in sys.argv[2:]

    if finish:
        run('triage_synthesize.py', dict_code)
        return

    for script in ('make_dict_package.py', 'triage_enrich.py', 'triage_bodies.py',
                   'triage_body_batches.py'):
        run(script, dict_code)

    work = os.path.join(ROOT, 'corrections_draft', dict_code, 'triage_work').replace('\\', '/')
    src = os.path.join(GITHUB, 'csl-orig', 'v02', dict_code.lower(),
                       '%s.txt' % dict_code.lower()).replace('\\', '/')
    wf = os.path.join(HERE, 'bodyaware_workflow.js').replace('\\', '/')
    payload = {'scriptPath': wf,
               'args': {'dict': dict_code, 'dir': work, 'src': src,
                        'hint': triage_lang.marker_hint(dict_code)}}
    print("\n" + "=" * 70)
    print("NEXT: launch the body-aware workflow (%s body) with:" % triage_lang.lang_name(dict_code))
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("\nthen: python triage_dict.py %s --finish" % dict_code)


if __name__ == '__main__':
    main()
