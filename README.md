# Mexico Wildlife & Habitat Impact Data Hub
 
> Compilation of multiple data sources to describe wildlife, natural habitats and environmental impact in Mexico.
 
## Overview
 
Mexico is one of the world's megadiverse countries, but the data that describes its biodiversity, the state of its ecosystems and the pressures acting on them is scattered across many agencies, formats and portals. This project gathers some of those sources into a single, consistent dataset that can be queried, cross-referenced and visualized.
 
The project is organized around three questions:
 
1. **What lives where?** Species occurrences, distributions and conservation status.
2. **What is the state of natural habitats?** Land cover aproximation (derived from the infered surface reported by multiple government datasets), vegetation, forests, protected areas and water bodies.
3. **What is impacting them?** Pollution of air, water and soil, industrial emissions, contaminated sites, environmental emergencies and land-use change.
## Objectives
 
- Build reproducible ETL pipelines for each data source.
- Normalize all data to a common geographic key (INEGI state/municipality codes and watershed IDs).
- Provide a unified data model that links species and habitats to environmental pressures.
<!-- - Publish analysis-ready tables and dashboards. -->
<!-- - Document the provenance, license and update frequency of every dataset. -->
## Data Sources
 
## Architecture
 
```
┌──────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────┐
│   Extract    │ ─▶ │  Raw storage │ ─▶ │  Transform   │ ─▶ │   Curated    │
│ APIs, files, │    │  data/raw/   │    │ clean, stan- │    │  data model  │
│  scrapers    │    │ (immutable)  │    │ darized, join│    │ + dashboards │
└──────────────┘    └──────────────┘    └──────────────┘    └──────────────┘
```
 
- **Extract:** one connector per source (API client, file downloader or scraper).
- **Raw:** original files are stored unchanged with a download timestamp.
- **Transform:** cleaning, unit standardization, coordinate reprojection (EPSG:4326).
- **Curated:** star-schema tables ready for BI tools and spatial analysis.

## Getting Started
 
### Requirements
 
- Python 3.15+

### Installation
 
<!-- ```bash
git clone <repo-url>
cd <repo-name>
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
``` -->
 
<!-- ### Running the pipelines
 
```bash
# Extract a single source
python -m src.extract.gbif --country MX
 
# Run the full pipeline
python -m src.pipeline --all

# Run a single stage for one source
python -m src.pipeline --source renameca --stage transform
``` -->
 
## Example Analyses
 
<!-- - Endangered species occurrences inside vs. outside protected areas
- Forest loss trends by state and ecoregion
- Water quality in watersheds with high biodiversity
- Proximity of contaminated sites and RETC facilities to protected areas and Ramsar wetlands
- Correlation between environmental emergencies and changes in local water quality -->

## Data Licensing & Attribution
 
Each dataset keeps its original license and terms of use. Before redistributing any derived data, check:
 
- **Mexican government open data:** Libre Uso MX license (datos.gob.mx)
<!-- - **GBIF / NaturaLista:** per-record licenses (CC0, CC BY, CC BY-NC)
- **IUCN Red List:** non-commercial terms; redistribution is restricted
- **GEMStat:** CC BY 4.0 for openly licensed data
- **Copernicus:** free and open, with attribution required
Every curated table includes a `source_id` that links back to `dim_source` for citation. -->
 
## Contributing
 
1. Open an issue that describes the source or feature.
2. Create a branch: `feature/<source-or-feature>`.
3. Add or update the source documentation in `docs/sources/`.
4. Include tests for new connectors and transformations.
5. Open a pull request.