# LLM Chatbot

LLM Chatbot is a question answering chatbot based on the LLM (Language, Logic, and Math) framework. It can read the data from the input PDF files and store them in the form of embeddings in the FAISS vector store. It can then answer the user’s questions based on the query asked by referring to the information from the vector store.

# Demo
The solution is not in the production yet. You can try out the chatbot in your local environment.

# Installation
To install the chatbot locally, you need to have Python 3.8 or higher and pip installed. Then, you can follow these steps:

- Clone this repository:

` git clone https://github.com/hargurjeet/LLMs-Chat-with-PDFs `

- Install the required dependencies:
  `pip install -r requirements.txt`

- Run the chatbot:
  `python chatbot.py`

# Usage
To use the chatbot, you need to provide some PDF files that the chatbot can use as sources of information. You can either upload your own PDF files or use the default ones provided in the data folder.

To upload your own PDF files, you need to create a folder named custom inside the data folder and place your PDF files there. Then, you need to edit the config.json file and change the value of the pdf_path key to data/custom.

To use the default PDF files, you can leave the config.json file as it is.

Once you have the PDF files ready, you can run the chatbot and start asking questions. The chatbot will try to find the best answer from the PDF files using the LLM model and the FAISS vector store. You can also ask the chatbot to perform some tasks related to the PDF files, such as extracting, summarizing, or translating.

Here are some examples of questions and tasks you can ask the chatbot:

What is the main idea of the document named sample.pdf?
- Extract the table of contents from the document named sample.pdf.
- Translate the first paragraph of the document named sample.pdf to French.
- How do I install FAISS?
- What is the LLM framework?

# License
This project is licensed under the MIT License. See the [LICENSE] file for more details.

