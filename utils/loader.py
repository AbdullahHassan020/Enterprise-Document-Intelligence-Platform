from pathlib import Path
from pypdf import PdfReader


def load_document(file_path):
    """
    Load PDF/TXT/MD document.
    """

    path = Path(file_path)

    extension = path.suffix.lower()

    filename = path.name

    # ---------------- PDF ----------------

    if extension == ".pdf":

        reader = PdfReader(file_path)

        pages = []

        for page in reader.pages:

            text = page.extract_text()

            if text:

                pages.append(text)

        return {

            "filename": filename,

            "text": "\n".join(pages),

            "pages": len(reader.pages)

        }

    # ---------------- TXT ----------------

    elif extension == ".txt":

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        return {

            "filename": filename,

            "text": text,

            "pages": 1

        }

    # ---------------- Markdown ----------------

    elif extension == ".md":

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        return {

            "filename": filename,

            "text": text,

            "pages": 1

        }

    else:

        raise ValueError(
            f"Unsupported file type: {extension}"
        )