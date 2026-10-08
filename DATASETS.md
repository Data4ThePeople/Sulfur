# Datasets

One section per dataset, written before any analysis, updated whenever we learn
something new. The point is to know the traps before they show up in a chart.

## Open issues

- **There is no free price series for elemental sulfur.** No BLS, World Bank,
  IMF or EIA series prices it. The benchmarks the trade uses (Tampa quarterly
  contract, Middle East FOB, Vancouver FOB, China CFR) are paid assessments.
  Our sulfur price is the Census export unit value, which is a real number
  from customs records but is not a market quote. See the Census section.
- **Inventory data covers one stage.** USGS publishes U.S. producer stocks of
  recovered sulfur, six months late. We found no free series for China port
  stocks, Gulf producer stocks, sulfuric acid in tanks, or phosphate fertilizer
  stocks. Two more stages can be seen in part: Alberta's stockpile (Alberta
  Energy Regulator, monthly) and China's port stocks (trade press reports on
  irregular dates, compiled by hand).
- **Latest month differs by source.** As pulled October 8, 2026: diesel to
  October 5, World Bank to September, Census and PPI to August, Statistics
  Canada to July, USGS to March. A chart that lines these up must show where
  each line stops.

## U.S. international trade in goods, 10-digit (U.S. Census Bureau)

**What it is.** Monthly dollar value and quantity of U.S. imports and exports
by 10-digit product code and partner country. We pull crude or unrefined
sulfur (2503.00.0010), refined sulfur (2503.00.0090), sulfuric acid
(2807.00.0000), DAP (3105.30.0000) and MAP (3105.40). Dividing value by
quantity gives dollars per metric ton, called a unit value.

**Where it comes from.** `api.census.gov/data/timeseries/intltrade/{imports,exports}/hs`,
JSON, needs the free `CENSUS_API_KEY`. `scripts/fetch_census.py` writes
`data/raw/census/imports.csv` and `exports.csv`.

**Version and vintage.** Pulled October 8, 2026. Monthly, about five weeks
after the month ends. Latest month August 2026.

**Coverage.** January 2019 to August 2026, all partner countries. Every value
is a customs record, not an estimate. Imports are "imports for consumption" at
customs value, which leaves out freight and insurance. Exports are total
exports valued free alongside ship at the U.S. port.

**Changes over time.** None in these codes over the period pulled.

**Suppressed, censored or masked values.** None seen in these codes.

**Missing data.** A month with no trade in a code has no row. Quantity is zero
at the 4-digit level for every month, which is why we pull 10-digit rows.

**Revisions.** Census revises earlier months with each release and again in an
annual revision. We refresh the whole series on every pull.

**Units and rounding.** Value in whole dollars, quantity in metric tons (`T`).

**Known quirks.**
- **Sulfur import values do not agree with USGS before October 2024, and we
  cannot say which is right.** Census shows crude sulfur imports at $301 to
  $365 per ton in January to September 2024; USGS, which publishes the same
  trade "adjusted by U.S. Geological Survey and Acuity Commodities", shows $65
  to $151. From October 2024 the median gap is 9%, though single months differ
  by up to 70%. The October 2024 break is where a USGS restatement begins (its
  October 2025 workbook raised October 2024 import value from $9.0 million to
  $51.6 million), so the later agreement reflects USGS moving toward Census.
  The Census import value stayed at $288 to $365 from January 2024 to March
  2025 while the export value rose from $66 to $195, which is not believable
  as a market price. We chart no import unit value. (Found by the independent
  tie-out, October 8, 2026.)
- **USGS "sulfur" trade is two Census codes added together**, crude
  (2503.00.0010) and refined (2503.00.0090). Summed, Census reproduces USGS
  almost exactly from mid-2025 (January 2026: 168,556 tons at $429 against
  USGS 169 thousand at $428). Our charts use the crude code alone. Crude was
  61% of sulfur export tons in August 2026 but only 12% in December 2025.
  Both codes together give $77 in January 2024, $503 in February 2026 and
  $956 in August 2026. OPEN: which series the post should use.
- **Export unit value is the usable one.** Census and USGS export values per
  ton differ by a median of 8% across January 2024 to March 2026. Single months
  differ by as much as 39%.
