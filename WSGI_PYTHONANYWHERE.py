"""
===============================================
ARQUIVO WSGI PARA PYTHONANYWHERE
===============================================

Nome do arquivo no servidor:
/var/www/tauan_pythonanywhere_com_wsgi.py

Estrutura do projeto:
/home/tauan/Feed_box/
├── manage.py
├── feedback_system/
│   ├── settings.py         ← Django procura aqui
│   ├── urls.py
│   ├── wsgi.py
│   └── __init__.py
├── accounts/
├── feedbacks/
├── clima/
├── setores/
├── templates/
├── static/
├── staticfiles/            ← Criado pelo collectstatic
├── inicial.json
└── requirements.txt

===============================================
EXPLICAÇÃO DO ARQUIVO WSGI:
===============================================

1. Adiciona o projeto ao Python PATH
   → Django consegue importar os módulos (feedback_system, accounts, etc)

2. Define qual settings.py usar
   → 'feedback_system.settings' aponta para feedback_system/settings.py

3. Carrega a aplicação WSGI
   → PythonAnywhere chama esse 'application' para processar requisições HTTP

===============================================
"""

import os
import sys

# ========== CONFIGURAÇÃO DO PATH DO PROJETO ==========

# Caminho da pasta raiz do seu projeto
# IMPORTANTE: Use o caminho EXATO do seu servidor PythonAnywhere
path = '/home/tauan/Feed_box'

# Adiciona ao Python path se não existir
if path not in sys.path:
    sys.path.append(path)


# ========== CONFIGURAÇÃO DO DJANGO ==========

# Define qual arquivo settings.py usar
# feedback_system/settings.py é a pasta de configuração principal
# se tivesse em outra pasta (ex: setup/), seria 'setup.settings'
os.environ['DJANGO_SETTINGS_MODULE'] = 'feedback_system.settings'

# Garante que as variáveis de ambiente do Django estão carregadas
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'feedback_system.settings')


# ========== CARREGA A APLICAÇÃO WSGI ==========

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
except Exception as e:
    # Se der erro, logue aqui para debug
    import traceback
    print(f"Erro ao carregar WSGI: {e}")
    traceback.print_exc()
    raise


# ========== NOTA IMPORTANTE ==========
# Se você receber erro como:
# - "ModuleNotFoundError: No module named 'textblob'"
#   → No console, rode: pip install textblob
#
# - "ALLOWED_HOSTS violation"
#   → No settings.py, altere para: ALLOWED_HOSTS = ['tauan.pythonanywhere.com', 'localhost']
#
# - "Static files not found"
#   → No console, rode: python manage.py collectstatic --noinput
#
# - "No such table"
#   → No console, rode: python manage.py migrate
#
# Depois clique em "Reload" na aba Web do PythonAnywhere
