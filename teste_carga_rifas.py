# Esse teste visava acompanhar o comportamento da aplicação com uma grande quantidade de requisições sendo feita. Como se trata de um sistema menos complexo, optei por
# não utilizar o K6 nesse teste.

import concurrent.futures
import time
import requests
import logging
from datetime import datetime

# Configuração básica de logging para exibir informações no console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutomacaoPagamento:
    """
    Classe para automatizar o fluxo de criação, confirmação e spin de pagamento via API.
    """

    def iniciar_pagamento(self):
        """
        Envia a requisição inicial para gerar um depósito e captura o NSU da resposta.
        
        Returns:
            dict: Um dicionário contendo 'nsu' e 'value' capturados da resposta, ou None se ocorrer um erro.
        """
        url = "https://api.exemplo.com/api2/deposits"
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "Buyer": {
                "cpf": "11111111111", 
                "email": "fil******", 
                "name": "fil******", 
                "phone": "+55******", 
                "birthday": "199******"
            },
            "captcha": "0.OFiR7aND1IfuUDauh220zloOFlAWPmgprP8v8nv6jsD2Op0N7rzMdS5TFQz8rlrM_vuTItc8wEyt0TApJSTMiS2HyQcPaxxdR0S2y4xmnjbkvF1l9HSxxilX5KqenbF3raeH6tqApKEI_jGh_34DSCmjBTeWtlUgiVipGV52uhDvMNE6xVKyYQZx6w8H8z7TsBCobRn6lZYZA-b8YVP-hNLT85FBUnQWR5lMP1ySolHZtf-ZHYd_hbbVVMrMdVSotHW261S6q3vXKPC2dCpZZ6ywTR6bSYkJMHgjUWYnBQtf8ngsANQ10Ta7sNnF_FIBHdeQTJbrHRGE5shg4kFPCtvbHF9Fr9AO8CDfkjHt-A2Vb6mvqWli3_VQfV3aUXFwmnBpBOGEDtbZr8Tua1xq98qP93FsBHUIS5kyTnPo2yWdVYI5vEdmWFMZnKzbdzwX2jcHqGE4HxS5myamTg3hilAFHeHEpm0LY1p36lCtmpYbgqpePrKzwdfpGPLwqY0DvXPu4LhEBJC3oqQhLClThlwg7rljwMbKUoUUG4V0zOycBDfDst3fWf64pvd5obtEhrJ_8pbc9rchS4nURd6GNGi0WBLmkWTvXG9gkiqHMM4ono0fAyh4tyz_ZC4TRvvziW8iaobeJcT1vd2iHDbj-_oYwKc6cIXK5WNMnRBiubzu_tWfqeH6vrJTfHyRIjWACU-KtD7Wyib09YUs7ZVTi57eSBXOyAAXPvEXm6WEXUwrzs2ZvE6-rZhcz9Oztaa4R1QgaO0UjxY_WxNzVJnmNqdYiOAmD_n7FOTyWakKEw6bj9ZjMC_-CNUn39I7xFPGGuCpgqPBbWU61HShOYNO6wmCZ8OBEo0LP4bsjrPTswIfsxpJMlTT6ZO_Jzt13IYRin4LN0ObuWukSxX_Pkc6FQ.tWnoUBKxXJmT5grans2FmA.d65cb5047aa8666c7f7a3e5a395e077b985af8267386eb7d7a7612efcff88e96",
            "quantity": 5,
            "edition":5
        }
        
        logging.info("Enviando requisição para iniciar pagamento...")
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            response_data = response.json()
            logging.info("[OK] Resposta da iniciação de pagamento recebida.")
            
            nsu = response_data.get('data', {}).get('nsu')
            value = response_data.get('data', {}).get('value')

            if not nsu: 
                nsu = response_data.get('nsu')

            if value is None:
                value = response_data.get('value')

            if nsu and value is not None:
                logging.info(f"[SUCESSO] NSU capturado: {nsu}")
                logging.info(f"[SUCESSO] Valor capturado: {value}")
                return {'nsu': nsu, 'value': value}
            else:
                logging.error("A chave 'nsu' e/ou 'value' não foi encontrada na resposta da API.")
                logging.debug(f"Corpo da resposta: {response_data}")
                return None

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP ao iniciar pagamento: {http_err}")
            logging.error(f"Corpo da resposta de erro: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Falha na requisição para iniciar pagamento: {e}")
            return None
        except ValueError:
            logging.error("Falha ao decodificar a resposta. Não é um JSON válido.")
            logging.error(f"Conteúdo recebido: {response.text}")
            return None

    def confirmar_pagamento(self, nsu, value):
        """
        Envia uma requisição POST para confirmar/simular o pagamento usando um NSU.
        """
        if not nsu or value is None:
            logging.warning("NSU ou Value não fornecidos. A confirmação do pagamento foi abortada.")
            return False
        
        url = "https://api.exemplo.com/api2/services/deposit/updates"
        payload = {
            "data": {
                "txId": nsu,
                "endToEndId": "E12345678202009091221abcdef12345",
                "createdAt": "2020-09-09T20:15:00.358Z",
                "payment": {"amount": f"{value}"},
                "debtorAccount": {"name": "Nome Pagador Teste", "document": "11111111111"}
            }
        }
        headers = {'Content-Type': 'application/json'}
        
        logging.info(f"Enviando requisição de confirmação para o NSU: {nsu}")
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            logging.info(f"[SUCESSO] Requisição de confirmação enviada. Status: {response.status_code}")
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"Falha ao enviar requisição de confirmação para o NSU '{nsu}': {e}")
            return False

    def enviar_spin(self, nsu):
        """
        Envia a requisição POST para o endpoint /api2/spin usando o NSU.
        Esta requisição será enviada 3 vezes com 2 segundos de intervalo.
        """
        if not nsu:
            logging.warning("NSU não fornecido para o spin. O spin foi abortado.")
            return False

        url = "https://api.exemplo.com/api2/spins"
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "cpf": "11111111111", 
            "nsu": nsu
        }

        for i in range(1, 4): # Envia 3 vezes
            logging.info(f"[{i}/3] Enviando requisição de spin para o NSU: {nsu}")
            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                logging.info(f"[SUCESSO] Spin {i} enviado para NSU '{nsu}'. Status: {response.status_code}")
                # logging.debug(f"Resposta do spin: {response.text}") # Descomente para ver a resposta do spin
            except requests.exceptions.RequestException as e:
                logging.error(f"Falha ao enviar spin {i} para NSU '{nsu}': {e}")
                # Não retorna False aqui para permitir as próximas tentativas, mas registra a falha.
            
            if i < 3: # Não espera após a última tentativa
                time.sleep(2) # Espera 2 segundos antes da próxima tentativa
        return True # Retorna True se todas as tentativas foram feitas (independentemente de falhas individuais)

    def executar_fluxo_de_pagamento(self):
            """
            Orquestra a execução do fluxo completo de automação: iniciar, confirmar e spin.
            """
            logging.info("--- INICIANDO FLUXO DE TESTE DE PAGAMENTO ---")
            
            dados_pagamento = self.iniciar_pagamento()
            
            if dados_pagamento:
                nsu_capturado = dados_pagamento['nsu']
                valor_capturado = dados_pagamento['value']
                
                # Confirma o pagamento
                if self.confirmar_pagamento(nsu_capturado, valor_capturado):
                    # Envia o spin se a confirmação foi bem-sucedida
                    self.enviar_spin(nsu_capturado)
                    logging.info("--- FLUXO DE TESTE DE PAGAMENTO CONCLUÍDO COM SUCESSO ---")
                    return True # Indica sucesso do fluxo completo
                else:
                    logging.error("O fluxo de pagamento falhou na etapa de confirmação.")
                    logging.info("--- FLUXO DE TESTE DE PAGAMENTO FALHOU ---")
                    return False
            else:
                logging.error("O fluxo de pagamento falhou pois o NSU e/ou o valor não puderam ser obtidos.")
                logging.info("--- FLUXO DE TESTE DE PAGAMENTO FALHOU ---")
                return False


