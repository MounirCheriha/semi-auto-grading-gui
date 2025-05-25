from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import Tuple, List, Dict

# Initialize the embedding model globally to avoid reloading
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

def build_index(responses: List[str], labels: List[int]) -> Tuple[faiss.Index, np.ndarray, Dict[int, Tuple[str, int]]]:
    """
    Builds a FAISS index for semantic similarity search of responses.
    
    Args:
        responses: List of text responses to index
        labels: List of corresponding labels (1=correct, 0=incorrect)
        
    Returns:
        tuple: (FAISS index, response embeddings, index-to-response/label mapping)
    """
    # Generate embeddings for all responses
    embeddings = embedding_model.encode(responses, convert_to_numpy=True)
    dim = embeddings.shape[1]

    # Create and populate FAISS index
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)

    # Create mapping from index to (response, label) pairs
    idx_map = {i: (resp, lbl) for i, (resp, lbl) in enumerate(zip(responses, labels))}
    return index, embeddings, idx_map

def retrieve_examples(
    index: faiss.Index, 
    idx_map: Dict[int, Tuple[str, int]], 
    answer: str, 
    top_k: int = 10
) -> Tuple[List[str], List[str]]:
    """
    Retrieves similar correct and incorrect examples for a given answer.
    
    Args:
        index: Pre-built FAISS index
        idx_map: Mapping from FAISS indices to (response, label) pairs
        answer: Input answer to find similar examples for
        top_k: Number of similar items to retrieve initially
        
    Returns:
        tuple: (list of 3 most similar correct examples, 
               list of 3 most similar incorrect examples)
    """

    # Encode the query answer
    vector = embedding_model.encode([answer], convert_to_numpy=True)
    
    # Search for similar items in the index
    D, I = index.search(vector, top_k)
    correct, incorrect = [], []

    for idx in I[0]:
        # Skip invalid indices
        if idx == -1 or idx not in idx_map:
            continue 
        resp, lbl = idx_map[idx]

        # Collcet unique examples until we have enough
        if lbl == 1 and resp not in correct:
            correct.append(resp)
        elif lbl == 0 and resp not in incorrect:
            incorrect.append(resp)

        # Early exit if we have enough examples
        if len(correct) >= 3 and len(incorrect) >= 3:
            break

    return correct[:3], incorrect[:3]