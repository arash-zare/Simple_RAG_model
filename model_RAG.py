# import ollama

from openai import OpenAI
import chromadb
from dotenv import load_dotenv
import os



load_dotenv()
api_key = os.getenv("API_KEY")
base_url = os.getenv("BASE_URL")


client = OpenAI(base_url=base_url, api_key=api_key)


chroma_client = chromadb.Client()
collection = chroma_client.get_or_create_collection(name="my_private_docs")

documents = [
    "Arash Zare is a Data & DevOps Engineer specializing in Python, Docker, Apache Kafka, and Kubernetes.",
    "Holds an M.Sc. in Computer Engineering from Shiraz University with a focus on Cloud Computing and distributed systems.",
    "Published a research paper in Springer Cluster Computing (2023) on multi-objective service placement in fog-cloud platforms.",
    "Worked as a Data Engineer at Derak Cloud Company, leading the Cluster Health Check and monitoring project.",
    "Expertise in Big Data systems including Apache Kafka, ClickHouse, Apache Hadoop (HDFS, Parquet), and Apache Spark.",
    "Proficient in DevOps tools such as Docker, Kubernetes, GitLab CI/CD, Ansible, and Terraform.",
    "Experienced in Monitoring & Observability using Prometheus (PromQL), Grafana dashboards, and the ELK Stack.",
    "Developed a NetFlow & Log Forwarding pipeline using syslog-ng, goflow2, and RabbitMQ.",
    "Developed Auto Kian, a car dealership platform using Django, Python, SQLite, and Bootstrap.",
    "Served as Graduate Teaching Assistant for Cloud Computing course under Prof. Dr. Khunjush at Shiraz University."
]

# for i, doc in enumerate(documents):
#     collection.add(
#         documents=[doc],
#         ids=[str(i)]
#     )

ids = [str(i) for i in range(len(documents))]

collection.add(
    documents=documents,
    ids=ids
)



user_query = "What did Arash do at Derak Cloud?"

results = collection.query(
    query_texts=[user_query],
    n_results=2
)
# context = results['documents'][0][0]
# print(f"Retrieved Context: \n{context}")



if results and results.get('documents') and results['documents'][0]:
    context = "\n".join(results['documents'][0][:2])
else:
    context = "No relevant context found."

print(f"Retrieved Context:\n{context}\n" + "-"*40)


system_prompt = (
    "You are an AI assistant answering questions about Arash Zare's background. "
    "Answer directly and concisely using only this context: "
    f"{context}"
)

# response = ollama.chat(model='qwen3:4b', messages=[
#     {'role': 'system', 'content': system_prompt},
#     {'role': 'user', 'content': user_query}
# ])


response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query}
    ]
)

print("\nAI Response:")
print(response.choices[0].message.content)