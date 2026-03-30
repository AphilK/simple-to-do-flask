"""WSGI application for production/serverless deployment."""
import os
import sys

try:
    from app import create_app
    app = create_app()
except Exception as e:
    # Log error for debugging
    print(f"ERROR creating app: {str(e)}", file=sys.stderr)
    import traceback
    traceback.print_exc()
    raise

if __name__ == "__main__":
    app.run()
