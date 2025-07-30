# import os
# import sys

# # Add the project root directory to sys.path
# project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# sys.path.insert(0, project_root)

# from src.main import run_plagiarism_detector

# def test_basic_functionality():
#     """Test Basic Functionality with files A, B."""
#     print("Running Basic Functionality Test...")
#     input_dir = "inputs"
#     metadata_file = os.path.join(input_dir, "metadata.json")
#     output_file = "outputs/test_basic.txt"
#     run_plagiarism_detector(input_dir, metadata_file, output_file, threshold=0.5)
#      # Lowered threshold to 0.6
#     print(f"Check {output_file} for clusters and representatives.")

# def test_constraint_edge_cases():
#     """Placeholder for Constraint & Edge Case Test."""
#     print("Running Constraint & Edge Case Test...")
#     print("Add files E, F, G, H, I to inputs/ and update metadata.json, then rerun.")
#     # Implement additional test logic as needed

# if __name__ == "__main__":
#     test_basic_functionality()
#     test_constraint_edge_cases()

import os
import sys
import time
import shutil

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.main import run_plagiarism_detector, real_time_update

def generate_test_files():
    """Generate additional test files for scalability testing"""
    print("Generating additional test files for scalability testing...")
    inputs_dir = "inputs"
    
    # Create 50 additional files for scalability testing
    for i in range(1, 51):
        filename = f"file_{i}.py"
        file_path = os.path.join(inputs_dir, filename)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                f.write(f"def function_{i}(x):\n    return x + {i}\n")
    
    # Create test edge cases if they don't exist
    
    # 1. JavaScript file - should be included but in its own cluster
    js_file = os.path.join(inputs_dir, "file_h.js")
    if not os.path.exists(js_file):
        with open(js_file, 'w') as f:
            f.write("function add(a, b) {\n    return a + b;\n}\n\n// This is a JavaScript file\n")
    
    # 2. Empty Python file - should be included but in its own cluster
    empty_file = os.path.join(inputs_dir, "file_i.py")
    if not os.path.exists(empty_file):
        with open(empty_file, 'w') as f:
            f.write("")  # Empty file
    
    # Update metadata.json to include the new files
    metadata_path = os.path.join(inputs_dir, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, 'r') as f:
            content = f.read()
        
        # Add entries for special edge case files if they don't exist
        if "file_h.js" not in content:
            # Add js file metadata before the closing brace
            js_entry = ',\n    "file_h.js": {"student_id": "2004", "timestamp": "2025-01-02T10:45:00"}'
            if content.rstrip().endswith("}"):
                updated_content = content[:-1] + js_entry + "\n}"
                
                with open(metadata_path, 'w') as f:
                    f.write(updated_content)
                print(f"Updated metadata.json with entry for file_h.js")
                content = updated_content  # Update content for the next check
        
        if "file_i.py" not in content:
            # Add empty file metadata before the closing brace
            empty_entry = ',\n    "file_i.py": {"student_id": "2005", "timestamp": "2025-01-02T11:00:00"}'
            if content.rstrip().endswith("}"):
                updated_content = content[:-1] + empty_entry + "\n}"
                
                with open(metadata_path, 'w') as f:
                    f.write(updated_content)
                print(f"Updated metadata.json with entry for file_i.py")
                content = updated_content  # Update content for the next check
        
        # Check if we need to update the metadata for regular files
        if "file_1.py" not in content:
            # Add new entries before the closing brace
            new_entries = ""
            for i in range(1, 51):
                new_entries += f',\n    "file_{i}.py": {{"student_id": "{4000+i}", "timestamp": "2025-01-04T{i:02d}:00:00"}}'
            
            # Insert the new entries before the last closing brace
            updated_content = content[:-1] + new_entries + "\n}"
            
            with open(metadata_path, 'w') as f:
                f.write(updated_content)
            
            print(f"Updated metadata.json with entries for file_1.py to file_50.py")
    
    print(f"Generated test files including special edge cases.")

def test_basic_functionality():
    """Test Basic Functionality with files A, B, C, D."""
    print("Running Basic Functionality Test...")
    start_time = time.time()
    input_dir = "inputs"
    metadata_file = os.path.join(input_dir, "metadata.json")
    output_file = "outputs/test_basic.txt"
    run_plagiarism_detector(input_dir, metadata_file, output_file, threshold=0.7, cluster_method="bfs", k=7)
    end_time = time.time()
    print(f"Test completed in {end_time-start_time:.2f} seconds.")
    print(f"Check {output_file} for clusters and representatives. Expected: A, B, C clustered together; D separate.")

