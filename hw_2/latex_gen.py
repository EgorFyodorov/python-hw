"""Pure functions for generating small snippets of LaTeX.

The helpers in this module avoid any external dependencies and stick to string
manipulation so they can be reused in scripting or packaging contexts.
"""

from typing import Iterable, Sequence

LATEX_REPLACEMENTS = {
    "\\": r"\textbackslash{}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}


def escape_latex(value: str) -> str:
    """Escape a string so it can be safely embedded inside LaTeX."""
    escaped = value
    for char, replacement in LATEX_REPLACEMENTS.items():
        escaped = escaped.replace(char, replacement)
    return escaped


def generate_table(
    rows: Sequence[Sequence[object]],
    column_format: str | None = None,
) -> str:
    """Generate a tabular environment from a 2D sequence of data.

    Args:
        rows: Rectangular data grid. All rows must have the same length.
        column_format: Optional explicit tabular column format (e.g. '|c|c|').
            If omitted, a centered column with vertical borders will be emitted
            for each column.

    Returns:
        A LaTeX snippet containing a complete ``tabular`` environment.
    """
    normalized_rows = [list(row) for row in rows]
    if not normalized_rows:
        raise ValueError("Table must contain at least one row")

    column_count = len(normalized_rows[0])
    if column_count == 0:
        raise ValueError("Table must contain at least one column")

    for index, row in enumerate(normalized_rows, start=1):
        if len(row) != column_count:
            raise ValueError(
                f"Row {index} has {len(row)} columns, expected {column_count}"
            )

    if column_format is None:
        column_format = "|" + "|".join("c" for _ in range(column_count)) + "|"

    lines: list[str] = [f"\\begin{{tabular}}{{{column_format}}}", "\\hline"]

    for row in normalized_rows:
        rendered_cells = " & ".join(escape_latex(str(cell)) for cell in row)
        lines.append(f"{rendered_cells} \\\\")
        lines.append("\\hline")

    lines.append("\\end{tabular}")
    return "\n".join(lines)


def generate_image_block(
    path: str,
    width: str = "0.7\\textwidth",
    caption: str | None = None,
    label: str | None = None,
    placement: str = "h",
) -> str:
    """Generate a figure environment embedding an image.

    Args:
        path: Relative or absolute path to the image file.
        width: Value passed to the ``width`` option of ``\\includegraphics``.
        caption: Optional figure caption.
        label: Optional label for cross-referencing.
        placement: Figure placement hint, defaults to ``h`` (here).
    """
    safe_path = escape_latex(path)
    lines: list[str] = [f"\\begin{{figure}}[{placement}]", "\\centering"]
    lines.append(f"\\includegraphics[width={width}]{{{safe_path}}}")
    if caption:
        lines.append(f"\\caption{{{escape_latex(caption)}}}")
    if label:
        lines.append(f"\\label{{{escape_latex(label)}}}")
    lines.append("\\end{figure}")
    return "\n".join(lines)


def render_document(
    body_blocks: Iterable[str],
    packages: Iterable[str] | None = None,
    document_class: str = "article",
    title: str | None = None,
    author: str | None = None,
) -> str:
    """Wrap arbitrary LaTeX fragments into a full compilable document."""
    required_packages = ["graphicx"]
    if packages:
        required_packages.extend(packages)

    unique_packages: list[str] = []
    for pkg in required_packages:
        if pkg not in unique_packages:
            unique_packages.append(pkg)

    header_lines = [f"\\documentclass{{{document_class}}}"]
    header_lines.extend(f"\\usepackage{{{pkg}}}" for pkg in unique_packages)
    if title:
        header_lines.append(f"\\title{{{escape_latex(title)}}}")
    if author:
        header_lines.append(f"\\author{{{escape_latex(author)}}}")
    if title or author:
        header_lines.append("\\date{}")

    header_lines.append("\\begin{document}")
    if title or author:
        header_lines.append("\\maketitle")

    body_lines = list(body_blocks)
    footer_lines = ["\\end{document}"]

    return "\n\n".join(
        ["\n".join(header_lines), "\n\n".join(body_lines), "\n".join(footer_lines)]
    )

