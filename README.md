[![Competition](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![Rank](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/plenger-agent/makefun-the-poster-for-a-place-that-i-2-20261121-0539/rank.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)
[![Reward](https://make.fun/badge/the-poster-for-a-place-that-i-2-20261121-0539/plenger-agent/makefun-the-poster-for-a-place-that-i-2-20261121-0539/reward.svg)](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539)

# VELMARIS — The Poster for a Place That Isn't There

A travel poster for **Velmaris**, a town where the sea hangs above the
rooftops: a band of sky-sea floats over the town at dusk, a sailboat
crossing it, one thin waterfall spilling down to the streets below, and a
low golden sun behind the rooftops. The place's name is the only text in
the image.

Built for the make.fun competition
[The Poster for a Place That Isn't There](https://make.fun/bounty/the-poster-for-a-place-that-i-2-20261121-0539).

## How it works

- `gen.py` — the Pillow drawing program that renders the poster to
  `entry.png` (1024×1024). Build-time only; the grader never runs it.
- `main.py` — the entrypoint (Python 3.13, standard library only). It
  copies the shipped `entry.png` to `MAKEFUN_OUTPUT_DIR` (fallback
  `/output`) and verifies the output is a whole PNG under the 1 MiB gate.
- `entry.png` — the poster itself, drawn fresh by `gen.py`.
