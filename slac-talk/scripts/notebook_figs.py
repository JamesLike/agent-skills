"""Extract every PNG output from a notebook, labelled by the markdown heading above it.
Usage: python3 notebook_figs.py analysis.ipynb fig_analysis
Prints "<file> | <heading> | <first code line>" per figure, so you can pick figures by section.
A notebook on another branch: git show origin/<branch>:<path>.ipynb > nb/<name>.ipynb, then run on that copy.
"""
import json,sys,base64,os,re
nb=json.load(open(sys.argv[1])); out=sys.argv[2]; os.makedirs(out,exist_ok=True)
head='(top)'; k=0
for ci,c in enumerate(nb['cells']):
    src=''.join(c['source'])
    if c['cell_type']=='markdown':
        hs=[l for l in src.splitlines() if l.startswith('#')]
        if hs: head=hs[-1][:90]
        continue
    for o in c.get('outputs',[]):
        d=o.get('data',{})
        if 'image/png' in d:
            k+=1; fn=f'{out}/c{ci:03d}_{k:03d}.png'; open(fn,'wb').write(base64.b64decode(d['image/png']))
            print(os.path.basename(fn),'|',head,'|',src.splitlines()[0][:60] if src else '')
