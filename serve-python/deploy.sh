#!/bin/bash
cd models
[[ -f requirements.txt ]] && pip3 install -r requirements.txt
cd ..
uvicorn serve:app --host 0.0.0.0 --port 8501