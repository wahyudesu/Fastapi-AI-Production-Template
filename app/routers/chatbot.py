# routers/assignment.py

import os
import re
import json
import numpy as np
from fastapi import APIRouter, HTTPException, Form, Depends
from supabase import create_client
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_pinecone import PineconeEmbeddings
from gliner import GLiNER
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
from datetime import datetime
import pickle
from sklearn.preprocessing import StandardScaler
import pandas as pd
from pydantic import BaseModel
from typing import Dict, Any, Optional

from ..dependencies import get_query_token

load_dotenv()

router = APIRouter(prefix="/assignment", tags=["assignment"], dependencies=[Depends(get_query_token)])


# Initialize services with error handling
def initialize_services():
    """Initialize external services with proper error handling"""
    services = {}

    try:
        # Supabase client
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_KEY")
        if not supabase_url or not supabase_key:
            raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in environment variables")
        services["supabase"] = create_client(supabase_url, supabase_key)
    except Exception as e:
        print(f"Warning: Failed to initialize Supabase: {e}")
        services["supabase"] = None

    try:
        # GLiNER model for entity extraction
        services["gliner_model"] = GLiNER.from_pretrained("urchade/gliner_medium-v2.1")
    except Exception as e:
        print(f"Warning: Failed to initialize GLiNER model: {e}")
        services["gliner_model"] = None

    try:
        # Pinecone embeddings
        services["embeddings"] = PineconeEmbeddings(model="multilingual-e5-large")
    except Exception as e:
        print(f"Warning: Failed to initialize Pinecone embeddings: {e}")
        services["embeddings"] = None

    try:
        # Load the saved clustering model
        model_path = os.path.join(os.path.dirname(__file__), "..", "model", "pickle", "best_model-1.pkl")
        with open(model_path, "rb") as file:
            services["clustering_model"] = pickle.load(file)
    except Exception as e:
        print(f"Warning: Failed to load clustering model: {e}")
        services["clustering_model"] = None

    return services


# Initialize services
services = initialize_services()


# Pydantic models for request/response
class AssignmentUploadRequest(BaseModel):
    uuid: str
    file_url: str


class AssignmentUploadResponse(BaseModel):
    message: str
    extracted_entities: Dict[str, str]
    vector: Optional[list] = None
    page_count: int
    sentence_count: int
    plagiarism_results: Dict[str, float]
    clustering: Optional[float] = None


