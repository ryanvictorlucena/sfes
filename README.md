# SFES - Sistema de Fila de Espera do SUS

Sistema de fila de espera onde o intuito é fazer com que o paciente possa ter mais flexibilidade e não precise ficar esperando por um longo período de tempo nas unidades de atendimento.

## Para colocar a API em execução

    .\venv\Scripts\Activate

### Instalar as dependências do projeto

    pip install -r requirements.txt

### Rodando a aplicação

    python -m uvicorn app.main:app --reload
