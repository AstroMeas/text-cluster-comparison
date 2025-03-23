import pandas as pd
import logging
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def filter_ordered_clusters(cluster_df, text_a_name='a', text_b_name='b'):
    """
    Filters clusters to keep only those that maintain a consistent order in both texts.
    
    This function ensures that as cluster positions increase in text A, they also increase
    in text B, which is required for a meaningful linguistic comparison.
    
    Args:
        cluster_df (pandas.DataFrame): DataFrame containing cluster information
        text_a_name (str): Name of the first text/sequence
        text_b_name (str): Name of the second text/sequence
        
    Returns:
        pandas.DataFrame: Filtered DataFrame with only consistently ordered clusters
    """
    if len(cluster_df) <= 1:
        return cluster_df
    
    # Sort clusters by their position in text A
    sorted_clusters = cluster_df.sort_values(by=f'start_{text_a_name}').copy()
    
    # Calculate if the ordering is consistent in text B
    b_positions = sorted_clusters[f'start_{text_b_name}'].values
    is_ordered = np.all(np.diff(b_positions) >= 0)
    
    if is_ordered:
        logger.info("All clusters are in consistent order in both texts")
        return sorted_clusters
    
    # If not ordered, we need to filter out problematic clusters
    logger.warning("Found clusters with inconsistent ordering between texts")
    
    # We'll use a greedy approach to find the largest subset of ordered clusters
    
    # Initialize with first cluster
    valid_indices = [0]
    last_b_pos = b_positions[0]
    
    # Greedily add clusters that maintain ordering
    for i in range(1, len(b_positions)):
        if b_positions[i] >= last_b_pos:
            valid_indices.append(i)
            last_b_pos = b_positions[i]
        else:
            logger.warning(f"Dropping out-of-order cluster at position {sorted_clusters.iloc[i][f'start_{text_a_name}']} "
                          f"in text A and {b_positions[i]} in text B")
    
    logger.info(f"Keeping {len(valid_indices)} of {len(cluster_df)} clusters that maintain ordering")
    
    return sorted_clusters.iloc[valid_indices].reset_index(drop=True)


