# Feedbox - Gestão de Feedback com IA e eNPS

Sistema desenvolvido para o TCC de Análise e Desenvolvimento de Sistemas.

## Como rodar o projeto em outra máquina:

1. Clone o repositório.
2. Crie um ambiente virtual: `python -m venv venv`.
3. Ative o venv: `source venv/bin/activate` (Linux/Mac) ou `venv\Scripts\activate` (Windows).
4. Instale o Django: `pip install django django-tailwind`.
5. Rode as migrações: `python manage.py migrate`.
6. **Importe os dados iniciais (ADM e Setores):** ```bash
   python manage.py loaddata inicial.json