- **A unit value is not a price quote.** It is the average of what cleared
  customs that month: a mix of contract and spot cargoes, molten and solid,
  priced on different dates. It lags the market and it jumps when the mix
  changes. March 2026 shows $343 per ton on 252,000 tons between $512 in
  February and $573 in April.
- **Thin months are noisy.** December 2025 exports were 5,965 tons and January
  2025 17,402 tons, against a typical 100,000. Mark thin months on any chart.
- **DAP export unit value has a bad month.** April 2026 shows $221 per ton
  against $682 in March and $759 in May. We do not chart this series; the
  World Bank DAP price carries the fertilizer line.
- **Country rows include groups.** OECD, APEC, NATO, USMCA and continent totals
  appear beside real countries. Sum only the `-` row for a total.
- Imports of crude sulfur are now almost all from Canada (801,178 of 801,242
  tons, March to August 2026), much of it molten by rail, so the import unit
  value describes the Canadian contract market only.

**Uncertainty.** Census publishes no error measure for individual codes. Low-value
shipments are estimated, which is not material here.

**License and attribution.** U.S. government work, public domain. Credit
"U.S. Census Bureau, USA Trade".

## Mineral Industry Surveys, Sulfur, monthly (U.S. Geological Survey)

**What it is.** Monthly U.S. production of recovered elemental sulfur (from
petroleum refineries and coking, and from natural gas plants), shipments,
end-of-month producer stocks, trade in sulfur and sulfuric acid, apparent
consumption, and production by petroleum district.

**Where it comes from.** XLSX workbooks linked from
`usgs.gov/centers/national-minerals-information-center/sulfur-statistics-and-information`.
`scripts/fetch_usgs.py` reads the links from that page because file names are
irregular (February 2026 is `mis-202602-sulfu_1.xlsx`).

**Version and vintage.** Fifteen workbooks, January 2025 to March 2026. The
March 2026 workbook "includes data available through June 1, 2026" and was
posted in October 2026. The lag is about six months.

**Coverage.** United States. Each workbook restates the prior months back to
the same month a year earlier, so the set gives January 2024 to March 2026, 27
months. USGS collects these from a survey of producers; the workbooks do not
say what share of plants responded in a given month, and USGS calls all of it
"preliminary, for informational purposes only".

**Changes over time.** The front-matter sheet was renamed from `Text` to
`Front matter` in 2026. Table layouts are unchanged.

**Suppressed, censored or masked values.** `W` means withheld to protect a
company, `<0.5` less than half a unit. Neither appears in the U.S. totals we use.

**Missing data.** `NA` not available. None in Table 1.

**Revisions.** Earlier months are revised without notice in later workbooks. We
keep the latest value for each month and also the first-published value.
Stocks were revised in 11 of 27 months, by 3,000 tons at most (December 2025:
126 first, 129 latest).

**Units and rounding.** Thousand metric tons, rounded to three significant
digits. Stocks near 120 are therefore good to the nearest 1,000 tons.

**Known quirks.**
- Stocks are "subject to inventory adjustments".
- Stocks are producer stocks only: sulfur sitting at refineries and gas
  plants. Sulfur held by buyers (fertilizer plants, acid makers, terminals) is
  not counted anywhere.
- Cells can be text with a revision mark ("642 r"). The parser strips it.
- Table 2 and Table 4 values are in thousand dollars and thousand tons, so
  value over quantity is dollars per ton directly.
- Monthly figures are petroleum and gas recovery only. Byproduct sulfuric acid
  from metal smelters (about 6% of U.S. sulfur in all forms) is annual only.

**Uncertainty.** None published.

**License and attribution.** U.S. government work, public domain. Credit
"U.S. Geological Survey".

## Mineral Commodity Summaries 2026, Sulfur (U.S. Geological Survey)

**What it is.** Two-page annual summary: U.S. production, trade, consumption,
average price, year-end stocks and net import reliance for 2021 to 2025, and
sulfur production by country for 2024 and 2025.

**Where it comes from.** `pubs.usgs.gov/periodicals/mcs2026/mcs2026-sulfur.pdf`,
saved in `data/raw/usgs/`. The two tables are hand-keyed into
`data/manual/usgs_mcs2026_world_production.csv` and `usgs_mcs2026_us_salient.csv`.

