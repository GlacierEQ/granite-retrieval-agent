from fastapi import FastAPI, UploadFile, File, HTTPException
from image_researcher_granite_crewai import Pipe as ImageResearchAgent
from granite_autogen_rag import Pipe as RetrievalAgent

app = FastAPI()

# Initialize agents
image_research_agent = ImageResearchAgent()
retrieval_agent = RetrievalAgent()

@app.post("/analyze-image")
async def analyze_image(file: UploadFile = File(...)):
    try:
        image_data = await file.read()
        # Call the image research agent's method to analyze the image
        result = await image_research_agent.pipe({"messages": [{"content": image_data}]}, None, None)  # Placeholder for actual call
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.post("/retrieve-documents")
async def retrieve_documents(query: str):
    try:
        # Call the Granite Retrieval Agent with the query
        documents = await retrieval_agent.pipe({"messages": [{"content": query}]}, None, None)  # Placeholder for actual call
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
