from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from app.api.routes import router
from app.api.errors import validation_exception_handler, generic_exception_handler

app = FastAPI(
    title="Name Verification API",
    description="Generate and verify names with deterministic matching",
    version="1.0.0"
)

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
app.include_router(router)
