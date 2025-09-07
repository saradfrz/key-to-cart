import os 
# config.py

BASE_DIR = os.path.dirname(__file__)

# Scrapper variables
SEFAZ_LOGIN_URL = "https://nfg.sefaz.rs.gov.br/Login/LoginNfg.aspx?urlRedir=%2fcadastro%2fConsultaDocumentos.aspx"
NFCE_URL_TEMPLATE = "https://www.sefaz.rs.gov.br/NFE/NFE-NFC.aspx?chaveNFe="
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
USER_DATA_DIR = r'C:/Users/saraf/AppData/Local/Google/Chrome/User Data/Default'
COOKIES_DIR = os.path.join(BASE_DIR, "session")
COOKIES_FILE = os.path.join(COOKIES_DIR, "cookies.json")
NFCE_DATA_DIR = os.path.join(BASE_DIR, "output", "nfce", "html")
MASTER_DATA = os.path.join(BASE_DIR, "input", "master_data")


# Parser Variables
STORE_NAME__CLASS = "NFCCabecalho_SubTitulo"
CNPJ_STORE_STATE_CODE__CLASS = "NFCCabecalho_SubTitulo1"
PARSER_OUTPUT_FOLDER = os.path.join(BASE_DIR, "output", "nfce", "csv")

