FROM python:3.11-slim-bullseye
LABEL authors="empress"

WORKDIR /app

COPY . .

ENV VENV=/app/venv

RUN python3 -m venv $VENV

#venv activation
ENV PATH="$VENV/bin:$PATH"

RUN pip3 install -r requirements.txt

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

ENTRYPOINT ["streamlit", "run", "SignUp_or_Login.py", "--server.port=8501", "--server.address=0.0.0.0"]