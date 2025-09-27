# Proxy Interno para API de Score

## Descrição
Proxy resiliente para consumir a API de score com rate limiting de 1 req/s.


---

## 🚀 COMO EXECUTAR:

```bash
# 1. Criar diretório e arquivos
mkdir proxy_score
cd proxy_score
# Cole cada arquivo conforme a estrutura acima

# 2. Instalar dependências
pip install -r requirements.txt

# 3. Configurar variável de ambiente
export CLIENT_ID="seu_client_id_aqui"

# 4. Executar
python main.py

# 5. Testar (em outro terminal)
python test_burst.py