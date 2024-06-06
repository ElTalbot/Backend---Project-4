import os

db_URI = os.getenv('DATABASE_URL', 'postgresql://localhost:5432/movements_db')
SECRET = os.getenv('SECRET', 'helloyobonjourolawhoopwhoop')

if db_URI.startswith("postgres://"):
    db_URI = db_URI.replace("postgres://", "postgresql://", 1)
