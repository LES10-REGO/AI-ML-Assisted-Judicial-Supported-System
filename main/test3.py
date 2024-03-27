# test3.py

import PyPDF2
from sentence_transformers import SentenceTransformer, util
import spacy  # For named entity recognition (optional)

def find_relevant_cases(query_file, previous_case_files, model_name="all-mpnet-base-v2"):
    """Compares a query case file with previous cases and recommends relevant ones."""

    # Load PDF files and extract text
    query_text = extract_text_from_pdf(query_file)
    previous_case_texts = [
        extract_text_from_pdf(file) for file in previous_case_files
    ]

    # Load semantic embedding model
    embedder = SentenceTransformer(model_name)

    # Generate embeddings for text
    query_embedding = embedder.encode(query_text, convert_to_tensor=True)
    previous_case_embeddings = embedder.encode(previous_case_texts, convert_to_tensor=True)

    # Calculate pairwise similarities
    similarities = util.pytorch_cos_sim(query_embedding, previous_case_embeddings)

    # Filter and rank relevant cases (optionally using NER)
    relevant_cases = []
    for i, similarity_score in enumerate(similarities[0]):
        if similarity_score > 0.15:  # Adjust threshold as needed
            previous_case_file = previous_case_files[i]
            previous_case_text = previous_case_texts[i]

            # Optional: Filter based on named entities
            # if filter_using_ner(previous_case_text):
            relevant_cases.append((similarity_score, previous_case_file, previous_case_text))

    return sorted(relevant_cases, reverse=True)

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""

    with open(pdf_file, "rb") as pdf_reader:
        pdf_reader = PyPDF2.PdfReader(pdf_reader)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text
