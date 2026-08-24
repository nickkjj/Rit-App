# Documentação do Código (Architecture & Codebase)

Bem-vindo à documentação técnica do código-fonte do **RIT App**. Este documento visa explicar como o projeto foi estruturado, as decisões arquiteturais tomadas tanto no Backend quanto no Frontend, e o modelo de dados utilizado.

---

## 1. Visão Geral da Arquitetura

O projeto utiliza uma arquitetura baseada no padrão **Monorepo** para fins práticos do case, dividida em dois ecossistemas principais executados através do Docker Compose:

* **Backend**: Django (Python) + Django REST Framework (DRF)
* **Frontend**: Vue 3 + Vite + TailwindCSS + Pinia
* **Banco de Dados**: PostgreSQL

A comunicação entre Frontend e Backend acontece estritamente via APIs RESTful consumindo e devolvendo `JSON`.

---

## 2. Backend (Django)

O backend foi estruturado utilizando o conceito de **Micro-Apps** do Django, para separar responsabilidades de domínio. O projeto principal `rit_app` gerencia o roteamento e configurações, mas a lógica de negócios está segmentada:

### 2.1 Módulos (Django Apps)

1. **`table_administration_service`**:
   Responsável pelo domínio administrativo do negócio.
   - **Gerencia os Funcionários** (`Employee`).
   - **Gerencia a Hierarquia** (quem lidera quem).
   - **Gerencia as Versões de Questões** (`QuestionVersion` e `Question`), permitindo que a liderança crie novas versões de formulários sem quebrar relatórios antigos.

2. **`evaluation_service`**:
   Responsável pelo domínio transacional de avaliação (RIT).
   - **Gerencia as Avaliações** (`Rating`).
   - Contém a lógica pesada de cálculo de média das equipes (dashboards e históricos).
   - Valida regras de negócio de tempo (ex: *cooldown* de 7 dias entre avaliações de um mesmo líder para um mesmo funcionário).

### 2.2 Decisão Arquitetural Crítica: Modelagem de Hierarquia

Uma das maiores complexidades de aplicações de RH é descobrir "toda a árvore de liderados" (diretos e indiretos).
Em vez de utilizar padrões complexos para o código manter (como *Closure Tables* ou *Nested Sets*), optamos por um padrão simples no código e robusto no banco:

* **Adjacency List (Lista de Adjacência)**: A tabela de empregados possui apenas um campo `leader_id` referenciando ela mesma.
* **CTE Recursiva**: Para descobrir todos os níveis indiretos sem fazer o Django gerar o problema de *N+1 Queries*, o backend utiliza uma *Raw Query* com `RECURSIVE CTE` do Postgres. Isso permite descer a árvore infinita de funcionários com apenas **uma única ida ao banco de dados**, garantindo altíssima performance.

### 2.3 Autenticação e Segurança (RBAC)

Para simplificar o contexto do case (focado em features de negócio), em vez de JWT, foi implementada uma autenticação por **Custom Header**:
* Os endpoints são protegidos por uma classe de permissão customizada.
* O client envia o header `X-User-Email: email@empresa.com`.
* O Backend intercepta o header, valida se o funcionário existe e o anexa ao `request.user`.
* **RBAC (Role-Based Access Control)**: Algumas rotas (como alteração de métricas globais e questões) bloqueiam usuários comuns e exigem que o `position_name` do funcionário seja C-Level (CEO, CTO, CFO).

---

## 3. Frontend (Vue 3)

O Frontend foi projetado como uma **Single Page Application (SPA)** de alta performance utilizando Vue 3 com `Composition API` e `<script setup>`.

### 3.1 Estrutura de Pastas (`frontend/src/`)

* **`api/`**: Contém o interceptador global do Axios. Ele injeta a base URL do servidor (porta 8000) e o Header de e-mail automaticamente em todas as requisições.
* **`components/`**: Arquitetura orientada a componentes granulares (Smart/Dumb components). Exemplos: `EvaluationModal.vue` (contém lógica) e `PerformanceGauge.vue` (apenas apresentação gráfica).
* **`stores/`**: Gerenciamento de estado global com **Pinia**.
  * `auth.js`: Controla a sessão, quem está logado, bloqueios de roteamento.
  * `team.js`: Centraliza os dados do Dashboard e Equipe (para evitar requests repetidos entre telas que compartilham a mesma lista).
* **`views/`**: Componentes de Página. (`DashboardView`, `SettingsView`, etc).
* **`router/`**: Vue Router com *Navigation Guards* integrados ao Pinia para redirecionar usuários não autenticados.

### 3.2 Design de Código e UX
* Foi utilizado o **Tailwind CSS** puro sem bibliotecas de componentes prontas pesadas (como Vuetify). Isso garante uma customização absoluta do design proposto, resultando em um visual moderno (Glassmorphism, Cores Sólidas, Espaçamentos fluídos).
* Gráficos desenhados através de **Chart.js** via *vue-chartjs*.

---

## 4. Banco de Dados e Seed (Auto-Setup)

Para facilitar a validação do case, foi criada uma estratégia de **Data Seeding Automático** (via Data Migrations do Django).

No primeiro start do Docker (`docker compose up`), o banco de dados Postgres sobe vazio e o Django automaticamente:
1. Roda as `migrations` estruturais criando as tabelas.
2. Roda as *Data Migrations* (`0003_seed_employees.py` e `0004_seed_questions.py`) injetando toda a árvore hierárquica e perguntas base propostas na documentação original do Monks.
3. O ambiente fica **Plug & Play**.

---

## 5. Testes Unitários

O backend foi construído com a mentalidade de garantir qualidade nas rotas e regras de negócios. 
Estão presentes cenários de testes via `pytest`/`django.test` na pasta `tests/` de cada micro-app, validando desde o cálculo dos pesos das notas e CTE Recursiva até as travas de segurança C-Level.

---

## 6. Documentação da API (Endpoints)

A documentação interativa de rotas (Swagger-like) foi desenvolvida sob medida e acoplada nativamente.
Para consultar as especificações completas de Endpoints (JSON, Request, Response, Status Codes), acesse a rota na api `/api/docs/` ou acesse a versão .md em: [API_DOCS.md](https://github.com/nickkjj/Rit-App/blob/main/API_DOCS.md)
