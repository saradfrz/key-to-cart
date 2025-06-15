import os 
# config.py

BASE_DIR = os.path.dirname(__file__)

# Scrapper variables
SEFAZ_LOGIN_URL = "https://nfg.sefaz.rs.gov.br/Login/LoginNfg.aspx?urlRedir=%2fcadastro%2fConsultaDocumentos.aspx"
NFCE_URL_TEMPLATE = "https://www.sefaz.rs.gov.br/NFE/NFE-NFC.aspx?chaveNFe="
CSV_FOLDER = os.path.join(BASE_DIR, "sefaz_scrapper", "data")
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
USER_DATA_DIR = r'C:/Users/saraf/AppData/Local/Google/Chrome/User Data/Default'
COOKIES_DIR = os.path.join(BASE_DIR, "session")
COOKIES_FILE = os.path.join(COOKIES_DIR, "cookies.json")
NFCE_DATA_DIR = os.path.join(BASE_DIR, "nfce_data")


# Parser Variables

