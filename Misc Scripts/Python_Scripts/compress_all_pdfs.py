import subprocess
from pathlib import Path


def compress_pdf(input_pdf):
    output_pdf = input_pdf.with_name(f"{input_pdf.stem}-Compressed{input_pdf.suffix}")

    cmd = [
        "gs",
        "-sDEVICE=pdfwrite",
        "-dCompatibilityLevel=1.4",
        "-dPDFSETTINGS=/ebook",  # Change to /screen for more compression
        "-dNOPAUSE",
        "-dQUIET",
        "-dBATCH",
        f"-sOutputFile={output_pdf}",
        str(input_pdf),
    ]

    result = subprocess.run(cmd)

    if result.returncode == 0:
        print(f"✓ {input_pdf.name} -> {output_pdf.name}")
    else:
        print(f"✗ Failed: {input_pdf.name}")


def main():
    # Current directory
    for pdf in Path.cwd().glob("*.pdf"):
        # Skip already compressed files
        if pdf.stem.endswith("-Compressed"):
            continue

        compress_pdf(pdf)

    print("\nDone!")


if __name__ == "__main__":
    main()
