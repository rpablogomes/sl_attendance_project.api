import json
import time
from .embedding.generate_embbeding import Embedding
from .config.pinecone_ import PineconeClient
from .data import data

def main(symptom):
    if symptom == "__init_db__":
        
        texts_for_embedding = []
        metadata_list = []
        
        for item in data:
            texts_for_embedding.append(item["text"])
            metadata_list.append({
                "input": item["input"],
                "output": json.dumps(item["output"]),
                "text": item["text"]
            })
        
        embedding = Embedding()
        embeddings = embedding.get_embedding(texts_for_embedding)
        
        pc = PineconeClient()
        
        index = pc.pinecone.Index(pc.index_name)
        index.delete(delete_all=True)
        
        time.sleep(2)
        
        formatted_vectors = []
        for i, (emb, meta) in enumerate(zip(embeddings, metadata_list)):
            normalized_emb = pc.normalize_embedding(emb)
            formatted_vectors.append({
                "id": str(i + 1),
                "values": normalized_emb.tolist(),
                "metadata": meta
            })
        
        index.upsert(vectors=formatted_vectors)
        
        # wait for indexation
        time.sleep(5)
        
        stats = index.describe_index_stats()
        
        return {"status": "Database initialized successfully"}
    
    embedding = embedding()
    pc = PineconeClient()
    
    query_text = symptom
    query_embedding = embedding.get_embedding([query_text])[0]
    
    index = pc.pinecone.Index(pc.index_name)
    
    stats = index.describe_index_stats()
    
    search_results = index.query(
        vector=query_embedding.tolist(),
        top_k=7,
        include_metadata=True
    )
    
    results_list = []
    if hasattr(search_results, 'matches'):
        results_list = search_results.matches
    elif isinstance(search_results, dict) and 'matches' in search_results:
        results_list = search_results['matches']
    
    

        try:
            if metadata.get('output'):
                output_list = json.loads(metadata['output'])
                print(f"  Output (parsed): {output_list}")
        except json.JSONDecodeError:
            print("Error JSON")
        print()
    
    exact_match_found = False
    closest_match = None
    synonyms = []
    
    for result in results_list:
        metadata = result.get('metadata', {})
        if isinstance(metadata, dict) and "input" in metadata:
            if symptom.lower() == metadata["input"].lower():
                try:
                    synonyms = json.loads(metadata["output"])
                    print(f"Sinônimos encontrados: {synonyms}")
                except json.JSONDecodeError:
                    print("Erro ao converter sinônimos de JSON")
                    synonyms = []
                exact_match_found = True
                break
            elif closest_match is None or result.get("score", 0) > closest_match.get("score", 0):
                closest_match = result
    
    if not exact_match_found:
        if closest_match and "metadata" in closest_match:
            closest_metadata = closest_match.get("metadata", {})
            if "output" in closest_metadata:
                try:
                    synonyms = json.loads(closest_metadata["output"])
                    closest_term = closest_metadata.get("input", "")
                except json.JSONDecodeError:
                    synonyms = []
            
    
    if exact_match_found:
        result = f"Term: {symptom}. Synonyms: {', '.join(synonyms)}"
    elif closest_match and len(synonyms) > 0:
        closest_term = closest_match.get("metadata", {}).get("input", "Unknown")
        result = f"Closest term found: {closest_term}. Synonyms: {', '.join(synonyms)}"
    else:
        result = "I did not find synonyms for this term in the database."
    
    
    return {
        "symptom": symptom,
        "synonyms": result,
        "exact_match": exact_match_found
    }


if __name__ == "__main__":

    main("__init_db__")
    
    time.sleep(5)
    

    symptons = "Allergic Esophagitis"
    output = main(symptons)
