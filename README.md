# RIT App - Rate It (Monks Case)

Plataforma de monitoramento de desempenho e avaliações de funcionários.

## Requisitos

### Pré-requisitos
- Docker
- Docker Compose

### Passos
1. Clone o repositório.
2. Na raiz do projeto, suba a infraestrutura:
   ```bash
   docker-compose up --build -d
   ```
3. Acesse a aplicação:
   - **Frontend:** [http://localhost:5173](http://localhost:5173)
   - **Documentação da API:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/) (Interativa)

> **Nota:** As migrations e a população inicial (seed) do banco de dados (funcionários, hierarquias e questões base) ocorrem automaticamente ao subir o container do backend. As chaves de banco de dados e variáveis de ambiente já estão configuradas no `docker-compose.yml` para facilitar a inicialização. O login pode ser feito selecionando qualquer e-mail no frontend.

## Possíveis Problemas

- **Conflito de portas**: Verifique se as portas `8000` (Backend), `5173` (Frontend) e `5432` (Postgres) estão livres na sua máquina.
- **Dependências do Frontend**: O `node_modules` utiliza um volume anônimo. Caso o frontend apresente erro de importação ao iniciar, rode:
  ```bash
  docker exec frontend npm install
  ```
  E reinicie o container: `docker compose restart frontend`.

## Tecnologias

- Backend: Django, Django REST Framework, PostgreSQL
- Frontend: Vue 3, Vite, Tailwind CSS, FontAwesome
