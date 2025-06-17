import os
import logging
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
logging.basicConfig(level=logging.INFO)

DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GROQ_API = os.getenv("GROQ_API_KEY")
HUGGINGFACE_API = os.getenv("HUGGING_API_KEY")

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage,
)
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.node_parser import SentenceSplitter
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.llms.groq import Groq

import chromadb
import chromadb.utils.embedding_functions as embedding_functions

embedding_model_name = "intfloat/multilingual-e5-large"
huggingface_ef = embedding_functions.HuggingFaceEmbeddingFunction(
    api_key=HUGGINGFACE_API,
    model_name=embedding_model_name
)

chroma_client = chromadb.PersistentClient(path="./chroma.db")
collection_name = "documentos_llm"
chroma_collection = chroma_client.get_or_create_collection(
    name=collection_name,
    embedding_function=huggingface_ef
)

vector_store = ChromaVectorStore(chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
embed_model = HuggingFaceEmbedding(model_name=embedding_model_name)

if os.path.exists("./chroma.db") and os.listdir("./chroma.db"):
    try:
        logging.info("Índice existente detectado. Carregando do armazenamento...")
        index = load_index_from_storage(storage_context=storage_context, embed_model=embed_model)
    except Exception as e:
        logging.warning(f"Erro ao carregar índice existente: {e}")
        logging.info("Criando índice do zero...")
        docs = SimpleDirectoryReader(input_dir="files").load_data()
        nodes = SentenceSplitter(chunk_size=1000).get_nodes_from_documents(docs, show_progress=True)
        index = VectorStoreIndex(nodes, storage_context=storage_context, embed_model=embed_model)
        index.storage_context.persist()
        logging.info("Índice criado e salvo.")
else:
    logging.info("Nenhum índice encontrado. Criando embeddings e índice...")
    docs = SimpleDirectoryReader(input_dir="files").load_data()
    logging.info(f"{len(docs)} documentos carregados.")
    nodes = SentenceSplitter(chunk_size=1000).get_nodes_from_documents(docs, show_progress=True)
    logging.info(f"{len(nodes)} nós criados.")
    index = VectorStoreIndex(nodes, storage_context=storage_context, embed_model=embed_model)
    index.storage_context.persist()
    logging.info("Índice criado e salvo.")

llm = Groq(model="meta-llama/llama-4-scout-17b-16e-instruct", api_key=GROQ_API)

system_prompt = (
    "Você é um professor universitário que responde perguntas com clareza sobre algoritmos genéticos, "
    "seu fundamento é no livro Algoritmos Genéticos, por Ricardo Linden, "
    "você deve responder às perguntas em português do Brasil, de forma didática e acadêmica."
)

chat_engine = index.as_chat_engine(mode="context", llm=llm, system_prompt=system_prompt)

# =============== DISCORD BOT ===============
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    await client.wait_until_ready()
    try:
        synced = await client.tree.sync()
        logging.info(f"Comandos sincronizados: {[cmd.name for cmd in synced]}")
    except Exception as e:
        logging.error(f"Erro ao sincronizar comandos: {e}")
    logging.info(f"Bot online como {client.user}")

@client.tree.command(name="pergunta", description="Pergunte algo com base nos documentos")
@app_commands.describe(ag="Digite sua pergunta")
async def pergunta(interaction: discord.Interaction, ag: str):
    await interaction.response.defer(thinking=True)  # evita erro de timeout
    try:
        resposta = chat_engine.chat(ag).response
        await interaction.followup.send(f"**Pergunta:** {ag}\n**Resposta:** {resposta}")
    except Exception as e:
        await interaction.followup.send(f"Ocorreu um erro: {e}")

client.run(DISCORD_TOKEN)