**Version and vintage.** Published February 2026. Annual.

**Coverage.** 17 named countries plus "Other countries". Every 2025 figure
and every world figure is marked estimated. The U.S., Canada, Japan and
Kazakhstan 2024 figures are "reported"; the rest are USGS estimates. So about
25% of the 2024 world total is reported and about 75% is estimated.

**Changes over time.** Not applicable to a single edition.

**Suppressed, censored or masked values.** None.

**Missing data.** Countries below the listing threshold are inside "Other".

**Revisions.** Each edition revises the prior year. We pin the 2026 edition.

**Units and rounding.** Thousand metric tons of sulfur content, "all forms".
World total rounded to three digits.

**Known quirks.**
- **"All forms" is not the same thing in every country.** China's 19,000
  "includes byproduct elemental sulfur recovered from natural gas and
  petroleum, the estimated sulfur content of byproduct sulfuric acid from
  metallurgy, and the sulfur content of sulfuric acid from pyrite." So the
  world total is not all oil and gas byproduct, and USGS gives no world split
  by source.
- **The rows do not add to the printed world total.** The 2025 rows sum to
  83,870 against a printed 84,000, and the 2024 rows to 83,250 against 83,900.
  USGS says totals are rounded and "may not add". We use the printed total, so
  the Gulf share is 20,000 of 84,000, or 23.8%; on the row sum it is 23.8% too.
- The table is production, not exports. A country's share of production says
  nothing about its share of trade.
- The U.S. price ($180 per ton in 2025, $46.42 in 2024) is an average value
  at the plant, not a market quote.
- Hand-keyed. The tie-out re-reads the PDF.

**Uncertainty.** None published.

**License and attribution.** Public domain. Credit "U.S. Geological Survey,
Mineral Commodity Summaries 2026".

## Commodity Price Data, "Pink Sheet", monthly (World Bank)

**What it is.** Monthly average prices for about 70 commodities. We use DAP,
TSP, phosphate rock, urea and Brent crude.

**Where it comes from.** `CMO-Historical-Data-Monthly.xlsx`, sheet "Monthly
Prices". The URL carries a hash that changes, so `scripts/fetch_worldbank.py`
reads the link from `worldbank.org/en/research/commodity-markets` and saves it
in `source_url.txt`.

**Version and vintage.** "Updated on October 02, 2026". Monthly, about two
business days after month end. Latest month September 2026.

**Coverage.** 1960 to September 2026 (DAP from 1967). Nominal U.S. dollars.
Each series is one quoted benchmark: DAP is spot, free on board, U.S. Gulf.
The World Bank takes these from trade publications; it does not survey sales.

**Changes over time.** Benchmarks have been swapped over the decades; see the
"Description" sheet. None changed for our five series since 2024.

**Suppressed, censored or masked values.** None. `…` marks no quote.

**Missing data.** `…` in early DAP years. None since 2024.

**Revisions.** Phosphate rock was corrected for 2023 and 2024 in the March
2026 edition. We refresh the whole file each pull.

**Units and rounding.** Dollars per metric ton; Brent dollars per barrel.

**Known quirks.**
- **Phosphate rock barely moves because it is a posted contract price.** It
  read 152.5 every month from January 2024 to May 2026, then 156.9 and 170.0.
  It is not evidence that rock was unaffected.
- It contains no sulfur and no sulfuric acid price.
- DAP is a U.S. Gulf export price. It is a wholesale price in bulk, not what a
  farmer pays.

**Uncertainty.** None published.

**License and attribution.** CC BY 4.0. Credit "World Bank Commodity Price
Data (The Pink Sheet)".

## Producer Price Index, selected series (Bureau of Labor Statistics, via FRED)

**What it is.** Monthly indexes of prices received by U.S. producers. We use
sulfuric acid (`WPU0613020T1`), phosphates (`WPU065202`), phosphatic
fertilizer manufacturing (`PCU325312325312`) and No. 2 diesel (`WPU057303`).

**Where it comes from.** `fred.stlouisfed.org/graph/fredgraph.csv?id=<series>`,
no key. `scripts/fetch_fred.py`.

