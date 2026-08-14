"""Lightweight REST API wrapper for IndianConstitution using FastAPI."""

from typing import Any, Dict, List

from .. import get_constitution

try:
    from fastapi import FastAPI, HTTPException, Query  # type: ignore[import-untyped]

    FASTAPI_AVAILABLE = True
except ImportError:
    FASTAPI_AVAILABLE = False

if FASTAPI_AVAILABLE:
    app = FastAPI(
        title="IndianConstitution REST API",
        description="Programmatic HTTP REST endpoints for the Constitution of India.",
        version="1.5.0",
    )

    @app.get("/")
    def root() -> Dict[str, Any]:
        """API Root health check endpoint."""
        return {
            "name": "IndianConstitution REST API",
            "version": "1.5.0",
            "docs": "/docs",
            "status": "healthy",
        }

    @app.get("/api/v1/articles/{number}")
    def get_article(number: str) -> Dict[str, Any]:
        """Retrieve an article by number."""
        ic = get_constitution()
        article = ic.get_article(number)
        if not article:
            raise HTTPException(status_code=404, detail=f"Article {number} not found")
        result: Dict[str, Any] = article.model_dump()
        return result

    @app.get("/api/v1/search")
    def search(q: str, limit: int = Query(10, ge=1, le=100)) -> List[Dict[str, Any]]:
        """Search articles by keyword."""
        ic = get_constitution()
        results = ic.search(q, limit=limit)
        return [r.model_dump() for r in results]

    @app.get("/api/v1/preamble")
    def preamble() -> Dict[str, str]:
        """Get Preamble text."""
        ic = get_constitution()
        return {"preamble": ic.preamble}

    @app.get("/api/v1/cases/{number}")
    def get_cases(number: str) -> List[Dict[str, Any]]:
        """Get landmark Supreme Court judgments linked to an article."""
        ic = get_constitution()
        cases = ic.get_related_cases(number)
        return [c.model_dump() for c in cases]

    @app.get("/api/v1/amendments/{number}")
    def get_amendments(number: str) -> List[Dict[str, Any]]:
        """Get amendment history for an article."""
        ic = get_constitution()
        events = ic.get_amendment_history(number)
        return [e.model_dump() for e in events]

    @app.get("/api/v1/duties/{number}")
    def get_duties(number: str) -> List[Dict[str, Any]]:
        """Get duty cross-references for a fundamental right."""
        ic = get_constitution()
        duties = ic.get_related_duties(number)
        return [d.model_dump() for d in duties]

    @app.get("/api/v1/graph/related/{number}")
    def get_graph_related(number: str) -> Dict[str, List[str]]:
        """Get referenced and referencing articles."""
        ic = get_constitution()
        graph_data: Dict[str, List[str]] = ic.get_related_articles(number)
        return graph_data


else:
    app = None  # type: ignore[assignment]
