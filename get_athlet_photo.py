"""from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from concurrent.futures import ThreadPoolExecutor
import pandas as pd
from queue import Queue

num = 0

csv_atleta = 'C:/Users/user/Desktop/Desafio #05 Comunidade Data Driven/05-Olimpiadas/split_atletas{}.csv'.format(num)

arquivo_destino = 'C:/Users/user/Desktop/Desafio #05 Comunidade Data Driven/05-Olimpiadas/foto_atletas{}.csv'.format(num)

# habilitando opções para abrir o navegador sem erros, ingorar site inseguro e abrir usando um perfil logado
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches",["enable-automation", 'enable-logging'])
chrome_options.add_argument("--disable-blink-features=AutomationControlled") 
# chrome_options.add_argument('start-maximized')
# chrome_options.add_argument('--disable-infobars')
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--ignore-ssl-errors')
chrome_options.add_argument('--ignore-certificate-errors-spki-list')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--no-zygote')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36')
# chrome_options.add_argument('--profile-directory=Default')
# chrome_options.add_argument("user-data-dir=C:/Users/user/AppData/Local/Google/Chrome/User Data") 
chrome_options.add_argument('--headless=new')  # Executar o navegador em segundo plano
chrome_options.add_argument('--disable-gpu')

list_url = list()

def coletar_dados(atleta):
    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(0.5)
    # driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})") 
    
    driver.get(atleta)
    
    try:
        user = driver.find_element(By.XPATH, "//*[@id=\"globalTracking\"]/div/section[1]/div[1]/div[1]/div/div/div/picture/img").get_attribute('src')
        list_url.append(user)
    
    except NoSuchElementException:
        list_url.append('')
    
    finally:
        driver.quit()
        
def salvar_fotos(list_atleta):
    
    df = pd.DataFrame.from_dict({
        'atleta': list_atleta,
        'foto':  list_url
    })
    
    df.to_csv(arquivo_destino, index=False)
    
    
def ler_atletas():    
    atletas = pd.read_csv(csv_atleta)
    lista_atleta = atletas['atleta'].str.strip().tolist()
    # lista_atleta = ['https://olympics.com/en/athletes/cooper-woods-topalovic',
    # 'https://olympics.com/en/athletes/elofsson',
    # 'https://olympics.com/en/athletes/dylan-walczyk',
    # 'https://olympics.com/en/athletes/olli-penttala',
    # 'https://olympics.com/en/athletes/reikherd',
    # 'https://olympics.com/en/athletes/matt-graham',
    # 'https://olympics.com/en/athletes/ikuma-horishima',
    # 'https://olympics.com/en/athletes/daichi-hara',
    # 'https://olympics.com/en/athletes/laurent-dumais',
    # 'https://olympics.com/en/athletes/james-matheson',
    # 'https://olympics.com/en/athletes/pavel-kolmakov',
    # 'https://olympics.com/en/athletes/kosuke-sugimoto',
    # 'https://olympics.com/en/athletes/brodie-summers',
    # 'https://olympics.com/en/athletes/severi-vierela',
    # 'https://olympics.com/en/athletes/marco-tade',
    # 'https://olympics.com/en/athletes/william-feneley',
    # 'https://olympics.com/en/athletes/mikael-kingsbury',
    # 'https://olympics.com/en/athletes/so-matsuda',
    # 'https://olympics.com/en/athletes/wallberg',
    # 'https://olympics.com/en/athletes/bradley-wilson'
    # ]

    with ThreadPoolExecutor(max_workers=2) as executor:  # Ajuste o número de threads conforme necessário
        executor.map(coletar_dados, lista_atleta)
        executor.shutdown(wait=True) 
    
    # for i in lista_atleta:
        # coletar_dados(i.strip())
    
    salvar_fotos(lista_atleta)
    
if __name__ == '__main__':
    ler_atletas()"""
    
    
    
import requests
from bs4 import BeautifulSoup
import pandas as pd

num = 0

csv_atleta = 'C:/Users/user/Desktop/Desafio #05 Comunidade Data Driven/05-Olimpiadas/olympic_athletes.csv'
# csv_atleta = 'C:/Users/user/Desktop/Desafio #05 Comunidade Data Driven/05-Olimpiadas/split_atletas{}.csv'.format(num)

arquivo_destino = 'C:/Users/user/Desktop/Desafio #05 Comunidade Data Driven/05-Olimpiadas/foto_atletas.csv'
# arquivo_destino = 'C:/Users/user/Desktop/Desafio #05 Comunidade Data Driven/05-Olimpiadas/foto_atletas{}.csv'.format(num)

list_url = list()

def coletar_dados(atleta):
    # print('entrou')
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    })
    
    try:
        # Fazer a requisição para a página do atleta
        response = session.get(atleta, timeout=3)
        # print('fez request')
        if response.status_code == 200:
            # Parsear o conteúdo HTML com BeautifulSoup
            # print('site')
            soup = BeautifulSoup(response.text, 'html.parser')
            # Procurar a imagem do atleta usando o XPath antigo convertido para um seletor CSS
            user = soup.select_one("#globalTracking > div > section:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(1) > div > div > div > picture > img")
            
            # Verificar se a imagem foi encontrada e obter o atributo 'src'
            if user:
                # print('tem foto')
                list_url.append(user.get('src'))
            else:
                # print('sem foto')
                list_url.append('')
        else:
            # print('erro site')
            list_url.append('')
    
    except Exception as e:
        # print(f"Erro ao processar {atleta}: {e}")
        list_url.append('')
        

def salvar_fotos(list_atleta):
    df = pd.DataFrame.from_dict({
        'atleta': list_atleta,
        'foto':  list_url
    })
    
    df.to_csv(arquivo_destino, index=False)
    
def ler_atletas():    
    atletas = pd.read_csv(csv_atleta)
    lista_atleta = atletas['athlete_url'].str.strip().tolist()
    # lista_atleta = atletas['atleta'].str.strip().tolist()
    
    # lista_atleta = ['https://olympics.com/en/athletes/cooper-woods-topalovic',
    # 'https://olympics.com/en/athletes/elofsson',
    # 'https://olympics.com/en/athletes/dylan-walczyk',
    # 'https://olympics.com/en/athletes/olli-penttala',
    # 'https://olympics.com/en/athletes/reikherd',
    # 'https://olympics.com/en/athletes/matt-graham',
    # 'https://olympics.com/en/athletes/ikuma-horishima',
    # 'https://olympics.com/en/athletes/daichi-hara',
    # 'https://olympics.com/en/athletes/laurent-dumais',
    # 'https://olympics.com/en/athletes/james-matheson',
    # 'https://olympics.com/en/athletes/pavel-kolmakov',
    # 'https://olympics.com/en/athletes/kosuke-sugimoto',
    # 'https://olympics.com/en/athletes/brodie-summers',
    # 'https://olympics.com/en/athletes/severi-vierela',
    # 'https://olympics.com/en/athletes/marco-tade',
    # 'https://olympics.com/en/athletes/william-feneley',
    # 'https://olympics.com/en/athletes/mikael-kingsbury',
    # 'https://olympics.com/en/athletes/so-matsuda',
    # 'https://olympics.com/en/athletes/wallberg',
    # 'https://olympics.com/en/athletes/bradley-wilson'
    # ]
    
    j = 0
    for i in lista_atleta:
        print('atleta ',j)
        j+=1
        coletar_dados(i.strip())
    
    salvar_fotos(lista_atleta)

if __name__ == '__main__':
    ler_atletas()