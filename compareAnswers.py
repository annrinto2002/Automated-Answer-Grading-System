from sentence_transformers import SentenceTransformer, util

def compare_answers(answer_key, student_answer):
    # Load the pre-trained SBERT model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Encode the answers into embeddings
    embeddings = model.encode([answer_key, student_answer], convert_to_tensor=True)

    # Compute cosine similarity
    similarity = util.pytorch_cos_sim(embeddings[0], embeddings[1]).item()

    # Convert to percentage
    return round(similarity * 100, 2)

# # Example answers
# answer_key = "Python is a dynamically typed, interpreted programming language that supports multiple paradigms, including object-oriented, procedural, and functional programming. It features a large standard library, automatic memory management, and a strong ecosystem of third-party packages, making it ideal for applications ranging from scripting and automation to machine learning and scientific computing."

# student_answer = "Python is a high-level, interpreted programming language known for its simplicity, readability, and versatility. It is widely used in web development, data science, artificial intelligence, automation, and more."

# # Compute similarity
# similarity_percentage = compare_answers(answer_key, student_answer)
# print(f"Similarity: {similarity_percentage}%")