def compare_texts(a, b, cluster_df=None, text_a_name='a', text_b_name='b', separator=' ', enforce_order=True):
    """
    Compares two sequences and organizes their similarities and unique elements into a structured DataFrame.

    This function takes two sequences (`a` and `b`), a DataFrame of clusters, and optional text names, 
    then generates a DataFrame detailing both unique elements and clustered matches between the sequences.

    Args:
        a (list): The first sequence to compare.
        b (list): The second sequence to compare.
        cluster_df (pandas.DataFrame, optional): A DataFrame containing cluster information. Defaults to None.
            Expected columns:
            - f'start_{text_a_name}', f'end_{text_a_name}', f'start_{text_b_name}', f'end_{text_b_name}', 'length'.
        text_a_name (str, optional): The name of the first sequence for labeling. Defaults to 'a'.
        text_b_name (str, optional): The name of the second sequence for labeling. Defaults to 'b'.
        separator (str, optional): Character used to join sequence elements in output. Defaults to '་'.
        enforce_order (bool, optional): Whether to enforce consistent ordering of clusters. Defaults to True.

    Returns:
        pandas.DataFrame: A DataFrame with the following columns:
            - 'tag': Indicates whether the entry is 'unique' or part of a 'cluster'.
            - f'Pos_{text_a_name}': Start position in `a`.
            - f'Length_{text_a_name}': Length of the segment in `a`.
            - f'{text_a_name}': Content of the segment in `a`.
            - f'Pos_{text_b_name}': Start position in `b`.
            - f'Length_{text_b_name}': Length of the segment in `b`.
            - f'{text_b_name}': Content of the segment in `b`.
            - 'Length_Cluster': Length of the cluster (0 for unique segments).
            - 'Cluster': Content of the matching cluster (empty for unique segments).

    Raises:
        ValueError: If the `cluster_df` does not contain the required columns.
        TypeError: If input sequences are not lists or cluster_df is not a DataFrame.

    Example:
        a = ["word1", "word2", "word3", "word4"]
        b = ["wordA", "wordB", "word3", "word4"]
        cluster_df = pd.DataFrame({
            "start_a": [2],
            "end_a": [4],
            "start_b": [2],
            "end_b": [4],
            "length": [2],
        })
        result = compare_texts(a, b, cluster_df, text_a_name="a", text_b_name="b")
        print(result)
        # Output: A DataFrame with rows for unique and cluster segments.
    """
    # Input validation
    if not isinstance(a, list) or not isinstance(b, list):
        raise TypeError("Input sequences 'a' and 'b' must be lists")
    
    if cluster_df is None:
        logger.info("No cluster information provided, returning empty DataFrame")
        return pd.DataFrame()
    
    if not isinstance(cluster_df, pd.DataFrame):
        raise TypeError("cluster_df must be a pandas DataFrame")
    
    if len(cluster_df) == 0:
        logger.info("Empty cluster DataFrame provided, returning empty DataFrame")
        return pd.DataFrame()
    
    # Define required column names based on text names
    required_columns = [
        f'start_{text_a_name}', f'end_{text_a_name}', 
        f'start_{text_b_name}', f'end_{text_b_name}', 
        'length'
    ]
    
    # Check if all required columns exist in the DataFrame
    if not all(column in cluster_df.columns for column in required_columns):
        missing = [col for col in required_columns if col not in cluster_df.columns]
        raise ValueError(f"cluster_df must contain columns {required_columns}. Missing: {missing}")
    
    # Filter clusters to ensure consistent ordering if requested
    if enforce_order:
        cluster_df = filter_ordered_clusters(cluster_df, text_a_name, text_b_name)
        
        if len(cluster_df) == 0:
            logger.warning("No consistently ordered clusters found, returning empty DataFrame")
            return pd.DataFrame()
    
    # Prepare output dictionary
    result_data = {
        'tag': [], 
        f'Pos_{text_a_name}': [], 
        f'Length_{text_a_name}': [], 
        f'{text_a_name}': [],
        f'Pos_{text_b_name}': [], 
        f'Length_{text_b_name}': [], 
        f'{text_b_name}': [],
        'Length_Cluster': [], 
        'Cluster': []
    }
    
    if enforce_order:
        # For ordered processing, we use a sequential approach with start positions
        # Sort clusters by start position in text A
        sorted_clusters = cluster_df.sort_values(by=f'start_{text_a_name}')
        
        # Initialize start positions
        a_start = 0
        b_start = 0
        
        # Process each cluster in order
        for _, cluster_row in sorted_clusters.iterrows():
            # Extract cluster positions
            start_a = int(cluster_row[f'start_{text_a_name}'])
            end_a = int(cluster_row[f'end_{text_a_name}'])
            start_b = int(cluster_row[f'start_{text_b_name}'])
            end_b = int(cluster_row[f'end_{text_b_name}'])
            length = int(cluster_row['length'])
            
            # Validate positions
            if start_a < a_start or start_b < b_start:
                logger.warning(f"Skipping cluster with invalid positions: a_start={a_start}, start_a={start_a}, "
                              f"b_start={b_start}, start_b={start_b}")
                continue
            
            # Add unique elements before this cluster
            if start_a > a_start or start_b > b_start:
                result_data['tag'].append('unique')
                result_data[f'Pos_{text_a_name}'].append(a_start)
                result_data[f'Pos_{text_b_name}'].append(b_start)
                result_data[f'Length_{text_a_name}'].append(start_a - a_start)
                result_data[f'Length_{text_b_name}'].append(start_b - b_start)
                
                # Safe indexing for content
                a_segment = a[a_start:start_a] if a_start < len(a) else []
                b_segment = b[b_start:start_b] if b_start < len(b) else []
                
                result_data[f'{text_a_name}'].append(separator.join(a_segment))
                result_data[f'{text_b_name}'].append(separator.join(b_segment))
                result_data['Length_Cluster'].append(0)
                result_data['Cluster'].append('')
            
            # Add cluster
            result_data['tag'].append('cluster')
            result_data[f'Pos_{text_a_name}'].append(start_a)
            result_data[f'Pos_{text_b_name}'].append(start_b)
            result_data[f'Length_{text_a_name}'].append(0)
            result_data[f'Length_{text_b_name}'].append(0)
            result_data[f'{text_a_name}'].append('')
            result_data[f'{text_b_name}'].append('')
            result_data['Length_Cluster'].append(length)
            
            # Safe indexing for cluster content
            a_cluster = a[start_a:end_a] if start_a < len(a) and end_a <= len(a) else []
            result_data['Cluster'].append(separator.join(a_cluster))
            
            # Update start positions for next iteration
            a_start = end_a
            b_start = end_b
        
        # Add any remaining unique elements after the last cluster
        if a_start < len(a) or b_start < len(b):
            result_data['tag'].append('unique')
            result_data[f'Pos_{text_a_name}'].append(a_start)
            result_data[f'Pos_{text_b_name}'].append(b_start)
            result_data[f'Length_{text_a_name}'].append(len(a) - a_start)
            result_data[f'Length_{text_b_name}'].append(len(b) - b_start)
            
            # Safe indexing for content
            a_segment = a[a_start:] if a_start < len(a) else []
            b_segment = b[b_start:] if b_start < len(b) else []
            
            result_data[f'{text_a_name}'].append(separator.join(a_segment))
            result_data[f'{text_b_name}'].append(separator.join(b_segment))
            result_data['Length_Cluster'].append(0)
            result_data['Cluster'].append('')
    else:
        # For unordered processing, we handle each cluster individually without maintaining global positions
        # This allows out-of-order clusters but produces a less coherent reading experience
        
        # Sort clusters by start position in text A just for processing order
        sorted_clusters = cluster_df.sort_values(by=f'start_{text_a_name}')
        
        # Process each cluster independently
        for i, (_, cluster_row) in enumerate(sorted_clusters.iterrows()):
            # Extract cluster positions
            start_a = int(cluster_row[f'start_{text_a_name}'])
            end_a = int(cluster_row[f'end_{text_a_name}'])
            start_b = int(cluster_row[f'start_{text_b_name}'])
            end_b = int(cluster_row[f'end_{text_b_name}'])
            length = int(cluster_row['length'])
            
            # Add unique elements before this cluster (if this is the first cluster)
            if i == 0 and (start_a > 0 or start_b > 0):
                result_data['tag'].append('unique')
                result_data[f'Pos_{text_a_name}'].append(0)
                result_data[f'Pos_{text_b_name}'].append(0)
                result_data[f'Length_{text_a_name}'].append(start_a)
                result_data[f'Length_{text_b_name}'].append(start_b)
                
                # Safe indexing for content
                a_segment = a[:start_a] if start_a <= len(a) else []
                b_segment = b[:start_b] if start_b <= len(b) else []
                
                result_data[f'{text_a_name}'].append(separator.join(a_segment))
                result_data[f'{text_b_name}'].append(separator.join(b_segment))
                result_data['Length_Cluster'].append(0)
                result_data['Cluster'].append('')
            
            # Add cluster
            result_data['tag'].append('cluster')
            result_data[f'Pos_{text_a_name}'].append(start_a)
            result_data[f'Pos_{text_b_name}'].append(start_b)
            result_data[f'Length_{text_a_name}'].append(0)
            result_data[f'Length_{text_b_name}'].append(0)
            result_data[f'{text_a_name}'].append('')
            result_data[f'{text_b_name}'].append('')
            result_data['Length_Cluster'].append(length)
            
            # Safe indexing for cluster content
            a_cluster = a[start_a:end_a] if start_a < len(a) and end_a <= len(a) else []
            result_data['Cluster'].append(separator.join(a_cluster))
            
            # If this is the last cluster, add unique elements after it
            if i == len(sorted_clusters) - 1:
                remaining_a = a[end_a:] if end_a < len(a) else []
                remaining_b = b[end_b:] if end_b < len(b) else []
                
                if remaining_a or remaining_b:
                    result_data['tag'].append('unique')
                    result_data[f'Pos_{text_a_name}'].append(end_a)
                    result_data[f'Pos_{text_b_name}'].append(end_b)
                    result_data[f'Length_{text_a_name}'].append(len(a) - end_a)
                    result_data[f'Length_{text_b_name}'].append(len(b) - end_b)
                    result_data[f'{text_a_name}'].append(separator.join(remaining_a))
                    result_data[f'{text_b_name}'].append(separator.join(remaining_b))
                    result_data['Length_Cluster'].append(0)
                    result_data['Cluster'].append('')
    
    logger.info(f"Created comparison with {len(result_data['tag'])} segments")
    
    # Convert to DataFrame
    return pd.DataFrame(result_data)


