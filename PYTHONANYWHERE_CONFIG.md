# CONFIGURAÇÃO FINAL - PYTHONANYWHERE
## Feedbox - Gestão de Feedback com IA e eNPS

> **Projeto:** [Tauan2710/Feed_box](https://github.com/Tauan2710/Feed_box)  
> **Username GitHub:** Tauan2710  
> **Domínio:** tauan2710.pythonanywhere.com  
> **Status:** Pronto para deploy no PythonAnywhere

---

## ESTRUTURA DO PROJETO NO SERVIDOR

```
/home/tauan2710/feedback_system/
├── accounts/                    (App Django)
├── clima/                       (App Django)
├── feedbacks/                   (App Django)
├── feedback_system/             (Pasta de configuração)
├── setores/                     (App Django)
├── static/                      (CSS, JS, Imagens - DESENVOLVIMENTO)
├── staticfiles/                 (Coletados em produção)
├── templates/                   (Templates globais)
├── manage.py
├── db.sqlite3                   (Banco de dados)
├── inicial.json                 (Dados iniciais)
└── requirements.txt             (Dependências Python)
```

---

## 4. CONFIGURAÇÃO NA ABA "Web" DO PYTHONANYWHERE

### 4.1 Source code
**Caminho para a pasta principal do projeto:**
```
/home/tauan2710/feedback_system
```

💡 Este é o diretório raiz onde estão todos os arquivos do seu projeto Django, incluindo manage.py, apps, templates e staticfiles.

### 4.2 Virtualenv
**Caminho do virtualenv criado:**
```
/home/tauan2710/.virtualenvs/feedback_system_env
```

💡 Ambiente Python isolado com todas as dependências (Django, etc) instaladas via requirements.txt.

### 4.3 Static files
**Configure os URLs e caminhos conforme abaixo:**

| URL | Path |
|-----|------|
| `/static/` | `/home/tauan2710/feedback_system/staticfiles` |

💡 Arquivos estáticos (CSS, JavaScript, imagens) do Django e do seu projeto após executar `collectstatic`.

---

## 5. CONFIGURAÇÃO DO ARQUIVO WSGI

**Arquivo** no servidor:
```
/var/www/tauan2710_pythonanywhere_com_wsgi.py
```

**Conteúdo completo do arquivo WSGI:**
```python
import os
import sys

# Adiciona o diretório do projeto ao Python path
path = '/home/tauan2710/feedback_system'
if path not in sys.path:
    sys.path.append(path)

# Define o módulo de configurações do Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'feedback_system.settings'

# Importa a aplicação WSGI do Django
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

💡 Este arquivo WSGI é o intermediário entre o servidor web do PythonAnywhere e sua aplicação Django. O PythonAnywhere o executa para processar todas as requisições HTTP.

---

## 6. CONFIGURAÇÃO DO ARQUIVO settings.py

**Localização no seu repositório:**
```
feedback_system/settings.py
```

### ✅ Já está configurado corretamente no seu projeto:

**Linha 26 - DEBUG:**
```python
DEBUG = False  # ✅ Correto para produção
```

**Linha 28 - ALLOWED_HOSTS:**
```python
ALLOWED_HOSTS = ['seu-usuario.pythonanywhere.com', 'localhost', '127.0.0.1']
```

⚠️ **Altere para:**
```python
ALLOWED_HOSTS = ['tauan2710.pythonanywhere.com', 'localhost', '127.0.0.1']
```

**Linha 135-138 - Static files (já está correto):**
```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

💡 O `STATIC_ROOT` aponta para `/home/tauan2710/feedback_system/staticfiles` (automaticamente calculado por BASE_DIR)

**Linha 84-87 - Database:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

💡 Seu banco SQLite estará em `/home/tauan2710/feedback_system/db.sqlite3`

---

## 7. FINALIZAÇÃO NO TERMINAL DO SERVIDOR

### Acesso ao terminal:
```
PythonAnywhere → Consoles → Bash
```

### Execute os seguintes comandos (em sequência):

```bash
# 1. Navegue até a pasta do projeto
cd /home/tauan2710/feedback_system

# 2. Ative o ambiente virtual
source /home/tauan2710/.virtualenvs/feedback_system_env/bin/activate

# 3. Instale as dependências do projeto
pip install -r requirements.txt

# 4. Execute as migrações do banco de dados
python manage.py migrate

# 5. Coleta os arquivos estáticos (CSS, JS, imagens)
python manage.py collectstatic --noinput

# 6. Carrega os dados iniciais (setores, admin demo, etc)
python manage.py loaddata inicial.json

# 7. Cria o usuário administrador (você será solicitado)
python manage.py createsuperuser
```

💡 **Explicação de cada comando:**
- `cd` = navega até a pasta do projeto
- `source` = ativa o ambiente virtual Python isolado
- `pip install` = instala as bibliotecas do requirements.txt
- `python manage.py migrate` = cria as tabelas no banco de dados
- `python manage.py collectstatic` = copia arquivos estáticos para a pasta `staticfiles/`
- `python manage.py loaddata` = importa os dados do arquivo `inicial.json`
- `python manage.py createsuperuser` = cria usuário para acessar `/admin/`

---

## 8. RELOAD E TESTE

### 8.1 Recarregar a aplicação

Na aba **Web** do PythonAnywhere:
```
Clique no botão verde "Reload"
```

💡 Isto reinicia a aplicação com as novas configurações do WSGI.

### 8.2 Teste o site

**Acesse o domínio:**
```
https://tauan2710.pythonanywhere.com
```

**Páginas para testar:**
- ✅ Homepage: `https://tauan2710.pythonanywhere.com/`
- ✅ Login: `https://tauan2710.pythonanywhere.com/login/`
- ✅ Dashboard: `https://tauan2710.pythonanywhere.com/dashboard/`
- ✅ Enviar Feedback: `https://tauan2710.pythonanywhere.com/enviar_feedback/`
- ✅ Pesquisas de Clima: `https://tauan2710.pythonanywhere.com/pesquisas/`
- ✅ Admin: `https://tauan2710.pythonanywhere.com/admin/`

---

## ESTRUTURA DO PROJETO CONFIGURADA

| Componente | Localização |
|-----------|-----------|
| **Projeto Django** | `feedback_system` |
| **Apps instalados** | `accounts`, `feedbacks`, `setores`, `clima` |
| **Templates globais** | `templates/` |
| **Arquivos estáticos (dev)** | `static/` |
| **Arquivos estáticos (prod)** | `staticfiles/` (coletados pelo collectstatic) |
| **Banco de dados** | `db.sqlite3` |
| **Dados iniciais** | `inicial.json` |
| **Dependências** | `requirements.txt` |

---

## DICAS IMPORTANTES DE PRODUÇÃO

⚠️ **SEGURANÇA:**
- ✅ `DEBUG = False` - Já está correto no seu settings.py
- ⚠️ Guardar a `SECRET_KEY` em segredo (não comitar em repositório público)
- ⚠️ `ALLOWED_HOSTS` deve incluir seu domínio do PythonAnywhere

🔍 **TROUBLESHOOTING (Se der erro):**
- Erro 404 ou 500? → Verifique o **Error log** na aba Web
- Arquivos estáticos não carregam? → Rode `python manage.py collectstatic --noinput`
- Banco de dados vazio? → Rode `python manage.py migrate` e `python manage.py loaddata inicial.json`
- Não consegue fazer login? → Rode `python manage.py createsuperuser`

📦 **CARACTERÍSTICAS DO SEU PROJETO:**
- Banco SQLite (compatível com PythonAnywhere gratuito)
- 4 Apps principais: accounts (usuários), feedbacks (formulários), setores, clima
- Templates em pasta global `templates/`
- Arquivos estáticos em `static/` (imagens, CSS personalizados)

---

## 📋 CHECKLIST FINAL

### Configuração da Interface Web do PythonAnywhere
- [ ] **Source code:** `/home/tauan2710/feedback_system`
- [ ] **Virtualenv:** `/home/tauan2710/.virtualenvs/feedback_system_env`
- [ ] **Static files URL:** `/static/` aponta para `/home/tauan2710/feedback_system/staticfiles`
- [ ] **Arquivo WSGI:** Atualizado com código Python correto

### Configuração do Projeto (settings.py)
- [ ] **DEBUG:** `False`
- [ ] **ALLOWED_HOSTS:** Contém `tauan2710.pythonanywhere.com`
- [ ] **STATIC_URL:** `/static/`
- [ ] **STATIC_ROOT:** `/home/tauan2710/feedback_system/staticfiles`

### Comandos Executados no Terminal
- [ ] Navegou até `/home/tauan2710/feedback_system`
- [ ] Ativou virtualenv com `source`
- [ ] Instalou dependências: `pip install -r requirements.txt`
- [ ] Executou migrações: `python manage.py migrate`
- [ ] Coletou estáticos: `python manage.py collectstatic --noinput`
- [ ] Carregou dados iniciais: `python manage.py loaddata inicial.json`
- [ ] Criou superusuário: `python manage.py createsuperuser`

### Teste e Validação
- [ ] Clicou em "Reload" na aba Web
- [ ] Site abre em `tauan2710.pythonanywhere.com`
- [ ] Login funciona com o superusuário criado
- [ ] Dashboard carrega corretamente
- [ ] Admin acessível em `/admin/`
- [ ] Formulários de feedback funcionam
- [ ] Pesquisas de clima carregam
- [ ] CSS e imagens aparecem corretamente

---

**Última atualização:** Abril 2026  
**Projeto:** Feedbox - Gestão de Feedback com IA e eNPS  
**GitHub:** [Tauan2710/Feed_box](https://github.com/Tauan2710/Feed_box)  
**Status:** ✅ Pronto para Deploy