def run_single_payment_flow():
    """Função wrapper para executar um único fluxo de pagamento."""
    automacao_qa = AutomacaoPagamento()
    return automacao_qa.executar_fluxo_de_pagamento()

if __name__ == '__main__':
    num_requests_per_minute = 100
    duration_minutes = 1 # Ajuste para a duração desejada do teste
    
    total_requests_to_send = num_requests_per_minute * duration_minutes
    requests_sent = 0
    successful_flows = 0
    failed_flows = 0
    start_time = time.time()

    logging.info(f"Iniciando teste de carga: {num_requests_per_minute} fluxos de pagamento por minuto por {duration_minutes} minuto(s).")

    # Ajuste max_workers para o número de fluxos simultâneos que você quer permitir.
    # Um valor razoável seria entre 10 a 50, dependendo dos recursos da sua máquina.
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor: 
        futures = []
        for i in range(total_requests_to_send):
            futures.append(executor.submit(run_single_payment_flow))
            requests_sent += 1
            
            # Controle de taxa (um pouco mais robusto para tentar manter o ritmo)
            elapsed = time.time() - start_time
            expected_elapsed_for_current_request = (i + 1) * (60 / num_requests_per_minute)
            if elapsed < expected_elapsed_for_current_request:
                # O atraso é calculado para distribuir as requisições uniformemente ao longo do minuto.
                time.sleep(expected_elapsed_for_current_request - elapsed)

        # Coleta os resultados de todos os fluxos
        for future in concurrent.futures.as_completed(futures):
            try:
                if future.result(): # True para sucesso, False para falha do fluxo
                    successful_flows += 1
                else:
                    failed_flows += 1
            except Exception as exc:
                logging.error(f'Um fluxo de pagamento gerou uma exceção não esperada: {exc}')
                failed_flows += 1

    end_time = time.time()
    total_duration = end_time - start_time

    logging.info(f"\n--- RELATÓRIO DO TESTE DE CARGA ---")
    logging.info(f"Duração total: {total_duration:.2f} segundos")
    logging.info(f"Total de fluxos de pagamento tentados: {requests_sent}")
    logging.info(f"Fluxos de pagamento bem-sucedidos: {successful_flows}")
    logging.info(f"Fluxos de pagamento com falha: {failed_flows}")
    logging.info(f"Taxa de execução de fluxos: {requests_sent / total_duration:.2f} fluxos/segundo ({requests_sent / total_duration * 60:.2f} fluxos/minuto)")