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
        # Process the image using the Image Research Agent
        image_data = await file.read()
        # Here you would call the image research agent's method to analyze the image
        # For example: result = await image_research_agent.analyze(image_data)
        result = {"description": "Image analysis result", "items": ["item1", "item2"]}  # Placeholder
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrieve-documents")
async def retrieve_documents(query: str):
    try:
        # Process the query using the Granite Retrieval Agent
        # For example: documents = await retrieval_agent.retrieve(query)
        documents = ["doc1", "doc2"]  # Placeholder
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
