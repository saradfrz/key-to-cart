# KeyToCart

**From invoice keys to item-level purchase data.**

KeyToCart is a Python data ingestion and processing project built to reconstruct my purchase history from electronic consumer invoices (NFC-e) linked to my CPF. It reads invoice access keys from a manually downloaded **Nota Fiscal Gaúcha (NFG)** history file, retrieves receipt HTML from **SEFAZ-RS**, and extracts purchase and product details for CSV export.

The project applies data engineering practices to personal spending data: configuration-driven execution, separate source and parsing components, raw HTML capture, download retries, and tabular outputs for downstream analysis.

## Purpose
Purchase history becomes more useful when individual receipts can be analyzed together. KeyToCart aims to consolidate merchant, product, quantity, and price information into a dataset that can support spending analysis, purchase frequency reporting, and price comparisons over time.

Its coverage depends on the keys available in the supplied NFG export and the receipts successfully retrieved and parsed. It does not discover receipts by querying a CPF directly.

## Data workflow

| Stage | Source or component | Responsibility |
| --- | --- | --- |
| Obtain keys | Nota Fiscal Gaúcha, manual step | Download the invoice history associated with your CPF. |
| Read input | `InvoiceSource` | Select a file for the configured year, read keys from its seventh column, and save a copy of the history. |
| Retrieve receipts | `InvoiceDownloader` | Open SEFAZ-RS receipt pages in Chrome and save their HTML, with up to five attempts per key. Some failures return early. |
| Parse details | `InvoiceParser` | Extract merchant information, invoice metadata, and product rows using BeautifulSoup. |
| Export data | `InvoicePipeline` and `FileManager` | Combine item rows and write CSV outputs. |

**NFG provides the list of keys; SEFAZ-RS provides the receipt details.** Retrieval is sequential and uses browser navigation, page waits, and iframe interaction.

## Architecture

| Path | Responsibility |
| --- | --- |
| `main.py` | Load configuration, recreate the HTML and log directories, initialize logging, and start the pipeline. |
| `config.json` | Configure the year, directories, receipt URL, and HTML selectors. |
| `app/source/invoice_source.py` | Read the invoice history and extract access keys. |
| `app/downloader/invoice_downloader.py` | Manage browser navigation, retries, alerts, and HTML capture. |
| `app/parser/invoice_parser.py` | Extract receipt metadata and line items from HTML tables. |
| `app/pipeline/invoice_pipeline.py` | Coordinate ingestion, parsing, and CSV export. |
| `app/utils/` | Provide configuration, file, directory, logging, and text utilities. |
| `models/` | Additional model files; the active pipeline uses dictionaries and lists. |
| `input/` | Manually downloaded invoice history files. |
| `output/` | Generated CSV files and receipt HTML. |
| `logs/` | Local execution logs. |

The active workflow uses Python, Selenium, `undetected-chromedriver`, BeautifulSoup, and standard-library CSV and JSON utilities. Export is handled by the pipeline and file utility rather than a separate exporter component.

## Setup

### 1. Prepare the environment

From the repository root, create a virtual environment. On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install wheel setuptools beautifulsoup4 selenium undetected-chromedriver
```

Google Chrome must be installed.

### 2. Prepare the input
Download your invoice history from Nota Fiscal Gaúcha and place it in `input/`, using a filename containing the target year, such as `nfg_2026.csv`.
The source reader currently expects:

- UTF-8, comma-delimited CSV with a header row.
- Invoice access keys in the **seventh column** (`row[6]`).
- One matching input file per year. If several filenames contain the configured year, it selects the first match without a guaranteed ordering.

Check the downloaded file's encoding, delimiter, and column layout before running. Preserve keys as text to avoid spreadsheet conversion or precision loss.

### 3. Configure the run

Edit the existing `config.json`:

| Setting | Current role |
| --- | --- |
| `year` | Selects the input filename and prefixes the main output filenames. |
| `dir.input` | Directory containing invoice history CSVs. |
| `dir.output` | Destination for CSV exports. |
| `dir.output_html` | Destination for downloaded receipt HTML. |
| `dir.logs` | Directory recreated at startup; the logger itself uses the literal path `logs/`. |
| `invoice_downloader.nfce_url_template` | SEFAZ-RS receipt URL prefix, to which each access key is appended. |
| `invoice_parser.store_name__class` | HTML class used to locate merchant and receipt metadata. |
| `invoice_parser.cnpj_store_state_code__class` | HTML class used to locate merchant registration details. |

### 4. Execute
Run from the repository root:

```powershell
python main.py
```

**Each run deletes and recreates the configured HTML and log directories.** Existing CSV outputs with the same filenames are overwritten. Preserve any previous results you need before execution.

### Intended item-level schema

Each row represents one receipt line item, with invoice and merchant attributes repeated across items. These are the column names currently declared by the pipeline:

| Column | Meaning |
| --- | --- |
| `id_scrapping` | Run-local sequence identifier; original spelling retained. |
| `nm_store` | Merchant name. |
| `id_cnpj` | Merchant CNPJ, not the consumer's CPF. |
| `id_store_state_code` | Merchant state registration. |
| `dt_purchase` | Invoice issue date and time. |
| `id_nfce` | Invoice access key. |
| `id_item` | Product code reported on the receipt. |
| `ds_item` | Product description. |
| `qt_item` | Purchased quantity. |
| `tp_unit` | Unit of measure. |
| `vl_unit` | Unit price. |
| `vl_total` | Line-item total. |

## Outputs
Paths below assume the default `output` directory.

| Artifact | Contents |
| --- | --- |
| `output/invoice_history.csv` | Copy of the selected input history, rewritten using the output CSV format. |
| `output/html/<sequence>_<access_key>.html` | Receipt HTML captured during retrieval. |
| `output/<year>_purchase_data_items.csv` | Intended item-level dataset; currently affected by the parsing/export blocker. |
| `output/<year>_failed_nfces.csv` | Intended failure report; failure collection is currently incomplete. |

CSV exports use UTF-8, a semicolon delimiter, and quoting on every field. Dates, quantities, and prices remain source-formatted strings; downstream analysis requires type conversion and validation.