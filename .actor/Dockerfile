FROM apify/actor-python:3.12

ENV PYTHONPATH=/usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install playwright && python -m playwright install-deps firefox
# Xvfb lets camoufox run on a virtual display ("headless=virtual"), which passes
# AWS WAF's JS challenge that blocks pure-headless browsers.
RUN apt-get update && apt-get install -y --no-install-recommends xvfb && rm -rf /var/lib/apt/lists/*
RUN python -m camoufox fetch

COPY . ./

CMD ["python3", "src/main.py"]
