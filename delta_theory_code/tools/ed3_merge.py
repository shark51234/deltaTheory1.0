import re
main=open('/mnt/user-data/outputs/delta_theory_mathematics.tex').read()
p3=open('/home/claude/part3/delta_theory_part3.tex').read()
ticks=open('/home/claude/part3/ticks_chapter.tex').read()
def rep(s,old,new,count=1):
    n=s.count(old)
    assert n==count, f"expected {count} of:\n{old[:120]}\nfound {n}"
    return s.replace(old,new)

# ---------------- Parts I and II ----------------
m=main
m=rep(m,r"\date{Working draft, second edition \textperiodcentered{} 23 September 2026}",
        r"\date{Working draft, third edition \textperiodcentered{} 24 September 2026}")
m=rep(m,r"\newcommand{\Open}{\textcolor{openc}{\textsf{\footnotesize[open]}}}",
        r"\newcommand{\Open}{\textcolor{openc}{\textsf{\footnotesize[open]}}}"+"\n"+r"\newcommand{\Postulated}{\textcolor{choicec}{\textsf{\footnotesize[postulate]}}}")
m=rep(m,r"""over. Nothing quantum has appeared yet. Every result is labelled as derived, chosen, numerical or open.""",
r"""over.

Part III opens with the author's note on ticks and remainders, which restates the life-budget postulate: a
part's own time is its steps of $\eta$, counted from the whole, which approach $I$ but never reach it, and the
remainders of vanishing parts pass to other parts, the act of vanishing disturbing the field. If all clocks
agreed at once the remainders would rebuild $I$ and reality would cease; this never happens. The note closes
the discrepancy between the derived budget $2\eta_0$ and $I$, makes the remainder of Part I the
desynchronisation of the clocks, and, with vanishing as an act, gives the universe a set point of
desynchronisation near one tenth. Part III then builds a quantum layer: latency gives rotations by the imaginary unit, the linearised dynamics of any
network is lossless with an exactly conserved total, and single outcomes follow squared amplitudes of motion.
Two attempts to obtain the local circle symmetry of electromagnetism fail for identified structural reasons.
Every result is labelled as derived, chosen, numerical or open.""")
# notation table
m=rep(m,r"R & the remainder, $1-\sum_a\eta_a$ \\",
        r"R & the motion remainder, $1-\sum_a\eta_a$; also the desynchronisation of clocks (Chapter~\ref{ch:ticks}) \\"+"\n"+
        r"\Delta_a & a part's remainder when its clock stops, equal to $\eta_a$ (\ref{P:budget}, Chapter~\ref{ch:ticks}) \\")
# P6
m=rep(m,r"""coincides with the whole, $\eta_a\to0$ as $\delta_a\to0$, and over a life $\eta$ travels from near $1$
toward $0$. The quantity $\eta$ is a ratio, $\eta=\phi/\psi$, of what the part is in itself ($\phi$) to
its relation with the whole ($\psi$). \hfill(\Ch{15}; working notes III(a)--(c))""",
r"""coincides with the whole, $\eta_a\to0$ as $\delta_a\to0$, and over a life $\eta$ travels from near $1$
toward $0$. The quantity $\eta$ is a ratio, $\eta=\phi/\psi$, of what the part is in itself,
$\phi=f(\tau_a,\delta_a)$, to its relation with the whole, $\psi=R\bigl(f(\tau,\delta),f(\tau_a,\delta_a)\bigr)$.
\hfill(\Ch{15}; working notes III(a)--(c); the tick note \cite{ticknote})""")
# P7
m=rep(m,r"""\begin{postulate}[Life budget]\label{P:budget}
Summed over a part's steps, $\eta$ adds up to the full budget only in a special case; otherwise it falls
short by a remainder. \hfill(working notes III(d))
\end{postulate}""",
r"""\begin{postulate}[Ticks and remainders]\label{P:budget}
$\eta$ changes in discrete steps of stabilisation, and each step is a tick of the part's own clock, at a
time stamp drawn from a probability distribution set by the part's environment. Summed over a part's ticks,
the clock tends toward $I$ but never reaches it: when the part's clock stops, a remainder $\Delta_a$ is
left for other parts. A part whose clock completes vanishes, and the vanishing is itself an event that
disturbs the field. If all the clocks agreed at once, the remainders would add up to the whole and
reconstitute $I$, and reality would cease. \hfill(the tick note \cite{ticknote} and its clarification;
working notes III(d))
\end{postulate}
This replaces the life-budget postulate of the earlier editions, which let the sum reach its budget ``in a
special case'' and did not say what a step is. Chapter~\ref{ch:ticks} works out its consequences.""")
m=rep(m,r"""part lives strictly between being identical to the whole and having nothing left. A life adds up to its
budget only in a special case.""",
r"""part lives strictly between being identical to the whole and having nothing left. A part's clock ticks in
discrete steps that approach the whole's value but never reach it; what is left is its remainder, which it
leaves to other parts when it vanishes. If every clock agreed at once, the remainders would make up the whole
and reality would end.""")
m=rep(m,r"""If a life of $N$ steps has $\sum_n\eta_n=I-R$ with every $\eta_n<1$, then $N>I-R$.""",
        r"""If a clock of $N$ ticks has $\sum_n\eta_n=I-\Delta$ with every $\eta_n<1$, then $N>I-\Delta$.""")
