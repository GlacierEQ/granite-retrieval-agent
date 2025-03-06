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
        result = await image_research_agent.pipe({"messages": [{"content": image_data}]}, None, None)  # Placeholder for actual call
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.post("/retrieve-documents")
async def retrieve_documents(query: str):
    try:
        documents = await retrieval_agent.pipe({"messages": [{"content": query}]}, None, None)  # Placeholder for actual call
        return {"documents": documents}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

@app.post("/organize-photos")
async def organize_photos(files: list[UploadFile] = File(...)):
    try:
with open("photo_organization_config.json", encoding='utf-8') as config_file:

            config = json.load(config_file)

        organized_photos = {}  # Initialize the dictionary to store organized photos

            "Family & Friends": {},
            "Travel & Vacations": {},
            "Work & Professional": {},
            "Art & Creative Projects": {},
            "Special Collections": {}
        }

        for file in files:
            await file.read()  # Read the image data but do not store it

            extracted_date = "2023-01-01"  # Example date
            extracted_tags = ["example_tag"]  # Example tags

            if "Family" in extracted_tags:
                year, month, day = extracted_date.split("-")
                if year not in organized_photos["Family & Friends"]:
                    organized_photos["Family & Friends"][year] = {}
                if month not in organized_photos["Family & Friends"][year]:
                    organized_photos["Family & Friends"][year][month] = {}
                if day not in organized_photos["Family & Friends"][year][month]:
                    organized_photos["Family & Friends"][year][month][day] = []
                organized_photos["Family & Friends"][year][month][day].append(file.filename)

            # Similar logic for other categories...

        return {"organized_photos": organized_photos}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) from e

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
