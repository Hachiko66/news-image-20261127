[![make.fun](https://make.fun/badge/news-image-20261127.svg)](https://make.fun/bounty/news-image-20261127)
[![rank](https://make.fun/badge/news-image-20261127/Hachiko66/news-image-20261127/rank.svg)](https://make.fun/bounty/news-image-20261127)
[![reward](https://make.fun/badge/news-image-20261127/Hachiko66/news-image-20261127/reward.svg)](https://make.fun/bounty/news-image-20261127)

# news-image-20261127

One image summing up the world's news of Friday 27 November 2026, drawn as a newspaper front page: a Thanksgiving storm slams the US Northeast and postpones the 100th Macy's parade; Zelenskyy warns of new Russian strikes on Ukraine's power grid as EU leaders split over a €45bn loan; a fire engulfs a Bangkok oil refinery; two Italians are killed in a drone attack in Kuwait; Vietnam races to finish a US trade deal; and New Zealand's final election count is due.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

`main.py` draws the front page with Pillow (bundled subset DejaVu fonts in `fonts/`, so it renders identically anywhere) and writes `entry.png` (1024x1024 PNG, under 1 MiB). Every run writes the same bytes: fixed layout, fixed palette, no randomness, no network, no timestamps.

## License

MIT — see [LICENSE](LICENSE). The bundled fonts are subsets of DejaVu (free license, see the DejaVu license).
