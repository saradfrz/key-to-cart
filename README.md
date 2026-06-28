# sefaz-rs

Automação para extração, download e parsing de Notas Fiscais de Consumidor Eletrônica (NFC-e) do portal da SEFAZ-RS.

## Visão Geral
Este projeto automatiza o processo de:
- Extração de dados mestre (CSV) do portal da SEFAZ-RS
- Download dos arquivos HTML das NFC-e usando Selenium e undetected-chromedriver
- Parsing dos arquivos HTML para extração de informações estruturadas
- Geração de arquivos CSV com os dados extraídos

## Estrutura do Projeto

- `main.py`: Script principal que orquestra scraping e parsing
- `app/sefaz_scrapper/scrapper.py`: Scraper Selenium para baixar HTML das NFC-e
- `app/nfce_parser/parser.py`: Parser para extrair dados dos HTMLs das NFC-e
- `app/data_tools.py`: Utilitários para manipulação de arquivos e dados
- `input/master_data/nfg.csv`: CSV mestre baixado manualmente do portal
- `output/nfce/html/`: HTMLs das NFC-e baixadas
- `output/nfce/csv/`: CSVs gerados a partir dos HTMLs
- `logs/`: Logs do processo
- `requirements.txt`: Dependências Python


## Como Usar

1. Baixe manualmente o CSV mestre do portal [SEFAZ-RS](https://nfg.sefaz.rs.gov.br/Login/LoginNfg.aspx?urlRedir=%2fcadastro%2fConsultaDocumentos.aspx) e coloque em `input/master_data/nfg.csv`.
2. Execute o script principal:
   ```sh
   python main.py
   ```
   O scraper irá baixar os HTMLs das NFC-e e o parser irá gerar os CSVs.

## Observações

- O scraping utiliza Selenium com undetected-chromedriver para evitar bloqueios.
- É necessário realizar login manual no primeiro uso para salvar os cookies.
- O parser utiliza BeautifulSoup para extrair dados estruturados dos HTMLs.

# Fluxo orientado a responsabilidades

Config
   │
   ▼
InvoicePipeline
   │
   ├──────────────► InvoiceSource
   │                     │
   │                     ▼
   │              List[Invoice]
   │
   ├──────────────► ReceitaSession
   │                     │
   │                     ▼
   ├──────────────► ReceitaDownloader
   │                     │
   │                     ▼
   │                html/*.html
   │
   ├──────────────► ReceitaParser
   │                     │
   │                     ▼
   │              List[InvoiceResult]
   │
   └──────────────► CSVExporter
                         │
                         ▼
                    resultado.csv
---
Atualizado em: 20/02/2026