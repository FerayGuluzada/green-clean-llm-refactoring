import os
import time
import requests
import re
import random
from pathlib import Path

# =====================================
# CONFIG
# =====================================

API_KEY = ""
API_URL = "https://api.deepinfra.com/v1/openai/chat/completions"

INPUT_FOLDER = "deepseek_scripts"
OUTPUT_FOLDER = "results"

TEMPERATURE = 0

# Replace / edit with your final selected models
MODELS = {
    "deepseek": "deepseek-ai/DeepSeek-V3.2"
}

# =====================================
# UPDATED PROMPTS
# =====================================

PROMPTS = {
    "clean": """
You are a software engineer specializing in code maintainability and readability.

Task:
Analyze the code and identify maintainability issues.
Apply refactoring to improve maintainability and readability.

Constraints:
- Do not add external dependencies
- Refactoring is strictly limited to internal computation logic only. Input and output must remain the same.
- Preserve meaningful comments and docstrings unless replaced by clearer structure

Optimization goals:
- Reduce Cyclomatic Complexity (CC)
- Reduce unnecessary Lines of Code (LOC)
- Reduce Halstead Volume
- Increase code readability and modularity
- Eliminate code smells and structural issues

Output:
Return ONLY the refactored code.

Code to refactor:
""",

    "green": """
You are a software engineer specializing in performance optimization and energy-efficient code.

Task:
Analyze the code and identify performance bottlenecks.
Apply efficiency-focused refactoring to improve runtime and energy consumption.

Constraints:
- Do not add external dependencies
- Refactoring is strictly limited to internal computation logic only. Input and output must remain the same.
- Preserve meaningful comments and docstrings unless replaced by clearer structure

Optimization goals:
- Reduce runtime execution time
- Reduce CPU energy consumption

Output:
Return ONLY the refactored code.

Code to refactor:
""",

    "multi": """
You are a software engineer specializing in code maintainability, performance optimization, and energy efficiency.

Task:
Analyze the code for both maintainability and efficiency issues.
Apply refactoring that balances both objectives.

Constraints:
- Do not add external dependencies
- Refactoring is strictly limited to internal computation logic only. Input and output must remain the same.
- Preserve meaningful comments and docstrings unless replaced by clearer structure

Optimization goals:
- Reduce Cyclomatic Complexity (CC)
- Reduce unnecessary Lines of Code (LOC)
- Reduce Halstead Volume
- Increase code readability and modularity
- Eliminate code smells and structural issues
- Reduce runtime execution time
- Reduce CPU energy consumption

Output:
Return ONLY the refactored code.

Code to refactor:
"""
}

STAGED_PROMPTS = {
    "staged_green": """You are a software engineer specializing in performance optimization and energy-efficient code.

Context:
The input code has already been refactored for maintainability and readability.

Task:
Analyze the code and identify performance and energy inefficiencies.
Apply efficiency-focused refactoring while preserving the existing clean structure.

Constraints:
- Do not add external dependencies
- Refactoring is strictly limited to internal computation logic only. Input and output must remain the same.
- Do not undo prior maintainability improvements
- Preserve meaningful comments and docstrings unless replaced by clearer structure

Optimization goals:
- Reduce runtime execution time
- Reduce CPU energy consumption
- Maintain or improve readability and modularity

Output:
Return ONLY the refactored code.

Code to refactor:""",
    "staged_clean": """You are a software engineer specializing in code maintainability and readability.

Context:
The input code has already been optimized for performance and energy efficiency.

Task:
Analyze the code and identify maintainability and readability issues.
Apply refactoring to improve code structure while preserving efficiency.

Constraints:
- Do not add external dependencies
- Refactoring is strictly limited to internal computation logic only. Input and output must remain the same.
- Do not undo prior efficiency improvements
- Preserve meaningful comments and docstrings unless replaced by clearer structure

Optimization goals:
- Reduce Cyclomatic Complexity (CC)
- Reduce unnecessary Lines of Code (LOC)
- Reduce Halstead Volume
- Increase code readability and modularity
- Eliminate code smells and structural issues
- Maintain or improve runtime efficiency
- Maintain or reduce CPU energy consumption

Output:
Return ONLY the refactored code.

Code to refactor:"""
}


# =====================================
# CLEAN OUTPUT FUNCTION
# =====================================

def clean_output(text: str) -> str:
    text = text.strip()

    if text.startswith("```"):
        lines = text.splitlines()

        # remove opening fence
        if lines and lines[0].startswith("```"):
            lines = lines[1:]

        # remove closing fence
        if lines and lines[-1].startswith("```"):
            lines = lines[:-1]

        return "\n".join(lines).strip()

    return text


def run_staged(model_key, model_name, script_name, model_cache):

    staged_map = {
        "stagedcg": ("staged_green", "clean"),
        "stagedgc": ("staged_clean", "green"),
    }

    for prompt_key, (template_key, cache_key) in staged_map.items():

        code = model_cache.get(cache_key)

        if not code:
            print(f"⚠️ Missing {cache_key} cache for {model_key}")
            continue

        print(f"Running {script_name} | {model_key} | {prompt_key}")

        full_prompt = STAGED_PROMPTS[template_key] + "\n\n" + code
        result = call_model(model_name, full_prompt)

        if result:
            final_code = clean_output(result)
            save_output(model_key, prompt_key, script_name, final_code)
# =====================================
# API CALL
# =====================================

def call_model(model_name, prompt_text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "temperature": TEMPERATURE
    }

    retries = 5

    for attempt in range(retries):
        try:
            response = requests.post(
                API_URL,
                headers=headers,
                json=payload,
                timeout=180
            )

            if response.status_code == 200:
                data = response.json()
                return data["choices"][0]["message"]["content"]

            print(f"ERROR {response.status_code}: {response.text}")

        except requests.exceptions.RequestException as e:
            print(f"Network error (attempt {attempt+1}/{retries}): {e}")

        time.sleep((2 ** attempt) + random.uniform(0, 1))

    return None

# =====================================
# SAVE RESULTS
# =====================================

def save_output(model_key, prompt_key, script_name, content):
    Path(OUTPUT_FOLDER).mkdir(exist_ok=True)

    filename = f"{model_key}_{prompt_key}_{script_name}"
    path = Path(OUTPUT_FOLDER) / filename

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

# =====================================
# MAIN LOOP
# =====================================

def run_experiment():

    script_files = list(Path(INPUT_FOLDER).glob("*.py"))

    print(f"Found {len(script_files)} scripts.")

    for script_path in script_files:
        script_name = script_path.name

        with open(script_path, "r", encoding="utf-8") as f:
            code = f.read()

        for model_key, model_name in MODELS.items():

            model_cache = {}

            for prompt_key, prompt_template in PROMPTS.items():

                print(f"Running {script_name} | {model_key} | {prompt_key}")

                full_prompt = prompt_template + "\n\n" + code
                result = call_model(model_name, full_prompt)

                if result:
                    cleaned = clean_output(result)
                    save_output(model_key, prompt_key, script_name, cleaned)


                    if prompt_key in ["clean", "green"]:
                        model_cache[prompt_key] = cleaned

                time.sleep(2)

            run_staged(model_key, model_name, script_name, model_cache)

if __name__ == "__main__":
    run_experiment()
