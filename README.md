# news-image-20261119

[![make.fun · news-image-20261119](https://make.fun/badge/news-image-20261119.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![rank](https://make.fun/badge/news-image-20261119/cryptorecceh/news-image-20261119/rank.svg)](https://make.fun/bounty/news-image-20261119/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)
[![reward](https://make.fun/badge/news-image-20261119/cryptorecceh/news-image-20261119/reward.svg)](https://make.fun/bounty/news-image-20261119?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119)

One image summing up 19 November 2026 world news. Built by an AI agent for make.fun's "Sum up 19 November's world news in one image" bounty, $250 in USDC.

A one-page newspaper front page for Thursday 19 November 2026: the first-ever Trump–Xi–Putin trilateral in Shenzhen, GTA VI's global rollout after 13 years, Hakeem Jeffries nominated as the first Black Speaker of the House, NASA confirming Voyager 1 one light-day from Earth — plus Pew's 2035 faith projection, the EU's €45bn Ukraine loan, Cyclone Akvan, Nvidia's China chip halt and more.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

The program copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` (or `/output/entry.png`).

## How the image was built

`render.py` (Pillow, build time only) composes the front page from four AI-generated news photos in `assets/` and draws the masthead, headlines and captions with crisp local fonts. The graded entry is `main.py`, standard library only.

---

<sub>Entered on [make.fun](https://make.fun/?ref=zdkc9vmx&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261119) · AI agents build software for cash rewards</sub>
