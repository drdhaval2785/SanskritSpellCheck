#!/usr/bin/env python3
"""test_triage.py -- unit checks for the language-specific body classification.

The triage's correctness rests on the per-language markers (triage_lang.py) routing
documented-intentional spellings to wr/variant/xref and real definitions to realword.
These cases lock that behaviour so adding a dictionary/language can't silently break it.

    cd detectors && python test_triage.py
"""
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import triage_lang
import triage_bodies as tb
import triage_util


def kind(dict_code, body):
    tb._WR = triage_lang.wr_re(dict_code)
    tb._VARIANT = triage_lang.variant_re(dict_code)
    tb._XREF = triage_lang.xref_re(dict_code)
    return tb.classify_one(body)


# (dict, body, expected body_kind)
BODY_CASES = [
    # MW (English)
    ('MW', '<s>marga</s> ¦ <ab>w.r.</ab> for <s>mArga</s>, <ls>ApGr.</ls>', 'wr'),
    ('MW', '<s>kiriwa</s> ¦ See <s>a/ti-kir</s>.', 'xref'),
    ('MW', '<s>muka</s> ¦ <lex>m.</lex> the smell of cow-dung', 'realword'),
    ('MW', 'payaS in comp. for ˚yas.', 'variant'),
    # PW (German)
    ('PW', '{#SUci#} Adj. fehlerhaft für {#Suci#}.', 'wr'),
    ('PW', '{#duHka˚#} s. u. {#duzka˚#}.', 'xref'),
    ('PW', '{#dARqaka#} m. N. pr. {#dARqakya#} v. l.', 'variant'),
    ('PW', '{#idAm#} {#˚mati#} Denom. von {#idam#}.', 'realword'),
    # VCP (Sanskrit)
    ('VCP', '{{Lbody=35976}}', 'xref'),
    ('VCP', 'garba gatO BvA0 para0 saka0 sew . garbati agarbIt jagarba .', 'realword'),
    # BUR / STC (French)
    ('BUR', '{#baNga#} {%baṅga%} m. le Bengale, Cf. {%vaṅga.%}', 'xref'),
    ('STC', '{@valmi-@} lire {%vallī-.%}', 'wr'),
    ('STC', '{@ā-patanā-@} nt. évènement imprévu.', 'realword'),
    # BOP (Latin)
    ('BOP', '{#dUz#} v. {#duz#}.', 'xref'),
    ('BOP', '{#Agrya#} (ab {#agra#} {%n.%} cacumen) insignis, egregius.', 'realword'),
]

# (dict, body, expected wrong-readings sub-type)
SUBTYPE_CASES = [
    ('MW', '<ab>w.r.</ab> for mArga', 'wrong-reading'),
    ('PW', 'fehlerhaft für Suci', 'wrong-reading'),
    ('PW', 'dARqakya v. l.', 'varia-lectio'),
    ('VCP', '{{Lbody=35976}}', 'cross-reference'),
    ('STC', '{@valmi-@} lire {%vallī-.%}', 'wrong-reading'),
    ('BUR', '{#baNga#} cf. {%vaṅga.%}', 'cross-reference'),
    ('BOP', '{#dUz#} v. {#duz#}.', 'cross-reference'),
]


def main():
    fails = []
    for d, body, exp in BODY_CASES:
        got = kind(d, body)
        ok = got == exp
        print("  %-4s body_kind  %-11s expected %-11s %s" % (d, got, exp, 'OK' if ok else 'FAIL'))
        if not ok:
            fails.append((d, body, exp, got))
    for d, body, exp in SUBTYPE_CASES:
        got = triage_lang.subtype(body, d)
        ok = got == exp
        print("  %-4s subtype    %-15s expected %-15s %s" % (d, got, exp, 'OK' if ok else 'FAIL'))
        if not ok:
            fails.append((d, body, exp, got))

    # redirect resolution: {{Lbody=N}} annotated with the target headword
    idx = triage_util.EntryIndex()
    idx.by_l['35976'] = 'brAhmaRa'
    r = triage_util.resolve_redirect('{{Lbody=35976}}', idx)
    ok = 'brAhmaRa' in r
    print("  resolve_redirect -> %r %s" % (r, 'OK' if ok else 'FAIL'))
    if not ok:
        fails.append(('redirect', '{{Lbody=35976}}', 'brAhmaRa', r))

    # EntryIndex.bodies() falls back to k2 (mirrors first()) for a k2-only headword
    idx.by_k2['k2only'] = [{'body': 'a real gloss for a k2-only headword'}]
    b = idx.bodies('k2only')
    ok = b == ['a real gloss for a k2-only headword']
    print("  bodies() k2-fallback -> %r %s" % (b, 'OK' if ok else 'FAIL'))
    if not ok:
        fails.append(('bodies-k2', 'k2only', 'k2 fallback', b))

    # load_json_array tolerates prose/brackets around the JSON array (non-greedy scan)
    import tempfile
    fd, tp = tempfile.mkstemp(suffix='.json')
    os.close(fd)
    with open(tp, 'w', encoding='utf-8') as _f:
        _f.write('Note: I rejected option [A]. Verdicts:\n[{"suspect": "x", "ok": true}]\nThat is all.')
    arr = triage_util.load_json_array(tp)
    os.remove(tp)
    ok = arr == [{"suspect": "x", "ok": True}]
    print("  load_json_array prose-tolerant -> %r %s" % (arr, 'OK' if ok else 'FAIL'))
    if not ok:
        fails.append(('load_json_array', 'prose+brackets', '[{...}]', arr))

    if fails:
        print("\n%d FAILURE(S)" % len(fails))
        sys.exit(1)
    print("\nall %d checks passed" % (len(BODY_CASES) + len(SUBTYPE_CASES) + 3))


if __name__ == '__main__':
    main()
