# ⚙️ CONFIGURE O ARQUIVO WSGI NO PYTHONANYWHERE

## 1. Acesse o arquivo WSGI

### No PythonAnywhere:
```
Painel → Web → Arquivo de configuração WSGI
```

Você deve ver um link como:
```
/var/www/tauan_pythonanywhere_com_wsgi.py
```

Clique nesse link para abrir o editor.

---

## 2. EXCLUA TODO O CONTEÚDO ATUAL

Selecione tudo e delete (Ctrl+A → Delete)

---

## 3. COPIE E COLE EXATAMENTE ESTE CÓDIGO:

```python
import os
import sys

# Caminho da pasta raiz do seu projeto
path = '/home/tauan/Feed_box'

if path not in sys.path:
    sys.path.append(path)

# Define qual arquivo settings.py usar
os.environ['DJANGO_SETTINGS_MODULE'] = 'feedback_system.settings'

# Carrega a aplicação WSGI do Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

---

## 4. CLIQUE EM "SAVE"

Salve o arquivo.

---

## 5. VOLTE À ABA "Web" E CLIQUE EM "RELOAD"

O PythonAnywhere irá recarregar a aplicação com o novo WSGI.

---

## ✅ PRONTO!

Seu WSGI agora está correto para:
- 📁 Projeto em: `/home/tauan/Feed_box`
- ⚙️ Settings em: `feedback_system/settings.py`
- 🐍 Python: `3.10`
- 🔗 Virtualenv: `/home/tauan/.virtualenvs/feedback_system_env`

---

## ❓ Se der erro após reload:

Verifique o **error log**:
```
Painel → Web → Logs → error log
```

Os erros comuns são:
1. **ModuleNotFoundError: textblob** → `pip install textblob` no console
2. **ALLOWED_HOSTS violation** → Altere em `settings.py` linha 28
3. **Static files 404** → `python manage.py collectstatic --noinput` no console
4. **Database error** → `python manage.py migrate` no console
