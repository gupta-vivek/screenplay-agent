# 📄 Screenplay Agent

Screenplay Agent is a RAG Agent that can answer queries from the movie scripts present in https://imsdb.com/

---

- **Data**: Movie scripts are scraped from the https://imsdb.com/ website.
- **Chunking**:Movie scripts are chunked by INTERIOR/EXTERIOR scenes. Some scripts don't provide this information. Those
  scripts are chunked by character length.
- **Embedding Model**: Only few chunks are greater than 384 token. Token Limit for `all-mpnet-base-v2` is 384. The
  all-mpnet-base-v2 are designed as a general purpose model and provides the best quality. Hence this model is used for
  the project.
- **Vector Store**: LanceDB
- **Search/Retrieve**: Hybrid Search using text and vector is used to search and retrieve relevant documents.
- **LLM Integration**: Deepseek is used to generate responses based on the retrieved data.

---

`Langgraph` is used for building the agent.

`Langsmith` is used for tracing, evaluation and monitoring.

`Langgraph Chat UI` is used for interface.

---

# Deployment

The agent is deployed as a `Standalone Container` using `Langgraph Server`. `Postgres DB` is used for
persistence/memory. `Redis` for managing queue.

The free version of `render` is used for cloud deployment. Vector search is disabled in cloud deployment as the free
version has a memory limit and hence can't load the embedding model.

To interact with the Agent:
Click [here](https://agentchat.vercel.app/?apiUrl=https://screenplay-agent.onrender.com&assistantId=agent&chatHistoryOpen=true) (
Give it a minute to load as the server goes to sleep due to inactivity)

To deploy it locally:

`docker compose up`