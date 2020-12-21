from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from listenmoe import ws
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

async def homepage(request):
    return JSONResponse({'song': ws.song, "artists": ws.artist})

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'])
]
app = Starlette(debug=True, routes=[
    Route('/', homepage),
], on_startup=[ws.start_socket_thread], middleware=middleware)