# relational death
m=rep(m,r"""part when its remaining difference falls below what its neighbours can register, and its remainder is
then absorbed by them.""",
r"""part when its remaining difference falls below what its neighbours can register, and its remainder is
then left to them: its clock completes, and its vanishing disturbs the field around it
(Definition~\ref{def:vanish}).""")
# discrete time
m=rep(m,r"""\begin{corollary}[A part's own time is discrete]\label{cor:discrete} \Derived{}
A part's own time is the count of its exchanges.
\end{corollary}
\begin{proof}
By \ref{P:contact} a part changes only at exchanges. By \Ch{2}, a state with no change contains no
distinguishable event: repeated self-return $F(I_0)=I_0$ is not a sequence of events at all. So between
exchanges no internal time passes, and a part's own time advances in discrete steps, one per exchange.
\end{proof}""",
r"""\begin{corollary}[A part's own time is discrete]\label{cor:discrete} \Derived{}
A part's own time advances only at its ticks, the events that change its $\eta$: births, absorptions and
registrations. Exchanges do not advance it.
\end{corollary}
\begin{proof}
By \ref{P:budget} a part's clock advances only by steps of $\eta$. By \Ch{2}, a state with no change contains
no distinguishable event: repeated self-return $F(I_0)=I_0$ is not a sequence of events at all. The exchange
law conserves every $\eta$ (Theorem~\ref{thm:remainder}), so an exchange is not a tick
(Proposition~\ref{prop:notick}). A part's own time therefore advances in discrete ticks, one per event that
changes its $\eta$.
\end{proof}
The earlier editions counted exchanges. That conflicted with Corollary~\ref{cor:nobind} (exchange cannot make a
part age) and is corrected by the tick note.""")
m=rep(m,r"""A part that exchanges with nothing has no events. Its state is fixed, it reaches neither exit, and it
persists indefinitely while its own time stands still.""",
r"""A part with no events has a stopped clock. Its state is fixed, it reaches neither exit, and it persists
indefinitely with its remainder $\Delta_a=\eta_a$ (\ref{P:budget}).""")
# participant sum reading
m=rep(m,r"""Adding up every part's $\eta$ at one moment gives the whole's value only in a special case, when every
part is in the whole's proportion. Otherwise something is left over. This is the pattern of the working
notes (``adds up to $I$ in a special case, otherwise a remainder''), now across participants. What the
remainder \emph{is} becomes clear in Chapter~\ref{ch:exchange}: it is motion.""",
r"""Adding up every part's $\eta$ at one moment gives the whole's value only when every part is in the
whole's proportion. Since a part's remainder is its $\eta$ (\ref{P:budget}), this is the note's column of
remainders: they would add up to the whole only if every clock agreed with the whole's
(Theorem~\ref{thm:column}), which would end reality and never happens (Corollary~\ref{cor:noclosure}). What
the shortfall \emph{is} becomes clear in Chapter~\ref{ch:exchange}: it is motion.""")
m=rep(m,r"\begin{theorem}[The remainder]\label{thm:remainder}",r"\begin{theorem}[The motion remainder]\label{thm:remainder}")
m=rep(m,r"""``It adds up to $I$ only in a special case; otherwise a remainder is left'' turns out to be conservation
of energy. What is left over is motion, and it is zero only in a universe where nothing moves relative to
anything else.""",
r"""What the parts' remainders fall short of the whole by is motion. It measures how far the parts' clocks
disagree, and it would be zero only in a universe where nothing moves relative to anything else
(Theorem~\ref{thm:column}), which never happens (Corollary~\ref{cor:noclosure}).""")
# life in halvings
m=rep(m,r"""The life reaches its full budget $2\eta_0$ only if it is endless. Otherwise it falls short by exactly
$\eta_N$, the amount left at death, which is what the neighbours absorb
(Corollary~\ref{cor:relational}).
\end{corollary}
This is the pattern of \ref{P:budget}, with one difference: the budget comes out as $2\eta_0$ rather than
$I$. \Open""",
r"""Counted from the whole, as \ref{P:budget} requires (the whole has $\eta=1$ and is not itself a tick; the
first tick is the first halving), $\eta_n=2^{-n}$ and $\sum_{n=1}^{N}\eta_n=1-\eta_N$: the ticks tend to $I$ and
fall short by exactly the remainder $\eta_N$, which is what the neighbours absorb
(Corollary~\ref{cor:relational}).
\end{corollary}
Counting from the part's own birth and including its starting value gives a budget $2\eta_0$ instead of $I$;
that was an open problem in the earlier editions. Counting from the whole closes it
(Corollary~\ref{cor:budgetI}).""")
m=rep(m,r"""it starts high and tends toward zero in discrete steps, as the working notes proposed. Summed over a
life, it adds up to a fixed budget minus exactly what is left at death.""",
r"""it starts high and tends toward zero in discrete steps, as the working notes proposed. Counted from the
whole, its halvings add up to the whole's value minus exactly what is left when its clock stops.""")
# activity rule wording
m=rep(m,r"""\item \textbf{Activity belongs to processes, not amounts.} A part's own time is the count of its exchanges
  (Corollary~\ref{cor:discrete}). With no preferred scale, a part's clock cannot run faster because it is
  bigger or has more relations: every part ticks at the same rate.""",
r"""\item \textbf{Activity belongs to processes, not amounts.} A part's own time advances at its events
  (Corollary~\ref{cor:discrete}). With no preferred scale, a part's clock cannot run faster because it is
  bigger or has more relations: every part has events at the same rate.""")
