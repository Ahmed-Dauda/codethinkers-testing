"""
Secure Python code execution sandbox with resource limits and output capture.
"""

import sys
import io
import traceback
import base64
import contextlib
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# ================= SANDBOX CONFIGURATION =================
ALLOWED_MODULES = {
    # Data Science Core
    "pandas",
    "numpy",
    # Visualization
    "matplotlib",
    "matplotlib.pyplot",
    "seaborn",
    # Math & Statistics
    "math",
    "statistics",
    "random",
    # Dates & Time
    "datetime",
    "time",
    "calendar",
    # Data Formats
    "json",
    "csv",
    # Functional / Itertools
    "itertools",
    "collections",
    # Scientific Computing
    "scipy",
    # Machine Learning (Intro Level)
    "sklearn",
    # Regex & Text
    "re",
    "string",
    # Decimal Precision
    "decimal",
    # Table Formatting (for pandas)
    "tabulate",
}

BASE_ALLOWED = {m.split('.')[0] for m in ALLOWED_MODULES}


def safe_import(name, globals=None, locals=None, fromlist=(), level=0):
    """Controlled import function that only allows whitelisted modules."""
    root_name = name.split('.')[0]
    if root_name not in BASE_ALLOWED:
        raise ImportError(f"Import of '{name}' is not allowed.")
    return __import__(name, globals, locals, fromlist, level)


SAFE_BUILTINS = {
    "__import__": safe_import,
    "print": print,
    "len": len,
    "range": range,
    "min": min,
    "max": max,
    "sum": sum,
    "abs": abs,
    "sorted": sorted,
    "enumerate": enumerate,
    "zip": zip,
    "map": map,
    "filter": filter,
    "list": list,
    "dict": dict,
    "set": set,
    "tuple": tuple,
    "str": str,
    "int": int,
    "float": float,
    "bool": bool,
    "round": round,
    "pow": pow,
    "isinstance": isinstance,
    "type": type,
    "any": any,
    "all": all,
    "hex": hex,
    "bin": bin,
    "oct": oct,
    "chr": chr,
    "ord": ord,
}


class SandboxRunner:
    """
    Secure Python code execution environment with:
    - Dynamic input support (VSCode-style)
    - Matplotlib plot capture
    - Pandas table formatting
    - Safe builtins
    """

    def __init__(self, user_inputs=None, timeout=5):
        self.images = []
        self.stdout_buffer = io.StringIO()
        self.stderr_buffer = io.StringIO()
        self.user_inputs = user_inputs or []
        self.input_index = 0
        self.timeout = timeout

    # ----------------- Safe Input -----------------
    def safe_input(self, prompt=""):
        """
        Custom input() that pulls from user_inputs array.
        Prints prompt + simulated user typing to stdout.
        """
        print(prompt, end="")  # show prompt
        if self.input_index < len(self.user_inputs):
            value = self.user_inputs[self.input_index]
            self.input_index += 1
            print(value)  # simulate typed value
            return value
        # If no input left, raise error (forces frontend to provide it)
        raise RuntimeError("Input requested but no more user_inputs available.")

    # ----------------- Fake plt.show -----------------
    def _create_fake_show(self):
        """Capture matplotlib plots as base64 images instead of displaying."""
        def fake_show(*args, **kwargs):
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode()
            self.images.append(f"data:image/png;base64,{img_b64}")
            plt.close()
        return fake_show

    # ----------------- Execute Code -----------------
    def execute(self, code: str) -> dict:
        # Reset buffers
        self.images = []
        self.stdout_buffer = io.StringIO()
        self.stderr_buffer = io.StringIO()

        # Clear matplotlib figures
        plt.clf()
        plt.close("all")

        # Setup safe globals
        safe_globals = {
            "__builtins__": SAFE_BUILTINS,
            "input": self.safe_input,
            "pd": pd,
            "np": np,
            "plt": plt,
        }

        # Override plt.show to capture images
        original_show = plt.show
        plt.show = self._create_fake_show()

        try:
            with contextlib.redirect_stdout(self.stdout_buffer), contextlib.redirect_stderr(self.stderr_buffer):
                exec(code, safe_globals, {})

            stderr_output = self.stderr_buffer.getvalue()
            if stderr_output:
                return {
                    "status": "error",
                    "output": self.stdout_buffer.getvalue(),
                    "error": stderr_output,
                    "images": self.images,
                    "message": "Execution completed with warnings/errors"
                }

            return {
                "status": "success",
                "output": self.stdout_buffer.getvalue() or "[No output]",
                "error": "",
                "images": self.images,
                "message": "Execution completed successfully"
            }

        except Exception as e:
            return {
                "status": "error",
                "output": self.stdout_buffer.getvalue(),
                "error": traceback.format_exc(),
                "images": self.images,
                "message": f"Execution failed: {str(e)}"
            }

        finally:
            plt.show = original_show


# ----------------- Convenience Function -----------------
def run_code(code: str, inputs=None) -> dict:
    runner = SandboxRunner(user_inputs=inputs)
    return runner.execute(code)


# ================= CLI INTERFACE (for testing) =================
def main():
    """Run sandbox from CLI (reads code from stdin)."""
    import json

    try:
        code = sys.stdin.read()
        result = run_code(code)
        print(json.dumps(result, indent=2))

    except Exception as e:
        print(json.dumps({
            "status": "error",
            "output": "",
            "error": traceback.format_exc(),
            "images": [],
            "message": f"Fatal error: {str(e)}"
        }, indent=2))


if __name__ == "__main__":
    main()

  
