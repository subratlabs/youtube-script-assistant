from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

from app.main import app
from app.routers import saved_scripts as saved_scripts_router


client = TestClient(app)


def test_generate_titles_returns_503_when_gemini_fails():
    with patch(
        "app.routers.topic.generate_content",
        side_effect=Exception("Simulated Gemini API failure"),
    ):
        response = client.post(
            "/api/generate-titles",
            json={
                "topic": "Python for Beginners",
                "target_audience": "Beginners",
                "language": "English",
                "duration": 5,
                "content_type": "Tutorial",
                "tone": "Friendly",
                "instructions": None,
            },
        )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Unable to generate titles right now. Please try again later."
    )


def test_generate_hooks_returns_503_when_gemini_fails():
    with patch(
        "app.routers.hooks.generate_content",
        side_effect=Exception("Simulated Gemini API failure"),
    ):
        response = client.post(
            "/api/generate-hooks",
            json={
                "topic": "Python for Beginners",
                "target_audience": "Beginners",
                "language": "English",
                "duration": 5,
                "content_type": "Tutorial",
                "tone": "Friendly",
                "instructions": None,
            },
        )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Unable to generate hooks right now. Please try again later."
    )


def test_save_script_rolls_back_when_commit_fails():
    mock_db = MagicMock()
    mock_db.commit.side_effect = Exception("Simulated database failure")

    def override_get_db():
        yield mock_db

    app.dependency_overrides[
        saved_scripts_router.get_db
    ] = override_get_db

    try:
        response = client.post(
            "/api/saved-scripts/",
            json={
                "topic": "Python for Beginners",
                "title": "Learn Python",
                "content": "Introduction to Python.",
            },
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 500
    assert response.json()["detail"] == (
        "Unable to save the script right now. Please try again later."
    )
    mock_db.rollback.assert_called_once()



def test_generate_visuals_returns_503_when_response_is_empty():
    with patch(
        "app.routers.visuals.generate_content",
        return_value="",
    ):
        response = client.post(
            "/api/generate-visuals",
            json={
                "topic": "Python for Beginners",
                "target_audience": "Beginners",
                "language": "English",
                "duration": 5,
                "content_type": "Tutorial",
                "tone": "Friendly",
                "instructions": None,
                "selected_title": "Learn Python Basics",
                "script": (
                "Welcome to Python for beginners. "
                "Today we will learn variables, data types, and simple examples."
              ),
            },
        )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Gemini returned an empty response. Please try again later."
    )


def test_generate_visuals_returns_502_when_response_is_invalid_json():
    with patch(
        "app.routers.visuals.generate_content",
        return_value="not valid JSON",
    ):
        response = client.post(
            "/api/generate-visuals",
            json={
                "topic": "Python for Beginners",
                "target_audience": "Beginners",
                "language": "English",
                "duration": 5,
                "content_type": "Tutorial",
                "tone": "Friendly",
                "instructions": None,
                "tone": "Friendly",
                "instructions": None,
                "selected_title": "Learn Python Basics",
                "script": (
                "Welcome to Python for beginners. "
                "Today we will learn variables, data types, and simple examples."
             ),
        },
            
        )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Gemini returned an invalid visual suggestions response."
    )




def test_generate_description_returns_503_when_response_is_empty():
    with patch(
        "app.routers.description.generate_content",
        return_value="",
    ):
        response = client.post(
            "/api/generate-description",
            json={
                "topic": "Python for Beginners",
                "target_audience": "Beginners",
                "language": "English",
                "duration": 5,
                "content_type": "Tutorial",
                "tone": "Friendly",
                "instructions": None,
                "selected_title": "Learn Python Basics",
                "script": (
                    "Welcome to Python for beginners. "
                    "Today we will learn variables, data types, and simple examples."
                ),
            },
        )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Gemini returned an empty response. Please try again later."
    )


def test_generate_description_returns_502_when_response_is_invalid_json():
    with patch(
        "app.routers.description.generate_content",
        return_value="not valid JSON",
    ):
        response = client.post(
            "/api/generate-description",
            json={
                "topic": "Python for Beginners",
                "target_audience": "Beginners",
                "language": "English",
                "duration": 5,
                "content_type": "Tutorial",
                "tone": "Friendly",
                "instructions": None,
                "selected_title": "Learn Python Basics",
                "script": (
                    "Welcome to Python for beginners. "
                    "Today we will learn variables, data types, and simple examples."
                ),
            },
        )

    assert response.status_code == 502
    assert response.json()["detail"] == (
        "Gemini returned an invalid description response."
    )



def test_regenerate_section_returns_503_when_response_is_empty():
    with patch(
        "app.routers.regeneration.generate_content",
        return_value="",
    ):
        response = client.post(
            "/api/regenerate-section",
            json={
                "topic": "Python for Beginners",
                "target_audience": "Beginners",
                "language": "English",
                "duration": 5,
                "content_type": "Tutorial",
                "tone": "Friendly",
                "instructions": None,
                "selected_title": "Learn Python Basics",
                "section_name": "Introduction",
                "current_section": (
                    "Welcome to this beginner-friendly Python tutorial."
                ),
                "full_script": (
                    "Welcome to Python for beginners. "
                    "Today we will learn variables, data types, and simple examples."
                ),
            },
        )

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Gemini returned an empty response. Please try again later."
    )



def test_generate_script_returns_503_when_response_is_empty():
    payload = {
        "topic": "Python for Beginners",
        "target_audience": "Beginners",
        "language": "Hindi",
        "duration": 5,
        "content_type": "Tutorial",
        "tone": "Friendly",
        "instructions": "",
        "selected_title": "Learn Python Basics",
        "selected_hook": "Want to learn Python easily?",
        "outline": ["Introduction", "Python basics", "Conclusion"]
    }

    with patch("app.routers.script.generate_content", return_value=""):
        response = client.post("/api/generate-script", json=payload)

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Gemini returned an empty response. Please try again later."
    )



