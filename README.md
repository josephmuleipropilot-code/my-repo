Physics Solver - Flask web app

Quickstart (local):

1. Create a virtualenv and install dependencies:

```powershell
python -m venv venv; .\\venv\\Scripts\\Activate; pip install -r requirements.txt
```

2. Run the app:

```powershell
python webapp\\app.py
```

3. Open http://127.0.0.1:5000 in your browser.

Deploying to PythonAnywhere (summary):

- Create a PythonAnywhere account and start a Bash console.
- Upload your project files (you can use git, or upload zip).
- Create a virtualenv on PythonAnywhere and `pip install -r requirements.txt`.
- In the PythonAnywhere Web tab, create a new web app (manual configuration). Set the working directory to the folder containing `webapp`.
- Modify the WSGI configuration to import the Flask `app` from `webapp.app`:

  Replace the default WSGI contents with something like:

```python
import sys
path = '/home/yourusername/path-to-project'
if path not in sys.path:
    sys.path.insert(0, path)

from webapp.app import app as application
```

- Configure static files mapping: map `/static/` to the `webapp/static` folder.
- Reload the web app.

If you want, I can create a git repo, push these files, and provide an exact PythonAnywhere WSGI snippet for your username.
