import os
import sys
import time
from src.parser import load_submissions, tokenize_code
from src.similarity import build_similarity_graph
from src.clustering import find_clusters
from src.greedy import select_representative, select_multiple_representatives
from src.bplus_tree import load_metadata

def run_plagiarism_detector(input_dir, metadata_file, output_file, threshold=0.5, cluster_method="bfs", k=7):
    """
    Run the plagiarism detector and output results.
    
    Args:
        input_dir: Directory containing submission files
        metadata_file: Path to the metadata JSON file
        output_file: Path to write the results
        threshold: Similarity threshold for creating edges in the graph (0.0 to 1.0)
        cluster_method: Method for finding clusters ("bfs" or "dfs")
        k: Length of token sequences to compare
    """
    print("Starting plagiarism detection...")
    start_time = time.time()
    
    # Step 1: Load submissions
    print(f"Loading submissions from {input_dir}...")
    submissions = load_submissions(input_dir)
    if not submissions:
        with open(output_file, 'w') as f:
            f.write("No valid submissions found.\n")
        print("No valid submissions found.")
        return
    print(f"Loaded {len(submissions)} submissions.")
    
    # Step 2: Load metadata
    print(f"Loading metadata from {metadata_file}...")
    metadata_tree = load_metadata(metadata_file)
    
    # Step 3: Build similarity graph
    print(f"Building similarity graph with threshold {threshold}...")
    graph = build_similarity_graph(submissions, threshold, k)
    
    # Step 4: Find clusters
    print(f"Finding clusters using {cluster_method}...")
    clusters = find_clusters(graph, method=cluster_method)
    
    # Calculate some statistics for the summary
    total_submissions = len(submissions)
    total_clusters = len(clusters)
    suspicious_clusters = sum(1 for cluster in clusters if len(cluster) > 1)
    isolated_submissions = sum(1 for cluster in clusters if len(cluster) == 1)
    largest_cluster_size = max([len(cluster) for cluster in clusters]) if clusters else 0
    
    # Count file types processed
    python_files = sum(1 for f in submissions if f.endswith('.py'))
    js_files = sum(1 for f in submissions if f.endswith('.js'))
    empty_files = sum(1 for f in submissions if submissions[f] == ["EMPTY_FILE"])
    
    # Calculate average similarity within suspicious clusters
    avg_similarities = []
    for cluster in clusters:
        if len(cluster) > 1:
            # Calculate average similarity in this cluster
            total_sim = 0
            count = 0
            for file1 in cluster:
                for file2 in cluster:
                    if file1 != file2:
                        sim = graph[file1].get(file2, 0)
                        total_sim += sim
                        count += 1
            if count > 0:
                avg_similarities.append(total_sim / count)
    
    avg_cluster_similarity = sum(avg_similarities) / len(avg_similarities) if avg_similarities else 0
    
    # Step 5: Generate output
    print(f"Writing results to {output_file}...")
    with open(output_file, 'w') as f:
        f.write("Plagiarism Detection Results\n")
        f.write("=" * 30 + "\n\n")
        
        if not clusters:
            f.write("No clusters found. Try lowering the similarity threshold.\n")
        else:
            f.write(f"Found {len(clusters)} cluster(s).\n\n")
            
            for i, cluster in enumerate(clusters, 1):
                # Select representative(s)
                if len(cluster) > 3:
                    representatives = select_multiple_representatives(cluster, graph, 2)
                    rep_str = ", ".join(representatives)
                else:
                    representative = select_representative(cluster, graph)
                    representatives = [representative]
                    rep_str = representative
                
                # Write cluster info
                f.write(f"Cluster {i}: {len(cluster)} files\n")
                f.write(f"Files: {', '.join(sorted(cluster))}\n")
                f.write(f"Representative(s): {rep_str}\n")
                
                # Write similarity info within cluster
                f.write("Similarity matrix:\n")
                for file1 in sorted(cluster):
                    f.write(f"  {file1}: ")
                    similarities = []
                    for file2 in sorted(cluster):
                        if file1 != file2:
                            sim = graph[file1].get(file2, 0)
                            similarities.append(f"{file2}={sim:.2f}")
                    f.write(", ".join(similarities) + "\n")
                
                # Write metadata for representatives
                f.write("Representative metadata:\n")
                for rep in representatives:
                    metadata = metadata_tree.search(rep)
                    f.write(f"  {rep}: {metadata}\n")
                
                f.write("\n" + "-" * 30 + "\n\n")
                
        # Write summary section
        f.write("Summary:\n")
        f.write("-" * 10 + "\n")
        f.write(f"- Total Submissions Processed: {total_submissions}\n")
        f.write(f"- Python Files: {python_files}\n")
        f.write(f"- JavaScript Files: {js_files}\n")
        f.write(f"- Empty Files: {empty_files}\n")
        f.write(f"- Total Clusters Found: {total_clusters}\n")
        f.write(f"- Suspicious Clusters (>1 submission): {suspicious_clusters}\n")
        f.write(f"- Isolated Submissions: {isolated_submissions}\n")
        f.write(f"- Largest Cluster Size: {largest_cluster_size}\n")
        f.write(f"- Average Similarity in Suspicious Clusters: {avg_cluster_similarity:.2f}\n")
        f.write(f"- Similarity Threshold: {threshold}\n")
        f.write(f"- K-gram Size: {k}\n")
        f.write(f"- Clustering Method: {cluster_method}\n")
        f.write(f"\nAnalysis completed in {time.time() - start_time:.2f} seconds.\n")
    
    end_time = time.time()
    print(f"Plagiarism detection completed in {end_time - start_time:.2f} seconds.")
    print(f"Results written to {output_file}")

