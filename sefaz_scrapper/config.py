import os 
# config.py
LOGIN_URL = "https://nfg.sefaz.rs.gov.br/Login/LoginNfg.aspx?urlRedir=%2fcadastro%2fConsultaDocumentos.aspx"
NFE_URL_TEMPLATE = "https://www.sefaz.rs.gov.br/NFE/NFE-NFC.aspx?chaveNFe="
CSV_FOLDER = "data"
DOWNLOAD_FOLDER = "downloads"
USER_DATA_DIR = r'C:/Users/saraf/AppData/Local/Google/Chrome/User Data/Default'

BASE_DIR = os.path.dirname(__file__)
COOKIES_DIR = os.path.join(BASE_DIR, "session")
COOKIES_FILE = os.path.join(COOKIES_DIR, "cookies.json")

NFE_DATA_DIR = os.path.join(BASE_DIR, "nfe_data")

