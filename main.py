from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from app.api.auth.routes import routerauth
from app.api.auth.routes import routeUser

templates = Jinja2Templates(directory="app/templates")


app = FastAPI(
   title="Stater Kit",
   version="1.0.0",
   docs_url='/api/docs',
   redoc_url='/api/redoc'
)


# Charger les fichiers Statics
app.mount("/app/style", StaticFiles(directory="app/style"), name="style")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def read_root(request: Request):
   return templates.TemplateResponse(
      'home.html',
      {"request":request}
   )

app.include_router(routerauth)
app.include_router(routeUser)