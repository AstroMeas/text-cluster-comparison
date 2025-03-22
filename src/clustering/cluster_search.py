from src.clustering.cluster import Cluster
import src.text_example.load_example_Notre_dame_wikipedia as load_example
from src.preprocessing.text_preprocessing import cluster_preprocess
import pandas as pd
import numpy as np
import logging
from numba import njit

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def hash_strings(words, hash_mod=2**30-1):
    """
    Converts a list of strings to integer values with optimized hashing.
    
    Args:
        words (list): List of strings to hash
        hash_mod (int, optional): Modulus for hash values to prevent collisions.
                                  Defaults to 2^30-1 (a large prime)
    
    Returns:
        numpy.ndarray: Array of hash values
        
    Raises:
        TypeError: If words is not a list or contains non-string elements
    """
    if not isinstance(words, list):
        raise TypeError("Input must be a list of strings")
    
    if not all(isinstance(word, str) for word in words):
        raise TypeError("All elements in the list must be strings")
    
    # More efficient array creation with pre-allocation and defined data type
    result = np.zeros(len(words), dtype=np.int32)
    
    for i, word in enumerate(words):
        # Use a consistent hash algorithm with fewer collisions
        # XOR the hash with its shifted value to distribute bits better
        h = abs(hash(word))
        h = (h ^ (h >> 16)) % hash_mod
        result[i] = h
    
    logger.debug(f"Hashed {len(words)} strings")
    return result


@njit
def cluster_search(a, b, min_length):
    """
    Core algorithm to find matching clusters between two sequences using Numba acceleration.
    
    This function identifies matching subsequences between two arrays of hashed values.
    It implements an efficient skipping mechanism to avoid redundant comparisons.
    
    Args:
        a (numpy.ndarray): First sequence of hashed values
        b (numpy.ndarray): Second sequence of hashed values
        min_length (int): Minimum length for a cluster to be considered valid
        
    Returns:
        tuple: (clusters_array, cluster_count)
            - clusters_array: Array of [start_a, start_b, length] for each cluster
            - cluster_count: Number of clusters found
    """
    len_a = len(a)
    len_b = len(b)
    skips = 0
    
    # Estimate maximum possible number of clusters
    max_possible_clusters = min(len_a, len_b) // min_length + 1
    clusters = np.zeros((max_possible_clusters, 3), dtype=np.int32)
    clus_pos = 0 # position in array of clusters, not in the sequence

    # Main loop: iterate through first sequence
    for i in range(len_a):
        # Skip positions that are part of previous clusters
        if skips > 0:
            skips -= 1
            continue
        
        # Inner loop: compare with each position in second sequence
        for j in range(len_b):
            # Check if current elements match
            if a[i] == b[j]:
                # Initialize pointers and counter for extending the match
                h = i
                k = j
                length = 1  
                
                # Extend the match as far as possible
                while h + 1 < len_a and k + 1 < len_b and a[h + 1] == b[k + 1]:
                    h += 1
                    k += 1
                    length += 1
                
                # If match meets minimum length requirement, record it
                if length >= min_length:
                    clusters[clus_pos, 0] = i      # Start position in text A
                    clusters[clus_pos, 1] = j      # Start position in text B
                    clusters[clus_pos, 2] = length # Cluster length
                    clus_pos += 1
                    
                    # Update skip count to avoid redundant processing
                    skips = length - 1

    # Return only the valid clusters (up to clus_pos)
    return clusters[:clus_pos], clus_pos


