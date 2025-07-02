# app/main.py
from flask import Flask, request, jsonify
import tempfile
import subprocess
import os
import json

app = Flask(__name__)
USE_NSJAIL = os.getenv("USE_NSJAIL", "true").lower() == "true"

@app.route("/execute", methods=["POST"])
def execute_script():
    data = request.get_json()
    if not data or "script" not in data:
        return jsonify({"error": "Missing 'script' field"}), 400

    script_code = data["script"]

    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(script_code.encode("utf-8"))
        tmp_path = tmp.name

    try:
        if USE_NSJAIL:
            command = ["bash", "scripts/run_in_nsjail.sh", tmp_path]
        else:
            command = ["python3", tmp_path]

        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5,
        )
    except subprocess.TimeoutExpired:
        return jsonify({"error": "Script execution timed out"}), 400
    finally:
        os.remove(tmp_path)

    try:
        output_lines = result.stdout.decode().splitlines()
        json_result = json.loads(output_lines[-1])
        stdout = "\n".join(output_lines[:-1])
        return jsonify({
            "result": json_result,
            "stdout": stdout
        })

    except Exception:
        return jsonify({
            "error": "Invalid output. Ensure main() returns JSON.",
            "raw_stdout": result.stdout.decode(),
            "raw_stderr": result.stderr.decode()
        }), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