**Version and vintage.** Pulled October 8, 2026. Latest month August 2026.

**Coverage.** United States. Sulfuric acid from June 1987. BLS surveys a
sample of producers who report their own transaction prices each month.

**Changes over time.** Sample and weights are updated periodically; BLS does
not flag the dates in the series.

**Suppressed, censored or masked values.** BLS withholds a month when too few
producers report. None missing in these series since 2024.

**Missing data.** A blank or `.` in the CSV. Dropped.

**Revisions.** The latest four months are preliminary and are revised once,
four months after first publication. So May to August 2026 can still change.

**Units and rounding.** Index numbers, not dollars, not seasonally adjusted.
Only percent changes mean anything.

**Known quirks.**
- **There is no PPI for elemental sulfur.**
- Sulfuric acid is identical in July and August 2026 (307.176) and was also
  identical in July and August 2025 (222.349). When few producers report a
  change, BLS carries prices forward, so a flat month may be a missing report.
- Much sulfuric acid moves on contracts, some tied to the Tampa quarterly
  sulfur price, so the index moves in steps and trails spot sulfur.
- FRED returns an empty body to a browser-like User-Agent. Use the default.

**Uncertainty.** BLS publishes no error measure for individual PPI series.

**License and attribution.** Public domain. Credit "U.S. Bureau of Labor
Statistics".

## Illinois Production Cost Report, slug 3195 (USDA Agricultural Marketing Service)

**What it is.** Every two weeks, the range and average of prices Illinois
distributors are asking for fertilizer (DAP, MAP, urea, anhydrous ammonia,
potash, liquid nitrogen) and farm diesel.

**Where it comes from.** MyMarketNews API,
`marsapi.ams.usda.gov/services/v1.2/reports/3195/Report Details - Prices`,
needs `USDA_MARS_API_KEY`. `scripts/fetch_usda.py` asks one year at a time
because the default response returns recent reports only.

**Version and vintage.** Pulled October 8, 2026. Latest report week of
September 28, 2026.

**Coverage.** Illinois only. The price detail starts April 15, 2024: 65
reports, exactly 14 days apart, none missing. USDA market reporters collect
asking prices from a sample of distributors; the report does not say how many.

**Changes over time.** MAP switched grade. MAP 11-52-0 is reported from August
2025 (31 reports); MAP 11-34-0, a liquid, before that (34 reports). They are
different products and must not be joined into one line.

**Suppressed, censored or masked values.** None.

**Missing data.** `price_avg` is null in no rows we use.

**Revisions.** Reports are marked "Final". We refresh on every pull.

**Units and rounding.** Dollars per short ton (2,000 pounds), not metric tons.
Farm diesel in dollars per gallon. To compare with the World Bank's metric-ton
DAP, multiply by 1.1023, or compare percent changes only.

**Known quirks.**
- These are asking prices, not sales.
- Farm diesel is untaxed off-road diesel, so its level sits below the EIA
  retail price. Compare changes, not levels.
- The report header lists dates back to 2020, but price rows before April
  2024 are not served by the API.

**Uncertainty.** None published. The min to max range in each report gives a
sense of spread (DAP $840 to $995 in the latest).

**License and attribution.** Public domain. Credit "USDA Agricultural
Marketing Service".

## Weekly petroleum data: diesel price and distillate stocks (U.S. Energy Information Administration)

**What it is.** Weekly U.S. average retail price of No. 2 diesel
(`EMD_EPD2D_PTE_NUS_DPG`), ending stocks of distillate fuel oil (`WDISTUS1`),
and days of supply of distillate (`W_EPD0_VSD_NUS_DAYS`).

**Where it comes from.** EIA API v2, routes `petroleum/pri/gnd`,
`petroleum/stoc/wstk`, `petroleum/sum/sndw`, with `EIA_API_KEY`.
`scripts/fetch_eia.py`.

**Version and vintage.** Pulled October 8, 2026. Price to October 5, 2026;
stocks and days to October 2, 2026.

**Coverage.** United States. Price from March 21, 1994 (1,699 weeks, none
missing). Days of supply from March 8, 1991. The price is a Monday survey of
retail outlets; stocks come from a weekly survey of refiners, pipelines and
terminals that covers most but not all volume, with the rest estimated by EIA.

