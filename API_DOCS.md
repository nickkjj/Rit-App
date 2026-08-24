# Documentação da API (RIT App)

Esta é a especificação técnica dos endpoints disponíveis na API do projeto RIT App (Monks Case). A API segue o padrão REST e todas as requisições/respostas utilizam o formato `application/json`.

## Autenticação

A API utiliza autenticação via *Custom Header*. Para endpoints marcados como **[Autenticado]**, você deve enviar o seguinte header na requisição HTTP:

```http
X-User-Email: email@empresa.com
```

---

## 1. Geral & Sessão

### 1.1 Iniciar Sessão
**[Público]**
Inicia a sessão validando a existência do e-mail do usuário no sistema.

* **Método:** `POST`
* **Rota:** `/api/session/`

**Request Body:**
```json
{
  "email": "macielniiicolas@gmail.com"
}
```

**Respostas:**
* `200 OK`: Retorna os dados do usuário.
  ```json
  {
    "id": 16,
    "name": "Nicolas Maciel",
    "email": "macielniiicolas@gmail.com",
    "position_name": "Software Analyst"
  }
  ```
* `404 Not Found`: Usuário não cadastrado.
  ```json
  { "error": "User not found" }
  ```

### 1.2 Listar Usuários Mock (Fast Login)
**[Público]**
Retorna a lista de todos os funcionários cadastrados para popular o seletor de acesso rápido do frontend.

* **Método:** `GET`
* **Rota:** `/api/login-users/`

**Respostas:**
* `200 OK`:
  ```json
  [
    {
      "id": 1,
      "name": "Alice Hartman",
      "email": "alice.hartman@company.com",
      "position_name": "CEO"
    },
    {
      "id": 2,
      "name": "Bob Sinclair",
      "email": "bob.sinclair@company.com",
      "position_name": "CTO"
    }
  ]
  ```

---

## 2. Dashboard & Equipe

### 2.1 Resumo do Dashboard da Equipe
**[Autenticado]**
Retorna a hierarquia do usuário logado (liderados diretos e indiretos), além dos dados do líder acima dele e pendências.

* **Método:** `GET`
* **Rota:** `/api/team/dashboard/`

**Respostas:**
* `200 OK`:
  ```json
  {
    "total_evaluations_remaining": 5,
    "leader": {
      "id": 2,
      "name": "Bob Sinclair"
    },
    "team": [
      {
        "id": 10,
        "name": "Jane Doe",
        "position_name": "Developer",
        "evaluations_remaining": 1,
        "days_until_next_evaluation": 0,
        "average_score": 4.5
      }
    ]
  }
  ```
* `403 Forbidden`: Credenciais não fornecidas no header.

### 2.2 Histórico de Avaliações
**[Autenticado]**
Retorna o histórico de média das avaliações da equipe nos últimos 6 meses para desenhar o gráfico analítico.

* **Método:** `GET`
* **Rota:** `/api/team/history/`

**Respostas:**
* `200 OK`:
  ```json
  [
    {
      "month": "2026-08",
      "average": 4.2
    },
    {
      "month": "2026-07",
      "average": 3.8
    }
  ]
  ```

---

## 3. Avaliações (RIT)

### 3.1 Submeter Avaliação
**[Autenticado]**
Submete as notas de uma avaliação de desempenho para um membro da equipe.

* **Método:** `POST`
* **Rota:** `/api/evaluations/`

**Request Body:**
```json
{
  "lead_id": 10,
  "ratings": [
    { "question_id": 1, "score": 5 },
    { "question_id": 2, "score": 4 }
  ]
}
```

**Respostas:**
* `201 Created`:
  ```json
  { "message": "Avaliação enviada com sucesso." }
  ```
* `400 Bad Request` (Cooldown Ativo):
  ```json
  { "error": "Cooldown ativo. Você só pode avaliar este funcionário novamente em 4 dias." }
  ```
* `403 Forbidden` (Sem Permissão Hierárquica):
  ```json
  { "error": "Você não tem permissão para avaliar este funcionário." }
  ```

### 3.2 Checar Avaliação Recente (Cooldown)
**[Autenticado]**
Verifica se o funcionário já foi avaliado dentro da janela de cooldown (7 dias). Utilizado para bloquear múltiplas avaliações em curto período.

* **Método:** `GET`
* **Rota:** `/api/evaluations/recent/?lead_id=10`

**Respostas:**
* `200 OK`:
  ```json
  {
    "has_recent": true,
    "days_remaining": 4
  }
  ```

---

## 4. Configurações Globais (Admin)

### 4.1 Buscar Questões Ativas
**[Autenticado]**
Retorna o bloco de perguntas da "versão ativa" do sistema de avaliações, incluindo os pesos individuais (em %) para o cálculo de RIT.

* **Método:** `GET`
* **Rota:** `/api/questions/versions/current/`

**Respostas:**
* `200 OK`:
  ```json
  [
    {
      "id": 1,
      "title": "Entrega de Resultados",
      "weight": 25
    },
    {
      "id": 2,
      "title": "Qualidade Técnica",
      "weight": 25
    }
  ]
  ```

### 4.2 Publicar Nova Versão de Questões
**[Restrito: CEO, CTO, CFO]**
Gera uma nova versão de formulário. Todos os relatórios gerados a partir deste ponto utilizarão essa nova composição para seus cálculos de performance.

* **Método:** `POST`
* **Rota:** `/api/questions/versions/`

**Request Body:**
```json
{
  "questions": [
    { "title": "Entrega de Resultados", "weight": 25 },
    { "title": "Execução e Qualidade", "weight": 20 }
  ]
}
```

**Respostas:**
* `201 Created`:
  ```json
  { "message": "Nova versão de formulário criada com sucesso." }
  ```
* `403 Forbidden` (Usuário não é C-Level):
  ```json
  { "error": "Apenas membros da diretoria (C-Level) podem alterar métricas globais." }
  ```
