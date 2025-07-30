from src.rabin_karp import find_matches

def calculate_similarity(tokens1, tokens2, k=7):
    """
    Calculate similarity score between two tokenized code submissions.
    
    The similarity is based on the number of matching k-length token sequences,
    normalized by the average length of the two sequences.
    
    Args:
        tokens1: First list of tokens
        tokens2: Second list of tokens
        k: Length of token sequences to compare
        
    Returns:
        A similarity score between 0.0 and 1.0
    """
    # Special handling for empty files or EMPTY_FILE tokens
    if tokens1 == ["EMPTY_FILE"] or tokens2 == ["EMPTY_FILE"]:
        # If both are empty files, they're identical (similarity = 1.0)
        if tokens1 == tokens2:
            return 1.0
        # Otherwise, empty files are dissimilar to non-empty files
        return 0.0
    
    # Handle edge cases
    if not tokens1 or not tokens2:
        return 0.0
    
    # If file types are different (e.g., .py vs .js), lower the similarity
    # We can infer this if their tokens are very different
    if len(set(tokens1).intersection(set(tokens2))) < min(len(set(tokens1)), len(set(tokens2))) * 0.3:
        return 0.0
    
    if len(tokens1) < k or len(tokens2) < k:
        # If either sequence is too short for k-gram comparison,
        # use a direct comparison of common tokens
        common = set(tokens1).intersection(set(tokens2))
        total = set(tokens1).union(set(tokens2))
        return len(common) / len(total) if total else 0.0
    
    # Find matching k-grams using Rabin-Karp
    matches = find_matches(tokens1, tokens2, k)
    
    # Calculate maximum possible matches
    max_matches1 = len(tokens1) - k + 1
    max_matches2 = len(tokens2) - k + 1
    
    # Normalized similarity score (Jaccard-inspired)
    # This considers the proportion of matching sequences relative to the total possible sequences
    similarity = matches / (max_matches1 + max_matches2 - matches) if (max_matches1 + max_matches2 - matches) > 0 else 0.0
    
    return min(similarity, 1.0)  # Cap at 1.0

def build_similarity_graph(submissions, threshold=0.5, k=7):
    """
    Build a graph representation of submission similarities.
    
    Args:
        submissions: Dictionary mapping filenames to tokenized content
        threshold: Minimum similarity score to create an edge
        k: Length of token sequences to compare
        
    Returns:
        A graph represented as an adjacency list with weighted edges
    """
    # Initialize empty graph with nodes for all submissions
    graph = {file: {} for file in submissions}
    
    # Compare each pair of submissions
    for file1 in submissions:
        for file2 in submissions:
            if file1 != file2:  # Don't compare a file with itself
                # Calculate similarity score
                score = calculate_similarity(submissions[file1], submissions[file2], k)
                
                # Add edge if similarity exceeds threshold
                if score >= threshold:
                    graph[file1][file2] = score
    
    return graph