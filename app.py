import db
from utils import index
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, condecimal
from fastapi.middleware.cors import CORSMiddleware

db.init_db()
app = FastAPI()

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Measurement(BaseModel):
    username: str
    microscope_size: float
    magnification: float

@app.post("/calculate")
def calculate(measurement: Measurement):
    try:
        if not isinstance(measurement.microscope_size, (int, float)) or measurement.microscope_size <= 0:
            raise HTTPException(status_code=400, detail="Microscope size must be a positive number.")
        
        if not isinstance(measurement.magnification, (int, float)) or measurement.magnification == 0:
            raise ValueError("Magnification must be a non-zero number.")
            
        actual_size = measurement.microscope_size / measurement.magnification
        db.save_to_db(measurement.username, measurement.microscope_size, actual_size)
        return {
            "status": "success",
            "message": "Calculations complete",
            "actual_size": round(actual_size, 4),
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

if __name__ == "__main__":
    db.init_db()
    username = input("Enter your username: ")
    microscope_size = float(input("Enter microscope size (mm): "))
    magnification = float(input("Enter magnification: "))
    actual_size = index.calculate_actual_size(microscope_size, magnification)
    db.save_to_db(username, microscope_size, actual_size)
    print(f"Actual size saved: {actual_size:.4f}mm")