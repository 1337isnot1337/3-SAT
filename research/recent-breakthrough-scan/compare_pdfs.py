"""Optional Poppler comparison; equal extracted text is narrower than equal PDFs."""
from hashlib import sha256
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
SOURCE = HERE/"sources/anthropic"


def main():
    results = []
    for name in ("hexagon-v1-paper.pdf","github-paper.pdf"):
        path = SOURCE/name
        text = subprocess.check_output(["pdftotext","-layout",str(path),"-"],text=True)
        normalized = re.sub(r"\s+","",text.replace("hexagon:2610.00577v1",""))
        results.append({"path":name,"pdf_sha256":sha256(path.read_bytes()).hexdigest(),
                        "normalized_text_sha256":sha256(normalized.encode()).hexdigest(),
                        "normalized_characters":len(normalized)})
    if results[0]["normalized_text_sha256"] != results[1]["normalized_text_sha256"]:
        raise ValueError("The normalized extractions differ")
    print(json.dumps({"result":"PASS","scope":"equal whitespace-normalized Poppler text after Hexagon watermark removal; PDFs differ in bytes",
                      "command":["pdftotext","-layout","PDF","-"],"files":results},
                     indent=2,sort_keys=True))


if __name__ == "__main__":
    main()
