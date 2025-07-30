def merge(left, right, key_func):
    """
    Merge two sorted lists into a single sorted list.
    
    Args:
        left: First sorted list
        right: Second sorted list
        key_func: Function to extract the sorting key from an element
        
    Returns:
        A merged sorted list
    """
    result = []
    i = j = 0
    
    # Compare and merge items from both lists
    while i < len(left) and j < len(right):
        if key_func(left[i]) >= key_func(right[j]):  # Descending order
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    # Add remaining items
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def merge_sort(arr, key_func):
    """
    Sort a list using the merge sort algorithm.
    
    Args:
        arr: List to sort
        key_func: Function to extract the sorting key from an element
        
    Returns:
        A sorted list in descending order by the key function
    """
    # Base case: lists of 0 or 1 items are already sorted
    if len(arr) <= 1:
        return arr
    
    # Divide the list into two roughly equal parts
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key_func)
    right = merge_sort(arr[mid:], key_func)
    
    # Merge the sorted parts
    return merge(left, right, key_func)

def select_representative(cluster, graph):
    """
    Select a representative submission from a cluster using a greedy approach.
    
    The representative is chosen based on having the highest average similarity
    to other submissions in the same cluster.
    
    Args:
        cluster: List of filenames in the cluster
        graph: Dictionary representation of the similarity graph
        
    Returns:
        The filename of the selected representative
    """
    if not cluster:
        return None
    
    if len(cluster) == 1:
        return cluster[0]  # If there's only one submission, it's the representative
    
    # Calculate average similarity for each node in the cluster
    avg_similarities = {}
    
    for node in cluster:
        # Sum similarity scores with all other nodes in the cluster
        total_similarity = sum(graph[node].get(other, 0) for other in cluster if other != node)
        
        # Calculate average similarity
        avg_similarity = total_similarity / (len(cluster) - 1)
        avg_similarities[node] = avg_similarity
    
    # Use merge sort to sort nodes by average similarity (highest first)
    sorted_nodes = merge_sort(list(cluster), 
                             key_func=lambda x: avg_similarities.get(x, 0))
    
    # Select node with highest average similarity
    representative = sorted_nodes[0]
    
    return representative

def select_multiple_representatives(cluster, graph, num_representatives=2):
    """
    Select multiple representatives from a cluster using a greedy approach.
    
    Representatives are chosen to maximize coverage of the cluster while
    minimizing redundancy.
    
    Args:
        cluster: List of filenames in the cluster
        graph: Dictionary representation of the similarity graph
        num_representatives: Number of representatives to select
        
    Returns:
        List of filenames of the selected representatives
    """
    if not cluster:
        return []
    
    if len(cluster) <= num_representatives:
        return cluster  # If cluster is smaller than requested reps, return all
    
    # First, select the submission with highest average similarity
    representatives = [select_representative(cluster, graph)]
    
    # Select remaining representatives greedily
    remaining = [node for node in cluster if node not in representatives]
    
    while len(representatives) < num_representatives and remaining:
        # For each remaining node, calculate its similarity to existing representatives
        dissimilarities = {}
        
        for node in remaining:
            # Calculate average similarity to existing representatives
            avg_similarity_to_reps = sum(graph[node].get(rep, 0) for rep in representatives) / len(representatives)
            
            # We want to maximize dissimilarity (pick diverse representatives)
            dissimilarity = 1 - avg_similarity_to_reps
            dissimilarities[node] = dissimilarity
        
        # Use merge sort to sort remaining nodes by dissimilarity (highest first)
        sorted_remaining = merge_sort(remaining, 
                                     key_func=lambda x: dissimilarities.get(x, 0))
        
        if sorted_remaining:
            next_rep = sorted_remaining[0]
            representatives.append(next_rep)
            remaining.remove(next_rep)
        else:
            break  # No suitable next representative found
    
    return representatives