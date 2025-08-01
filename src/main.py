"""!
@file main.py
@brief Main entry point for the CodeRunner FastAPI application
@details This module sets up the FastAPI application for CodeRunner, a platform for practicing timed LeetCode problems.
         It includes authentication routing and provides the main server entry point.
"""

from fastapi import FastAPI
from auth.router import router

## @brief FastAPI application instance
app = FastAPI(
    title="CodeRunner API",
    description="this is the API for CodeRunner, a platform for praciting timed leetocde problems",
    version="1.0.0"
)

app.include_router(router)

@app.get("/")
async def root():
    """!
    @brief Root endpoint handler
    @details Provides a simple welcome message for the API root path
    @return dict: A dictionary containing a welcome message
    @retval {"message": "Hello World!"} Success response
    """
    return {"message": "Hello World!"}

if __name__ == "__main__":
    """!
    @brief Main execution block
    @details Starts the uvicorn server when the script is run directly
    """
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
