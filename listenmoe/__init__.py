from starlette.applications import Starlette
from starlette.responses import JSONResponse
from starlette.routing import Route
from listenmoe import ws

async def homepage(request):
    return JSONResponse({'song': ws.song, "artists": ws.artist})


app = Starlette(debug=True, routes=[
    Route('/', homepage),
], on_startup=[ws.start_socket_thread])