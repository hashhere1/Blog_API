from fastapi import FastAPI
from database import engine
import models
import uvicorn
from routers import blog, user, authentication

app = FastAPI()
models.Base.metadata.create_all(engine)
app.include_router(blog.router)
app.include_router(user.router)
app.include_router(authentication.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
