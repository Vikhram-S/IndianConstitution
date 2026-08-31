"""REST API server implementation using FastAPI for IndianConstitution."""

from typing import Any, Dict, List, Optional

from ..core.engine import Constitution

try:
    from fastapi import FastAPI, HTTPException, Query

    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False


def create_app() -> Optional[Any]:  # noqa: ANN401
    """Factory function to construct FastAPI app instance."""
    if not FASTAPI_AVAILABLE:
        return None

    app = FastAPI(
        title="IndianConstitution REST API",
        description="Programmatic HTTP REST endpoints for the Constitution of India.",
        version="1.5.3",
    )
    ic = Constitution()

    @app.get("/")
    def root() -> Dict[str, Any]:
        """API Root health check endpoint."""
        return {
            "name": "IndianConstitution REST API",
            "version": "1.5.3",
            "docs": "/docs",
            "status": "healthy",
        }

    @app.get("/api/v1/articles/{number}")
    def get_article(number: str) -> Dict[str, Any]:
        """Retrieve an article by number."""
        article = ic.get_article(number)
        if not article:
            raise HTTPException(status_code=404, detail=f"Article '{number}' not found.")
        result: Dict[str, Any] = article.model_dump()
        return result

    @app.get("/api/v1/search")
    def search(q: str, limit: int = Query(10, ge=1, le=100)) -> List[Dict[str, Any]]:
        """Search articles by keyword."""
        results = ic.search(q, limit=limit)
        return [r.model_dump() for r in results]

    @app.get("/api/v1/preamble")
    def preamble() -> Dict[str, str]:
        """Get Preamble text."""
        return {"preamble": ic.preamble}

    @app.get("/api/v1/cases/{number}")
    def get_cases(number: str) -> List[Dict[str, Any]]:
        """Get landmark Supreme Court judgments linked to an article."""
        cases = ic.get_related_cases(number)
        return [c.model_dump() for c in cases]

    @app.get("/api/v1/amendments/{number}")
    def get_amendments(number: str) -> List[Dict[str, Any]]:
        """Get amendment history for an article."""
        events = ic.get_amendment_history(number)
        return [e.model_dump() for e in events]

    @app.get("/api/v1/duties/{number}")
    def get_duties(number: str) -> List[Dict[str, Any]]:
        """Get duty cross-references for a fundamental right."""
        duties = ic.get_related_duties(number)
        return [d.model_dump() for d in duties]

    @app.get("/api/v1/graph/related/{number}")
    def get_graph_related(number: str) -> Dict[str, List[str]]:
        """Get referenced and referencing articles."""
        graph_data: Dict[str, List[str]] = ic.get_related_articles(number)
        return graph_data

    return app


app = create_app()
