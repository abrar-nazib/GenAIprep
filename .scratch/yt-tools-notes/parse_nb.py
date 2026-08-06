import json
with open('/home/abrar/Programming/GenAI/.scratch/yt-tools-notes/notebook.ipynb') as f:
    nb = json.load(f)
for i, cell in enumerate(nb['cells']):
    print(f'--- Cell {i} ({cell["cell_type"]}) ---')
    print(''.join(cell['source']))
    if cell.get('outputs'):
        for out in cell['outputs']:
            if 'text' in out:
                print('OUTPUT:', ''.join(out['text']))
            elif 'data' in out:
                for k, v in out['data'].items():
                    if 'text' in k:
                        print('OUTPUT:', ''.join(v))
    print()