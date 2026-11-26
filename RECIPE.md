# Recipe: the lite-live firmware, from a stock OS you download

This repository holds no firmware. You download the stock OS from Elektron and
the patcher in this repository builds the modded image from it. Here is the
exact recipe for the build this tree was released at (build 42, the four live
loops).

## Ingredients

| what | where | check |
|---|---|---|
| Analog Rytm MKII **OS 1.73**, stock | Elektron's support site | SHA-256 `8ad671087ec30433d5407c7380d2396e0915ab931c5d3dd18a78bf284d3d1e52` (`stock/SHA256SUMS`) |
| Python 3, venv, git, make, gcc | your OS's packages | |
| m68k binutils: `m68k-elf-as`, `-ld`, `-objcopy`, `-objdump` | `binutils-m68k-linux-gnu` (link `m68k-linux-gnu-*` to `m68k-elf-*`), or `brew install m68k-elf-binutils` | |
| elektron-firmware-tool (mischa85), pinned to `a5bce9a` | fetched by `make setup` | |

Linux, macOS, or Windows through WSL (Ubuntu).

## Steps

    git clone https://github.com/mrarm84/ar2_fx_porta_recordtotrigs_cvtrigs
    cd ar2_fx_porta_recordtotrigs_cvtrigs
    cp ~/Downloads/Analog-Rytm_MKII_OS1.73.syx stock/
    make setup        # once: the venv and the pinned container tool
    make verify       # builds every enabled mod, then verifies the image

The build refuses a stock file whose hash differs from the one above.

## What goes in

Every mod whose `mod.toml` says `enabled = true`, in this order:

| mod | what you get |
|---|---|
| 0000 shared | the runtime the other mods call |
| 0002 euclid-accents | the euclidean generator places accents |
| 0004 lfo-rnd | LFO RND page: random modifiers; SYN and SMP; DEGRADE knobs |
| 0010 kit-ab | NO + PLAY flips edited and saved kit |
| 0013 voice-dac | DAC SUM; degrade (SRD, BIT); **portamento** (GLD, TIM) with trig locks |
| 0014 ctrl-all | TRK + knob sets every sound track |
| 0015 env-reset-amp | ENV RESET restarts the amp envelope |
| 0019 reverb-srr | **FX**: phaser on REVERB, REVERB 2 page, a filter on DISTORTION |
| 0020 cv-trig | **CV trigs**: CTRL IN and AUDIO IN gates play tracks |
| 0021 dg-machines | DG SINE, SAW, PULSE, FM2, ORGAN, CHORD, SUPER, PLUCK, CHIP |
| 0022 fx-ram | delay RAM halved, 2 MB for 0019 and 0021 |
| 0024 lean | half-rate smoothing; performance locks and CV modulation out |
| 0025 perf-push | PERF pads push their track |
| 0027 sample-skip | silent sample voices skipped |
| 0028 live-slot | **record to trigs**: tracks 1, 2, 5, 6 record into slots 124..127 and play while recording |

Left out: 0023 isr-meter (measuring only; it shares cave space with 0028) and
0026 cache (retracted).

## What comes out

    build/Analog-Rytm_MKII_OS1.73_0000_0002_0004_0010_0013_0014_0015_0019_0020_0021_0022_0024_0025_0027_0028.syx

SHA-256 of the released build:
`e4953a9c975ce077b1ddc063e4377e739bea5bdc317b597d069b17c0cdda9708`. The build
is deterministic, so the same stock file and this tree give the same hash.

Send it to the Rytm as an OS update over USB (Elektron Transfer or any SysEx
tool); see `docs/FLASHING.md`, and read `docs/HAZARDS.md` first. Keep the stock
`.syx` to go back. Most of the lite changes have not been run on a unit: use
at your own risk.

## Variations

- Only some mods: `.venv/bin/python tools/build.py --mods 0000-shared 0013-voice-dac 0028-live-slot`
  (most mods need 0000).
- With the meter instead of the live loops: `--mods` without 0028, plus
  `0023-isr-meter`; read its numbers with `tools/isr_meter.py`.
- A name for the output: `make verify TAG=mine`.

Do not commit or share what comes out: every image contains Elektron's stock
OS. `make check-clean` proves the tree holds none.
