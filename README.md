# gif_maker
My own gif maker for all my animator needs.

## Setup

Create and activate a virtual environment, then install the dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

Use the virtual environment Python when launching the app:

```bash
python main.py
```

If you see `ModuleNotFoundError: No module named 'PySide6'`, it usually means the app is being run with a different Python interpreter than the one where PySide6 is installed.
