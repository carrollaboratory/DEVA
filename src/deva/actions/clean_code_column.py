"""
Cleans a datafile column that contains codes.
Expects a column with data similar to: '|HP:0004323|HP:0000234|''|HP:0004323||HP:0000234|'
"""

import argparse
import re
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.table import Table  # used for Output 2

from deva.common import read_file, write_file

console = Console()

def clean_codes(codes):
    codes = codes.replace(" ", "")
    codes = codes.replace("''", "")
    codes = codes.replace('"', "")
    codes = codes.replace("||", "|")
    codes = codes.replace("|'", "'").replace("'|", "'")
    codes = (
        codes.replace("| ", "|")
        .replace(" |", "|")
        .replace(" '", "'")
        .replace("' ", "'")
    )
    codes = codes.replace("'", "").replace('"', "")
    return codes


def is_valid_format(code):
    # Check format STRING:12345 (uppercase string, colon, string)
    return bool(re.fullmatch(r"[A-Z]+:.*?", code))


def collect_distinct_codes(series):
    """Return a sorted set of all distinct codes found across the cleaned column."""
    codes: set[str] = set()
    for cell in series:
        normalized = str(cell).strip().lower()
        if normalized in {"", "nan", "none", "null"}:
            continue
        for code in str(cell).split("|"):
            code = code.strip()
            if code:
                codes.add(code)
    return codes


def create_flag_column(codes):
    # Treat null/empty values as valid (no codes to validate).
    if codes is None:
        return [True]

    normalized = str(codes).strip().lower()
    if normalized in {"", "nan", "none", "null"}:
        return [True]

    # Check if each code matches the valid format
    return [is_valid_format(code) for code in codes.split("|") if code.strip()]


def main():
    parser = argparse.ArgumentParser(
        description="Get metadata for a code using the available locutus OntologyAPI connection."
    )

    parser.add_argument(
        "-df",
        "--data_file",
        required=True,
        help="File containing the codes requiring metadata. Format: 'path/to/datafile.csv'",
    )
    parser.add_argument(
        "-c",
        "--column",
        required=True,
        help="Column name containing the codes requiring metadata. The utils can do some amount of cleaning. # Format: 'ExactFieldName'",
    )
    parser.add_argument(
        "-o",
        "--output",
        required=False,
        help="Output CSV path. If not provided, a file named 'cleaned_codes.csv' will be created in the same directory as the input file.",
    )

    args = parser.parse_args()
    file_path = Path(args.data_file)
    filename = file_path.stem
    file_dir = file_path.parent

    output_path = args.output or file_dir / f"deva_files/{filename}_cleaned_codes.csv"
    output_dir = Path(output_path).parent
    output_dir.mkdir(parents=True, exist_ok=True)

    df = read_file(file_path)

    df["cleaned_col"] = df[args.column].astype(str).apply(clean_codes)
    df["correct_format"] = df["cleaned_col"].apply(create_flag_column)

    # Output 1: distinct codes found across the entire file
    distinct = collect_distinct_codes(df["cleaned_col"])
    codes_str = ";".join(distinct)
    console.print(Panel(f"[cyan]{codes_str}[/cyan]", title="[bold green]Output 1 — Distinct Codes[/bold green]", border_style="green"))

    # Output 2: rows whose codes did not pass format validation
    questionable = df[df["correct_format"].apply(lambda x: not all(x))]
    if len(questionable) >= 1:
        q_table = Table(title="Rows with format issues", show_lines=True)
        q_table.add_column("index", style="dim")
        q_table.add_column("cleaned_col", style="yellow")
        q_table.add_column("correct_format", style="red")
        for idx, row in questionable[["cleaned_col", "correct_format"]].iterrows():
            q_table.add_row(str(idx), str(row["cleaned_col"]), str(row["correct_format"]))
        console.print(Panel(q_table, title="[bold red]Output 2 — Questionable Rows[/bold red]", border_style="red"))
        if args.output:
            q_path = Path(args.output).with_stem(Path(args.output).stem + "_questionable")
            write_file(q_path, questionable[["cleaned_col", "correct_format"]])
            console.print(f"[orange1]Output 3 - A file was written to:[/orange1] {q_path}")
        else:
            console.print(
                f"[orange1]Output 3 - None - No questionable rows exist.[/orange1]"
            )

    write_file(output_path, df)
    console.print(f"[bold]File written →[/bold] {output_path}")


if __name__ == "__main__":
    main()
