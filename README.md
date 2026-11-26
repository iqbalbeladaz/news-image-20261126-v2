# The World in One Day — 26 November 2026

[![make.fun](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/iqbalbeladaz/news-image-20261126-v2/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/iqbalbeladaz/news-image-20261126-v2/reward.svg)](https://make.fun/bounty/news-image-20261126)

A broadsheet front page summing up the world's news of **Thursday, 26 November 2026** in one image.

## The image

`entry.png` (1024×1024) is a newspaper front page, "THE WORLD IN ONE DAY":

- **Lead story:** the Nasdaq plunges 4% as the AI sell-off deepens, Nvidia down 8.6%, and Trump's new tariff plan for 14 trading partners.
- **Six story cards:** Bangladesh raises garment pay 36% after protests; North Korea orders Switzerland's Pyongyang office shut; India marks Constitution Day and 18 years since the 26/11 Mumbai attacks; 15-year-old Vaibhav Sooryavanshi smashes 204 off 53 balls; a South African court backs Ramaphosa in the Phala Phala case; a 5.6-magnitude quake hits Koshi, Nepal, while Gukesh faces Sindarov in Geneva.
- **The Day in Numbers:** Nasdaq −4.0%, Nvidia −8.6%, 204 off 53, 1,220 IPL sign-ups, +36% pay rise, quake 5.6.
- **Also today:** Hasina's planned return, the Greek cost-of-living strike, the Pope on COP31, Bulgaria's migrant rescue, the Flipkart CEO stepping down, and US consumer confidence at a near two-year high.

Every event was first reported on 26 November 2026.

## How it is built

`generate.py` draws the page from scratch with Pillow (no network, no downloaded assets) and writes `entry.png`. `main.ts` copies that image to `/output/entry.png` when the entry runs.

```sh
python3 generate.py          # regenerate entry.png
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## Bounty

[Sum up 26 November's world news in one image — make.fun](https://make.fun/bounty/news-image-20261126)

License: MIT.
