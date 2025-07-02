# STACKSYNC-ASSESSMENT: Safe Python Script Execution API

This project is a secure Flask-based API service that enables safe execution of arbitrary user-defined Python scripts inside a Docker container using `nsjail`. Only the result of the `main()` function is returned — all `print()` statements are separated into `stdout`.

## Features

- **Secure sandboxing** with `nsjail`
- **Dockerized** for consistent and lightweight deployment
- Supports libraries like `os`, `pandas`, and `numpy`
- Minimal API with a single `/execute` endpoint
- Filters out all stdout except `main()` return
- Graceful error handling for invalid scripts or results

---

## Sample Request

### `POST /execute`

**Request Body (JSON):**

```bash
{
  "script": "def main():\n    return {\"message\": \"Hello from main\"}\n\nimport json\nprint(json.dumps(main()))"
}
```

**Successful Response:**

```bash
{
  "result": {
    "message": "Hello from main"
  },
  "stdout": ""
}
```

### Run Locally with Docker

**Clonse the Repository**

```bash
git clone https://github.com/RahulSP-4601/Stacksync-Assessment.git
cd Stacksync-Assessment
```

**Build the Docker image**

```bash
docker build -t safe-python-api .
```

**Run the container**

```bash
docker run -p 8080:8080 safe-python-api
```

#### Try on Local

```bash
curl -X POST http://127.0.0.1:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"message\": \"Hello from main\"}\n\nimport json\nprint(json.dumps(main()))"}'
```

#### Try on Google Cloud Run

```bash
curl -X POST https://stacksync-api-76854938786.us-central1.run.app/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"message\": \"Hello from Cloud Run\"}\n\nimport json\nprint(json.dumps(main()))"}'
```

##### Tech Stack

- Python 3.10
- Flask
- nsjail
- Docker
- Google Cloud Run
