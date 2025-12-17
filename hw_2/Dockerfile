FROM python:3.11-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends texlive-latex-base texlive-fonts-recommended texlive-latex-extra \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir .

CMD ["bash", "-lc", "python3 create_example.py && pdflatex -halt-on-error -interaction=nonstopmode -output-directory artifacts artifacts/table_and_image.tex && ls -lh artifacts && echo 'PDF готов в artifacts/'"]
