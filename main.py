from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
import os
import uuid
import sqlite3
import json
from datetime import datetime

from crewai import Crew, Process
from agents import financial_analyst, verifier, investment_advisor, risk_assessor
from task import analyze_financial_document, verification, investment_analysis, risk_assessment

# Initialize Database
DB_NAME = "financial_analysis.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analyses (
            id TEXT PRIMARY KEY,
            query TEXT,
            filename TEXT,
            status TEXT,
            result TEXT,
            created_at TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()

app = FastAPI(title="Financial Document Analyzer")

def run_crew(query: str, file_path: str, job_id: str):
    """Run the crew in the background and update the database"""
    try:
        financial_crew = Crew(
            agents=[verifier, financial_analyst, investment_advisor, risk_assessor],
            tasks=[verification, analyze_financial_document, investment_analysis, risk_assessment],
            process=Process.sequential,
        )

        result = financial_crew.kickoff({'query': query, 'path': file_path})

        # Update database with success
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE analyses SET status = ?, result = ? WHERE id = ?",
                       ("completed", str(result), job_id))
        conn.commit()
        conn.close()

    except Exception as e:
        # Update database with failure
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("UPDATE analyses SET status = ?, result = ? WHERE id = ?",
                       ("failed", str(e), job_id))
        conn.commit()
        conn.close()
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass  # Ignore cleanup errors

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Financial Document Analyzer API is running"}

@app.post("/analyze")
async def analyze_financial_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    query: str = Form(default="Analyze this financial document for investment insights")
):
    """Analyze financial document and provide comprehensive investment recommendations"""
    
    file_id = str(uuid.uuid4())
    file_path = f"data/financial_document_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # Validate query
        if query=="" or query is None:
            query = "Analyze this financial document for investment insights"

        # Create DB entry
        job_id = str(uuid.uuid4())
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO analyses (id, query, filename, status, result, created_at) VALUES (?, ?, ?, ?, ?, ?)",
                       (job_id, query, file.filename, "processing", None, datetime.now()))
        conn.commit()
        conn.close()

        # Start background task
        background_tasks.add_task(run_crew, query.strip(), file_path, job_id)
        
        return {
            "status": "processing",
            "job_id": job_id,
            "message": "Analysis started in background. Check status with /results/{job_id}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error starting analysis: {str(e)}")

@app.get("/results/{job_id}")
async def get_results(job_id: str):
    """Check the status and get results of an analysis job"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT status, result, created_at FROM analyses WHERE id = ?", (job_id,))
    row = cursor.fetchone()
    conn.close()
    
    if not row:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job_id,
        "status": row[0],
        "result": row[1],
        "created_at": row[2]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
