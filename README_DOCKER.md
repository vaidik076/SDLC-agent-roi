Docker quickstart (run demo + Streamlit)

1. Build the Docker image from the repository root:

   docker build -t enterprise-agent-roi:demo .

2. Run the container and map port 8501 to the host. The example below also mounts
   the current directory to /app/output inside the container so demo outputs are
   persisted to the host:

   docker run --rm -p 8501:8501 -v "%cd%:/app/output" enterprise-agent-roi:demo

3. Open the dashboard in your browser:

   http://localhost:8501

Notes:
- The container runs run_demo.py first to populate /app/output/demo then starts Streamlit.
- If you prefer Linux/macOS shell, use $(pwd) instead of %cd% for the -v mount.
- If you want to run without generating demo data, modify the CMD in the Dockerfile or pass a custom command to `docker run`.
