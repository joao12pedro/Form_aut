import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

# Caminho do ChromeDriver
chrome_driver_path = r'C:\Users\Prefeitura\Downloads\chromedriver-win64\chromedriver.exe'

# Configurações do Chrome
service = Service(chrome_driver_path)
chrome_options = Options()
chrome_profile_path = r'C:\Users\Prefeitura\AppData\Local\Google\Chrome\User Data\Profile 1'
chrome_options.add_argument(f"user-data-dir={chrome_profile_path}")
chrome_options.add_argument("--start-maximized")

# Inicia o WebDriver
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.get("https://web.whatsapp.com")
print("Aguardando login no WhatsApp Web...")


# Aguarda o login
def esperar_login(timeout=300):
    try:
        search_box = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@role="textbox" and @contenteditable="true" and @spellcheck="true"]')
            )
        )
        print("Login realizado com sucesso!")
        return search_box
    except TimeoutException:
        print("Tempo limite para login atingido.")
        driver.quit()
        exit()


search_box = esperar_login()
driver.minimize_window()

# Solicita o nome do contato
nome_contato = input("Digite o nome do contato para visualizar as mensagens: ")

# Realiza a busca do contato
search_box.click()
search_box.clear()
search_box.send_keys(nome_contato)
time.sleep(2)
driver.maximize_window()
search_box.send_keys(Keys.ENTER)


# Aguarda a conversa carregar completamente
def esperar_conversa_carregar(timeout=20, min_mensagens=5):
    tempo_decorrido = 0
    mensagens = []

    while tempo_decorrido < timeout:
        time.sleep(2)
        mensagens = driver.find_elements(By.XPATH,
                                         '//div[contains(@class, "message-in") or contains(@class, "message-out")]')

        if len(mensagens) >= min_mensagens:
            print(f"Conversa carregada com sucesso! {len(mensagens)} mensagens sincronizadas.")
            return mensagens

        print(f"Aguardando sincronização... {len(mensagens)} mensagens carregadas.")
        tempo_decorrido += 2

    print("Falha ao carregar a conversa completamente.")
    return mensagens


mensagens = esperar_conversa_carregar()


# Função para capturar e baixar até 3 imagens
def capturar_e_baixar_imagens():
    try:
        # Filtra as mensagens que possuem imagens
        imagens = []
        for mensagem in mensagens[::-1]:  # Inverte para pegar as mais recentes primeiro
            try:
                imagem_elemento = mensagem.find_element(By.XPATH, './/img[contains(@src, "blob:")]')
                imagens.append(imagem_elemento)
                if len(imagens) == 3:
                    break
            except NoSuchElementException:
                continue

        if not imagens:
            print("Nenhuma imagem encontrada.")
            return

        # Clica na primeira imagem para abrir o visualizador
        imagens[0].click()
        time.sleep(2)

        # Função auxiliar para fazer download da imagem visível
        def baixar_imagem():
            try:
                download_element = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//button[@role="button" and @title="Baixar"]'))
                )
                download_element.click()
                print("Download iniciado com sucesso!")
                time.sleep(5)  # Aguarda o download concluir
            except TimeoutException:
                print("Botão de download não encontrado ou tempo esgotado.")

        # Baixa até 3 imagens
        for i in range(min(6, len(imagens))):
            baixar_imagem()
            if i < len(imagens) - 1:  # Não tenta avançar após a última imagem
                try:
                    next_button = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, '//div[@role="button" and @aria-label="Anterior"]'))
                    )
                    next_button.click()
                    print(f"Avançando para a imagem {i + 2}...")
                    time.sleep(2)
                except TimeoutException:
                    print("Não foi possível avançar para a próxima imagem.")
                    break

        # Fecha o visualizador de imagens
        try:
            close_button = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '//div[@role="button" and @title="Fechar"]'))
            )
            close_button.click()
            print("Visualizador de imagem fechado.")
        except TimeoutException:
            print("Botão de fechar não encontrado.")

    except Exception as e:
        print(f"Erro ao capturar as imagens: {e}")


# Chama a função para capturar e baixar imagens
capturar_e_baixar_imagens()

# Encerra o WebDriver
driver.quit()