m=rep(m,r"""Every part ticks at the same rate; at each tick it meets neighbour $j$ with probability proportional to
$e^{-\theta_j}$.""",
r"""Every part has events at the same rate; at each it meets neighbour $j$ with probability proportional to
$e^{-\theta_j}$.""")
m=rep(m,r"takes part more than once per tick. Strict one-encounter-per-tick matching has not been tested. \Open",
        r"takes part more than once per step. Strict one-encounter-per-step matching was tested in Part III: it gives the lossless layer (Chapter~\ref{ch:A2}).")
m=rep(m,r"""(A variant in which timelike pairs use the pair-matrix selection of \S6.5 behaves similarly.)""",
r"""(A variant in which timelike pairs use the pair-matrix selection of \S6.5 behaves similarly.)
In the third edition the absorbed part vanishes as an act: its continuity stays with the containing part and
its difference spreads to all its neighbours (Definition~\ref{def:vanish}). The numerical results of Part II
were obtained with silent absorption; Chapter~\ref{ch:ticks} rechecks those that bear on the change.""")
# summary chapter of Parts I-II
m=rep(m,r"\chapter{Where the derivation stands}\label{ch:summary}",r"\chapter{Where Parts I and II stand}\label{ch:summary}")
m=rep(m,r"""  \item \textbf{Circular phases.} Nothing quantum appears: the primitives give hyperbolic phases. The only
  hint is the $\pm i$ produced by latency in the two-part universe (Proposition~\ref{prop:delay2}).""",
r"""  \item \textbf{Circular phases.} Nothing quantum appears: the primitives give hyperbolic phases. The only
  hint is the $\pm i$ produced by latency in the two-part universe (Proposition~\ref{prop:delay2}).
  \emph{Resolved in Part III (Chapters~\ref{ch:A1}--\ref{ch:A3}).}""")
m=rep(m,r"""  \item \textbf{The budget.} The derived life sum is $2\eta_0$; the working notes say $I$.
  \item \textbf{Strict clocks.} One encounter per tick for both parties has not been tested.""",
r"""  \item \textbf{The budget.} The derived life sum is $2\eta_0$; the working notes say $I$.
  \emph{Resolved by the tick note: counted from the whole, the budget is $I$ (Corollary~\ref{cor:budgetI}).}
  \item \textbf{Strict clocks.} One encounter per tick for both parties has not been tested.
  \emph{Tested in Part III: one encounter per part per exchange step gives a lossless layer
  (Chapter~\ref{ch:A2}).}""")
