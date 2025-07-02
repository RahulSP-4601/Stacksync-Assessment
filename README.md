# 🛡️ Safe Python Script Execution API

This project is a secure Flask-based API service that enables safe execution of arbitrary user-defined Python scripts inside a Docker container using `nsjail`. Only the result of the `main()` function is returned — all `print()` statements are separated into `stdout`.

## 🚀 Features

- 🔐 **Secure sandboxing** with `nsjail`
- ⚙️ **Dockerized** for consistent and lightweight deployment
- 🧪 Supports libraries like `os`, `pandas`, and `numpy`
- 📦 Minimal API with a single `/execute` endpoint
- 🧹 Filters out all stdout except `main()` return
- 🧾 Graceful error handling for invalid scripts or results

---

## 📥 Sample Request

### `POST /execute`

**Request Body (JSON):**

```json
{
  "script": "def main():\n    return {\"message\": \"Hello from main\"}\n\nimport json\nprint(json.dumps(main()))"
}
```

**Successful Response:**

```json
{
  "result": {
    "message": "Hello from main"
  },
  "stdout": ""
}
```

#### 🐳 Run Locally with Docker

**Clonse the Repository**

```json
git clone https://github.com/YOUR_USERNAME/safe-python-api.git
cd safe-python-api
```

**Build the Docker image**

```json
docker build -t safe-python-api .
```

**Run the container**

```json
docker run -p 8080:8080 safe-python-api
```

##### 🌐 Try on Google Cloud Run

```json
curl -X POST https://YOUR_CLOUD_RUN_URL/execute \
  -H "Content-Type: application/json" \
  -d '{"script": "def main():\n    return {\"message\": \"Hello from GCP\"}\n\nimport json\nprint(json.dumps(main()))"}'
```

###### Tech Stack

- Python 3.10
- Flask
- nsjail
- Docker
- Google Cloud Run
