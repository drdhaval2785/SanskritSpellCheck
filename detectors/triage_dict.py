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

import triage_lang
import triage_util

triage_util.reconfigure_stdio()
HERE = triage_util.HERE


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

    work = triage_util.work_dir(dict_code).replace('\\', '/')
    src = triage_util.csl_dict_file(dict_code).replace('\\', '/')
    wf = os.path.join(HERE, 'bodyaware_workflow.js').replace('\\', '/')
    payload = {'scriptPath': wf,
               'args': {'dict': dict_code, 'dir': work, 'src': src,
                        'hint': triage_lang.marker_hint(dict_code),
                        'clsModel': 'sonnet', 'confModel': 'opus', 'revModel': 'opus'}}
    print("\n" + "=" * 70)
    print("NEXT: launch the body-aware workflow (%s body) with:" % triage_lang.lang_name(dict_code))
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    print("\nthen: python triage_dict.py %s --finish" % dict_code)


if __name__ == '__main__':
    main()
