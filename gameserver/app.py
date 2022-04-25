from flask import Flask, request
from flask_cors import CORS # allow for cross origin resource sharing
import os
import subprocess
import ast
import json

app = Flask(__name__)
_ = CORS(app)

CUR_DIR = os.getcwd()
PATH_CAIRO_SCRIPTS_FOLDER = f"{CUR_DIR}/../cairo-scripts/"
PATH_MOVES_JSON_FOLDER = f"{CUR_DIR}/../moves/"
MASKER_COMPILED = "masker_compiled.json"
REVEALER_COMPILED = "revealer_compiled.json"

# TODO: should this be encapsulated in something? along with ENV variables above
SUBMIT_SHOT_PROOF_ARGS = [
    "./submit-reveal-sharp.sh"
]

MASKER_PROGRAM_HASH = [
    "cairo-hash-program", 
    f"--program={PATH_CAIRO_SCRIPTS_FOLDER}/{MASKER_COMPILED}"
]

REVEALER_PROGRAM_HASH = [
    "cairo-hash-program", 
    f"--program={PATH_CAIRO_SCRIPTS_FOLDER}/{REVEALER_COMPILED}"
]

def parse_stdout2(stdout):
    stdout_clean = stdout.replace("\n", "")
    return stdout_clean

@app.route("/game", methods=["GET"])
def game():
    return {
        
    }

@app.route("/masker_program_hash", methods=["GET"])
def masker_program_hash():
    completed_process = subprocess.run(MASKER_PROGRAM_HASH, capture_output=True, text=True)
    clean_stdout = parse_stdout2(completed_process.stdout)
    return {
        "ouput": completed_process.stdout,
        "stderr": completed_process.stderr,
        "clean_stdout": clean_stdout
    }

@app.route("/revealer_program_hash", methods=["GET"])
def revealer_program_hash():
    completed_process = subprocess.run(REVEALER_PROGRAM_HASH, capture_output=True, text=True)
    clean_stdout = parse_stdout2(completed_process.stdout)
    return {
        "ouput": completed_process.stdout,
        "stderr": completed_process.stderr,
        "clean_stdout": clean_stdout
    }   

@app.route("/mask", methods=["GET"])
def mask():
    return {

    }

@app.route("/reveal")
def reveal():
    return {
        
    }


def write_json(obj, path):
    with open(path, "w") as fout:
        json.dump(obj, fout)

@app.route("/submit-shot-proof", methods=["GET"])
def submit_shot_proof():
    shot_location = int(request.args.get("shot-location"))
    ship_location = int(request.args.get("ship-location"))
    shifter_value = int(request.args.get("shifter"))
    shot_data = {
            "shot_location": shot_location,
            "ship_location": ship_location,
            "shifter": shifter_value
        }
    write_json(shot_data, "logs/shot_input.json")
    completed_process = subprocess.run(SUBMIT_SHOT_PROOF_ARGS, capture_output=True, text=True)
    return_data = {
        **shot_data,
        "stdout": completed_process.stdout,
        "stderr": completed_process.stderr
    }
    return return_data


@app.route("/get-job-status", methods=["GET"])
def get_job_status():
    jobkey = request.args.get("job-key")

    return {

    }

if __name__ == "__main__":
    app.run()