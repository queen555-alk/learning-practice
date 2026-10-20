"""A tiny TF-IDF search engine built with only the Python standard library.

Search your own notes (.txt / .md files) or a built-in set of sample documents.

    python3 tfidf_search.py "how do neural networks learn"
    python3 tfidf_search.py --dir ./my_notes "gradient descent"
    python3 tfidf_search.py
"""

import argparse
import math
import re
from collections import Counter
from pathlib import Path

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "for", "from", "has", "how",
    "in", "is", "it", "its", "of", "on", "or", "that", "the", "to", "was", "what",
    "when", "where", "which", "who", "why", "will", "with", "do", "does", "can",
}

SAMPLE_DOCS = {
    "neural_networks": (
        "A neural network is made of layers of connected units. During training, "
        "the network makes predictions, measures its error with a loss function, "
        "and adjusts its weights using backpropagation and gradient descent."
    ),
    "gradient_descent": (
        "Gradient descent is an optimization method. It repeatedly moves the model "
        "weights a small step in the direction that reduces the loss. The step size "
        "is called the learning rate."
    ),
    "embeddings": (
        "An embedding turns text into a list of numbers called a vector. Texts with "
        "similar meaning end up close together, which makes semantic search possible."
    ),
    "rag": (
        "Retrieval augmented generation, or RAG, first searches a document collection "
        "for relevant passages and then gives them to a language model so it can "
        "answer using your own data."
    ),
    "overfitting": (
        "Overfitting happens when a model memorizes the training data instead of "
        "learning general patterns. It performs well on training data but poorly on "
        "new data. Validation sets and regularization help detect and reduce it."
    ),
    "transformers": (
        "A transformer is a neural network architecture built around attention. "
        "Attention lets every token in a sequence look at every other token, and it "
        "is the foundation of modern large language models."
    ),
}


def tokenize(text: str) -> list[str]:
    """Lowercase the text, split it into words, and drop stopwords."""
    words = re.findall(r"[a-z0-9']+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def load_docs(folder: Path) -> dict[str, str]:
    """Read every .txt and .md file in a folder (recursively)."""
    docs = {}
    for path in sorted(folder.rglob("*")):
        if path.suffix.lower() in {".txt", ".md"} and path.is_file():
            docs[str(path.relative_to(folder))] = path.read_text(encoding="utf-8", errors="ignore")
    return docs


def _norm(vector: dict[str, float]) -> float:
    return math.sqrt(sum(v * v for v in vector.values()))


        counts = Counter(w for w in tokenize(query) if w in self.idf)
        if not counts:
            return []

        total = sum(counts.values())
        q_vec = {w: (c / total) * self.idf[w] for w, c in counts.items()}
        q_norm = _norm(q_vec)

        results = []
        for name, d_vec in self.vectors.items():
            dot = sum(weight * d_vec.get(word, 0.0) for word, weight in q_vec.items())
            d_norm = _norm(d_vec)
            if dot > 0 and d_norm > 0:
                results.append((dot / (q_norm * d_norm), name))

        results.sort(reverse=True)
        return results[:top_k]


def show_results(index: Index, query: str, top_k: int) -> None:
    results = index.search(query, top_k)
    if not results:
        print("No matches. Try different words.\n")
        return
    for rank, (score, name) in enumerate(results, start=1):
        preview = " ".join(index.docs[name].split())[:90]
        print(f"{rank}. {name}  (score {score:.3f})")
        print(f"   {preview}...")
    print()


def main() -> None:
    parser = argparse.ArgumentParser(description="Tiny TF-IDF search engine.")
    parser.add_argument("query", nargs="*", help="what to search for (omit for interactive mode)")
    parser.add_argument("--dir", type=Path, help="folder of .txt/.md files to search")
    parser.add_argument("--top", type=int, default=3, help="number of results to show")
    args = parser.parse_args()

    if args.dir:
        docs = load_docs(args.dir)
        if not docs:
            raise SystemExit(f"No .txt or .md files found in {args.dir}")
    else:
        docs = SAMPLE_DOCS

    index = Index(docs)
    print(f"Indexed {len(docs)} documents.\n")

    if args.query:
        show_results(index, " ".join(args.query), args.top)
        return

    print("Type a search (or 'quit' to exit).")
    while True:
        try:
            query = input("search > ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if query.lower() in {"quit", "exit", "q"}:
            break
        if query:
            show_results(index, query, args.top)


if __name__ == "__main__":
    main()