m=rep(m,r"$x_a=\tau_a$, $y_a=\delta_a$ and $\eta_a=\sqrt{\tau_a\delta_a}$. The remainder is $R=1-\sum_a\eta_a$.",
        r"$x_a=\tau_a$, $y_a=\delta_a$ and $\eta_a=\sqrt{\tau_a\delta_a}$. The motion remainder (desynchronisation) is $R=1-\sum_a\eta_a$.")
m=rep(m,r"""\bibitem{handwritten} S.~Saket, handwritten notes,""",
r"""\bibitem{ticknote} S.~Saket, handwritten note, \emph{The stupidest postulate} and \emph{The stupid
hypothetical thought experiment} (ticks, remainders and the matrix of clocks), 24 September 2026.
\bibitem{handwritten} S.~Saket, handwritten notes,""")

# ---------------- Part III ----------------
body=p3.split(r"\setcounter{postulate}{7}")[1].split(r"\begin{thebibliography}")[0]
b=body
b=rep(b,"after a latency of $\\ell\\ge1$ ticks.","after a latency of $\\ell\\ge1$ exchange steps.")
b=rep(b,"In flux form the exchange law (Theorem~5.1) transfers","In flux form the exchange law (Theorem~\\ref{thm:exchange}) transfers")
b=rep(b,"exactly one and rotates by an odd multiple of $\\pi/(\\ell+1)$ per tick.","exactly one and rotates by an odd multiple of $\\pi/(\\ell+1)$ per exchange step.")
b=rep(b,"allowed exchange, $\\ell=1$, gives $\\lambda=\\pm i$: a quarter-turn per tick.","allowed exchange, $\\ell=1$, gives $\\lambda=\\pm i$: a quarter-turn per exchange step.")
b=rep(b,"4{,}096 ticks, the measured","4{,}096 exchange steps, the measured")
b=rep(b,"""If a part feels its partner's difference one tick late, the pair's imbalance never grows or dies: it goes
round a circle, a quarter-turn per tick. That quarter-turn is the number $i$.""",
"""If a part feels its partner's difference one exchange late, the pair's imbalance never grows or dies: it
goes round a circle, a quarter-turn per exchange. That quarter-turn is the number $i$. Exchanges are not
ticks of anyone's clock (Proposition~\\ref{prop:notick}), so this rotation happens between ticks.""")
b=rep(b,r"\section{One encounter per part per tick}",r"\section{One encounter per part per exchange step}")
b=rep(b,"so a part takes part in at most one encounter per tick.","so a part takes part in at most one encounter per exchange step.")
b=rep(b,"relation instead exchanged every tick, parts took several encounters per tick and the network blew up.",
        "relation instead exchanged at every step, parts took several encounters per step and the network blew up.")
b=rep(b,"It follows from Theorem~5.1 (the exchange law is a swap of shares) and Proposition~1.1 (only ratios are",
        "It follows from Theorem~\\ref{thm:exchange} (the exchange law is a swap of shares) and Proposition~\\ref{prop:ratios} (only ratios are")
b=rep(b,"""processes, each with rate proportional to its local squared amplitude.""","""processes, each with rate proportional to its local squared amplitude.""")
b=rep(b,"""Detection by the surroundings needs three steps: registrations at random moments (the activity rule is
stochastic, \\Derived{}); extra registration set by squared amplitude (\\Derived{}); and the first registration
taking the whole quantum. The last is not derivable from local rules. It was adopted:

\\begin{postulate}[Whole units]\\label{post:whole}\\Postulated{}
A quantum of difference, one halving's worth, exists only as a whole. A spread-out quantum is not located at
any part until it is registered, and registering it means registering all of it, at one place.
(\\Ch{17} read strictly.)
\\end{postulate}

With Postulate~\\ref{post:whole},""",
"""Detection by the surroundings needs three steps: registrations at random moments (the activity rule is
stochastic, \\Derived{}); extra registration set by squared amplitude (\\Derived{}); and the first registration
taking the whole quantum. The last does not follow from the local exchange rules. It follows from the tick
postulate:

\\begin{proposition}[Whole units]\\label{post:whole}\\Derived{}
A registration is a tick, and by \\ref{P:budget} a tick is one discrete step of $\\eta$; by
Proposition~\\ref{prop:halving} the step is a halving. So a quantum of difference, one halving's worth, is
registered whole, at one place, or not at all. A spread-out quantum is not located at any part until then.
\\end{proposition}
\\begin{remark}
In the first draft of Part III this was adopted as a separate Postulate~8, a strict reading of \\Ch{17}. The
tick note makes it a consequence of \\ref{P:budget}, and the list of postulates returns to seven.
\\end{remark}

With Proposition~\\ref{post:whole},""")
b=rep(b,"Outcome statistics follow squared motion amplitude & \\Postulated{} (P8) / \\Numerical{} \\\\",
        "Outcome statistics follow squared motion amplitude & \\Derived{} (from \\ref{P:budget}) / \\Numerical{} \\\\")
