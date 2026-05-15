from __future__ import annotations

from pathlib import Path

from pypdf import PdfReader, PdfWriter


ROOT = Path(__file__).resolve().parents[1]
SCORE_DIR = ROOT / "output" / "scores"


def main() -> None:
    writer = PdfWriter()
    for filename in ["pink_music.pdf", "brown_music.pdf"]:
        reader = PdfReader(str(SCORE_DIR / filename))
        for page in reader.pages:
            writer.add_page(page)
    with (SCORE_DIR / "pink_and_brown_music.pdf").open("wb") as f:
        writer.write(f)


if __name__ == "__main__":
    main()
