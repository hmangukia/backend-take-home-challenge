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

## AI flyer generation
As a fun side project and inspired by an idea I briefly discussed during my initial chat with Shardul, I’ve also started experimenting with AI-powered flyer generation. This part is not part of the original take home test, but something I wanted to explore independently.

I'm currently using OpenAI’s GPT-4.1 model for this prototype. A few sample images have been added to the assets folder and are used as visual references in the generation process. The resulting flyer is saved to the root directory as `flyer.png`.

### Sample Prompts & Results:

**Prompt 1**
> "Design a clean, modern promotional image for our upcoming sale. Match the visual theme and tone of the product images provided. Use soft pastel tones and minimal layout. Do not add any text in the image."

- Result 1:
![Result 1](./flyer1.png "Result 1")
- Result 2:
![Result 2](./flyer2.png "Result 2")

**Prompt 2**
> "Design a clean, modern promotional image for our upcoming sale. Match the visual theme and tone of the product images provided. Use soft pastel tones and minimal layout. Do not add any text in the image. The center of the image should be light colored/empty so a text can be added on the top."
- Result:
![Result 3](./flyer.png "Result 3")


Right now, the system uses only three sample product images. In a real world scenario, there could be hundreds of images, and the prompt could include more details about branding and context. This would help generate more accurate and visually appealing flyers.


### Future Improvement Ideas:
- Text overlay support: Add dynamic promotional text (could use Open AI or Pillow)
  - Editor: Incorporate a visual editor (e.g. Puck) for text overlay
- User personalization: Tailor flyer content based on customer segments (e.g. sporty vs. elegant, male vs. female).
- Batch generation: Give users multiple options to choose by generating multiple flyers at once with different designs or product sets
