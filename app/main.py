from fastapi import FastAPI, HTTPException, Request
from app.models import ScrapeSettings
from app.scraper import Scraper
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

SECRET_TOKEN = os.getenv("SECRET_TOKEN")

@app.post("/scrape")
def scrape(settings: ScrapeSettings, request: Request):
    token = request.query_params.get("token")
    if token != SECRET_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    scraper = Scraper(settings)
    result = scraper.scrape()
    return result
