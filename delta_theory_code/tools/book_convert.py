import re, json
ch=json.load(open('phil_chapters.json'))
EQ={
'1':r'\text{Reality is invariant continuity carrying irreducible difference.}',
'1.1':r'\text{continuity}\to\text{difference}\to\text{relation}\to\text{organization}\to\text{geometry.}',
'2.1':r'F(I_0)=I_0.','2.2':r'F^{\,n}(I_0)=I_0.',
'2.3':r'\delta\neq0\ \ \text{is the primitive condition for becoming.}',
'3.1':r'\tau\delta=I','3.2':r'\tau=\frac{I}{\delta}.',
'3.3':r'\tau\ \text{is dynamical},\qquad\delta\ \text{is dynamical},\qquad I\ \text{is invariant.}',
'3.4':None,'3.5':None,
'5.1':r'\tau_a,\ \tau_b,\ \tau_c,\ \dots','5.2':r'\delta\to\text{propagation}\to\text{processing}\to\text{new state}\to\text{new }\delta.',
'6.1':r'\tau_a=\tau_b,','6.2':r'\tau_a\neq\tau_b,','7.1':r'\tau\to\tau_a.',
'7.2':r'\text{mass}\sim\text{persistent localized temporal processing.}',
'8.1':r'\text{photon}=\text{propagating }\delta.','8.2':r'\text{localized temporal excitation}\;\longleftrightarrow\;\text{propagating temporal difference.}',
'9.1':r'\delta_b\longrightarrow P_a(\delta_b),','9.2':r'P_a(\delta_b)\neq\delta_b.','9.3':r'\delta_b\to\delta_{b\to a}\to\delta_{a\to c}\to\cdots',
'10.1':r'P_a(\delta_b)\neq P_b(\delta_a).','10.2':r'(\tau_a,\delta_a)\leftrightarrow(\tau_b,\delta_b)\ \ \text{produces}\ \ (\tau_a^{\prime},\delta_a^{\prime}),\ (\tau_b^{\prime},\delta_b^{\prime}).',
'10.3':r'\delta_0\to\delta_1\to\delta_2\to\delta_3\to\cdots','10.4':r'\delta_0=\delta_1=\delta_2=\delta_3.',
'11.1':r'\tau/\delta\ \text{relations}\to\text{topology}\to\text{geometry}\to\text{space.}',
'12.1':r'\text{object}\to\text{space}\to\text{motion.}','12.2':r'\text{temporal relation}\to\text{difference}\to\text{changing relation}\to\text{emergent trajectory.}',
'13.1':r'\tau\to\tau_a,','13.2':r'\delta\to\delta^{\prime},','13.3':r'\tau_a\to\text{processing of }\delta\to\text{changed }\delta\to\text{changed }\tau_a.',
'15.1':r'\delta\to0.','15.2':r'\text{perfect synchronization}<\text{manifest dynamics}<\text{perfect resolution.}',
'17.1':r'\delta\to\text{distinction}\to\text{information.}','17.2':r'\delta\to\text{information}\to\text{processing}\to\text{new relational difference.}',
'18.1':r'\text{energy}=\text{recognition of difference}','18.2':r'\text{mass}=\text{persistence of distinction.}',
'19.1':r'\text{observation}=\text{incoming difference}+\text{local temporal processing.}',
'22.1':r'(\tau_1,\delta_1),\ (\tau_2,\delta_2),\ \dots,\ (\tau_n,\delta_n),','22.2':r'\{(\tau_i,\delta_i)\}\longrightarrow C_1,\,C_2,\,\dots,\,C_m.','22.3':r'\tau_a\neq\tau_b',
'23.1':r'\text{particle}\to\text{cluster}\to\text{organism}\to\text{society}\to\text{planetary system}\to\text{galaxy}\to\text{universe.}',
'25.1':r'\tau=\text{continuity}','25.2':r'\delta=\text{difference.}',
'26.1':r'\tau\to\tau_a,\ \tau_b,\ \tau_c,\ \dots,','26.2':r'\delta\to\text{propagation}\to\text{distorted information}\to\text{new }\delta,',
'26.3':r'\text{relational network}\to\text{topology}\to\text{geometry}\to\text{space.}',
'26.4':r'\begin{aligned}\tau\to\delta&\to\text{local temporal states}\to\text{interaction}\to\text{information}\to\text{temporal persistence}\\&\to\text{clustering}\to\text{higher-order organization}\to\text{increasingly complex processing}\to\text{self-recognition.}\end{aligned}',
}
def inline(s):
    s=s.replace('δ-Theory','\\dT{}')
    s=s.replace('̸=','\u2260')
    s=re.sub(r'P([ab]) ?\((δ|τ)([ab]) ?\)',lambda m:f'$P_{m.group(1)}(\\{"delta" if m.group(2)=="δ" else "tau"}_{m.group(3)})$',s)
    s=re.sub(r'([τδηεερφΦΨ])([a-z0-9])(?=[\s,.;:)\]′]|$)',lambda m:'$'+{'τ':'\\tau','δ':'\\delta','η':'\\eta','ε':'\\varepsilon','ρ':'\\rho','φ':'\\phi','Φ':'\\Phi','Ψ':'\\Psi'}[m.group(1)]+'_{'+m.group(2)+'}$',s)
    s=re.sub(r'\bI0\b','$I_0$',s)
    rep={'τ':'$\\tau$','δ':'$\\delta$','η':'$\\eta$','ε':'$\\varepsilon$','ρ':'$\\rho$','→':'$\\to$','\u2260':'$\\neq$','∼':'$\\sim$',
         '←→':'$\\longleftrightarrow$','↔':'$\\leftrightarrow$','−→':'$\\longrightarrow$','′':"$'$",'·':'$\\cdot$','—':'---','–':'--',
         '“':'``','”':"''",'‘':'`','’':"'",'…':'\\ldots{}','%':'\\%','&':'\\&','∗':'$\\ast$'}
    for k,v in rep.items(): s=s.replace(k,v)
    s=s.replace('$$','')   # merge adjacent math
    s=re.sub(r'\$\s*\$',' ',s)
    return s
