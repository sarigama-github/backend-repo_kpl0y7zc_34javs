import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from schemas import Profile, Skill, Project, Experience, Education, Message
from database import db, create_document, get_documents

app = FastAPI(title="Technician Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok"}

@app.get("/test")
async def test():
    try:
        names = await db.list_collection_names()
        return {"backend": "running", "collections": names}
    except Exception as e:
        return {"backend": "running", "collections": [], "error": str(e)}

# Seed endpoint with demo data
@app.post("/seed")
async def seed():
    existing = await db["profile"].find_one({})
    if existing:
        return {"message": "already seeded"}

    profile = await create_document("profile", Profile(
        name="Max Muster",
        title="Elektronik- & IT-Techniker",
        bio="Ich verbinde Hardware und Software: von PCB-Design bis Cloud-Automation.",
        location="Berlin, DE",
        links={
            "github": "https://github.com/",
            "linkedin": "https://www.linkedin.com/",
            "email": "mailto:max@example.com"
        }
    ).model_dump())

    skills = [
        Skill(name="PCB Design", level="Expert", category="Electronics"),
        Skill(name="Soldering / Rework", level="Advanced", category="Electronics"),
        Skill(name="Embedded C/C++", level="Advanced", category="Embedded"),
        Skill(name="Python", level="Advanced", category="Software"),
        Skill(name="Linux / Debian", level="Advanced", category="IT"),
        Skill(name="Networking / VLAN", level="Intermediate", category="IT"),
        Skill(name="Docker & CI/CD", level="Advanced", category="DevOps"),
    ]
    for s in skills:
        await create_document("skill", s.model_dump())

    projects = [
        Project(name="IoT Sensor Hub", description="Modulares ESP32-Board mit LoRaWAN, OTA-Updates und Cloud-Dashboard.", tags=["ESP32","LoRaWAN","React","FastAPI"]),
        Project(name="FPGA Logic Analyzer", description="Gattersimulation und Signal-Visualisierung in Echtzeit.", tags=["FPGA","VHDL","Python"]),
        Project(name="Smart Lab Bench", description="Messgeräte orchestration via SCPI, Logging und Alarme.", tags=["SCPI","Raspberry Pi","Grafana"]),
    ]
    for p in projects:
        await create_document("project", p.model_dump())

    experience = [
        Experience(company="TechWorks GmbH", role="Elektronikentwickler", start="2019", end="2022", summary="Mixed-Signal-Design, EMV, Serienreife."),
        Experience(company="CloudOps AG", role="IT / DevOps", start="2022", end="Present", summary="Infra as Code, Monitoring, Automatisierung."),
    ]
    for e in experience:
        await create_document("experience", e.model_dump())

    education = [
        Education(school="FH München", degree="B.Eng. Elektro- und Informationstechnik", start="2015", end="2019"),
        Education(school="Cisco", degree="CCNA (Kurs)", start="2020", end="2020")
    ]
    for ed in education:
        await create_document("education", ed.model_dump())

    return {"message": "seeded"}

# Public endpoints
@app.get("/profile", response_model=List[Profile])
async def get_profile():
    items = await get_documents("profile")
    return items

@app.get("/skills", response_model=List[Skill])
async def get_skills():
    return await get_documents("skill")

@app.get("/projects", response_model=List[Project])
async def get_projects():
    return await get_documents("project")

@app.get("/experience", response_model=List[Experience])
async def get_experience():
    return await get_documents("experience")

@app.get("/education", response_model=List[Education])
async def get_education():
    return await get_documents("education")

# Contact form
@app.post("/contact")
async def contact(msg: Message):
    saved = await create_document("message", msg.model_dump())
    if not saved:
        raise HTTPException(status_code=500, detail="Could not save message")
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
