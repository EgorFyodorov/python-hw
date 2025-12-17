.PHONY: example pdf clean docker-build docker-run

IMAGE ?= hw2-latex
ARTIFACT_DIR := $(CURDIR)/artifacts

example:
	python3 create_example.py

pdf: example
	pdflatex -halt-on-error -output-directory artifacts artifacts/table_and_image.tex

clean:
	rm -f artifacts/*.aux artifacts/*.log artifacts/*.out artifacts/*.pdf

docker-build:
	docker build -t $(IMAGE) .

docker-run:
	docker run --rm -v "$(ARTIFACT_DIR):/app/artifacts" $(IMAGE)
