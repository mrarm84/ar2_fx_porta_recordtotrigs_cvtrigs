# Listing on elektronmods.com

elektronmods.com is an independent forum (not Elektron's) with a "GitHub Mod
List" (mods.php). A mod is listed as a card linking to its repository: author,
description, device tags, version. Its rules (thread 4, by the admin) are the
ones this repository already follows:

- Rule 1, "Firmware stays with Elektron": no uploads, messages or links to
  original or modified firmware, especially `.syx`. Links to Elektron's own
  download page are fine.
- Rule 2, "Patchers instead of patched firmware": asked for a finished file,
  point to the patcher or the project page.
- Rule 4: have the rights to what you share; credit original authors.

## Before submitting

1. `make check-clean`: every tracked file is free of firmware.
2. Read the history too: `git log --all --name-only --format= | grep -i '\.syx$'`
   prints nothing (checked 2026-11-26: no `.syx` or `.bin` was ever committed).
3. `make package`, if the maintainers want a zip rather than a link: it is
   `build/package/rytm-mods-lite-<commit>.zip`, HEAD's tracked files only.
4. Never attach or link a build (`build/*.syx`, `../rytm_syx_builds`).

## The listing

Submitted while logged in (forum, Google, Apple or GitHub account) through
"Add Mod" on mods.php. The form's fields could not be read logged out; these
are the texts to fill them from.

**Name:** rytm-mods lite: FX, portamento, live loops, CV trigs

**Author:** mrarm84, on MrScruff's rytm-mods

**Repository:** https://github.com/mrarm84/ar2_fx_porta_recordtotrigs_cvtrigs

**Devices:** Analog Rytm MKII (OS 1.73)

**Version:** the commit on `main`

**Short description:**

> Source mods for the Analog Rytm MKII OS 1.73, built on MrScruff's rytm-mods:
> new DG machines, REVERB 2 effects, portamento with trig locks, four live
> loops, CV/audio gate trigs. Ships patches, not firmware: you supply the stock
> OS file from Elektron and build on your own computer.

**Description:**

> A patcher for the Analog Rytm MKII, OS 1.73. Each mod is assembler source
> with a manifest; the build checks your stock OS against its SHA-256, refuses
> any other file, patches only the MAIN OS section and verifies every other
> section comes back byte-identical. No Elektron firmware is included.
>
> New here: nine digital machines (DG SINE, SAW, PULSE, FM2, ORGAN, CHORD,
> SUPER, PLUCK, CHIP), rewritten to cost about half the audio interrupt;
> REVERB 2 (width, darken, saturation, auto-pan), a phaser and a DIST filter;
> portamento for every machine, lockable per step on the TRIG page; per-sound
> DEGRADE (downsample, bit depth); four live loops on tracks 1, 2, 5 and 6 that
> play while recording; CTRL IN and AUDIO IN gates trigger tracks; PERF pads
> push their track; a leaner audio interrupt.
>
> From MrScruff's rytm-mods (GPL-2.0, with permission): euclid accents, LFO RND
> random modifiers, kit A/B, CTRL ALL, ENV RESET on AMP, DAC SUM.
>
> Use at your own risk: most of the new mods are emulator-tested and not yet
> run on a unit; each mod's README gives its status.

**Credits:** MrScruff (rytm-mods; mods 0000, 0002, 0004, 0010, 0013, 0014,
0015 and the build tools), Iced-Cream and Connor Way (publishing
rytm-mods-src), mischa85 (elektron-firmware-tool, fetched at build time).

**Licence:** GPL-2.0, as upstream.
