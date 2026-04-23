# 📤 PASSO 0 - UPLOAD DO PROJETO PARA PYTHONANYWHERE
## Feedbox - Gestão de Feedback

**Antes de qualquer configuração, você precisa enviar seu projeto para o servidor!**

---

## 🎯 SITUAÇÃO ATUAL

Você está vendo o erro:
```
Source code: /home/tauan2710/feedback_system
This directory does not exist.
```

**Isso significa que o projeto ainda não foi enviado para o PythonAnywhere.**

---

## 📋 MÉTODO 1: CLONE DO GITHUB (RECOMENDADO)

### Passo 1: Abra o terminal do PythonAnywhere
```
PythonAnywhere.com → Consoles → Bash
```

### Passo 2: Navegue até sua pasta home
```bash
cd /home/tauan
```

### Passo 3: Clone o repositório
```bash
git clone https://github.com/Tauan2710/Feed_box.git Feed_box
```

### Passo 4: Verifique se funcionou
```bash
ls -la /home/tauan/
```

**Resultado esperado:**
```
drwxr-xr-x  5 tauan registered_users 4096 Apr 22 12:00 Feed_box/
```

### Passo 5: Verifique o conteúdo
```bash
ls -la /home/tauan/Feed_box/
```

**Resultado esperado:**
```
-rw-r--r-- 1 tauan2710 registered_users    0 Apr 22 12:00 manage.py
drwxr-xr-x 2 tauan2710 registered_users 4096 Apr 22 12:00 feedback_system/
drwxr-xr-x 2 tauan2710 registered_users 4096 Apr 22 12:00 accounts/
drwxr-xr-x 2 tauan2710 registered_users 4096 Apr 22 12:00 clima/
drwxr-xr-x 2 tauan2710 registered_users 4096 Apr 22 12:00 feedbacks/
drwxr-xr-x 2 tauan2710 registered_users 4096 Apr 22 12:00 setores/
drwxr-xr-x 2 tauan2710 registered_users 4096 Apr 22 12:00 static/
drwxr-xr-x 2 tauan2710 registered_users 4096 Apr 22 12:00 templates/
-rw-r--r-- 1 tauan2710 registered_users  123 Apr 22 12:00 requirements.txt
-rw-r--r-- 1 tauan2710 registered_users   45 Apr 22 12:00 inicial.json
```

---

## 📋 MÉTODO 2: UPLOAD VIA ZIP (Alternativo)

### Passo 1: Prepare o ZIP no seu computador
1. Abra a pasta do projeto: `C:\Users\Talles\Desktop\PROJETO\feedback_system`
2. Clique com botão direito → "Enviar para" → "Pasta compactada (zipada)"
3. Nomeie como `feedback_system.zip`

### Passo 2: Upload para PythonAnywhere
1. No PythonAnywhere: `Files` (menu lateral esquerdo)
2. Clique em `Upload a file`
3. Selecione o arquivo `feedback_system.zip`
4. Clique em `Upload`

### Passo 3: Extraia o ZIP
```bash
# No terminal do PythonAnywhere
cd /home/tauan2710
unzip feedback_system.zip
```

### Passo 4: Renomeie se necessário
```bash
# Se o ZIP criou uma pasta extra, renomeie
mv feedback_system-main feedback_system
# ou
mv Feed_box-main feedback_system
```

---

## 📋 MÉTODO 3: UPLOAD VIA GIT (Se você tem SSH)

### Passo 1: Configure SSH Key (opcional)
```bash
# Gere chave SSH se não tiver
ssh-keygen -t rsa -b 4096 -C "seu_email@exemplo.com"

# Copie a chave pública
cat ~/.ssh/id_rsa.pub
```

### Passo 2: Clone via SSH
```bash
cd /home/tauan2710
git clone git@github.com:Tauan2710/Feed_box.git feedback_system
```

---

## ✅ VERIFICAÇÃO FINAL

### Execute estes comandos para confirmar:
```bash
# 1. Verifique se a pasta existe
ls -la /home/tauan2710/ | grep feedback_system

# 2. Verifique se manage.py existe
ls -la /home/tauan2710/feedback_system/manage.py

# 3. Verifique se requirements.txt existe
ls -la /home/tauan2710/feedback_system/requirements.txt

# 4. Verifique se settings.py existe
ls -la /home/tauan2710/feedback_system/feedback_system/settings.py
```

---

## 🎯 PRÓXIMO PASSO

Após confirmar que o upload funcionou, você pode prosseguir com:

1. **Criar o ambiente virtual** (se ainda não criou)
2. **Configurar a aba "Web"** no PythonAnywhere
3. **Executar os comandos** no terminal

---

## ❓ PROBLEMAS COMUNS

### Erro: "Permission denied (publickey)"
- Use HTTPS ao invés de SSH: `https://github.com/Tauan2710/Feed_box.git`

### Erro: "Repository not found"
- Verifique se o repositório é público
- Confirme o nome: `Tauan2710/Feed_box`

### ZIP muito grande
- PythonAnywhere tem limite de upload
- Use Git clone que é mais eficiente

---

**📅 Atualizado:** Abril 2026  
**🔗 Repositório:** [Tauan2710/Feed_box](https://github.com/Tauan2710/Feed_box)