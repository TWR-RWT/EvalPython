#! C:\Users\tgp\AppData\Local\Programs\Python\Python310\python.exe
from app import app

app.run(
    host="0.0.0.0",
    port=int("8080"),
    debug=True
)
#flask --app run --debug run

