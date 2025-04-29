from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import pandas as a
import time
from selenium.common.exceptions import TimeoutException
e_driver_path = "C:\Program Files\chromedriver-win64\chromedriver.exe"

service = Service(e_driver_path)
option = webdriver.ChromeOptions()
option.add_argument('--disable-gpu')
option.add_argument('--window-size=1920,1080')
driver = webdriver.Chrome(service=service, options = option)

url = 'https://www.vivareal.com.br/venda/?transacao=venda&pagina=1'
driver.get(url)
time.sleep(5)

dic_mobiliaria = {
'metragem':[],
'quartos':[],
'banheiros':[],
'vagas':[],
'valor':[],
'condominio_iptu':[],
'nome_rua':[]
}
pagina = 1
num_imoveis = 100
while len(dic_mobiliaria) < num_imoveis:
    print(f'\n coletando dados da pagina {pagina}')

    try:
        WebDriverWait(driver,10).until(ec.presence_of_all_elements_located((By.CSS_SELECTOR, '[data-cy="rp-property-cd"]')))
        

    except TimeoutException:
        print('tempo de espera excedido')

    imobiliaria = driver.find_elements(By.CSS_SELECTOR, '[data-cy="rp-property-cd"]')
    preco = driver.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-price-txt"]')

    for imovel in imobiliaria:
        if len(dic_mobiliaria['metragem']) >= num_imoveis:
            break  
        try:

            metragem = imovel.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-propertyArea-txt"]').text.strip()
            quartos = imovel.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bedroomQuantity-txt"]').text.strip()
            banheiros = imovel.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-bathroomQuantity-txt"]').text.strip()
            vagas = imovel.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-parkingSpacesQuantity-txt"]').text.strip()
            try:
                preco_p = preco.find_elements(By.TAG_NAME, 'p')  # captura todas as tags <p> dentro do seletor

                valor = preco_p[0].text if len(preco_p) > 0 else None
                condominio_iptu = preco_p[1].text if len(preco_p) > 1 else None
            except:    
               condominio_iptu = "desconhecido"
        
            nome_rua = imovel.find_element(By.CSS_SELECTOR, '[data-cy="rp-cardProperty-street-txt"]').text.strip()
            
            print(f'{condominio_iptu}')
            dic_mobiliaria['metragem'].append(metragem)
            dic_mobiliaria['quartos'].append(quartos)
            dic_mobiliaria['banheiros'].append(banheiros)
            dic_mobiliaria['vagas'].append(vagas)
            dic_mobiliaria['valor'].append(valor)
            dic_mobiliaria['condominio_iptu'].append(condominio_iptu)
            dic_mobiliaria['nome_rua'].append(nome_rua)
        
        except Exception as e:
            print(f'Erro ao coletar dados de um imóvel: {e}')
            continue  # pula para o próximo imóvel

    # Se já coletou 100 imóveis, sai do loop principal
    if len(dic_mobiliaria['metragem']) >= num_imoveis:
        print('Coletados 100 imóveis, finalizando.')
        break
    try:
        botao_proximo = WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.CSS_SELECTOR,'[data-testid="next-page"]')))
        if botao_proximo:
            driver.execute_script('arguments[0].scrollIntoView();',botao_proximo)
            time.sleep(1)

            driver.execute_script('arguments[0].click();', botao_proximo)
            print(f'indo para a pagin{pagina}')
            pagina +=1
            time.sleep(5)

        else: 
            print('voce esta na ultima pagina')
            break

    except Exception as e:
        print('erro ao tentar avancra para a proxima pagina')
        break

driver.quit()
dataframe = a.DataFrame(dic_mobiliaria)
dataframe.to_excel('imoveis.xlsx', index = False)

print(f'arquivo esta salvo com sucesso!')
