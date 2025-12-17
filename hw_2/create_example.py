"""Helper script that renders an example .tex file using latex_gen."""

from pathlib import Path

from latex_gen import generate_image_block, generate_table, render_document

ARTIFACTS_DIR = Path(__file__).parent / "artifacts"
TEX_OUTPUT = ARTIFACTS_DIR / "table_and_image.tex"
IMAGE_PATH = ARTIFACTS_DIR / "sample.png"

TABLE_DATA = [
    ["Name", "Role", "Score"],
    ["Alice", "Developer", 9.1],
    ["Bob", "Reviewer", 8.7],
    ["Charlie", "Analyst", 9.4],
]


def ensure_artifacts() -> None:
    ARTIFACTS_DIR.mkdir(parents=True, exist_ok=True)


def ensure_image(path: Path) -> None:
    """Ensure a sample image exists; relies on the committed file."""
    if not path.exists():
        raise FileNotFoundError(f"Expected sample image at {path}")


def build_example_tex() -> str:
    table_block = generate_table(TABLE_DATA)
    table_environment = "\n".join(
        [
            "\\begin{table}[h]",
            "\\centering",
            table_block,
            "\\caption{Generated table}",
            "\\label{tab:sample}",
            "\\end{table}",
        ]
    )

    figure_block = generate_image_block(
        path=str(IMAGE_PATH.relative_to(ARTIFACTS_DIR)),
        caption="Sample image",
        label="fig:sample-image",
        width="0.45\\textwidth",
    )

    document_body = [
        "\\section*{Table example}",
        table_environment,
        "\\section*{Image example}",
        figure_block,
    ]

    return render_document(
        document_body,
        packages=["array"],
        title="LaTeX Generator",
        author="hw_2",
    )


def main() -> None:
    ensure_artifacts()
    ensure_image(IMAGE_PATH)
    tex_content = build_example_tex()
    TEX_OUTPUT.write_text(tex_content, encoding="utf-8")
    print(f"Saved example LaTeX to {TEX_OUTPUT}")


if __name__ == "__main__":
    main()
