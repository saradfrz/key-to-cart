# sefaz-rs


### Extrair csv mestre
Abrir o link https://nfg.sefaz.rs.gov.br/Login/LoginNfg.aspx?urlRedir=%2fcadastro%2fConsultaDocumentos.aspx


- Realizar carga inicial com extração inicial dos dados desde 2020
- Para isso realizar 5 extrações por intervalos
	- 01/01/2020 - 01/01/2021
	- 01/01/2021 - 01/01/2022
	- 01/01/2022 - 01/01/2023
	- 01/01/2023 - 01/01/2024
	- 01/01/2024 - 01/01/2025
	- 01/01/2025 - 07/06/2025

- Unificar os arquivos num csv mestre
- A partir do csv mestre, baixar as NFs usando selenium, usando a url "https://www.sefaz.rs.gov.br/NFE/NFE-NFC.aspx?chaveNFe=43250589897201000309650080003178181661097065"


### Track package instalation
 - pip install <package>
 - pip freeze > requirements.txt
 - git add requirements.txt
 - git commit -m "add: <package>"

#### Using `ìnstallpkg.sh`
 - Make the script executable: `chmod +x installpkg.sh`
 - Run it like this: `./installpkg.sh pandas` 