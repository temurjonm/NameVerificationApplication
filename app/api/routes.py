from fastapi import APIRouter, HTTPException, Depends
from app.api.models import (
    GenerateRequest,
    GenerateResponse,
    VerifyRequest,
    VerifyResponse,
    HealthResponse
)
from app.generator.service import NameGenerator
from app.verifier.service import NameVerifier
from app.store.memory import NameStore
from app.security import sanitize_input
from app.logging_config import logger

router = APIRouter()
_store = NameStore()


def get_store() -> NameStore:
    """Dependency to get store instance."""
    return _store


def get_generator(store: NameStore = Depends(get_store)) -> NameGenerator:
    """Dependency to get generator instance."""
    return NameGenerator(store)


def get_verifier(store: NameStore = Depends(get_store)) -> NameVerifier:
    """Dependency to get verifier instance."""
    return NameVerifier(store)


@router.post("/generate", response_model=GenerateResponse)
async def generate_name(
    request: GenerateRequest,
    generator: NameGenerator = Depends(get_generator)
):
    """Generate a target name from a prompt."""
    try:
        logger.info("Generate request received")
        prompt = sanitize_input(request.prompt)
        target_name = await generator.generate(prompt)
        logger.info("Name generated successfully")
        return GenerateResponse(target_name=target_name)
    
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        raise HTTPException(status_code=422, detail=str(e))
    except RuntimeError as e:
        logger.error(f"Generation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.post("/verify", response_model=VerifyResponse)
def verify_name(
    request: VerifyRequest,
    verifier: NameVerifier = Depends(get_verifier)
):
    """Verify a candidate name against the stored target."""
    try:
        logger.info("Verify request received")
        candidate = sanitize_input(request.candidate_name)
        result = verifier.verify(candidate)
        logger.info(f"Verification complete: match={result.match}, confidence={result.confidence:.2f}")
        return VerifyResponse(
            match=result.match,
            confidence=result.confidence,
            reason=result.reason
        )
    
    except ValueError as e:
        logger.warning(f"Verification error: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@router.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint."""
    return HealthResponse(status="ok")
