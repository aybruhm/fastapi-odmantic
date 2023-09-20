# Uvicorn Imports
import uvicorn


if __name__ == "__main__":
    uvicorn.run("entrypoint:application", host="0.0.0.0", port=80, workers=4)
