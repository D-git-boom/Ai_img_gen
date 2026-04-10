#!/bin/bash
PROJECT_DIR="$HOME/Documents/Projects/Ai_img_gen"

# Open VS Code in the project root
code "$PROJECT_DIR" &

# Open a terminal, activate venv, and start uvicorn
gnome-terminal -- bash -c "
  cd '$PROJECT_DIR' && \
  source venv/bin/activate && \
  cd backend && \
  uvicorn main:app --reload; \
  exec bash
"
