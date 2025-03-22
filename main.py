from src.preprocessing.text_preprocessing import cluster_preprocess
from src.clustering.cluster_search import find_cluster
from src.clustering.compare import compare_texts
from src.text_example.load_example_Notre_dame_wikipedia import load_text_a, load_text_b, example_parameters

def main():
    # Beispieltexte laden
    text_a = load_text_a()
    text_b = load_text_b()
    
    # Parameter laden
    sep, replace_chars, text_a_name, text_b_name = example_parameters()
    
    # Texte vorverarbeiten
    a_processed = cluster_preprocess(text_a, sep, replace_chars)
    b_processed = cluster_preprocess(text_b, sep, replace_chars)
    
    # Cluster finden
    clusters = find_cluster(a_processed, b_processed, min_length=10, a_name=text_a_name, b_name=text_b_name)
    
    # Vergleich erstellen
    comparison = compare_texts(a_processed, b_processed, clusters, text_a_name, text_b_name)
    
    return clusters, comparison

if __name__ == "__main__":
    clusters, comparison = main()
    print(f"Gefundene Cluster: {len(clusters)}")
    #564