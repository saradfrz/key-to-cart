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

## Setup do Ambiente (WSL)

1. Instale Python no WSL:
   ```sh
   sudo apt update
   sudo apt install python3 python3-pip python3.12-venv
   ```
2. Crie e ative o ambiente virtual:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instale as dependências:
   ```sh
   pip install -r requirements.txt
   ```

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
- O projeto pode ser executado tanto no WSL quanto no Windows, mas recomenda-se o uso do WSL para maior compatibilidade.

## Instalação de Pacotes Python e Automação

Para instalar novos pacotes e atualizar o requirements.txt automaticamente, use:

```sh
pip install <package>
pip freeze > requirements.txt
git add requirements.txt
git commit -m "add: <package>"
```

Ou utilize o script PowerShell:

```powershell
./installpkg.ps1 -PackageName <package>
```

## Track package installation

- pip install <package>
- pip freeze > requirements.txt
- git add requirements.txt
- git commit -m "add: <package>"

#### Usando `installpkg.ps1`
- Execute no PowerShell:
  ```powershell
  ./installpkg.ps1 -PackageName <package>
  ```

#### Usando `installpkg.sh` (Linux)
- Torne o script executável: `chmod +x installpkg.sh`
- Execute: `./installpkg.sh selenium==3.14.0`

## Dicas de Debug

- Para salvar o HTML de uma página manualmente no console Python:
  ```python
  open("output.html", "w", encoding="utf-8").write(soup.prettify())
  ```

---
Atualizado em: 20/02/2026