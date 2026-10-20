# Sulfur prices and the supply chain from refineries to phosphate fertilizer

Data and code behind a Data 4 The People report on sulfur, a leftover from oil and gas processing that fertilizer makers need to make phosphate fertilizer. It tracks the price of sulfur, sulfuric acid, DAP fertilizer and diesel since January 2024, and the stocks of sulfur that public data can see.

## Live links

- Sulfur price tracker: https://data4thepeople.github.io/Sulfur/
- Published report: https://www.data4thepeople.com/p/sulfur-shortage

## What's here

- `posts/sulfur-shortage/POST.md`: the text of the report, with its chart images in `images/`.
- `DATASETS.md`: one section per data source, with coverage, revisions and known problems, plus the method for every figure we calculated.
- `TIEOUT.md`: results of the tie-out, which recomputes every number on the charts and page from the raw files.
- `research/BRIEF.md`: research notes, with the source for each fact and how sure we are of it.
- `data/raw/`: files as downloaded from each agency, with the pull date in `pulled.txt`.
- `data/manual/`: small tables keyed by hand from USGS publications and from trade press reports.
- `data/processed/`: `series.json`, the one file the charts, the tracker and the tie-out all read.
- `charts/`: the static chart PNGs, and `numbers.json` with the values each chart uses.
- `src/template.html`: the tracker page template.
- `dist/` and `docs/`: the built tracker page. GitHub Pages serves `docs/`.
- `scripts/`: the fetch, processing, chart, build and tie-out scripts.
- `run.sh`: rebuilds everything in order.

## Data sources

| Agency | Dataset | Used for |
|---|---|---|
| U.S. Census Bureau | International trade in goods, 10-digit (USA Trade API) | Sulfur export value per ton |
| U.S. Geological Survey | Mineral Industry Surveys, Sulfur, monthly | U.S. producer stocks and shipments |
| U.S. Geological Survey | Mineral Commodity Summaries 2026, Sulfur | Sulfur production by country |
| World Bank | Commodity Price Data ("Pink Sheet"), monthly | DAP, phosphate rock, urea and Brent crude prices |
| Bureau of Labor Statistics, via FRED | Producer Price Index series | Sulfuric acid, phosphates and diesel price indexes |
| USDA Agricultural Marketing Service | Illinois Production Cost Report (slug 3195) | Fertilizer and farm diesel asking prices |
| U.S. Energy Information Administration | Weekly petroleum data | Retail diesel price, distillate stocks and days of supply |
| Statistics Canada | Table 25-10-0036-01 | Sulphur supplied by Canadian gas plants |
| Alberta Energy Regulator | ST3 Supply and Disposition of Sulphur | Alberta's sulphur stockpile |
| Trade press (Argus, CRU, World Fertilizer, SunSirs, SMM, Mysteel) | Our compilation of published figures | Adnoc posted sulfur price and China port stocks |

Details, caveats and attribution for each source are in `DATASETS.md`.

## How to rebuild

Requirements:

- Python 3 in a virtual environment at `.venv/`, with `matplotlib`, `numpy`, `openpyxl` and `Pillow`.
- Google Chrome, used in headless mode to render the flow diagram and to test the tracker page. `scripts/build.py` expects it at the standard macOS path.
- Three free API keys for the fetch step: `CENSUS_API_KEY`, `EIA_API_KEY` and `USDA_MARS_API_KEY`. The scripts load keys from a private env file outside this repo, so you will need to supply your own. FRED, the World Bank, USGS, Statistics Canada and the Alberta Energy Regulator need no key.

Rebuild from the raw files already in `data/raw/`:

```sh
./run.sh
```

Pull fresh data first, then rebuild:

```sh
./run.sh --fetch
```

`run.sh` runs these steps from `scripts/`, in order:

1. With `--fetch`: `fetch_eia.py`, `fetch_fred.py`, `fetch_usda.py`, `fetch_worldbank.py`, `fetch_usgs.py`, `fetch_census.py`, `fetch_statcan.py`, `fetch_aer.py`.
2. `process.py`: turns the raw pulls into `data/processed/series.json`.
3. `charts.py`: draws the chart PNGs and writes `charts/numbers.json`.
4. `flow.py` and `molecule.py`: draw the supply-chain diagram and the dibenzothiophene drawing.
5. `post_images.py`: copies the charts into the post's `images/` folder.
6. `build.py`: builds `dist/index.html`, copies it to `docs/index.html`, and checks it runs in Chrome without errors.
7. `tieout.py`: recomputes every number from the raw files without using pipeline code, writes `TIEOUT.md`, and fails on any mismatch.

`scripts/animate.py` is not part of `run.sh`. It makes an animated GIF of the price chart for social posts.

## Method notes

- There is no free market price for elemental sulfur. Our sulfur price is the Census export value per ton: total dollars divided by total metric tons for the crude and refined sulfur codes combined. It is an average from customs records, not a market quote, so it lags the market and moves when the mix of cargoes changes.
- Percent changes use two base months: January 2024 and February 2026, the last full month before the February 28, 2026 strikes. Each series runs to the latest full month its own source has published, so end months differ.
- Months with very little sulfur exported (under a third of the median month since January 2024) are marked with an open circle on the charts and the tracker.
- The Gulf share of world production adds Iran, Kuwait, Qatar, Saudi Arabia and the United Arab Emirates and divides by the USGS printed world total for 2025.
- The sulfur cost in a ton of DAP uses 0.4 tons of sulfur per ton of DAP, from Mosaic's 2025 annual report, times our sulfur price.

---

Data 4 The People
