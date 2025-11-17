from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

from database import db, create_document, get_documents
from schemas import Profile, Skill, Project, Experience, Education, Message

app = FastAPI(title="Electronics & IT Portfolio API")

# CORS for local preview and hosted frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/test")
async def test():
    # Quick DB smoke check
    try:
        await db.command("ping")
        return {"status": "ok", "db": "connected"}
    except Exception as e:
        return {"status": "error", "detail": str(e)}


# Seed helper (optional for first run)
class SeedStatus(BaseModel):
    seeded: bool


@app.post("/seed", response_model=SeedStatus)
async def seed():
    # Only insert when empty
    profs = await get_documents("profile")
    if not profs:
        await create_document(
            "profile",
            Profile(
                name="Max Mustermann",
                title="Elektroniker & IT-Techniker",
                bio=(
                    "Ich entwickle robuste Hardware- und Softwarelösungen – von Leiterplatten"
                    " bis Cloud-Automation. Mein Fokus: zuverlässige Systeme mit sauberem"
                    " Design und klarer Benutzererfahrung."
                ),
                location="Berlin, DE",
                email="max@example.com",
                socials={
                    "github": "https://github.com/",
                    "linkedin": "https://www.linkedin.com/",
                },
            ).model_dump(),
        )
    skills = await get_documents("skill")
    if not skills:
        defaults = [
            ("Elektronik", "PCB-Design (KiCad)", 5),
            ("Elektronik", "Löten SMD/THT", 5),
            ("Elektronik", "EMV & Messmittel", 4),
            ("IT", "Python & FastAPI", 5),
            ("IT", "Embedded (C/C++)", 4),
            ("IT", "Linux & Docker", 5),
            ("IT", "Netzwerk (TCP/IP, VLAN)", 4),
        ]
        for c, n, l in defaults:
            await create_document("skill", Skill(category=c, name=n, level=l).model_dump())
    projects = await get_documents("project")
    if not projects:
        examples = [
            Project(
                title="IoT Sensor Node",
                description="Ultra-niedriger Energieverbrauch, MQTT over TLS, OTA-Updates.",
                tags=["PCB", "ESP32", "MQTT"],
                link="#",
            ),
            Project(
                title="Automatisiertes Test-Rig",
                description="Hardware-in-the-Loop mit Python, Relais-Matrix, grafische Reports.",
                tags=["Python", "Hardware", "HIL"],
                link="#",
            ),
            Project(
                title="Portfolio 3D Experience",
                description="Scroll-basierter 3D-Tunnel mit reaktiven Slides.",
                tags=["React", "Spline", "UX"],
                link="#",
            ),
        ]
        for p in examples:
            await create_document("project", p.model_dump())
    experiences = await get_documents("experience")
    if not experiences:
        await create_document(
            "experience",
            Experience(
                company="TechWerk GmbH",
                role="Elektroniker / IT-Systemtechniker",
                start="2019-03",
                end="2024-08",
                summary="Inbetriebnahme, Monitoring, CI/CD für Edge-Geräte und Backend-Services.",
            ).model_dump(),
        )
    education = await get_documents("education")
    if not education:
        await create_document(
            "education",
            Education(
                school="Berufsakademie für Elektrotechnik",
                degree="Staatl. gepr. Techniker (ET)",
                start="2015-09",
                end="2019-02",
            ).model_dump(),
        )

    return SeedStatus(seeded=True)


# Public read endpoints
@app.get("/profile")
async def get_profile():
    items = await get_documents("profile", limit=1)
    return items[0] if items else {}


@app.get("/skills")
async def get_skills():
    return await get_documents("skill", limit=100)


@app.get("/projects")
async def get_projects():
    return await get_documents("project", limit=100)


@app.get("/experience")
async def get_experience():
    return await get_documents("experience", limit=50)


@app.get("/education")
async def get_education():
    return await get_documents("education", limit=50)


# Contact form
@app.post("/contact")
async def contact(msg: Message):
    saved = await create_document("message", msg.model_dump())
    if not saved:
        raise HTTPException(status_code=500, detail="Message not saved")
    return {"ok": True}
