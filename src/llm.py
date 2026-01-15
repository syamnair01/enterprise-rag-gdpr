"""
Grounded LLM interaction layer.

"""

from ibm_watsonx_ai.foundation_models import Model

def generate_answer(context, question):
    prompt = f"""
You are an enterprise knowledge assistant.

Answer the question using ONLY the context below.
If the answer is not present, respond with:
"Insufficient context to answer this question."

Context:
{context}

Question:
{question}
"""

    model = Model(
        model_id="ibm/granite-13b-chat-v2",
        params={
            "max_new_tokens": 300,
            "temperature": 0.2
        }
    )

    return model.generate_text(prompt)
