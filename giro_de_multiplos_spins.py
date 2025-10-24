# Essa automação tem a finalidade de testar se a configuração de probabilidades está funcionando como esperado. O fluxo do teste consiste em solicitar a compra dos 
# bilhetes, em seguida confirmar o pagamento desses deles e por fim girar a roleta 10 vezes. 

import requests
import logging
import time

# Configuração básica de logging para exibir informações no console
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class AutomacaoSpin:
    """
    Classe para automatizar e contabilizar os giros da roleta (spins).
    """

    def __init__(self):
        """
        Inicializa o contador de prêmios.
        """
        self.contagem_premios = {
            "20 NÚMEROS": 0,
            "5 NÚMEROS": 0,
            "R$ 1000 REAIS": 0,
            "NÃO GANHOU": 0,
            "Iphone": 0,
            "15 NÚMEROS": 0,
            "10 NÚMEROS": 0
        }

    def girar_spin(self, cpf, nsu):
        """
        Envia uma única requisição para girar a roleta e contabiliza o resultado.
        """
        url = "https://api.exemplo.com/api2/spins"
        headers = {
            'Content-Type': 'application/json'
        }
        payload = {
            "cpf": cpf,
            "nsu": nsu
        }
        
        logging.info("Enviando requisição de spin...")
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            
            response_data = response.json()
            logging.info("[OK] Resposta do spin recebida.")
            
            prize = response_data.get('prize')
            
            if prize:
                logging.info(f"[SUCESSO] Prêmio obtido: {prize}")
                if prize in self.contagem_premios:
                    self.contagem_premios[prize] += 1
                else:
                    logging.warning(f"Prêmio desconhecido '{prize}' recebido e não contabilizado.")
                return response_data
            else:
                logging.error("A chave 'prize' não foi encontrada na resposta do spin.")
                logging.debug(f"Corpo da resposta: {response_data}")
                return None

        except requests.exceptions.HTTPError as http_err:
            logging.error(f"Erro HTTP ao girar spin: {http_err}")
            logging.error(f"Corpo da resposta de erro: {response.text}")
            return None
        except requests.exceptions.RequestException as e:
            logging.error(f"Falha na requisição para girar spin: {e}")
            return None
        except ValueError:
            logging.error("Falha ao decodificar a resposta. Não é um JSON válido.")
            logging.error(f"Conteúdo recebido: {response.text}")
            return None

    def girar_multiplos_spins(self, cpf, nsu, quantidade_giros=10):
        """
        Gira a roleta a quantidade de vezes especificada.
        """
        logging.info(f"Iniciando {quantidade_giros} giros da roleta para o NSU {nsu}...")
        for i in range(quantidade_giros):
            logging.info(f"--- Giro {i + 1}/{quantidade_giros} ---")
            self.girar_spin(cpf, nsu)

    def imprimir_resultados(self):
        """
        Imprime o resumo da contagem de todos os prêmios.
        """
        print("\n--- RESUMO DOS RESULTADOS ACUMULADOS DOS SPINS ---")
        for premio, contagem in self.contagem_premios.items():
            print(f"[{premio}]: {contagem} ocorrência(s)")
        print("---------------------------------------")