def find_cluster(a_seq, b_seq, min_length=10, a_name='text_a', b_name='text_b'):
    """
    Finds clusters of similar sequences in two lists of strings.
    
    This function orchestrates the cluster finding process:
    1. Converts string sequences to hash values
    2. Identifies clusters using the cluster_search algorithm
    3. Organizes clusters into a structured DataFrame
    
    Args:
        a_seq (list): First sequence of strings
        b_seq (list): Second sequence of strings
        min_length (int, optional): Minimum length for a cluster. Defaults to 10.
        a_name (str, optional): Name for the first sequence. Defaults to 'text_a'.
        b_name (str, optional): Name for the second sequence. Defaults to 'text_b'.
    
    Returns:
        pandas.DataFrame: DataFrame containing cluster information with positions and lengths
        
    Raises:
        ValueError: If sequences are empty or min_length is less than 1
        TypeError: If sequences are not lists of strings
    """
    # Input validation
    if not isinstance(a_seq, list) or not isinstance(b_seq, list):
        raise TypeError("Input sequences must be lists")
    
    if len(a_seq) == 0 or len(b_seq) == 0:
        logger.warning("One or both input sequences are empty")
        columns = [f'start_{a_name}', f'end_{a_name}', 
                  f'start_{b_name}', f'end_{b_name}', 'length', 'differenz']
        return pd.DataFrame(columns=columns)
    
    if min_length < 1:
        raise ValueError("min_length must be at least 1")
    
    logger.info(f"Length of sequences: {len(a_seq)} and {len(b_seq)} items")
    logger.info(f"Using minimum cluster length: {min_length}")
    
    try:
        # Hash the sequences for faster comparison
        a = hash_strings(a_seq)
        b = hash_strings(b_seq)
        
        # Find all potential clusters
        clusters, cluster_pos = cluster_search(a, b, min_length)
        
        # Handle case with no clusters found
        if cluster_pos == 0:
            logger.info("No clusters found that meet the minimum length requirement")
            columns = [f'start_{a_name}', f'end_{a_name}', 
                      f'start_{b_name}', f'end_{b_name}', 'length', 'differenz']
            return pd.DataFrame(columns=columns)
        
        # Process clusters into organized data structure
        cluster_lst = []
        last_cluster = -1
        
        # Create Cluster objects for each unique starting position
        for clus in clusters:
            # Finalize the previous cluster if moving to a new position
            if clus[0] > last_cluster and last_cluster != -1:
                cluster_lst[-1].pick_finalcluster()
            
            # Start a new cluster if at a new position
            if clus[0] > last_cluster:
                cluster_lst.append(Cluster(clus[0], a_name, b_name))
                last_cluster = clus[0]
            
            # Add this match to the current cluster
            cluster_lst[-1].append_cluster(clus[1], clus[2])
        
        # Finalize the last cluster
        if cluster_lst:
            cluster_lst[-1].pick_finalcluster()
        else:
            # Safety check - should not happen if cluster_pos > 0
            logger.warning("No clusters were created despite finding matches")
            columns = [f'start_{a_name}', f'end_{a_name}', 
                      f'start_{b_name}', f'end_{b_name}', 'length', 'differenz']
            return pd.DataFrame(columns=columns)
        
        # Prepare data for DataFrame
        cluster_dict = {}
        
        # Initialize dictionary with column names
        for j in range(5):
            cluster_dict[cluster_lst[0].clus_tupel_naming[j]] = []
        
        # Fill in the data
        for i in cluster_lst:
            for j in range(5):
                cluster_dict[i.clus_tupel_naming[j]].append(i.final_cluster[j])
        
        # Create DataFrame and add difference column
        data_df = pd.DataFrame(cluster_dict)
        data_df['differenz'] = data_df[f'start_{b_name}'] - data_df[f'start_{a_name}']
        
        logger.info(f"Found {len(data_df)} clusters")
        return data_df
        
    except Exception as e:
        logger.error(f"Error during cluster finding: {str(e)}")
        raise


if __name__ == "__main__":
    try:
        a = load_example.load_text_a()
        b = load_example.load_text_b()
        sep, repl, _, _ = load_example.example_parameters()

        a = cluster_preprocess(a, sep, repl)
        b = cluster_preprocess(b, sep, repl)
        
        result = find_cluster(a, b, 10)
        print(f"Found {len(result)} clusters")
        
    except Exception as e:
        logger.error(f"Error in main execution: {str(e)}")