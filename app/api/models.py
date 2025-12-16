from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    """Request to generate a target name."""
    prompt: str = Field(..., min_length=1)


class GenerateResponse(BaseModel):
    """Response from name generation."""
    target_name: str


class VerifyRequest(BaseModel):
    """Request to verify a candidate name."""
    candidate_name: str = Field(..., min_length=1)


class VerifyResponse(BaseModel):
    """Response from name verification."""
    match: bool
    confidence: float = Field(..., ge=0.0, le=1.0)
    reason: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str


class ErrorResponse(BaseModel):
    """Error response."""
    error: str
    detail: str