def test_constraint_edge_cases():
    """Test Constraint & Edge Case with files E, F, G, H, I."""
    print("Running Constraint & Edge Case Test...")
    start_time = time.time()
    input_dir = "inputs"
    metadata_file = os.path.join(input_dir, "metadata.json")
    output_file = "outputs/test_constraint.txt"
    run_plagiarism_detector(input_dir, metadata_file, output_file, threshold=0.6, cluster_method="bfs", k=7)
    end_time = time.time()
    print(f"Test completed in {end_time-start_time:.2f} seconds.")
    print(f"Check {output_file} for clusters. Expected: E, F clustered; G may cluster with E/F;")
    print(f"Special edge cases: file_h.js should be isolated; file_i.py (empty) should be isolated.")
    print(f"Also testing B+ Tree efficiency with 75+ files (original + generated).")

def test_algorithm_integration():
    """Test Algorithm Integration with files A to Y and generated files."""
    print("Running Algorithm Integration & Complexity Test...")
    start_time = time.time()
    input_dir = "inputs"
    metadata_file = os.path.join(input_dir, "metadata.json")
    output_file = "outputs/test_integration.txt"
    run_plagiarism_detector(input_dir, metadata_file, output_file, threshold=0.5, cluster_method="bfs", k=7)
    end_time = time.time()
    print(f"Test completed in {end_time-start_time:.2f} seconds.")
    print(f"Check {output_file} for clusters. Expected: J, K, L clustered; M, N clustered; W, X, Y clustered;")
    print(f"Using k=7 should prevent over-clustering of short files (Q, R, S, T, U).")
    print(f"Special edge cases: file_h.js and file_i.py should remain isolated.")

def test_real_time_update():
    """Test real-time update with a new submission."""
    print("Running Real-Time Update Test...")
    start_time = time.time()
    
    # Create a test file file_z.py that is similar to file_a.py, file_b.py, file_c.py
    input_dir = "inputs"
    file_z_path = os.path.join(input_dir, "file_z.py")
    with open(file_z_path, 'w') as f:
        f.write("def sum_numbers(a, b):\n    return a + b\n")
    
    # Create a copy of file_a.py to ensure high similarity
    file_a_path = os.path.join(input_dir, "file_a.py")
    if os.path.exists(file_a_path):
        with open(file_a_path, 'r') as src:
            content = src.read()
        with open(file_z_path, 'w') as dst:
            dst.write(content)
    
    # Update metadata.json to include file_z.py
    metadata_file = os.path.join(input_dir, "metadata.json")
    with open(metadata_file, 'r') as f:
        content = f.read()
    
    # Add new entry for file_z.py if not already present
    if "file_z.py" not in content:
        updated_content = content[:-1] + ',\n    "file_z.py": {"student_id": "5001", "timestamp": "2025-01-06T03:00:00"}\n}'
        with open(metadata_file, 'w') as f:
            f.write(updated_content)
    
    # Run real-time update test
    output_file = "outputs/test_realtime.txt"
    real_time_update(input_dir, metadata_file, output_file, file_z_path, threshold=0.7)
    end_time = time.time()
    print(f"Test completed in {end_time-start_time:.2f} seconds.")
    print(f"Check {output_file} for updated clusters. Expected: Z clusters with A, B, C.")

def test_threshold_sensitivity():
    """Test sensitivity to different similarity thresholds."""
    print("Running Threshold Sensitivity Test...")
    input_dir = "inputs"
    metadata_file = os.path.join(input_dir, "metadata.json")
    
    thresholds = [0.9, 0.7, 0.5, 0.3]
    
    for threshold in thresholds:
        output_file = f"outputs/test_threshold_{int(threshold*10)}.txt"
        print(f"Testing with threshold {threshold}...")
        start_time = time.time()
        run_plagiarism_detector(input_dir, metadata_file, output_file, threshold=threshold, cluster_method="bfs", k=7)
        end_time = time.time()
        print(f"Threshold {threshold} test completed in {end_time-start_time:.2f} seconds.")
    
    print("Threshold sensitivity tests completed. Check outputs/test_threshold_*.txt files.")

if __name__ == "__main__":
    # Generate test files for scalability testing
    generate_test_files()
    
    # Run tests
    test_basic_functionality()
    test_constraint_edge_cases()
    test_algorithm_integration()
    test_real_time_update()
    test_threshold_sensitivity()