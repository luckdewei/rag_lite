# 导入 chromadb 库
import chromadb

# 创建一个基于磁盘持久化的 chromadb 客户端，数据库路径为 ./chroma_db
client = chromadb.PersistentClient(path="./chroma_db")
# 获取所有集合对象的列表
collections = client.list_collections()
# 打印所有集合的名字
print("所有集合:", [col.name for col in collections])
# 遍历每一个集合
for collection in collections:
    # 获取集合中的所有文档、元数据和向量嵌入信息
    results = collection.get(include=["documents", "metadatas", "embeddings"])
    # 获取分块的 ids 列表
    ids = results["ids"]
    # 获取文档内容的列表
    documents = results["documents"]
    # 获取元数据的列表
    metadatas = results["metadatas"]
    # 获取嵌入向量的列表
    embeddings = results["embeddings"]
    # 遍历所有的文档，结合 id、文档内容、元数据和嵌入向量一起输出
    for i, (id, doc, meta, embedding) in enumerate(
        zip(ids, documents, metadatas, embeddings)
    ):
        # 打印每一条文档的详细信息
        print(f"第{i}条: {id} {doc} {meta} {embedding}")