@router.post("/upload", response_model=AssignmentUploadResponse)
async def upload_file(uuid: str = Form(...), file_url: str = Form(...)):
    """
    Process uploaded assignment file and extract relevant information.

    This endpoint:
    - Parses PDF documents
    - Extracts student information using NER
    - Performs plagiarism detection
    - Generates document embeddings
    - Performs clustering analysis
    """
    # Check if services are available
    if not services["supabase"]:
        raise HTTPException(status_code=500, detail="Database service not available")

    try:
        # Parse PDF
        if not file_url:
            raise HTTPException(status_code=400, detail="File URL is required")

        loader = PyPDFLoader(file_url)
        documents = loader.load()
        page_count = len(documents)
        full_text = " ".join(doc.page_content for doc in documents)
        sentence_count = len([s for s in re.split(r"[.!?]+", full_text) if s.strip()])

        # Chunking and embedding to vector DB
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        chunks = text_splitter.split_documents(documents)
        markdown_content = "\n\n".join(doc.page_content for doc in chunks)

        # Generate embeddings if service is available
        vector = None
        if services["embeddings"]:
            try:
                vector = services["embeddings"].embed_documents([markdown_content])[0]
            except Exception as e:
                print(f"Warning: Failed to generate embeddings: {e}")

        # Entity extraction
        extracted_data = {"Name": "", "ID": ""}
        if services["gliner_model"] and chunks:
            try:
                first_chunk = chunks[0].page_content
                entities = services["gliner_model"].predict_entities(first_chunk, labels=["Name", "ID"])
                for entity in entities:
                    if entity["label"] in extracted_data:
                        extracted_data[entity["label"]] = entity["text"]
            except Exception as e:
                print(f"Warning: Failed to extract entities: {e}")

        # Get data specific documents
        current_record = services["supabase"].table("documents").select("*").eq("id", uuid).execute()
        if not current_record.data:
            raise HTTPException(status_code=404, detail=f"No record found with uuid: {uuid}")

        # Plagiarism detection
        plagiarism_results = {}
        if vector is not None:
            try:
                folder = current_record.data[0]["folder"]
                uploaded_date = current_record.data[0]["uploadedDate"]
                previous_records = (
                    services["supabase"]
                    .table("documents")
                    .select("*")
                    .eq("folder", folder)
                    .lt("uploadedDate", uploaded_date)
                    .execute()
                    .data
                )

                if previous_records:
                    previous_embeddings = []
                    for record in previous_records:
                        if record.get("embedding"):
                            try:
                                if isinstance(record["embedding"], str):
                                    embedding = [float(x) for x in json.loads(record["embedding"])]
                                else:
                                    embedding = [float(x) for x in record["embedding"]]
                                previous_embeddings.append(embedding)
                            except (json.JSONDecodeError, ValueError, TypeError):
                                continue

                    if previous_embeddings:
                        current_embedding = (
                            vector if isinstance(vector, list) else [float(x) for x in json.loads(vector)]
                        )
                        similarities = cosine_similarity(np.array([current_embedding]), np.array(previous_embeddings))[
                            0
                        ]
                        similarity_list = [
                            (r["nameStudent"] or "Unknown", float(sim) if isinstance(sim, (int, float)) else 0.0)
                            for r, sim in zip([r for r in previous_records if r.get("embedding")], similarities)
                        ]
                        top_2 = sorted(similarity_list, key=lambda x: x[1], reverse=True)[:2]
                        plagiarism_results = dict(top_2)
            except Exception as e:
                print(f"Warning: Failed to perform plagiarism detection: {e}")

        # Calculate time difference in hours between deadline and uploaded date
        time_diff = 0
        try:
            deadline = current_record.data[0]["deadline"]
            uploaded_date = current_record.data[0]["uploadedDate"]
            deadline_dt = datetime.fromisoformat(deadline)
            uploaded_date_dt = datetime.fromisoformat(uploaded_date)
            time_diff = (deadline_dt - uploaded_date_dt).total_seconds() / 3600
        except Exception as e:
            print(f"Warning: Failed to calculate time difference: {e}")

        plagiarism_score = max(plagiarism_results.values()) if plagiarism_results else 0.0

        # Clustering
        clustering_value = None
        if services["clustering_model"]:
            try:
                data_prediction = pd.DataFrame(
                    {
                        "sentences": [sentence_count],
                        "page": [page_count],
                        "timing": [time_diff],
                        "plagiarism": [plagiarism_score],
                    }
                )

                data_scaled = StandardScaler().fit_transform(data_prediction)
                clustering = services["clustering_model"].predict(data_scaled)
                clustering_value = (
                    float(clustering[0]) if isinstance(clustering, (list, np.ndarray)) else float(clustering)
                )
            except Exception as e:
                print(f"Warning: Failed to perform clustering: {e}")

        # Update to database
        update_data = {
            "nameStudent": extracted_data["Name"] or "null",
            "NRP": extracted_data["ID"] or "null",
            "isiTugas": markdown_content,
            "page": page_count,
            "sentences": sentence_count,
            "plagiarism": plagiarism_results,
        }

        if vector is not None:
            update_data["embedding"] = vector.tolist() if isinstance(vector, np.ndarray) else vector

        if clustering_value is not None:
            update_data["clustering"] = clustering_value

        response = services["supabase"].table("documents").update(update_data).eq("id", uuid).execute()

        # Error handling
        if not response.data:
            raise HTTPException(status_code=404, detail=f"Failed to update record with uuid: {uuid}")

        # Variable return
        return AssignmentUploadResponse(
            message="File processed and record updated successfully in Supabase.",
            extracted_entities=extracted_data,
            vector=vector.tolist() if isinstance(vector, np.ndarray) else vector,
            page_count=page_count,
            sentence_count=sentence_count,
            plagiarism_results=plagiarism_results,
            clustering=clustering_value,
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/status")
async def get_assignment_status():
    """
    Check the status of assignment processing services.

    Returns the availability of each required service.
    """
    status = {
        "supabase": services["supabase"] is not None,
        "gliner_model": services["gliner_model"] is not None,
        "embeddings": services["embeddings"] is not None,
        "clustering_model": services["clustering_model"] is not None,
        "message": "Assignment processing service is running",
    }

    # Check if all critical services are available
    critical_services = ["supabase"]
    all_critical_available = all(services[service] is not None for service in critical_services)

    if not all_critical_available:
        status["warning"] = "Some critical services are not available"

    return status