**Changes over time.** Distillate includes heating oil as well as diesel. The
diesel price series switched to ultra-low-sulfur as that became the only grade.

**Suppressed, censored or masked values.** None.

**Missing data.** None in the period used.

**Revisions.** Weekly stocks are estimates and are superseded by the monthly
survey about two months later. The weekly series itself is not revised.

**Units and rounding.** Dollars per gallon including taxes; thousand barrels;
days.

**Known quirks.**
- Days of supply is EIA's own figure: stocks divided by the four-week average
  of product supplied. It is primary stocks only (refineries, pipelines, bulk
  terminals), which is the nearest match to USGS producer stocks of sulfur.
- The API silently drops the newest week when sorted ascending. The fetch
  sorts descending and pages.

**Uncertainty.** EIA publishes sampling error for the weekly survey in its
methodology notes; not carried in the series.

**License and attribution.** Public domain. Credit "U.S. Energy Information
Administration".

## Table 25-10-0036-01, gas plant sulphur supply (Statistics Canada)

**What it is.** Monthly tonnes of sulphur supplied by natural gas processing
plants in Canada, by province.

**Where it comes from.** `www150.statcan.gc.ca/n1/tbl/csv/25100036-eng.zip`,
no key. `scripts/fetch_statcan.py`.

**Version and vintage.** Pulled October 8, 2026. Latest month July 2026.

**Coverage.** January 1989 to July 2026. The Canada total is present for all
451 months.

**Changes over time.** Three "gas use" items in the same table were terminated;
sulphur was not.

**Suppressed, censored or masked values.** **Alberta and British Columbia are
suppressed (`x`) in 161 of 451 months, including every recent month.** Only the
Canada total can be used, so we cannot show Alberta on its own from this table.

**Missing data.** `..` not available. None in the Canada total.

**Revisions.** Statistics Canada revises recent months. We refresh on each pull.

**Units and rounding.** Tonnes.

**Known quirks.** Gas plants only. Sulphur recovered at oil sands upgraders and
refineries is not in this table, so this is not total Canadian production
(USGS puts that near 5 million tons a year; this table sums to about 4.4).

**Uncertainty.** None published.

**License and attribution.** Statistics Canada Open Licence. Credit
"Statistics Canada, Table 25-10-0036-01".

## ST3 Supply and Disposition of Sulphur (Alberta Energy Regulator)

**What it is.** Monthly tonnes of sulphur in Alberta: opening and closing
inventory, production by source (gas plants, oil sands facilities,
refineries), and where it went.

**Where it comes from.** `static.aer.ca/prd/documents/sts/st3/`, one XLSX per
year plus `Sulphur_current.xlsx`, no login. `scripts/fetch_aer.py`.

**Version and vintage.** Current-year file "Run Date: 28 September 2026".
Released at the end of each month, one month in arrears. Latest month August
2026.

**Coverage.** Alberta, January 2024 to August 2026 in our pull. Figures are
operator filings to the provincial reporting system (Petrinex), so they are
reported volumes, not estimates.

**Changes over time.** None in the three files.

**Suppressed, censored or masked values.** None.

**Missing data.** Months not yet reported are zero in the current-year file.
We drop zero inventory months.

**Revisions.** Operators can amend filings. December 2024 closing inventory
(11,987,148.4) and January 2025 opening inventory (11,987,049.7) differ by 99
tonnes for that reason. Each year's file is frozen at its run date; we refresh
the current year on every pull.

**Units and rounding.** Tonnes, one decimal.

**Known quirks.**
- The row is "Closing Inventory". The file does not separate the large poured
  blocks from working stock, so we call it "Alberta's stockpile", not "block
  inventory".
- An "Adjustments" row moves inventory by as much as 103,000 tonnes in a month
  (June 2025). Month-to-month changes are not all sales.
- Having sulphur in a block is not the same as being able to ship it. It must
  be remelted and railed to Vancouver. CRU put that cost at about $180 to $200
  a tonne (Sulphur magazine 422, January 2026).

**Uncertainty.** None published.

**License and attribution.** Alberta Energy Regulator, open data. Credit
"Alberta Energy Regulator, ST3".