def real_time_update(input_dir, metadata_file, output_file, new_submission, threshold=0.7):
    """
    Process a new submission in real-time and update the results.
    
    Args:
        input_dir: Directory containing existing submission files
        metadata_file: Path to the metadata JSON file
        output_file: Path to write the updated results
        new_submission: Path to the new submission file
        threshold: Similarity threshold
    """
    print(f"Processing new submission: {new_submission}")
    start_time = time.time()
    
    # Load existing submissions
    submissions = load_submissions(input_dir)
    
    # Process the new submission
    new_filename = os.path.basename(new_submission)
    try:
        # Use the tokenize_code function to process the file
        tokens = tokenize_code(new_submission)
        if tokens:
            submissions[new_filename] = tokens
            print(f"New submission '{new_filename}' tokenized successfully.")
        else:
            print(f"Error: Could not tokenize new submission '{new_filename}'.")
            return
    except Exception as e:
        print(f"Error processing new submission: {e}")
        return
    
    # Load metadata
    metadata_tree = load_metadata(metadata_file)
    
    # Update similarity graph
    k = 7  # Use the same k-gram size as in the original detection
    graph = build_similarity_graph(submissions, threshold, k)
    
    # Find updated clusters
    cluster_method = "bfs"  # Use the same method as in the original detection
    clusters = find_clusters(graph, method=cluster_method)
    
    # Calculate statistics for the summary
    total_submissions = len(submissions)
    total_clusters = len(clusters)
    suspicious_clusters = sum(1 for cluster in clusters if len(cluster) > 1)
    isolated_submissions = sum(1 for cluster in clusters if len(cluster) == 1)
    largest_cluster_size = max([len(cluster) for cluster in clusters]) if clusters else 0
    
    # Count file types processed
    python_files = sum(1 for f in submissions if f.endswith('.py'))
    js_files = sum(1 for f in submissions if f.endswith('.js'))
    empty_files = sum(1 for f in submissions if submissions[f] == ["EMPTY_FILE"])
    
    # Calculate average similarity within suspicious clusters
    avg_similarities = []
    for cluster in clusters:
        if len(cluster) > 1:
            # Calculate average similarity in this cluster
            total_sim = 0
            count = 0
            for file1 in cluster:
                for file2 in cluster:
                    if file1 != file2:
                        sim = graph[file1].get(file2, 0)
                        total_sim += sim
                        count += 1
            if count > 0:
                avg_similarities.append(total_sim / count)
    
    avg_cluster_similarity = sum(avg_similarities) / len(avg_similarities) if avg_similarities else 0
    
    # Find which cluster contains the new submission
    new_submission_cluster = None
    for cluster in clusters:
        if new_filename in cluster:
            new_submission_cluster = cluster
            break
    
    # Generate updated output
    with open(output_file, 'w') as f:
        f.write("Real-Time Plagiarism Detection Update\n")
        f.write("=" * 35 + "\n\n")
        
        f.write(f"New submission processed: {new_filename}\n\n")
        
        if not clusters:
            f.write("No clusters found after update. Try lowering the similarity threshold.\n")
        else:
            f.write(f"Updated clusters: {len(clusters)} cluster(s).\n\n")
            
            # First write the cluster containing the new submission (if any)
            if new_submission_cluster:
                f.write("Cluster containing new submission:\n")
                f.write("-" * 30 + "\n")
                i = clusters.index(new_submission_cluster) + 1
                
                # Select representative(s)
                if len(new_submission_cluster) > 3:
                    representatives = select_multiple_representatives(new_submission_cluster, graph, 2)
                    rep_str = ", ".join(representatives)
                else:
                    representative = select_representative(new_submission_cluster, graph)
                    representatives = [representative]
                    rep_str = representative
                
                # Write cluster info
                f.write(f"Cluster {i}: {len(new_submission_cluster)} files\n")
                f.write(f"Files: {', '.join(sorted(new_submission_cluster))}\n")
                f.write(f"Representative(s): {rep_str}\n")
                
                # Write similarity info within cluster
                f.write("Similarity matrix:\n")
                for file1 in sorted(new_submission_cluster):
                    f.write(f"  {file1}: ")
                    similarities = []
                    for file2 in sorted(new_submission_cluster):
                        if file1 != file2:
                            sim = graph[file1].get(file2, 0)
                            similarities.append(f"{file2}={sim:.2f}")
                    f.write(", ".join(similarities) + "\n")
                
                # Write metadata for representatives
                f.write("Representative metadata:\n")
                for rep in representatives:
                    metadata = metadata_tree.search(rep)
                    f.write(f"  {rep}: {metadata}\n")
                
                f.write("\n")
            
            f.write("All updated clusters:\n")
            f.write("-" * 20 + "\n")
            
            for i, cluster in enumerate(clusters, 1):
                # Skip detailed output for clusters not containing the new submission
                if cluster != new_submission_cluster:
                    f.write(f"Cluster {i}: {len(cluster)} files\n")
                    f.write(f"Files: {', '.join(sorted(cluster))}\n")
                    f.write("\n")
            
        # Write summary section
        f.write("Summary:\n")
        f.write("-" * 10 + "\n")
        f.write(f"- Total Submissions Processed: {total_submissions}\n")
        f.write(f"- Python Files: {python_files}\n")
        f.write(f"- JavaScript Files: {js_files}\n")
        f.write(f"- Empty Files: {empty_files}\n")
        f.write(f"- Total Clusters Found: {total_clusters}\n")
        f.write(f"- Suspicious Clusters (>1 submission): {suspicious_clusters}\n")
        f.write(f"- Isolated Submissions: {isolated_submissions}\n")
        f.write(f"- Largest Cluster Size: {largest_cluster_size}\n")
        f.write(f"- Average Similarity in Suspicious Clusters: {avg_cluster_similarity:.2f}\n")
        f.write(f"- Similarity Threshold: {threshold}\n")
        f.write(f"- K-gram Size: {k}\n")
        f.write(f"- Clustering Method: {cluster_method}\n")
        f.write(f"\nReal-time update completed in {time.time() - start_time:.2f} seconds.\n")
    
    end_time = time.time()
    print(f"Real-time update completed in {end_time - start_time:.2f} seconds.")
    print(f"Updated results written to {output_file}")

if __name__ == "__main__":
    # Parse command line arguments
    if len(sys.argv) > 1:
        input_dir = sys.argv[1]
    else:
        input_dir = "inputs"
    
    if len(sys.argv) > 2:
        threshold = float(sys.argv[2])
    else:
        threshold = 0.5
    
    metadata_file = os.path.join(input_dir, "metadata.json")
    output_file = "outputs/results.txt"
    
    # Run the plagiarism detector
    run_plagiarism_detector(input_dir, metadata_file, output_file, threshold)