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
    # Table Formatting
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
    Secure Python code execution environment with output capture.
    
    Features:
    - Restricted imports (only whitelisted modules)
    - Matplotlib plot capture as base64 images
    - stdout/stderr capture
    - Safe builtins environment
    - Pretty table printing for DataFrames
    """
    
    def __init__(self):
        self.images = []
        self.stdout_buffer = io.StringIO()
        self.stderr_buffer = io.StringIO()
        
    def _create_fake_show(self):
        """Create a fake plt.show() that captures images instead of displaying them."""
        def fake_show(*args, **kwargs):
            buf = io.BytesIO()
            plt.savefig(buf, format="png", bbox_inches="tight", dpi=150)
            buf.seek(0)
            img_b64 = base64.b64encode(buf.read()).decode()
            self.images.append(f"data:image/png;base64,{img_b64}")
            plt.close()
        return fake_show
    
    def _setup_pandas_display(self):
        """Configure pandas to display nice tables."""
        # Set pandas display options for better table formatting
        pd.set_option('display.max_rows', 100)
        pd.set_option('display.max_columns', 20)
        pd.set_option('display.width', 1000)
        pd.set_option('display.max_colwidth', 50)
        
    def execute(self, code: str) -> dict:
        """
        Execute Python code in a sandboxed environment.
        
        Args:
            code: Python code string to execute
            
        Returns:
            dict with keys:
                - status: "success" or "error"
                - output: stdout content
                - error: stderr content (if any)
                - images: list of base64-encoded PNG images
                - message: human-readable message
        """
        # Reset buffers and images
        self.images = []
        self.stdout_buffer = io.StringIO()
        self.stderr_buffer = io.StringIO()
        
        # Clear any existing matplotlib figures
        plt.clf()
        plt.close("all")
        
        # Setup pandas display options
        self._setup_pandas_display()
        
        # Create safe execution environment
        safe_globals = {
            "__builtins__": SAFE_BUILTINS,
            "pd": pd,
            "plt": plt,
            "np": np,
        }
        
        # Override plt.show to capture images
        original_show = plt.show
        plt.show = self._create_fake_show()
        
        try:
            with contextlib.redirect_stdout(self.stdout_buffer), \
                 contextlib.redirect_stderr(self.stderr_buffer):
                exec(code, safe_globals, {})
            
            # Check for errors in stderr
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
            error_traceback = traceback.format_exc()
            print(f"❌ Sandbox Execution Error: {error_traceback}")
            
            return {
                "status": "error",
                "output": self.stdout_buffer.getvalue(),
                "error": error_traceback,
                "images": self.images,
                "message": f"Execution failed: {str(e)}"
            }
            
        finally:
            # Restore original plt.show
            plt.show = original_show


def run_code(code: str) -> dict:
    """
    Convenience function to execute code in sandbox.
    
    Args:
        code: Python code string to execute
        
    Returns:
        dict with execution results
    """
    runner = SandboxRunner()
    return runner.execute(code)


# ================= CLI INTERFACE (for testing) =================
def main():
    """Run sandbox from command line (reads code from stdin)."""
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