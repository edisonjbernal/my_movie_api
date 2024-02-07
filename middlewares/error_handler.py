from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse

class ErrorHandler(BaseHTTPMiddleware ):
    def __init__(self, app : FastAPI) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next) -> Response | JSONResponse :
        try:
            response = await call_next(request)
        except Exception as e:
            response = JSONResponse(status_code=500, content={"error": str(e)})
        return response