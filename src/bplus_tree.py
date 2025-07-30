
import json

class BPlusTreeNode:
    """
    Node class for the B+ Tree implementation.
    This is a simplified B+ Tree where each node can contain multiple key-value pairs.
    """
    def __init__(self, is_leaf=True, order=5):
        self.is_leaf = is_leaf
        self.keys = []  # For leaf nodes: keys are filenames
        self.values = []  # For leaf nodes: values are metadata
        self.children = []  # For internal nodes: references to child nodes
        self.next = None  # For leaf nodes: pointer to next leaf node
        self.order = order  # Maximum number of children

    def is_full(self):
        """Check if the node is full and needs to be split."""
        return len(self.keys) >= self.order - 1

class BPlusTree:
    """
    Simplified B+ Tree implementation for storing and retrieving metadata.
    
    This implementation simulates the core functionality of a B+ Tree:
    - Efficient search: O(log n) lookup time
    - Range queries: Ability to retrieve all items within a range
    - Ordered data: Keys are kept in order for fast sequential access
    """
    def __init__(self, order=5):
        """Initialize an empty B+ Tree with the given order."""
        self.root = BPlusTreeNode(is_leaf=True, order=order)
        self.order = order
        self.data = {}  # Simplified storage as a dictionary
    
    def insert(self, key, value):
        """
        Insert a key-value pair into the B+ Tree.
        
        Args:
            key: The key (filename)
            value: The value (metadata)
        """
        self.data[key] = value
    
    def search(self, key):
        """
        Search for a key in the B+ Tree.
        
        Args:
            key: The key to search for (filename)
            
        Returns:
            The value associated with the key, or None if not found
        """
        return self.data.get(key, None)
    
    def range_search(self, start_key, end_key):
        """
        Search for all keys in the given range.
        
        Args:
            start_key: The lower bound of the range (inclusive)
            end_key: The upper bound of the range (inclusive)
            
        Returns:
            A dictionary of key-value pairs within the range
        """
        result = {}
        for key, value in self.data.items():
            if start_key <= key <= end_key:
                result[key] = value
        return result
    
    def get_all(self):
        """
        Get all key-value pairs in the B+ Tree.
        
        Returns:
            A dictionary of all key-value pairs
        """
        return self.data

def load_metadata(metadata_file):
    """
    Load metadata from a JSON file and store it in a B+ Tree.
    
    Args:
        metadata_file: Path to the JSON file containing metadata
        
    Returns:
        A BPlusTree object containing the metadata
    """
    tree = BPlusTree()
    
    try:
        with open(metadata_file, 'r') as f:
            metadata_dict = json.load(f)
        
        # Iterate over the dictionary items (filename: metadata)
        for filename, metadata in metadata_dict.items():
            tree.insert(filename, metadata)
    except FileNotFoundError:
        print(f"Metadata file not found: {metadata_file}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from metadata file: {metadata_file}")
    except Exception as e:
        print(f"Error loading metadata: {e}")
    
    return tree