# backend/utils/cors.py

import os                                               # Importing os for accessing environment variables
from fastapi import FastAPI                             # Importing FastAPI
from fastapi.middleware.cors import CORSMiddleware      # Importing CORSMiddleware

# NOTE: This function is used to configure CORS (Cross-Origin Resource Sharing) for the FastAPI application.
def setup_cors(app: FastAPI):
    # Get port from environment variable
    selected_port = os.getenv("LOCALHOST_PORT", "8000")

    # Get CORS origins from environment variable
    cors_bases = os.getenv("CORS_ORIGINS", "*").split(",")

    # If it's a wildcard (*), allow all without credentials, otherwise, allow with credentials and a list of origins with the selected port
    if cors_bases == ["*"]:
        allow_origins = ["*"]
        allow_credentials = False
    else:
        allow_origins = [base.strip() + ":" + selected_port for base in cors_bases if base.strip()]
        allow_credentials = True

    # Add CORS middleware to the FastAPI application
    app.add_middleware(
                        CORSMiddleware,
                        allow_origins=allow_origins,
                        allow_credentials=allow_credentials,
                        allow_methods=["*"],
                        allow_headers=["*"],
                    )
