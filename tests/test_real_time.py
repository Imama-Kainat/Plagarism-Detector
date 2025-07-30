import os
import sys

# Add the project root directory to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from src.main import real_time_update

def test_real_time_update():
    """Test real-time update with a new submission."""
    print("Running Real-Time Update Test...")
    
    # Create a test file file_z.py that is similar to file_a.py, file_b.py, file_c.py
    input_dir = "inputs"
    file_z_path = os.path.join(input_dir, "file_z.py")
    with open(file_z_path, 'w') as f:
        f.write("def sum_numbers(a, b):\n    return a + b\n")
    
    # Update metadata.json to include file_z.py
    metadata_file = os.path.join(input_dir, "metadata.json")
    with open(metadata_file, 'r') as f:
        content = f.read()
    
    # Add new entry for file_z.py if not already present
    if "file_z.py" not in content:
        updated_content = content[:-2] + ',\n    "file_z.py": {"student_id": "5001", "timestamp": "2025-01-06T03:00:00"}\n}'
        with open(metadata_file, 'w') as f:
            f.write(updated_content)
    
    # Run real-time update test
    output_file = "outputs/test_realtime.txt"
    real_time_update(input_dir, metadata_file, output_file, file_z_path, threshold=0.5)
    print(f"Check {output_file} for updated clusters. Expected: Z clusters with A, B, C.")

if __name__ == "__main__":
    test_real_time_update() 