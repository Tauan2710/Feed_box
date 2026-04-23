# 🚀 GUIA COMPLETO - DEPLOYMENT PYTHONANYWHERE
## Feedbox - Gestão de Feedback com IA e eNPS

**Projeto:** [Tauan2710/Feed_box](https://github.com/Tauan2710/Feed_box)  
**Username PythonAnywhere:** tauan  
**Domínio Final:** tauan.pythonanywhere.com  
**Atualizado:** Baseado na estrutura real do servidor

---

## ⚠️ PASSO 0 - UPLOAD DO PROJETO (IMPORTANTE!)

### Antes de qualquer configuração, você precisa enviar seu projeto para o PythonAnywhere!

### Opção 1: Clone do GitHub (Recomendado)
```bash
# No terminal do PythonAnywhere
cd /home/tauan
# Se quiser clonar com nome de pasta Feed_box
git clone https://github.com/Tauan2710/Feed_box.git Feed_box
```

### Opção 2: Upload via ZIP
1. No seu computador: Zip a pasta `feedback_system`
2. No PythonAnywhere: `Files` → `Upload a file` → Selecione o ZIP
3. Extraia: `unzip feedback_system.zip`

### Verifique se funcionou:
```bash
ls -la /home/tauan/
```
Deve aparecer a pasta `Feed_box/`

---

## 📁 ESTRUTURA REAL DO SEU PROJETO

```
/home/tauan/Feed_box/               ← PASTA RAIZ (Source code)
├── accounts/                                  ← App de autenticação
│   ├── migrations/, models.py, views.py, urls.py
├── clima/                                     ← App de pesquisas de clima
│   ├── migrations/, models.py, views.py, forms.py
├── feedbacks/                                 ← App principal de feedback
│   ├── migrations/, models.py, views.py, forms.py
├── feedback_system/                           ← CONFIGURAÇÕES DJANGO
│   ├── settings.py       ← Arquivo mais importante!
│   ├── urls.py
│   ├── wsgi.py
│   └── views.py
├── setores/                                   ← App de setores
│   ├── migrations/, models.py
├── static/                                    ← Pasta de desenvolvimento
│   └── images/
├── staticfiles/                               ← Pasta de produção (criada)
├── templates/                                 ← Templates HTML globais
├── manage.py                                  ← Comando Django
├── db.sqlite3                                 ← Banco de dados
├── inicial.json                               ← Dados iniciais
├── requirements.txt                           ← Dependências
└── [outros arquivos]
```

---

## ⚙️ CONFIGURAÇÃO - PASSO A PASSO VISUAL

### PASSO 1 - ABA "WEB" → Source code

**Na interface do PythonAnywhere:**
```
Painel → Web → Source code
```

**Preencha com:**
```
/home/tauan2710/feedback_system
```

✅ **Confirmação:** Deve apontar para a pasta raiz onde está `manage.py`

---

### PASSO 2 - ABA "WEB" → Virtualenv

**Na interface do PythonAnywhere:**
```
Painel → Web → Virtualenv
```

**Preencha com:**
```
/home/tauan2710/.virtualenvs/feedback_system_env
```

✅ **Confirmação:** Deve apontar para a pasta `.virtualenvs` do seu usuário

---

### PASSO 3 - ABA "WEB" → Static files

**Na interface do PythonAnywhere:**
```
Painel → Web → Static files
```

**Configure UMA linha apenas:**

| URL | Path |
|-----|------|
| `/static/` | `/home/tauan2710/feedback_system/staticfiles` |

⚠️ **IMPORTANTE:** 
- Use `staticfiles/` (com "s"), NÃO `static/`
- Django copiará os arquivos com `collectstatic`

---

### PASSO 4 - ABA "WEB" → Arquivo WSGI

**Na interface do PythonAnywhere:**
```
Painel → Web → Arquivo de configuração: /var/www/tauan2710_pythonanywhere_com_wsgi.py
```

**Clique no link do arquivo e substitua TODO o conteúdo por:**

```python
import os
import sys

# Adiciona a pasta do projeto ao Python path
path = '/home/tauan2710/feedback_system'
if path not in sys.path:
    sys.path.append(path)

# Define qual arquivo settings.py usar
os.environ['DJANGO_SETTINGS_MODULE'] = 'feedback_system.settings'

# Carrega e retorna a aplicação WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

✅ **Confirmação:** Salve o arquivo após colar

---

## 🔧 CONFIGURAÇÃO - FILE SETTINGS.PY

**Arquivo no seu computador:**
```
feedback_system/settings.py
```

### Altere a linha 28 de:
```python
ALLOWED_HOSTS = ['seu-usuario.pythonanywhere.com', 'localhost', '127.0.0.1']
```

### Para:
```python
ALLOWED_HOSTS = ['tauan2710.pythonanywhere.com', 'localhost', '127.0.0.1']
```

✅ **Confirmação:**
- Linha 26: `DEBUG = False` (correto para produção)
- Linha 28: `ALLOWED_HOSTS` inclui seu domínio
- Linhas 135-138: `STATIC_ROOT` aponta para `staticfiles/` ✅

---

## 💻 TERMINAL PYTHONANYWHERE - COMANDOS

### Acesso:
```
PythonAnywhere → Consoles → Bash
```

### Execute na sequência (copie e cole um de cada vez):

#### 1. Navegue até a pasta:
```bash
cd /home/tauan2710/feedback_system
```

#### 2. Ative o ambiente virtual:
```bash
source /home/tauan2710/.virtualenvs/feedback_system_env/bin/activate
```
(Deve aparecer `(feedback_system_env)` no começo da linha)

#### 3. Instale as dependências:
```bash
pip install -r requirements.txt
```

#### 4. Execute as migrações:
```bash
python manage.py migrate
```

#### 5. Coleta arquivos estáticos:
```bash
python manage.py collectstatic --noinput
```

#### 6. Carregue dados iniciais:
```bash
python manage.py loaddata inicial.json
```

#### 7. Crie o superusuário (admin):
```bash
python manage.py createsuperuser
```

Digite quando pedir:
- **Username:** seu_usuario
- **Email:** seu_email@exemplo.com
- **Password:** sua_senha_segura

---

## 🔄 ATIVAR A APLICAÇÃO

### Volte à aba "Web":
```
Painel → Web → [Scroll para cima]
```

### Clique no botão verde:
```
[ ✓ Reload ]
```

Aguarde recarregar (~5 segundos)

---

## ✅ TESTE O SITE

### Abra seu navegador:
```
https://tauan2710.pythonanywhere.com
```

### Teste estas páginas:
- ✅ Homepage: `https://tauan2710.pythonanywhere.com/`
- ✅ Login: `https://tauan2710.pythonanywhere.com/login/`
- ✅ Dashboard: `https://tauan2710.pythonanywhere.com/dashboard/`
- ✅ Feedback: `https://tauan2710.pythonanywhere.com/enviar_feedback/`
- ✅ Clima: `https://tauan2710.pythonanywhere.com/pesquisas/`
- ✅ Admin: `https://tauan2710.pythonanywhere.com/admin/`

---

## ❌ TROUBLESHOOTING - ERROS COMUNS

### Erro: "This directory does not exist" no Source code
**Solução:** Você precisa fazer o upload do projeto primeiro!

#### Passo 1: Clone do GitHub
```bash
# No terminal do PythonAnywhere
cd /home/tauan2710
git clone https://github.com/Tauan2710/Feed_box.git feedback_system
```

#### Passo 2: Verifique se funcionou
```bash
ls -la /home/tauan2710/
# Deve aparecer: feedback_system/
```

#### Passo 3: Verifique o conteúdo
```bash
ls -la /home/tauan2710/feedback_system/
# Deve aparecer: manage.py, feedback_system/, accounts/, etc.
```

### Erro: "No module named 'xxxxx'"

### Erro: "ALLOWED_HOSTS violation"
**Solução:** Altere em `settings.py` linha 28 para:
```python
ALLOWED_HOSTS = ['tauan2710.pythonanywhere.com', 'localhost', '127.0.0.1']
```

### Erro: "No such table"
**Solução:** Execute:
```bash
python manage.py migrate
```

### CSS/Imagens não carregam
**Solução:** Execute:
```bash
python manage.py collectstatic --noinput
```

Depois clique em **Reload**.

### Não consegue fazer login
**Solução:** Crie novo superusuário:
```bash
python manage.py createsuperuser
```

---

## 📋 CHECKLIST FINAL

### Upload do Projeto (PASSO 0)
- [ ] Projeto enviado para `/home/tauan2710/feedback_system`
- [ ] Comando `ls -la /home/tauan2710/feedback_system/` mostra os arquivos
- [ ] Ambiente virtual criado em `/home/tauan2710/.virtualenvs/feedback_system_env`

### Configuração da Interface
- [ ] Source code: `/home/tauan2710/feedback_system`
- [ ] Virtualenv: `/home/tauan2710/.virtualenvs/feedback_system_env`
- [ ] Static files: `/static/` → `/home/tauan2710/feedback_system/staticfiles`
- [ ] Arquivo WSGI: Atualizado corretamente

### Arquivo settings.py
- [ ] `DEBUG = False` ✅
- [ ] `ALLOWED_HOSTS = ['tauan2710.pythonanywhere.com', 'localhost', '127.0.0.1']`
- [ ] `STATIC_URL = '/static/'` ✅
- [ ] `STATIC_ROOT` aponta para `staticfiles/` ✅

### Comandos Executados
- [ ] `cd /home/tauan2710/feedback_system`
- [ ] `source /...virtualenvs/feedback_system_env/bin/activate`
- [ ] `pip install -r requirements.txt`
- [ ] `python manage.py migrate`
- [ ] `python manage.py collectstatic --noinput`
- [ ] `python manage.py loaddata inicial.json`
- [ ] `python manage.py createsuperuser`

### Teste Final
- [ ] Clicou em **Reload**
- [ ] Site abre em `tauan2710.pythonanywhere.com`
- [ ] Login funciona
- [ ] Dashboard carrega
- [ ] Admin acessível
- [ ] CSS/imagens aparecem

---

## 📞 REFERÊNCIA RÁPIDA DE CAMINHOS

| Item | Caminho |
|------|---------|
| **Source code** | `/home/tauan2710/feedback_system` |
| **Virtualenv** | `/home/tauan2710/.virtualenvs/feedback_system_env` |
| **Static URL** | `/static/` |
| **Static Path** | `/home/tauan2710/feedback_system/staticfiles` |
| **WSGI** | `/var/www/tauan2710_pythonanywhere_com_wsgi.py` |
| **Database** | `/home/tauan2710/feedback_system/db.sqlite3` |
| **Domínio** | `tauan2710.pythonanywhere.com` |

---

**✅ Status:** Pronto para Deploy  
**📅 Última atualização:** Abril 2026  
**🔗 Repositório:** [Tauan2710/Feed_box](https://github.com/Tauan2710/Feed_box)