b=rep(b,"Whole units (P8); outcomes follow squared motion amplitude & \\Postulated{} / \\Numerical{} \\\\",
        "Ticks from the whole; budget $I$; all clocks agreeing would end reality, so $R>0$ always & \\Derived{} \\\\\n"
        "With vanishing as an act, desynchronisation holds at 0.07--0.12; reality never closes & \\Derived{} / \\Numerical{} \\\\\n"
        "Whole units (from the tick postulate); outcomes follow squared motion amplitude & \\Derived{} / \\Numerical{} \\\\")
b=rep(b,"statistics (with P8), exact relativity","statistics, exact relativity")
b=rep(b,"""relations' memories never changes; and, once a quantum is taken to exist only as a whole, single outcomes
follow squared amplitudes of motion.""",
"""relations' memories never changes; and, because a registration is one whole tick, single outcomes follow
squared amplitudes of motion. A part's own clock ticks only when its $\\eta$ changes; counted from the whole, its
ticks approach the whole's value and never reach it. When a clock completes, its part vanishes, leaving its
remainder to others and disturbing the field, and those disturbances keep the clocks from ever all agreeing,
which would end reality.""")
b=rep(b,"""\\item \\textbf{Fringes and latency} \\Open{}. A clean driven two-path test; what sets $\\ell$.""",
"""\\item \\textbf{Fringes and latency} \\Open{}. A clean driven two-path test; what sets $\\ell$.
\\item \\textbf{Part II under vanishing} \\Open{}. The horizon and binding analyses used silent absorption and
have not been repeated with vanishing as an act.
\\item \\textbf{The note's closing questions} (free will, and what the author leaves unsaid) are outside the
mathematics.""")
b=rep(b,"""loops of composites act as flux. This would be Part~II's ``curvature is staleness'' with a circle in place
of boosts.""","""loops of composites act as flux. This would be Part~II's ``curvature is staleness'' with a circle in place
of boosts. The tick postulate makes tick times random and environment-dependent, so record ages do vary: the
premise of this lead is now part of the postulates.""")
b=rep(b,r"\texttt{quantum/}, \texttt{gauge/} and \texttt{composite/}.",
        r"\texttt{quantum/}, \texttt{gauge/}, \texttt{composite/} and \texttt{ticks/}. The synchronisation tests run the causal event rule with the derived activity rule (Part II), with silent absorption or with vanishing as an act, and record $R$ every 50{,}000--100{,}000 events; space is measured by breadth-first ball growth from 40 ordinary parts.")
b=rep(b,r"\chapter*{Numerical methods for this part}"+"\n"+r"\addcontentsline{toc}{chapter}{Numerical methods for this part}",
        r"\chapter*{Numerical methods for Part III}"+"\n"+r"\addcontentsline{toc}{chapter}{Numerical methods for Part III}")
b=rep(b,"""Stage A is complete (Chapters~\\ref{ch:A1}--\\ref{ch:A3}).""","""Stage A is complete (Chapters~\\ref{ch:A1}--\\ref{ch:A3}), with the tick postulate of
Chapter~\\ref{ch:ticks} in place.""")
part3=(r"""
% =====================================================================
\part*{Part III: The tick postulate, the quantum layer and the search for a first force}
\addcontentsline{toc}{part}{Part III: The tick postulate, the quantum layer and the search for a first force}
"""+ticks+b)
m=rep(m,"\n\n\\appendix\n",part3+"\n\n\\appendix\n")
open('delta_theory_mathematics_3rd.tex','w').write(m)
print("ok", len(m))
