# testes-de-performance-rifas
Testes de performance aplicados à plataforma de rifas.

🎰 **Teste de Probabilidade da Roleta (Spin Automation)**

🎯 **Objetivo**

O objetivo desta automação é validar se a configuração de probabilidades de prêmios da Roleta (Spin) está funcionando conforme o esperado, especialmente após a aquisição e confirmação de pagamento de bilhetes.

O teste simula um cenário real de usuário que compra bilhetes e, em seguida, utiliza os spins liberados por essa compra.

⚙️ **Pré-requisitos**
- Python 3.x
- Biblioteca requests
- Conexão ativa com as APIs de destino (api.exemplo.com).

🚀 **Fluxo de Execução do Teste**

O script executa um fluxo completo, que é repetido 1000 vezes (conforme a variável numero_de_repeticoes no bloco principal), para coletar uma amostra estatisticamente significativa dos resultados da roleta.

**O ciclo de teste é o seguinte:**

1. **Iniciação do Pagamento (Compra de Bilhetes):**
  - O método iniciar_pagamento da classe AutomacaoPagamento envia uma requisição para a API de depósitos (/api2/deposits) para simular a compra de bilhetes, capturando o NSU (Número Sequencial Único) e o Valor da transação.
2. **Confirmação do Pagamento:**
  - O método confirmar_pagamento da classe AutomacaoPagamento envia uma requisição de callback ou atualização (/api2/services/deposit/updates) para simular a aprovação do pagamento, usando o NSU capturado.
3. **Execução dos Spins (Giros da Roleta):**
  - O método girar_multiplos_spins da classe AutomacaoSpin é chamado para simular 10 giros da roleta (conforme a variável quantidade_giros), utilizando o CPF e o NSU da transação aprovada.Cada giro individual é registrado pelo método girar_spin.
4. **Contabilização e Resumo:**
  - A classe **AutomacaoSpin** acumula a contagem de todos os prêmios obtidos ao longo de todas as 1000 repetições do fluxo.
  - Ao final de todas as repetições, o método imprimir_resultados exibe o resumo total da contagem de cada prêmio.

📝 **Como Analisar os Resultados**

Ao final da execução (após as 1000 repetições), o resumo exibido (imprimir_resultados) deve ser comparado com as probabilidades configuradas no sistema:

- **Prêmio Esperado:** A contagem de cada prêmio no resumo final deve ser proporcional à sua probabilidade de ocorrência.
- **Detecção de Problemas:** Uma discrepância significativa (por exemplo, um prêmio de 10% aparecendo apenas 1% das vezes, ou um prêmio de 1% aparecendo 50% das vezes) pode indicar um problema na lógica de distribuição de probabilidades da API de Spin.

🛑 **ObservaçãoAs URLs e dados de payload (como CPF, e-mail, captcha e URLs de API) são dados fictícios/de exemplo e devem ser substituídos pelos dados reais do ambiente de teste.**
