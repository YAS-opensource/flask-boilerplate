import os

from project.server import app

if __name__ == ("__main__"):
    PORT = int(os.environ.get("PORT", 3000))
    app.run(host="0.0.0.0", port=PORT)