class AutomacaoPagamento:
    """
    Classe para automatizar o fluxo de criação e confirmação de pagamento via API.
    """
    def iniciar_pagamento(self):
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
            "captcha": "0.OFiR7aND1IfuUDauh220zloOFlAWPmgprP8v8nv6jsD2Op0N7rzMdS5TFQz8rlrM_vuTItc8wEyt0TApJSTMiS2HyQcPaxxdR0S2y4xmnjbkvF1l9HSxxilX5KqenbF3raeH6tqApKEI_jGh_34DSCmjBTeWtlUgiVipGV52uhDvMNE6xVKyYQZx6w8H8z7TsBCobRn6lZYZA-b8YVP-hNLT85FBUnQWR5lMP1ySolHZtf-ZHYd_hbbVVMrMdVSotHW261S6q3vXKPC2dCpZZ6ywTR6bSYkJMHgjUWYnBQtf8ngsANQ10Ta7sNnF_FIBHdeQTJbrHRGE5shg4kFPCtvbHF9Fr9AO8CDfkjHt-A2Vb6mvqWli3_VQfV3aUXFwmnBpBOGEDtbZr8Tua1xq98qT93FsBHUIS5kyTnPo2yWdVYI5vEdmWFMZnKzbdzwX2jcHqGE4HxS5myamTg3hilAFHeHEpm0LY1p36lCtmpYbgqpePrKzwdfpGPLwqY0DvXPu4LhEBJC3oqQhLClThlwg7rljwMbKUoUUG4V0zOycBDfDst3fWf64pvd6obtEhrJ_8pbc9rchS4nURd6GNGi0WBLmkWTvXG9gkiqHMM4ono0fAyh4tyM_ZC4TRvvziW8iaobeJcT1vd2iHDbj-_oYwKc6cIXK5WNMnRBiubzu_tWfqeH6vrJTfHyRIjWACU-KtD7Wyib09YUs7ZVTi57eSBXOyAAXPvEXm6WEXUwrzs2ZvE6-rZhcz9Oztaa4R1QgaO0UjxY_WxNzVJnmNqdYiOAmD_n7FOTyWakKEw6bj9ZjMC_-CNUn39I7xFPGGuCpgqPBbWU61HShOYNO6wmCZ9OBEo0LP4bsjrPTswIfsxpJMtTT6ZO_Jzt13IYRin4LN0ObuWukSxX_Pkc6FQ.tWnoUBKxXJmT5grans2FmA.d65cb5047aa8666c7f7a3e5a395e077b985af8267386eb7d7a7612efcff88e96",
            "quantity": 2,
            "edition": 2
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
        if not nsu or not value:
            logging.warning("NSU ou Value não fornecido. A confirmação do pagamento foi abortada.")
            return

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

    def executar_fluxo(self, automacao_spins, cpf_comprador="06077734489"):
        """
        Método auxiliar para executar um único ciclo de pagamento e spins.
        Recebe a instância de AutomacaoSpin para garantir a contagem cumulativa.
        """
        logging.info("--- INICIANDO FLUXO DE TESTE ---")
        
        dados_pagamento = self.iniciar_pagamento()
        
        if dados_pagamento:
            nsu_capturado = dados_pagamento['nsu']
            valor_capturado = dados_pagamento['value']

            pagamento_confirmado = self.confirmar_pagamento(nsu_capturado, valor_capturado)
            
            if pagamento_confirmado:
                automacao_spins.girar_multiplos_spins(
                    cpf=cpf_comprador, 
                    nsu=nsu_capturado, 
                    quantidade_giros=10
                )
            else:
                logging.error("A confirmação do pagamento falhou. Os spins não foram executados.")
        else:
            logging.error("O fluxo de pagamento falhou. NSU e/ou valor não puderam ser obtidos.")
            
        logging.info("--- FIM DO FLUXO DE TESTE ---")


# --- BLOCO PRINCIPAL COM O LOOP ---
if __name__ == '__main__':
    # 1. Define quantas vezes o fluxo completo será repetido.
    numero_de_repeticoes = 1000 
    
    # 2. Cria as instâncias das classes UMA ÚNICA VEZ, antes do loop.
    automacao_completa = AutomacaoPagamento()
    automacao_spins = AutomacaoSpin()
    
    # 3. Loop para repetir o fluxo.
    for i in range(numero_de_repeticoes):
        print(f"\n================ REPETIÇÃO {i + 1}/{numero_de_repeticoes} ================")
        
        # Chama o método auxiliar, passando a mesma instância de automacao_spins
        automacao_completa.executar_fluxo(automacao_spins, cpf_comprador="06077734489")
        
        # Adiciona um pequeno atraso entre as repetições
        time.sleep(2)
        
    print("\n================ TESTE CONCLUÍDO ================")
    # 4. Imprime o resumo final ACUMULADO de todas as repetições.
    automacao_spins.imprimir_resultados()