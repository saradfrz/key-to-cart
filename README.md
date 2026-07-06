# sefaz-rs

Automação para extração, download e parsing de Notas Fiscais de Consumidor Eletrônica (NFC-e) do portal da SEFAZ-RS.

## Visão Geral
Este projeto automatiza a leitura de dados de NFC-e do portal da SEFAZ-RS, baixando os HTMLs das notas fiscais e extraindo informações estruturadas. O resultado é exportado como CSV para análise e integração.

## Estrutura do Projeto

- `main.py`: Ponto de entrada da aplicação que carrega a configuração, prepara as pastas de saída e inicia o pipeline. Ele orquestra o fluxo completo de download e parsing.
- `config.json`: Define o ano de referência, diretórios de input/output, URLs de login e templates de NFC-e, além de classes específicas para o parser. Isso permite ajustar o comportamento do projeto sem alterar o código.
- `__init__.py`: Marca a raiz do projeto como pacote Python e facilita a importação dos módulos internos. Não contém lógica de execução.
- `project_structure.txt`: Arquivo de referência contendo a organização da estrutura de pastas do projeto. Serve como documentação adicional para a arquitetura do repositório.

### app/

- `app/downloader/invoice_downloader.py`: Controla o navegador undetected-chromedriver para acessar o portal SEFAZ-RS e capturar o HTML das NFC-e. Salva os arquivos HTML baixados na pasta de saída configurada.
- `app/parser/invoice_parser.py`: Analisa cada HTML de NFC-e com BeautifulSoup e extrai dados de compra e itens de produto. Converte as tabelas da nota fiscal em registros estruturados para exportação.
- `app/pipeline/invoice_pipeline.py`: Coordena a execução do fluxo completo, desde a leitura das fontes até a geração do CSV final. Usa fontes, downloaders e parsers para agrupar o resultado final.
- `app/source/invoice_source.py`: Lê os arquivos CSV de input para extrair os códigos NFC-e que serão baixados. Também salva o histórico de notas processadas em `output/invoice_history.csv`.
- `app/utils/config.py`: Faz a leitura do `config.json` e disponibiliza a configuração para todo o pipeline. Centraliza parâmetros de diretórios e acessos.
- `app/utils/directory.py`: Fornece utilitários para listar e manipular arquivos em diretórios. Facilita a busca de HTMLs e arquivos de entrada.
- `app/utils/file.py`: Inclui funções para ler e gravar arquivos CSV. É responsável por salvar o resultado do parser em disco.
- `app/utils/logger.py`: Configura o logger do projeto para capturar mensagens de execução e erros. Mantém os registros em arquivos na pasta `logs`.
- `app/utils/retry.py`: Implementa lógica de repetição para operações suscetíveis a falhas temporárias. Ajuda a tornar as requisições e interações mais robustas.
- `app/utils/string.py`: Reúne funções auxiliares de manipulação de texto usadas pelo parser. Normaliza e extrai valores de strings de HTML.

### models/

- `models/invoice.py`: Define a estrutura de dados da nota fiscal eletrônica dentro do projeto. Serve como referência para os campos usados no pipeline.
- `models/invoice_result.py`: Representa o resultado de parsing de uma nota fiscal, incluindo dados de compra e itens. Ajuda a padronizar o modelo de saída.

### input/

- `input/`: Contém os arquivos CSV de histórico baixados manualmente do portal da SEFAZ-RS. Esses arquivos são a fonte de códigos NFC-e para o download dos HTMLs.

### output/

- `output/html/`: Pasta onde os HTMLs das NFC-e baixadas são salvos. Cada arquivo é processado em seguida pelo parser.
- `output/parser/`: Diretório previsto para resultados de parsing intermediários ou finais. Pode ser usado para armazenar exportações adicionais.
- `output/2025_purchase_data_items.csv`: CSV final com itens de compra extraídos das NFC-e. É o artefato principal gerado pelo pipeline.
- `output/invoice_history.csv`: Histórico de notas fiscais extraídas do CSV de input e salvo como referência.

### logs/

- `logs/`: Contém os arquivos de log gerados durante a execução. Ajuda a diagnosticar erros e revisar o progresso do pipeline.

## Como Usar

1. Baixe manualmente o CSV mestre do portal [SEFAZ-RS](https://nfg.sefaz.rs.gov.br/Login/LoginNfg.aspx?urlRedir=%2fcadastro%2fConsultaDocumentos.aspx) e coloque o arquivo no diretório `input`.
2. Execute o script principal:
   ```sh
   python main.py
   ```
   O scraper irá baixar os HTMLs das NFC-e e o parser irá gerar os CSVs.

## Observações

- O scraping utiliza Selenium com undetected-chromedriver para evitar bloqueios.
- É necessário realizar login manual no primeiro uso para salvar os cookies.
- O parser utiliza BeautifulSoup para extrair dados estruturados dos HTMLs.