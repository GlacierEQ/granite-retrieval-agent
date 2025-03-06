from fastapi import FastAPI, UploadFile, File, HTTPException
from image_researcher_granite_crewai import Pipe as ImageResearchAgent
from granite_autogen_rag import Pipe as RetrievalAgent
import json

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

@app.post("/organize-photos")
async def organize_photos(files: list[UploadFile] = File(...)):
    try:
        # Load the organization configuration
        with open("photo_organization_config.json") as config_file:
            config = json.load(config_file)

        organized_photos = {
            "by_date": {},
            "by_tags": {}
        }

        for file in files:
            image_data = await file.read()
            # Here you would analyze the image and extract metadata (e.g., date, tags)
            # For now, let's assume we extract a date and tags from the image
            # Placeholder for actual metadata extraction
            extracted_date = "2023-01-01"  # Example date
            extracted_tags = ["example_tag"]  # Example tags

            # Organize by date
            year, month, day = extracted_date.split("-")
            if year not in organized_photos["by_date"]:
                organized_photos["by_date"][year] = {}
            if month not in organized_photos["by_date"][year]:
                organized_photos["by_date"][year][month] = {}
            if day not in organized_photos["by_date"][year][month]:
                organized_photos["by_date"][year][month][day] = []
            organized_photos["by_date"][year][month][day].append(file.filename)

            # Organize by tags
            for tag in extracted_tags:
                if tag not in organized_photos["by_tags"]:
                    organized_photos["by_tags"][tag] = []
                organized_photos["by_tags"][tag].append(file.filename)

        return {"organized_photos": organized_photos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
