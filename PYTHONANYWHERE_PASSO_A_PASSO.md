# GUIA PASSO A PASSO - CONFIGURAÇÃO PYTHONANYWHERE
## Feedbox - Gestão de Feedback com IA e eNPS

**Projeto:** [Tauan2710/Feed_box](https://github.com/Tauan2710/Feed_box)  
**Username:** tauan2710  
**Domínio:** tauan2710.pythonanywhere.com  
**Atualizado:** Baseado na estrutura real do repositório

---

## 📁 ESTRUTURA DO PROJETO

```
/home/tauan2710/feedback_system/
├── accounts/                    ← App de autenticação
│   ├── __init__.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
├── clima/                       ← App de pesquisas de clima
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── migrations/
├── feedbacks/                   ← App principal (feedback dos usuários)
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   └── migrations/
├── feedback_system/             ← Configurações do Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── views.py
├── setores/                     ← App de setores/departamentos
│   ├── models.py
│   └── migrations/
├── static/                      ← Arquivos estáticos (dev) - CSS, JS, imagens
│   └── images/
├── staticfiles/                 ← Coletados em produção (NÃO editar)
├── templates/                   ← Templates HTML globais
│   ├── base.html
│   ├── dashboard.html
│   └── (outros)
├── manage.py                    ← Comando principal do Django
├── db.sqlite3                   ← Banco de dados
├── inicial.json                 ← Dados iniciais (setores, admin)
├── requirements.txt             ← Dependências Python
└── .gitignore, README.md, etc
```

---

## PASSO 1: ABA "WEB" - SOURCE CODE

### Localização na interface:
```
PythonAnywhere.com → Painel → Web → Source code
```

### O que preencher:

**Campo: Source code**
```
/home/tauan2710/feedback_system
```

💡 **Explicação:** 
Este é o caminho da **pasta raiz do seu projeto** no servidor do PythonAnywhere. 
- Contém todos os apps (accounts, feedbacks, clima, setores)
- Contém o arquivo manage.py
- Contém os templates e arquivos estáticos
- O PythonAnywhere procurará pelo arquivo wsgi.py dentro de `feedback_system/` aqui

---

## PASSO 2: ABA "WEB" - VIRTUALENV

### Localização na interface:
```
Painel PythonAnywhere → Web → Virtualenv
```

### O que preencher:

**Campo: Virtualenv**
```
/home/tauan2710/.virtualenvs/feedback_system_env
```

💡 **Explicação:** Este é o ambiente virtual Python isolado onde suas dependências do projeto estão instaladas. As bibliotecas do seu requirements.txt estarão aqui.

---

## PASSO 3: ABA "WEB" - ARQUIVOS ESTÁTICOS (STATIC FILES)

### Localização na interface:
```
Painel PythonAnywhere → Web → Static files
```

### O que preencher:

Complete as seguintes linhas:

#### Linha 1 - Arquivos estáticos do projeto
| Campo | Valor |
|-------|-------|
| **URL** | `/static/` |
| **Path** | `/home/tauan2710/feedback_system/staticfiles` |

#### Linha 2 - Admin do Django (OPCIONAL)
| Campo | Valor |
|-------|-------|
| **URL** | `/static/admin/` |
| **Path** | `/home/tauan2710/.virtualenvs/feedback_system_env/lib/python3.X/site-packages/django/contrib/admin/static/admin` |

#### Linha 3 - Media files (uploads de usuários)
| Campo | Valor |
|-------|-------|
| **URL** | `/media/` |
| **Path** | `/home/tauan2710/feedback_system/media` |

💡 **Explicação:** 
- `/static/` = CSS, JavaScript, imagens do seu projeto
- `/static/admin/` = Interface do Django admin
- `/media/` = Arquivos enviados pelos usuários (feedbacks com anexos, etc)

---

## PASSO 4: ABA "WEB" - ARQUIVO WSGI

### Localização na interface:
```
Painel PythonAnywhere → Web → Arquivo de configuração: → Clique no link do arquivo WSGI
```

### Caminho do arquivo:
```
/var/www/tauan2710_pythonanywhere_com_wsgi.py
```

### O que preencher (substitua TUDO no arquivo):

```python
import os
import sys

# Adiciona o projeto ao path do Python
path = '/home/tauan2710/feedback_system'
if path not in sys.path:
    sys.path.append(path)

# Define o módulo de settings do Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'feedback_system.settings'

# Obtém a aplicação WSGI
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

💡 **Explicação:** O arquivo WSGI é o intermediário entre o servidor PythonAnywhere e sua aplicação Django. Ele carrega seu projeto e permite que as requisições HTTP sejam processadas.

---

## PASSO 5: CONFIGURAR O ARQUIVO settings.py

### Localização do arquivo no seu computador:
```
feedback_system/settings.py
```

### Alterações necessárias:

#### 5.1 - DEBUG (SEM SEGURANÇA)
Encontre a linha:
```python
DEBUG = True
```

Altere para:
```python
DEBUG = False
```

#### 5.2 - ALLOWED_HOSTS
Encontre:
```python
ALLOWED_HOSTS = []
```

Altere para:
```python
ALLOWED_HOSTS = ['tauan2710.pythonanywhere.com', 'localhost']
```

#### 5.3 - STATIC_URL (já deve estar assim)
```python
STATIC_URL = '/static/'
STATIC_ROOT = '/home/tauan2710/feedback_system/staticfiles'
```

#### 5.4 - MEDIA_FILES (se usar uploads)
Adicione estas linhas (ou altere se já existirem):
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/tauan2710/feedback_system/media'
```

#### 5.5 - DATABASES
Para banco de dados SQLite (padrão):
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/tauan2710/feedback_system/db.sqlite3',
    }
}
```

💡 **Explicação:** Estas configurações dizem ao Django como se comportar em produção, onde encontrar os arquivos estáticos, uploads, e o banco de dados.

---

## PASSO 6: TERMINAL DO PYTHONANYWHERE - PRIMEIRAS CONFIGURAÇÕES

### Acesso ao terminal:
```
Painel PythonAnywhere → Consoles → Bash
```

### Execute os seguintes comandos:

#### 6.1 - Navegue até a pasta do projeto:
```bash
cd /home/tauan2710/feedback_system
```

#### 6.2 - Ative o ambiente virtual:
```bash
source /home/tauan2710/.virtualenvs/feedback_system_env/bin/activate
```

#### 6.3 - Instale as dependências:
```bash
pip install -r requirements.txt
```

#### 6.4 - Execute as migrações do banco de dados:
```bash
python manage.py migrate
```

#### 6.5 - Coleta os arquivos estáticos:
```bash
python manage.py collectstatic --noinput
```

#### 6.6 - Carrega os dados iniciais (tabelas de setores e admin demo):
```bash
python manage.py loaddata inicial.json
```

#### 6.7 - Cria usuário administrador (você será solicitado):
```bash
python manage.py createsuperuser
```

Digite o username, email e senha para o seu administrador.

💡 **Explicação:** Estes comandos preparam o banco de dados, coletam os arquivos estáticos, e criam o usuário que irá acessar a interface admin em `/admin/`.

---

## PASSO 7: RELOAD E TESTE

### Na aba "Web":
```
Painel PythonAnywhere → Web → Clique em "Reload" (botão verde)
```

### Teste o site:

1. **Acesse o domínio:**
   ```
   https://tauan2710.pythonanywhere.com
   ```

2. **Teste a página de login:**
   ```
   https://tauan2710.pythonanywhere.com/login/
   ```

3. **Teste o dashboard:**
   ```
   https://tauan2710.pythonanywhere.com/dashboard/
   ```

4. **Teste o envio de feedback:**
   ```
   https://tauan2710.pythonanywhere.com/enviar_feedback/
   ```

5. **Acesse o admin (com o superusuário criado):**
   ```
   https://tauan2710.pythonanywhere.com/admin/
   ```

💡 **Explicação:** Aqui você verifica se tudo está funcionando corretamente. Se alguma página der erro, verifique os logs (próximo passo).

---

## PASSO 8: VERIFICAR ERROS (SE NECESSÁRIO)

### Acesso aos logs:
```
Painel PythonAnywhere → Web → Logs
```

### Dois arquivos importantes:

| Log | Localização | O que mostra |
|-----|-------------|-------------|
| **Error log** | Clique no link na seção Logs | Erros da aplicação Django |
| **Server log** | Clique no link na seção Logs | Erros do servidor |

💡 **Dica:** Se a página não carregar, leia o Error log para entender o problema. Os erros mais comuns são:
- Caminho de virtualenv incorreto
- Módulo Python faltando (instale via `pip install`)
- `DEBUG = True` em produção (deve ser False)
- `ALLOWED_HOSTS` configurado incorretamente

---

## CHECKLIST FINAL

Marque cada item conforme completa:

### Configuração da Interface Web
- [ ] **Source code:** `/home/tauan2710/feedback_system` inserido
- [ ] **Virtualenv:** `/home/tauan2710/.virtualenvs/feedback_system_env` inserido
- [ ] **Static files URL:** `/static/` com Path `/home/tauan2710/feedback_system/staticfiles`
- [ ] **Arquivo WSGI:** Atualizado com o código correto

### Configuração do Projeto
- [ ] **settings.py:** `DEBUG = False`
- [ ] **settings.py:** `ALLOWED_HOSTS` contém `tauan2710.pythonanywhere.com`
- [ ] **settings.py:** `STATIC_ROOT` aponta para `/home/tauan2710/feedback_system/staticfiles`

### Comandos no Terminal
- [ ] Ambiente virtual ativado
- [ ] Dependências instaladas (`pip install -r requirements.txt`)
- [ ] Migrações executadas (`python manage.py migrate`)
- [ ] Arquivos estáticos coletados (`python manage.py collectstatic --noinput`)
- [ ] Dados iniciais carregados (`python manage.py loaddata inicial.json`)
- [ ] Superusuário criado (`python manage.py createsuperuser`)

### Teste e Validação
- [ ] Botão "Reload" clicado na aba Web
- [ ] Site abre em `tauan2710.pythonanywhere.com`
- [ ] Login funciona
- [ ] Dashboard carrega corretamente
- [ ] Admin acessível em `/admin/`
- [ ] Nenhum erro de 404 ou 500

---

## REFERÊNCIA RÁPIDA DE CAMINHOS

```
├── Source code
│   └── /home/tauan2710/feedback_system
│
├── Virtualenv
│   └── /home/tauan2710/.virtualenvs/feedback_system_env
│
├── Static files
│   ├── URL: /static/ → Path: /home/tauan2710/feedback_system/staticfiles
│   └── URL: /media/ → Path: /home/tauan2710/feedback_system/media
│
├── WSGI
│   └── /var/www/tauan2710_pythonanywhere_com_wsgi.py
│
└── Banco de dados
    └── /home/tauan2710/feedback_system/db.sqlite3
```

---

## EM CASO DE DÚVIDA

1. **Erro 404:** Verifique o arquivo `error log`
2. **Erro 500:** Verifique Django logs e `settings.py`
3. **Arquivos estáticos não carregam:** Execute `python manage.py collectstatic --noinput`
4. **Precisa resetar:** Delete a web app e recrie do zero no PythonAnywhere
5. **Erro de virtualenv:** Verifique se o caminho está correto e se existe

**Última atualização:** Abril 2026  
**Projeto:** Feedbox  
**Status:** Pronto para Deploy

