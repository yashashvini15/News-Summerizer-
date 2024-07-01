import tkinter as tk
from textblob import TextBlob
from newspaper import Article
import nltk

# Download the 'punkt' tokenizer for NLTK
nltk.download('punkt')

# Function to summarize the article from the given URL
def summarize():
    # Retrieve the URL from the text widget
    url = u_text.get("1.0", "end").strip()

    # Initialize the Article object with the URL
    article = Article(url)

    try:
        # Download the article content
        article.download()
        # Parse the article to extract useful information
        article.parse()
        # Perform natural language processing to extract summary
        article.nlp()
    except Exception as e:
        # Handle exceptions (e.g., URL is not a valid article)
        title.config(state="normal")
        author.config(state="normal")
        publication.config(state="normal")
        summary.config(state="normal")
        sentiment.config(state="normal")

        title.delete(1.0, "end")
        author.delete(1.0, "end")
        publication.delete(1.0, "end")
        summary.delete(1.0, "end")
        sentiment.delete(1.0, "end")

        title.insert(1.0, "Error: Unable to retrieve article")
        author.insert(1.0, "")
        publication.insert(1.0, "")
        summary.insert(1.0, str(e))
        sentiment.insert(1.0, "")

        title.config(state="disabled")
        author.config(state="disabled")
        publication.config(state="disabled")
        summary.config(state="disabled")
        sentiment.config(state="disabled")
        return

    # Enable the text widgets to insert the extracted information
    title.config(state="normal")
    author.config(state="normal")
    publication.config(state="normal")
    summary.config(state="normal")
    sentiment.config(state="normal")

    # Clear the previous content in the text widgets
    title.delete(1.0, "end")
    author.delete(1.0, "end")
    publication.delete(1.0, "end")
    summary.delete(1.0, "end")
    sentiment.delete(1.0, "end")

    # Insert the extracted information into the respective text widgets
    title.insert(1.0, article.title)
    author.insert(1.0, ', '.join(article.authors))
    publication.insert(1.0, article.publish_date.strftime('%Y-%m-%d') if article.publish_date else "N/A")
    summary.insert(1.0, article.summary)

    # Perform sentiment analysis on the article's text
    analysis = TextBlob(article.text)
    # Insert the sentiment analysis results
    sentiment.insert(1.0,
                     f'Polarity: {analysis.sentiment.polarity}, Sentiment: {"Positive" if analysis.sentiment.polarity > 0 else "Negative" if analysis.sentiment.polarity < 0 else "Neutral"}')

    # Clear the URL text widget for the next input
    u_text.delete(1.0, "end")

    # Disable the text widgets to prevent editing
    title.config(state="disabled")
    author.config(state="disabled")
    publication.config(state="disabled")
    summary.config(state="disabled")
    sentiment.config(state="disabled")

# Initialize the main application window
root = tk.Tk()
root.title("AI News Analysis")
root.geometry("1500x800")

# Create and pack the widgets for displaying the article's title
t_label = tk.Label(root, text="Title")
t_label.pack()
title = tk.Text(root, height=1, width=140)
title.config(state="disabled", bg="#dddddd")
title.pack()

# Create and pack the widgets for displaying the article's author(s)
a_label = tk.Label(root, text="Author")
a_label.pack()
author = tk.Text(root, height=1, width=140)
author.config(state="disabled", bg="#dddddd")
author.pack()

# Create and pack the widgets for displaying the publication date
p_label = tk.Label(root, text="Publication Date")
p_label.pack()
publication = tk.Text(root, height=1, width=140)
publication.config(state="disabled", bg="#dddddd")
publication.pack()

# Create and pack the widgets for displaying the article's summary
s_label = tk.Label(root, text="Summary")
s_label.pack()
summary = tk.Text(root, height=20, width=140)
summary.config(state="disabled", bg="#dddddd")
summary.pack()

# Create and pack the widgets for displaying the sentiment analysis results
sa_label = tk.Label(root, text="Sentiment Analysis")
sa_label.pack()
sentiment = tk.Text(root, height=1, width=140)
sentiment.config(state="disabled", bg="#dddddd")
sentiment.pack()

# Create and pack the widgets for inputting the article URL
u_label = tk.Label(root, text="URL")
u_label.pack()
u_text = tk.Text(root, height=1, width=140)
u_text.pack()

# Create and pack the button to trigger the summarization process
btn = tk.Button(root, text="Analyze", command=summarize)
btn.pack()

# Start the Tkinter event loop
root.mainloop()
