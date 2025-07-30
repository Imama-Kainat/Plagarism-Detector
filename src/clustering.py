def bfs(graph, start, visited):
    """
    Breadth-First Search algorithm to find connected components in the graph.
    
    Args:
        graph: Dictionary representation of the graph (adjacency list)
        start: Starting node for BFS
        visited: Set of already visited nodes
        
    Returns:
        A list of nodes in the connected component
    """
    # Initialize cluster with the starting node
    cluster = []
    
    # Initialize queue with starting node
    queue = [start]
    visited.add(start)
    
    # Explore the graph starting from 'start'
    while queue:
        node = queue.pop(0)  # Dequeue
        cluster.append(node)
        
        # Visit all neighbors
        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(neighbor)
    
    return cluster

def dfs(graph, start, visited, cluster=None):
    """
    Depth-First Search algorithm to find connected components in the graph.
    
    Args:
        graph: Dictionary representation of the graph (adjacency list)
        start: Starting node for DFS
        visited: Set of already visited nodes
        cluster: List to accumulate nodes in the connected component
        
    Returns:
        A list of nodes in the connected component
    """
    if cluster is None:
        cluster = []
    
    # Mark node as visited and add to cluster
    visited.add(start)
    cluster.append(start)
    
    # Visit all neighbors
    for neighbor in graph[start]:
        if neighbor not in visited:
            dfs(graph, neighbor, visited, cluster)
    
    return cluster

def find_clusters(graph, method="bfs"):
    """
    Find all clusters (connected components) in the similarity graph.
    
    Args:
        graph: Dictionary representation of the graph (adjacency list)
        method: The graph traversal method to use ("bfs" or "dfs")
        
    Returns:
        A list of clusters, where each cluster is a list of filenames
    """
    clusters = []
    visited = set()
    
    # Try to find a cluster starting from each unvisited node
    for node in graph:
        if node not in visited:
            if method.lower() == "dfs":
                cluster = dfs(graph, node, visited)
            else:  # Default to BFS
                cluster = bfs(graph, node, visited)
            
            # Only add non-empty clusters
            if cluster:
                clusters.append(cluster)
    
    # Sort clusters by size (largest first)
    clusters.sort(key=len, reverse=True)
    
    return clusters