KEEPHY={'higher','self','well','non','long','step','out','one','two','three','co','re','pre','sub','multi','half','first','second','high','low','time','by','ever','near','sense','dimensional','end'}
def convert(num):
    L=ch[str(num)]['lines']
    out=[]; para=[]; disp=[]
    def flush_para():
        nonlocal para
        if para:
            txt=''
            for i,l in enumerate(para):
                if txt.endswith('-') and l[:1].islower():
                    word=re.findall(r'(\w+)-$',txt)
                    if word and word[0].lower() in KEEPHY: txt+=l
                    else: txt=txt[:-1]+l
                else: txt=(txt+' '+l) if txt else l
            out.append(inline(txt)); para=[]
    def flush_disp():
        nonlocal disp
        if not disp: return
        joined=' '.join(disp); nums=re.findall(r'\((\d+(?:\.\d+)?)\)\s*$',joined) or re.findall(r'^\((\d+\.\d+)\)$',joined)
        allnums=re.findall(r'\((\d+\.\d+|\d)\)',joined)
        key=None
        for n in allnums:
            if n in EQ: key=n; break
        if key and EQ[key] is None: disp=[]; return
        if key:
            out.append('\\begin{equation*}\n'+EQ[key]+'\n\\end{equation*}')
        else:
            if joined.strip().startswith('∗'): out.append('\\begin{center}$\\ast\\quad\\ast\\quad\\ast$\\end{center}')
            else: out.append('\\begin{center}\\itshape\n'+'\\\\\n'.join(inline(d) for d in disp)+'\n\\end{center}')
        disp=[]
    for l in L:
        if not l.strip():
            flush_disp(); continue
        ind=len(l)-len(l.lstrip()); st=l.strip()
        isdisp = ind>8 or re.search(r'\(\d+\.\d+\)\s*$',st) and ind>0
        if re.fullmatch(r'\(\d+\.\d+\)',st): disp.append(st); continue
        if isdisp:
            flush_para(); disp.append(st); continue
        flush_disp()
        if 2<=ind<=6: flush_para()
        para.append(st)
    flush_para(); flush_disp()
    return '\n\n'.join(out)
import os
os.makedirs('phil',exist_ok=True)
for num in range(0,28):
    open(f'phil/p{num:02d}.tex','w').write(convert(num)+'\n')
print(open('phil/p03.tex').read()[:3000]); print('....'); print(open('phil/p09.tex').read()[:1500])
