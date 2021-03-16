from app import create_app
from app.models import *

app = create_app()


@app.shell_context_processor
def shell_context():
    return {
        "db": db,
        "Complaint": Complaint,
    }


if __name__ == "__main__":
    app.run()
