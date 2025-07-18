# URL Stats Aggregation & Reporting API

## Installation

1. Clone the repository 
```
git clone https://github.com/hmangukia/backend-take-home-challenge.git
cd backend-take-home-challenge
```

2. Create environment variables

Create an `.env` file in your project root:
```
DATABASE_URL=postgresql://username:password@host:port/db_name
TEST_DATABASE_URL=postgresql://username:password@host:port/test_db_name
```

3. Update the user name in DATABASE_URL and TEST_DATABASE_URL, and POSTGRES_USER in docker-compose.yml

4. Build and run using docker
```
docker compose build
docker compose up

```
5. Run the migrations to create tables
```
alembic upgrade head
```

App will be available at:
http://localhost:8000


## Running tests
To execute the full test suite inside the container:
```
docker compose exec web pytest
```