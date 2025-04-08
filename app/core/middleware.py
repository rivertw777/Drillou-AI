from fastapi import Request
import logging
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("middleware")


async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    protocol = request.scope.get("http_version", "Unknown")
    status_code = response.status_code
    status_text = {
        200: "OK",
        400: "Bad Request",
        500: "Internal Server Error",
    }.get(status_code, "")
    logger.info(
        f" {request.method} {request.url} \"HTTP/{protocol} {status_code} {status_text}\", 소요 시간: {round(process_time * 1000)}ms"
    )
    return response
