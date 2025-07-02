# app/main.py
from flask import Flask, request, jsonify
import tempfile
import subprocess
import os
import json

app = Flask(__name__)

@app.route("/execute", methods=["POST"])
def execute_script():
    data = request.get_json()
    if not data or "script" not in data:
        return jsonify({"error": "Missing 'script' field"}), 400

    script_code = data["script"]

    # Write the script to a temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as tmp:
        tmp.write(script_code.encode("utf-8"))
        tmp_path = tmp.name

    try:
        # Run the script using nsjail
        result = subprocess.run(
            ["bash", "scripts/run_in_nsjail.sh", tmp_path],
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
        
    except Exception as e:
        return jsonify({
            "error": "Invalid output. Ensure main() returns JSON.",
            "raw_stdout": result.stdout.decode(),
            "raw_stderr": result.stderr.decode()
        }), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
