# -*- coding: utf-8 -*-
import re, sys

with open('jordan_schoenflies.tex', encoding='utf-8') as f:
    src = f.read()

main = src[:src.index('\\appendix')]

env_re = re.compile(
    r'\\begin\{(long)?(theorem|lemma|proposition|corollary|definition|remark)\}'
    r'(\[(?P<title>[^\]]*)\])?\s*\\label\{(?P<label>[^}]+)\}',
    re.S)

stmts = []          # (label, basetype, title, span_of_statement_body)
label_type = {}
for m in env_re.finditer(main):
    base = m.group(2)
    label = m.group('label')
    title = m.group('title') or ''
    endpat = '\\end{%s%s}' % (m.group(1) or '', base)
    end = main.index(endpat, m.end())
    stmts.append([label, base, title, (m.start(), end)])
    label_type[label] = base

# attach proofs
proof_re = re.compile(r'\\begin\{proof\}(\[(?P<opt>[^\]]*)\])?', re.S)
proof_scopes = {}   # label -> list of (start,end) proof spans
order = [s[0] for s in stmts]
for pm in proof_re.finditer(main):
    pend = main.index('\\end{proof}', pm.end())
    opt = pm.group('opt') or ''
    tgt = None
    r = re.search(r'\\ref\{([^}]+)\}', opt)
    if r and r.group(1) in label_type:
        tgt = r.group(1)
    else:
        # nearest preceding statement whose body ends before this proof
        for lab, base, title, (s, e) in reversed(stmts):
            if e < pm.start():
                # only attach if nothing but whitespace/short prose gap? attach to nearest
                tgt = lab
                break
    if tgt:
        proof_scopes.setdefault(tgt, []).append((pm.start(), pend))

ref_re = re.compile(r'\\ref\{((?:lem|thm|prop|cor|def|rem):[^}]+)\}')

def refs_in(text, self_label):
    out = []
    for r in ref_re.finditer(text):
        lab = r.group(1)
        if lab != self_label and lab in label_type and lab not in out:
            out.append(lab)
    return out

covered = []  # spans covered by statements+proofs (for the narrative row)
dep = {}
for lab, base, title, (s, e) in stmts:
    scope = main[s:e]
    covered.append((s, e))
    for ps, pe in proof_scopes.get(lab, []):
        scope += main[ps:pe]
        covered.append((ps, pe))
    dep[lab] = refs_in(scope, lab)

# narrative row: all refs in main-text prose outside statements/proofs
def strip_covered(text, offset):
    keep = []
    pos = 0
    spans = sorted((a - offset, b - offset) for (a, b) in covered
                   if a >= offset and b <= offset + len(text))
    for a, b in spans:
        if a > pos:
            keep.append(text[pos:a])
        pos = max(pos, b)
    keep.append(text[pos:])
    return ''.join(keep)

narrative = strip_covered(main, 0)
narr_refs = refs_in(narrative, None)
# drop refs that merely restate the theorem being introduced right there is
# hard to detect; keep all (syntactic artifact).

TYPE = {'theorem': 'Theorem', 'lemma': 'Lemma', 'proposition': 'Proposition',
        'corollary': 'Corollary', 'definition': 'Definition', 'remark': 'Remark'}

def fmt_dep(lab):
    return '%s~\\ref{%s}' % (TYPE[label_type[lab]], lab)

EMPTY = 'Definitions and imported background (\\hyperref[app:background]{Appendix~C}) only.'

def fmt_deps(labs):
    if not labs:
        return EMPTY
    parts = [fmt_dep(l) for l in labs]
    if len(parts) == 1:
        return parts[0]
    return ', '.join(parts[:-1]) + ' and ' + parts[-1]

rows = []
for lab, base, title, span in stmts:
    left = '%s~\\ref{%s}\\newline\\emph{%s}' % (TYPE[base], lab, title)
    rows.append('%s & %s \\\\' % (left, fmt_deps(dep[lab])))
rows.append('\\emph{Narrative outside labeled statements}\\newline'
            '(construction prose of Parts~I--II) & %s \\\\' % fmt_deps(narr_refs))

body = '\n'.join(rows)

start_key = '\\endlastfoot\n'
i = src.index(start_key) + len(start_key)
j = src.index('\\end{longtable}', i)
new_src = src[:i] + body + '\n' + src[j:]

with open('jordan_schoenflies.tex', 'w', encoding='utf-8') as f:
    f.write(new_src)
print('Rows written: %d statements + 1 narrative row' % len(stmts))
