import pandas as pd
import gradio as gr
import numpy as np
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db_books = Chroma(persist_directory="db", embedding_function=embedding_model)

books = pd.read_csv("books_cleaned.csv")
books["large_thumbnail"] = books["thumbnail"] + "&fife=w800"
books["large_thumbnail"] = np.where(
    books["large_thumbnail"].isna(),
    "cover-not-found.jpg",
    books["large_thumbnail"],
)

def retrieve_semantic_recommendations(query: str, top_k: int = 16) -> pd.DataFrame:
    recs = db_books.similarity_search(query, k=top_k)
    books_list = [int(rec.page_content.strip('"').split()[0]) for rec in recs]
    return books[books["isbn13"].isin(books_list)].head(top_k)

def recommend_books(query: str):
    recommendations = retrieve_semantic_recommendations(query)
    results = []

    for _, row in recommendations.iterrows():
        description = row["description"]
        truncated_desc_split = description.split()
        truncated_description = " ".join(truncated_desc_split[:30]) + "..."

        authors_split = row["authors"].split(";")
        if len(authors_split) == 2:
            authors_str = f"{authors_split[0]} and {authors_split[1]}"
        elif len(authors_split) > 2:
            authors_str = f"{', '.join(authors_split[:-1])}, and {authors_split[-1]}"
        else:
            authors_str = row["authors"]

        caption = f"{row['title']} by {authors_str}: {truncated_description}"
        results.append((row["large_thumbnail"], caption))
    return results


dark_theme = gr.themes.Base(
    primary_hue="blue",
    neutral_hue="gray"
).set(
    body_background_fill="#111111",
    body_text_color="#eeeeee",
    block_background_fill="#1a1a1a",
    block_border_color="#333333",
    input_background_fill="#1f1f1f",
    input_border_color="#444444",
    button_primary_background_fill="#2563eb",
    button_primary_text_color="white"
)

with gr.Blocks(theme=dark_theme) as dashboard:
    gr.Markdown("# 📚 Semantic Book Recommender", elem_id="title")

    with gr.Row():
        user_query = gr.Textbox(label="Enter a book idea:",
                                placeholder="e.g., A journey of self-discovery through space")
        submit_button = gr.Button("Find recommendations")

    gr.Markdown("## ✨ Recommendations")
    output = gr.Gallery(label="Books you might like", columns=8, rows=2)

    submit_button.click(fn=recommend_books,
                        inputs=[user_query],
                        outputs=output)

if __name__ == "__main__":
    dashboard.launch()
