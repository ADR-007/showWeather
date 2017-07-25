from showweather import app
import os

app.run(port=int(os.environ["PORT"]))