def test_generate_script_returns_503_when_gemini_fails():
    payload = {
        "topic": "Python for Beginners",
        "target_audience": "Beginners",
        "language": "Hindi",
        "duration": 5,
        "content_type": "Tutorial",
        "tone": "Friendly",
        "instructions": "",
        "selected_title": "Learn Python Basics",
        "selected_hook": "Want to learn Python easily?",
        "outline": ["Introduction", "Python basics", "Conclusion"]
    }

    with patch(
        "app.routers.script.generate_content",
        side_effect=Exception("Simulated Gemini failure")
    ):
        response = client.post("/api/generate-script", json=payload)

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Unable to generate the script right now. Please try again later."
    )



def test_regenerate_section_returns_503_when_gemini_fails():
    payload = {
        "topic": "Python for Beginners",
        "target_audience": "Beginners",
        "language": "Hindi",
        "duration": 5,
        "content_type": "Tutorial",
        "tone": "Friendly",
        "instructions": "",
        "selected_title": "Learn Python Basics",
        "section_name": "Introduction",
        "current_section": "Python is a beginner-friendly programming language.",
        "full_script": "Introduction: Python is beginner-friendly. Main section: Learn variables and data types. Conclusion: Practice coding every day."
    }

    with patch(
        "app.routers.regeneration.generate_content",
        side_effect=Exception("Simulated Gemini failure")
    ):
        response = client.post("/api/regenerate-section", json=payload)

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Unable to regenerate the section right now. Please try again later."
    )



def test_update_script_rolls_back_when_commit_fails():
    mock_db = MagicMock()
    mock_script = MagicMock()
    mock_script.id = 1

    mock_db.query.return_value.filter.return_value.first.return_value = mock_script
    mock_db.commit.side_effect = Exception("Simulated database failure")

    app.dependency_overrides[saved_scripts_router.get_db] = lambda: mock_db

    payload = {
        "topic": "Python for Beginners",
        "title": "Updated Python Tutorial",
        "content": "Updated script content"
    }

    try:
        response = client.put("/api/saved-scripts/1", json=payload)

        assert response.status_code == 500
        assert response.json()["detail"] == (
            "Unable to update the saved script right now. Please try again later."
        )
        mock_db.rollback.assert_called_once()
    finally:
        app.dependency_overrides.clear()



def test_delete_script_rolls_back_when_commit_fails():
    mock_db = MagicMock()
    mock_script = MagicMock()
    mock_script.id = 1

    mock_db.query.return_value.filter.return_value.first.return_value = mock_script
    mock_db.commit.side_effect = Exception("Simulated database failure")

    app.dependency_overrides[saved_scripts_router.get_db] = lambda: mock_db

    try:
        response = client.delete("/api/saved-scripts/1")

        assert response.status_code == 500
        assert response.json()["detail"] == (
            "Unable to delete the saved script right now. Please try again later."
        )
        mock_db.rollback.assert_called_once()
    finally:
        app.dependency_overrides.clear()



def test_generate_outline_returns_503_when_gemini_fails():
    payload = {
        "topic": "Python for Beginners",
        "target_audience": "Beginners",
        "language": "Hindi",
        "duration": 5,
        "content_type": "Tutorial",
        "tone": "Friendly",
        "instructions": ""
    }

    with patch(
        "app.routers.outline.generate_content",
        side_effect=Exception("Simulated Gemini failure")
    ):
        response = client.post("/api/generate-outline", json=payload)

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Unable to generate the outline right now. Please try again later."
    )



def test_generate_visuals_returns_503_when_gemini_fails():
    payload = {
        "topic": "Python for Beginners",
        "target_audience": "Beginners",
        "language": "Hindi",
        "duration": 5,
        "content_type": "Tutorial",
        "tone": "Friendly",
        "instructions": "",
        "selected_title": "Learn Python Basics",
        "script": (
            "Python is a beginner-friendly programming language. "
            "In this video, we will learn variables and data types."
        )
    }

    with patch(
        "app.routers.visuals.generate_content",
        side_effect=Exception("Simulated Gemini failure")
    ):
        response = client.post("/api/generate-visuals", json=payload)

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Unable to generate visual suggestions right now. Please try again later."
    )



def test_generate_description_returns_503_when_gemini_fails():
    payload = {
        "topic": "Python for Beginners",
        "target_audience": "Beginners",
        "language": "Hindi",
        "duration": 5,
        "content_type": "Tutorial",
        "tone": "Friendly",
        "instructions": "",
        "selected_title": "Learn Python Basics",
        "script": (
            "Python is a beginner-friendly programming language. "
            "In this video, we will learn variables and data types."
        )
    }

    with patch(
        "app.routers.description.generate_content",
        side_effect=Exception("Simulated Gemini failure")
    ):
        response = client.post("/api/generate-description", json=payload)

    assert response.status_code == 503
    assert response.json()["detail"] == (
        "Unable to generate the description right now. Please try again later."
    )



def test_get_saved_script_returns_404_when_not_found():
    mock_db = MagicMock()
    mock_db.query.return_value.filter.return_value.first.return_value = None

    app.dependency_overrides[saved_scripts_router.get_db] = lambda: mock_db

    try:
        response = client.get("/api/saved-scripts/999999")

        assert response.status_code == 404
        assert response.json()["detail"] == "Saved script not found"
    finally:
        app.dependency_overrides.clear()