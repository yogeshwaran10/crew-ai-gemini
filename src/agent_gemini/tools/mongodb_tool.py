import os
import json
from datetime import datetime
from typing import Type, Optional, Dict, Any

from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crewai.tools import BaseTool
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, OperationFailure

# Load environment variables
load_dotenv()


class MongoDBReportStorageInput(BaseModel):
    """Input schema for MongoDBReportStorageTool."""
    report_content: str = Field(..., description="The content of the report to be stored in MongoDB.")
    report_metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the report (e.g., topic, timestamp, etc.)."
    )
    collection_name: str = Field(
        default="reports",
        description="The name of the MongoDB collection to store the report in."
    )


class MongoDBReportStorageTool(BaseTool):
    """Tool for storing reports in MongoDB."""
    name: str = "Store Report in MongoDB"
    description: str = (
        "Stores a generated report in MongoDB for future reference and analytics. "
        "This tool connects to MongoDB using the connection string in the environment variables "
        "and saves the report content along with metadata."
    )
    args_schema: Type[BaseModel] = MongoDBReportStorageInput
    
    def _connect_to_mongodb(self, mongodb_uri):
        """Establish connection to MongoDB."""
        try:
            client = MongoClient(mongodb_uri)
            # Ping the server to confirm connection
            client.admin.command('ping')
            # Use a database named 'agent_reports' or customize as needed
            return client, client.agent_reports
        except ConnectionFailure as e:
            raise ConnectionFailure(f"Failed to connect to MongoDB: {str(e)}")
        except Exception as e:
            raise Exception(f"An error occurred while connecting to MongoDB: {str(e)}")
    
    def _run(
        self, 
        report_content: str, 
        report_metadata: Dict[str, Any] = None,
        collection_name: str = "reports"
    ) -> str:
        """Store report in MongoDB."""
        # Get MongoDB URI from environment
        mongodb_uri = os.getenv("MONGODB_URI")
        if not mongodb_uri:
            return "MongoDB URI not found in environment variables. Please set MONGODB_URI in your .env file."
            
        if report_metadata is None:
            report_metadata = {}
        
        client = None    
        try:
            # Connect to MongoDB
            client, db = self._connect_to_mongodb(mongodb_uri)
            
            # Get the specified collection
            collection = db[collection_name]
            
            # Prepare the document to insert
            document = {
                "content": report_content,
                "created_at": datetime.utcnow(),
                "metadata": report_metadata
            }
            
            # Insert the document
            result = collection.insert_one(document)
            return f"Report successfully stored in MongoDB with ID: {result.inserted_id}"
            
        except ConnectionFailure as e:
            return f"Failed to connect to MongoDB: {str(e)}"
        except OperationFailure as e:
            return f"Failed to store report in MongoDB: {str(e)}"
        except Exception as e:
            return f"An error occurred while storing the report: {str(e)}"
        finally:
            # Ensure connection is closed even if an error occurs
            if client:
                client.close()
