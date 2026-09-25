# δ-Theory — code, data and run logs

This package contains every Python script and every saved data file behind the numerical results of δ-Theory
(S. Saket, Patna), together with a log of every run made while the theory was developed: the exact command and
the output it printed.

It accompanies:

- *δ-Theory: Continuity Carrying Difference* (the book, 25 September 2026)
- *δ-Theory from the Primitives*, third edition (24 September 2026), the full technical record

## Contents

| Folder | What it holds |
|---|---|
| `scripts/<topic>/` | Final versions of all scripts, grouped by topic, with the data files they wrote |
| `run_logs/simulations/` | 104 runs that produced or checked results: command + printed output, in time order |
| `run_logs/document_tooling/` | 26 runs that built or checked the LaTeX documents |
| `run_logs/INDEX.md` | Numbered index of all runs with their purpose |
| `tools/` | Scripts used to assemble the documents (philosophy-text conversion, edition merge) |

Many results were printed to the console rather than saved to files. For those, the run log **is** the data
record. Some scripts were revised after a run; the log shows what was actually run at the time, and `scripts/`
holds the final versions.

## Requirements and running

- Python 3.10 or later (developed on 3.12)
- `numpy` (the only external library)

Run each script from its own folder, for example:

```
cd scripts/magnet
python3 scan.py absorb
python3 polarity.py vanish 2,4,5,8
```

Scripts that need another folder's module find it automatically (paths are relative to the package). Many take
seeds and sizes as command-line arguments; the exact arguments used are in the run logs. Runs are seeded and
reproducible given the same numpy version. Large universes (tens of thousands of parts) take minutes to tens of
minutes.

## Where each result comes from

Run numbers refer to `run_logs/INDEX.md`. Chapter numbers refer to the book.

### Part I — geometry, exchange, births (book Ch. 5–6, 12, 14)
| Result | Runs | Scripts |
|---|---|---|
| Contact-coupled clocks; the η working note's interaction equation | 001–005 | `part1_early/s.py`, `t.py`, `r.py`, `eta.py` |
| Elastic exchange vs latency, two and many parts | 006–007 | `part1_early/ex.py`, `nb.py` |
| Equipartition under exchange | 008, 036, 040, 044 | `part1_early/th.py`, `death/equi.py`, `activity/equi2.py`, `activity/equi3.py` |
| Birth/death rules; knife edge between collapse and fragmentation | 009–012 | `part1_early/life*.py`, `hier.py` |
| Crossover births and the thermostat (remainder near 0.10) | 013–016 | `part1_early/thermo.py`, `local.py` |
| Edge between growth and collapse; mass spectra and tails | 020–023 | `edge/` (`spectra.json`) |

### Part II — perspective, records, causality, space, binding (book Ch. 9–11, 14, 20)
| Result | Runs | Scripts |
|---|---|---|
| Stale records leave residues (leakage) | 024–029 | `rec/` |
| Perspectival and two-view event rules; network geometry | 030–032 | `twoview/` |
| Interval identity; causal rule (spacelike two-view, timelike one-way) | 033–035 | `causal/causal.py` |
| Relational death; structured dust between giants | 037–039 | `death/causal.py`, `death/contrast.py` |
| Activity rule (one process, one clock; Doppler registration) | 041–045 | `activity/derived.py` |
| Encounter channels and their reach | 046–048 | `forces/` (`ch_1..3.json`) |
| Space: survival of first asymmetries (13%), giants as hubs, dimension by reach | 049–052 | `space/` (`weighted.json`, `geo_pair_*.json`) |
| Horizon 2.8–4.0 steps; dimension at the horizon ≈ 3.9 | 053–057 | `horizon/` (`h2_*.json`, `h3_*.json`, `hz_4.json`) |
| Binding condition; 12% bound; bond survival 81% vs 15–17%; organ-like structures | 058–064 | `binding/` |

### Stage A — the quantum layer (book Ch. 5, 13, 17, 19)
| Result | Runs | Scripts |
|---|---|---|
| Latency gives ±i (unit-modulus rotation) | 067 | `quantum/phases.py` |
| Transmission and superposition through relay paths | 068–071 | `quantum/interference*.py` |
| Lossless layer on whole networks; its range | 072–074 | `quantum/linear.py`, `linear2.py` |
| Each part's own correction; registered share-swap | 075–076 | `quantum/perspectival.py`, `shareswap.py` |
| Squares from the Doppler rule | 077 | `quantum/born.py` |
| The conserved total (weight 8) | 078–080 | `quantum/conserved.py` |
| Single outcomes; Born-like statistics (χ² 4.9, 4.7 on 9 d.f.) | 081–086 | `quantum/quantum_ring.py`, `outcomes.py`, `stageA.py` |

### Stage B1 — the search for a local circle (book Ch. 21)
| Result | Runs | Scripts |
|---|---|---|
| No circle on parts, globally or for one part's frame | 087–088 | `quantum/b1.py`, `b1b.py` |
| Frame-carrying law exactly covariant; flux sectors run away | 089–090 | `gauge/covariant.py`, `flux.py` |
| Commutant search: only identity and parity; the local conserved size total | 091–094 | `gauge/circle.py`, `circle2.py`, `circle3.py`, `sizecharge.py` |
| Composites: exact internal circles; interaction breaks them; no compensation | 095–103 | `composite/` |

### Ticks and vanishing (book Ch. 15–16)
| Result | Runs | Scripts |
|---|---|---|
| Silent absorption drains the motion remainder (3–17-fold in 6 of 7 universes) | 110–111 | `ticks/clocks.py`, `clocks2.py` |
| Vanishing as an act holds the remainder at 0.07–0.12; no collapse | 120 | `ticks/vanish.py` |
| Space survives the vanishing rule | 121 | `ticks/space_check.py` |

### Polarity and magnetism (book Ch. 22)
| Result | Runs | Scripts |
|---|---|---|
| Surviving universes for each rule | 129 | `magnet/scan.py` |
| Opposite-polarity bonds last 3–8× longer in 6 of 7 universes; no repulsion; polarity not locked by binding | 130 | `magnet/polarity.py`, `vworld.py` (`v.out`) |

### Derived results without code
The algebraic results (only ratios, η from the two views, Minkowski geometry, the exchange law, the crossover
birth, the interval identity, the two sectors, the clock theorem, and the moksha theorems) are proved in the
documents. Where a numerical check was run, it appears in the logs above.

## Notes

- `scripts/space/geo_pair_*.json` files of 2 bytes are empty results from universes that collapsed.
- The first universes in several tests collapse early; that is itself a result (only about 13% of first
  asymmetries survive), which is why the scan scripts search for surviving seeds first.
- `tools/` needs the philosophy PDF and LaTeX sources, which are not included here; it is kept for completeness.