if __name__ == "__main__":
    # Example usage
    a_seq = ["word1", "word2", "word3", "word4", "word5", "word6"]
    b_seq = ["other1", "word3", "word4", "other2", "word1", "word2"]
    
    # Example cluster DataFrame with out-of-order clusters
    cluster_data = {
        "start_a": [0, 2],       # word1-word2 and word3-word4
        "end_a": [2, 4],
        "start_b": [4, 1],       # Notice that word1-word2 appears AFTER word3-word4 in text B
        "end_b": [6, 3],
        "length": [2, 2],
        "differenz": [4, -1]
    }
    
    cluster_df = pd.DataFrame(cluster_data)
    
    print("\nInput sequences:")
    print(f"a: {a_seq}")
    print(f"b: {b_seq}")
    print("\nClusters before filtering:")
    print(cluster_df)
    
    # Compare sequences with order enforcement
    result_ordered = compare_texts(a_seq, b_seq, cluster_df, text_a_name="a", text_b_name="b")
    
    print("\nComparison result (with order enforcement):")
    print(result_ordered)
    
    # Compare sequences without order enforcement
    result_unordered = compare_texts(a_seq, b_seq, cluster_df, text_a_name="a", text_b_name="b", enforce_order=False)
    
    print("\nComparison result (without order enforcement):")
    print(result_unordered)