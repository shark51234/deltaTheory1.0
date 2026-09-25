import re, json
raw=open('phil_layout.txt').read().replace('\x0c','\n')
lines=raw.split('\n')
# locate chapter starts
chap=[]; i=0
while i<len(lines):
    s=lines[i].strip()
    m=re.fullmatch(r'Chapter (\d+)',s)
    if m and i>80:
        # title is next non-empty line(s)
        j=i+1
        while not lines[j].strip(): j+=1
        title=lines[j].strip(); k=j+1
        # titles may wrap onto a second centered line
        if lines[k].strip() and len(lines[k])-len(lines[k].lstrip())>10 and not re.search(r'\(\d',lines[k]): title+=' '+lines[k].strip(); k+=1
        chap.append((int(m.group(1)),title,k)); i=k; continue
    if s.startswith('Prologue — The Question Beneath Physics') and i>60: chap.append((0,'Prologue — The Question Beneath Physics',i+1))
    i+=1
chap.sort(key=lambda c:c[2])
out={}
for n,(num,title,start) in enumerate(chap):
    end=chap[n+1][2]-3 if n+1<len(chap) else len(lines)
    body=[]
    for L in lines[start:end]:
        st=L.strip()
        if re.fullmatch(r'\d+|[ivx]+',st): continue
        if st.startswith('The Philosophy of') : continue
        if re.fullmatch(r'Chapter \d+',st): continue
        body.append(L.rstrip())
    out[num]=dict(title=title,lines=body)
json.dump(out,open('phil_chapters.json','w'))
for num in sorted(out): print(num,out[num]['title'],len(out[num]['lines']))
# list display blocks: lines indented > 8 spaces
disp=[]
for num in sorted(out):
    for L in out[num]['lines']:
        ind=len(L)-len(L.lstrip())
        if ind>8 and L.strip(): disp.append((num,L.strip()))
print(len(disp))
for d in disp: print(d)