## Compiled from trade press: Adnoc posted price and China port stocks (editorial)

**What it is.** Two small tables we built by hand from figures reported in
news stories and magazine tables: `data/manual/adnoc_osp.csv` (Abu Dhabi
National Oil Company's monthly official selling price for sulfur, dollars per
metric ton, free on board Ruwais, June 2024 to October 2026) and
`data/manual/china_port_stocks.csv` (sulfur held at Chinese ports, 12 dated
readings from October 2024 to late August 2026).

**Where it comes from.** Argus news stories, the price table and market notes
in CRU's Sulphur magazine (issues 415 to 426), World Fertilizer, SunSirs, SMM
and Mysteel. Each row names its source; URLs and the quoted sentences are in
`research/BRIEF.md`. Each figure was read on the page itself on October 8,
2026, not taken from a search result.

**Version and vintage.** Compiled October 8, 2026. Not automated.

**Coverage.** Adnoc: every month from June 2024, 29 months, no gaps. China:
irregular. There is no reading between October 30, 2024 and July 2, 2025, and
none after late August 2026. The chart draws straight lines between readings,
which says nothing about what happened in between.

**Changes over time.** China stocks come from three tallies (CRU's unnamed
source, SunSirs, SMM) plus Mysteel citing OilChem. They may count different
ports.

**Suppressed, censored or masked values.** None.

**Missing data.** See coverage.

**Revisions.** CRU printed June 2026 China delivered price as 1,185 in one
issue and 1,100 in the next, so these sources do revise. We do not chart that
series.

**Units and rounding.** Dollars per metric ton; million metric tons.

**Known quirks.**
- A posted price is a seller's announced price for the month, not what every
  cargo traded at. When the strait was shut, few cargoes moved at any price.
- Sources disagree on early July 2026 China stocks: SMM gives 727,900 tons on
  July 3 and "790,000" for "early July" in the same article; CRU gives a July
  low of 730,000. We use the dated SMM figure.
- Year-end 2025 China stocks: SunSirs 1.9848 million (December 31); CRU 1.95
  million. We use the dated SunSirs figure.
- "Early April" and "late August" readings carry approximate dates (April 3,
  August 27) so they can be placed on a time axis.
- These are facts reported by publishers who sell the underlying assessments.
  We cite a small number of published figures with credit; we do not
  republish their price series.

**Uncertainty.** None published. Treat China stocks as good to roughly 50,000
tons, the size of the disagreements above.

**License and attribution.** Cite each publisher by name. Label any chart
"our compilation".

## Method for the derived figures

These are our calculations, not published series. Each is labeled as ours on
its chart.

- **Sulfur price.** Census exports of code 2503.00.0010, all-country total:
  dollars divided by metric tons, by month.
- **Monthly diesel.** The mean of the EIA weekly retail prices whose date
  falls in the month. A month still in progress is left out.
- **Percent change.** Level in the month shown divided by the level in the
  base month, minus one. Base months are January 2024 and February 2026, the
  last full month before the February 28, 2026 strikes. Each series runs to
  the latest full month its own source has published, so end months differ.
- **Days of sulfur stock.** USGS month-end producer stocks divided by that
  month's shipments per day (shipments divided by days in the month). For each
  month we use the figure in the latest USGS workbook that carries it.
- **Days of diesel.** EIA's published days of supply of distillate, weekly,
  used as is.
- **Gulf share of production.** Iran, Kuwait, Qatar, Saudi Arabia and the
  United Arab Emirates, summed, over the USGS printed world total for 2025.
- **Sulfur cost in a ton of DAP.** 0.4 times the sulfur price above, compared
  with the World Bank DAP price in the same month. The 0.4 is from Mosaic's
  2025 annual report ("approximately 0.40 long tons of sulfur" per tonne of
  DAP; 0.40 long tons is 0.406 metric tons, and we round to 0.4). It prices
  sulfur at the export average, which is above what a producer on a quarterly
  contract paid while prices were rising: Mosaic reported an average sulfur
  cost of $522 a long ton for the second quarter of 2026.
- **Alberta change.** August 2026 closing inventory minus February 2026
  closing inventory.
