# Underwriting RAG Demo

A Python demonstration of retrieval-augmented generation (RAG) for exploring sample underwriting documents. The pipeline extracts PDF text, splits it into chunks, retrieves relevant passages with FAISS, and produces either an LLM response or a clearly labelled mock answer.

This is an educational prototype, not a production underwriting system. Sample documents are fictional fixtures, not authoritative insurance policies, legal guidance, or medical advice. Any references to legislation in the sample text should not be relied upon.

## What the demo demonstrates

- PDF text extraction with `pdfplumber`, preserving document names and page numbers.
- Sentence grouping using adjacent-sentence TF-IDF cosine similarity and a character-length threshold.
- OpenAI embeddings when configured, with local TF-IDF vectors otherwise.
- FAISS `IndexFlatIP` search over normalized vectors.
- Comparison of a short question with a question expanded using supplied risk factors.
- A small retrieval-evaluation example using precision and recall.
- Answer generation with OpenAI or Anthropic, or a deterministic mock response without API keys.

The baseline uses TF-IDF for chunk boundaries; it does not implement neural sentence-embedding chunking. Query expansion appends supplied case context rather than using an LLM to rewrite the question.

## Files

| File | Purpose |
| --- | --- |
| `underwriting_copilot_rag_demo.py` | Main extraction, chunking, retrieval, evaluation and generation demo |
| `generate_sample_docs.py` | Generates three sample PDFs in `docs/` |
| `docs/` | Generated sample policy, product and investigation documents |
| `requirements.txt` | Python dependencies, if included |

The main script builds its FAISS index in memory on each run. Prebuilt `.faiss` and `.pkl` files are not required.

## Quick start

Use Python 3.10 or newer. Download the repository and open a terminal in its folder.

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it using the command for your terminal:

**Windows Command Prompt**

```bat
.venv\Scripts\activate.bat
```

**Windows PowerShell**

```powershell
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
source .venv/bin/activate
```

### 2. Install dependencies

```bash
python -m pip install numpy pdfplumber faiss-cpu scikit-learn reportlab
```

For optional API-backed generation and embeddings:

```bash
python -m pip install openai anthropic
```

If a matching `requirements.txt` is included, installation can instead use `python -m pip install -r requirements.txt`. Dependency versions are not pinned in these instructions.

### 3. Generate sample documents

From the repository root:

```bash
python generate_sample_docs.py
```

This creates `underwriting_policy_manual.pdf`, `product_guidelines.pdf`, and `rcu_report_template.pdf` inside `docs/`.

### 4. Run the demo

```bash
cd docs
python ../underwriting_copilot_rag_demo.py
```

Run from `docs/` because the current script searches for PDFs in the working directory. It does not automatically search the `docs/` subfolder or accept a document-directory CLI argument.

For a local run without API calls, ensure both `OPENAI_API_KEY` and `ANTHROPIC_API_KEY` are unset. After dependencies are installed, this mode uses local TF-IDF vectors and a mock answer.

## Optional API mode

The script reads credentials from environment variables; it does not automatically load a `.env` file. Configure keys locally through your environment or IDE, never in committed source files.

| Environment variables available | Retrieval vectors | Answer generation |
| --- | --- | --- |
| Neither key | Local TF-IDF | Deterministic mock answer |
| `OPENAI_API_KEY` only | OpenAI `text-embedding-3-small` | OpenAI `gpt-4o-mini` |
| `ANTHROPIC_API_KEY` only | Local TF-IDF | Anthropic `claude-haiku-4-5-20251001` |
| Both keys | OpenAI `text-embedding-3-small` | Anthropic takes priority |

These are the model identifiers configured in the supplied code, not a guarantee of current account access. API mode sends document chunks and/or questions to the configured providers and may incur charges. Use only permitted sample content.

Provider selection is based on available keys. Automatic failover after an API error is not implemented.

## Example question and output

The script contains a fixed demonstration question:

> Why was this flagged?

It compares retrieval for that question with retrieval after adding these fictional case factors:

- Sum assured is 18 times annual income.
- No medical loading is declared at age 58.
- Agent persistency is 34%, compared with a branch average of 72%.

The terminal prints extraction counts, sample chunks, embedding mode, index dimensions, retrieval scores, source document/page references, evaluation metrics and a final answer.

Without API keys, the answer follows this template (the source list depends on retrieval):

```text
[MOCK ANSWER — no API key set] Based on <retrieved document/page references>,
the retrieved clauses above are the basis for this flag.
Final decision rests with the underwriter.
```

This is an illustrative output template, not a recorded benchmark result. The mock response does not perform substantive underwriting reasoning.

To change the demonstration, edit `raw_q` and `risk_factors` in the script's `if __name__ == "__main__":` block. There is no interactive chat interface in this version.

## Retrieval evaluation

The demo includes three queries with manually specified relevant chunk IDs. Precision measures how many retrieved chunks are marked relevant; recall measures how many marked relevant chunks were retrieved.

**Validate the relevance labels before interpreting the printed metrics.** Chunk IDs depend on PDF text and chunking settings. The supplied IDs have not been validated for every generated document version. Regenerating documents or changing chunking can invalidate them.

The evaluation function tests ordinary retrieval; the raw-versus-expanded comparison is printed separately. Higher similarity scores alone do not establish better retrieval quality. No verified benchmark results are claimed here.

## Known limitations

- Text-based PDFs only; OCR for scanned pages is not implemented.
- TF-IDF chunking uses lexical overlap, and the length threshold is not a strict limit for an individual long sentence.
- No minimum-relevance threshold or reliable abstention behaviour for unsupported questions.
- Citations are included in retrieved context and requested in the prompt, but generated citation accuracy is not automatically checked.
- No implemented authentication, conversation memory, web interface or API service.
- No application-level retry, provider-failover or monitoring workflow.
- Small demonstration corpus and evaluation set; no production accuracy or business-impact claims.
- Sample text needs editorial review before public release, especially any wording that appears to state real legal requirements.

## Development priorities

- Replace fragile numeric relevance labels with reviewed, stable source references.
- Add meaningful tests for extraction, retrieval and missing-document handling.
- Add low-relevance handling and evaluate groundedness and citation accuracy.
- Compare baseline chunking with a separately documented neural approach.
- Pin a tested dependency environment and publish reproducible evaluation results.

