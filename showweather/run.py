from showweather import app
import os

app.run(port=int(os.environ["PORT"]) if "PORT" in os.environ else 5000)
