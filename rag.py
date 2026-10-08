from pypdf import PdfReader


def read_pdf(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        # Blank line between pages so each page is at least one chunk
        text += (page.extract_text() or "") + "\n\n"
    return text


def get_context(text, question):
    chunks = text.split("\n\n")
    words = [w.strip("?.,!").lower() for w in question.split() if len(w) > 3]

    # Score each chunk by how many question words it contains
    scored = []
    for chunk in chunks:
        score = sum(1 for word in words if word in chunk.lower())
        if score > 0:
            scored.append((score, chunk))

    scored.sort(key=lambda item: item[0], reverse=True)
    results = [chunk for score, chunk in scored]
    return "\n".join(results[:3])
