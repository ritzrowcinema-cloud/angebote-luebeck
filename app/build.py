# Baut android/assets/index.html aus app/app.html + recipes.js + icons.js + aktueller data.json
import json,os
H=os.path.dirname(os.path.abspath(__file__)); R=os.path.dirname(H)
t=open(os.path.join(H,'app.html'),encoding='utf-8').read()
D=json.load(open(os.path.join(R,'data.json'),encoding='utf-8'))
for a,b in [('__RECIPES__',open(os.path.join(H,'recipes.js'),encoding='utf-8').read()),
            ('__ICONS__',open(os.path.join(H,'icons.js'),encoding='utf-8').read()),
            ('__EMB__',json.dumps(D,ensure_ascii=False,separators=(',',':')))]:
    assert t.count(a)==1,a; t=t.replace(a,b)
os.makedirs(os.path.join(R,'android','assets'),exist_ok=True)
open(os.path.join(R,'android','assets','index.html'),'w',encoding='utf-8').write(t)
print('index.html',round(len(t)/1e3),'KB')
