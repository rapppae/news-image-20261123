# World news poster — Monday 23 November 2026

Entry for the make.fun competition
[news-image-20261123](https://make.fun/bounty/news-image-20261123):
one image summing up the world's news of Monday 23 November 2026.

## The image

`entry.png` (1024x1024) is a front-page poster, "THE WORLD TODAY",
drawn procedurally by `draw.py` with the Python standard library only
(no Pillow, no network). Ten stories from the day:

- **Lead:** a Russian cargo ship still burning off Finland after a
  drone strike in the Baltic Sea.
- 14 missing after a Russian drone hit a building in the Kyiv region.
- Factory fire in Indonesia: several dead, dozens missing.
- COP31: Turkiye's final draft makes no mention of fossil fuels.
- South Korea's education minister resigns over an AI exam-cheating
  scandal.
- Nepal PM Balendra Shah's state visit to India, talks with PM Modi.
- India smash a record 720/9d in the Wellington Test vs New Zealand.
- UN states agree to keep negotiating on lethal autonomous weapons.
- Migrant boat capsizes off Senegal: at least 4 dead, dozens missing.
- Thousands march in Lisbon over the cost of living.

## How it runs

`main.py` (stdlib only) copies `entry.png` to
`$MAKEFUN_OUTPUT_DIR/entry.png` (default `out/`). Running it twice
produces byte-identical output. Regenerate the poster with:

```sh
python3 draw.py
```

## Files

- `main.py` — entrypoint, copies `entry.png` to the output dir.
- `draw.py` — the poster renderer (stdlib PNG encoder + 5x7 bitmap font).
- `entry.png` — the poster, 1024x1024.
- `LICENSE` — MIT.
