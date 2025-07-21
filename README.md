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

## Endpoints

- POST `/shorten`
  - Accepts a long URL and returns a short slug-based URL and the slug. Format as follows:
  ```
    {
       "slug": "abcd123",
       "short_url": "http://your-service.com/abcd123"
    }
  ```
  - Reuses slug if the same URL is submitted again

- GET `/{slug}`
  - Redirects to the original long URL
  - Records visit timestamp corresponding to the URL

- GET `/stats`
  - Returns top number_of_links (default: 10), ordered by visit count (descending).
  ```
  [
    {
      "slug": "abcd12",
      "long_url": "https://www.example.com/...",
      "visits": 42,
      "last_visit": "2025-12-01T13:00:00Z"
    },
    {
      "slug": "efgh34",
      "long_url": "https://www.example.com/other/long/url",
      "visits": 0,
      "last_visit": null
    }
  ]
  ```

- GET `/stats/{slug}`
  - Returns analytics of the slug specified
  ```
  {
    "slug": "abcd12",
    "long_url": "https://www.example.com/...",
    "visits": 42,
    "last_visit": "2025-12-01T13:00:00Z"
  }
  ```

## Database Modelling

![Database modelling](./database-modelling.png "Database Modelling")

## URL shortening flow
![URL shortening flow](./URL-Shortening-Flow.png "URL shortening flow")

## URL redirect flow
![URL redirect flow](./URL-Redirect-Flow.png "URL redirect flow")

## 🚧 In Progress: Redis Caching
Redis-based caching is currently being implemented to optimize performance.
A [draft pull request](https://github.com/hmangukia/backend-take-home-challenge/pull/5) is open.

## 🚧 In Progress: AI flyer generation
As a fun side project and inspired by an idea I briefly discussed during my initial chat with Shardul, I’ve also started experimenting with AI-powered flyer generation. This part is not part of the original take home test, but something I wanted to explore independently.
A [draft pull request](https://github.com/hmangukia/backend-take-home-challenge/pull/6)
