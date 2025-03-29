import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from zipfile import ZipFile

def setup_driver():
    """Configura o driver do Selenium (Chrome) em modo headless."""
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def handle_cookies_banner(driver, wait):
    possible_texts = ["Aceitar cookies", "Rejeitar cookies", "Gerenciar cookies"]
    for text in possible_texts:
        try:
            button = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//button[contains(text(), '{text}')]"))
            )
            button.click()
            print(f"Botão de cookies clicado: {text}")
            time.sleep(2)
            return
        except Exception:
            continue
    print("Nenhum botão de cookies foi encontrado.")

def download_file(url, filename):
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        with open(filename, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Download concluído: {filename}")
        return True
    except Exception as e:
        print(f"Erro ao baixar {url}: {e}")
        return False

def obter_link_por_click(driver, wait, xpath_text, anexo_label):
    try:
        print(f"Tentando clicar no elemento de {anexo_label}...")
        elemento = driver.find_element(By.XPATH, f"//*[contains(translate(text(), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{xpath_text}')]")
        original_window = driver.current_window_handle
        windows_before = driver.window_handles
        elemento.click()
        wait.until(EC.new_window_is_opened(windows_before))
        windows_after = driver.window_handles
        new_window = [w for w in windows_after if w != original_window][0]
        driver.switch_to.window(new_window)
        time.sleep(2)
        url_pdf = driver.current_url
        print(f"Link do {anexo_label} obtido na nova guia: {url_pdf}")
        driver.close()
        driver.switch_to.window(original_window)
        return url_pdf
    except Exception as e:
        print(f"Erro ao clicar e capturar o link do {anexo_label}: {e}")
        return None

def main():
    base_url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    output_dir = "anexos"
    zip_filename = "anexos_ans.zip"
    
    anexo_i_path = None
    anexo_ii_path = None
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        
        print("Iniciando navegador...")
        driver = setup_driver()
        wait = WebDriverWait(driver, 15)
        
        print(f"Acessando {base_url}...")
        driver.get(base_url)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        handle_cookies_banner(driver, wait)
        
        anexo_i_url = None
        anexo_ii_url = None
        
        all_links = driver.find_elements(By.TAG_NAME, "a")
        for link in all_links:
            href = link.get_attribute("href") or ""
            if ".pdf" in href.lower():
                text = link.text.lower()
                if ("anexo i" in text or "anexo_i" in href.lower()) and not anexo_i_url:
                    anexo_i_url = href
                elif ("anexo ii" in text or "anexo_ii" in href.lower()) and not anexo_ii_url:
                    anexo_ii_url = href
        
        if not anexo_i_url:
            anexo_i_url = obter_link_por_click(driver, wait, "anexo i", "Anexo I")
        if not anexo_ii_url:
            anexo_ii_url = obter_link_por_click(driver, wait, "anexo ii", "Anexo II")
        
        if not anexo_i_url:
            raise Exception("Não foi possível encontrar o link do Anexo I.pdf")
        if not anexo_ii_url:
            raise Exception("Não foi possível encontrar o link do Anexo II.pdf")
        
        print(f"URL do Anexo I: {anexo_i_url}")
        print(f"URL do Anexo II: {anexo_ii_url}")
        
        anexo_i_path = os.path.join(output_dir, "Anexo_I.pdf")
        anexo_ii_path = os.path.join(output_dir, "Anexo_II.pdf")
        
        print("Iniciando download dos arquivos...")
        if not download_file(anexo_i_url, anexo_i_path):
            raise Exception("Falha ao baixar Anexo I")
        if not download_file(anexo_ii_url, anexo_ii_path):
            raise Exception("Falha ao baixar Anexo II")
        
        print("Compactando arquivos...")
        with ZipFile(zip_filename, 'w') as zipf:
            zipf.write(anexo_i_path, os.path.basename(anexo_i_path))
            zipf.write(anexo_ii_path, os.path.basename(anexo_ii_path))
        
        print(f"Processo concluído! Arquivos compactados em: {zip_filename}")
        
    except Exception as e:
        print(f"ERRO: {e}")
        if 'driver' in locals():
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("HTML salvo em page_source.html")
    finally:
        if 'driver' in locals():
            driver.quit()
        for filepath in [anexo_i_path, anexo_ii_path]:
            if filepath and os.path.exists(filepath):
                try:
                    os.remove(filepath)
                except Exception as cleanup_error:
                    print(f"Erro ao remover {filepath}: {cleanup_error}")
        if os.path.exists(output_dir) and not os.listdir(output_dir):
            try:
                os.rmdir(output_dir)
            except Exception as cleanup_error:
                print(f"Erro ao remover o diretório {output_dir}: {cleanup_error}")

if __name__ == "__main__":
    main()
