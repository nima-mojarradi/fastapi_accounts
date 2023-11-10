from account.router.v1.router import router
from fastapi import FastAPI

app = FastAPI()

app.include_router(router=router)


import uvicorn

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)