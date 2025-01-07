import json
import os
from pathlib import Path
from typing import Tuple
import pytest

from flask import Flask, Response, jsonify, request
from presidio_analyzer import AnalyzerEngine, AnalyzerEngineProvider, AnalyzerRequest
from werkzeug.exceptions import HTTPException, UnsupportedMediaType

from presidio_analyzer.nlp_engine.transformers_nlp_engine import TransformersNlpEngine


class TestServer:
    def __init__(self):
        self.app = Flask(__name__)

        analyzer_conf_file =  Path(__file__).parent.parent / "presidio_analyzer" / "conf" / "default_analyzer.yaml"
        nlp_engine_conf_file = Path(__file__).parent.parent / 'presidio_analyzer' / 'conf' / 'transformers.yaml'
        recognizer_registry_conf_file =  Path(__file__).parent.parent / "presidio_analyzer" / "conf" / "default_recognizers.yaml"

        self.engine: AnalyzerEngine = AnalyzerEngineProvider(
            analyzer_engine_conf_file=analyzer_conf_file,
            nlp_engine_conf_file=nlp_engine_conf_file,
            recognizer_registry_conf_file=recognizer_registry_conf_file
        ).create_engine()
        assert isinstance(self.engine.nlp_engine, TransformersNlpEngine)

        @self.app.route("/health")
        def health() -> str:
            """Return basic health probe result."""
            return "Presidio Analyzer service is up"

        @self.app.route("/analyze", methods=["POST"])
        def analyze() -> Tuple[str, int]:
            """Execute the analyzer function."""
            # Parse the request params
            try:
                req_data = AnalyzerRequest(request.get_json())
                if not req_data.text:
                    raise KeyError("No text provided")

                if not req_data.language:
                    raise KeyError("No language provided")

                recognizer_result_list = self.engine.analyze(
                    text=req_data.text,
                    language=req_data.language,
                    correlation_id=req_data.correlation_id,
                    score_threshold=req_data.score_threshold,
                    entities=req_data.entities,
                    return_decision_process=req_data.return_decision_process,
                    ad_hoc_recognizers=req_data.ad_hoc_recognizers,
                    context=req_data.context,
                )

                return Response(
                    json.dumps(
                        recognizer_result_list,
                        default=lambda o: o.to_dict(),
                        sort_keys=True
                    ),
                    content_type="application/json",
                )
            except TypeError as te:
                error_msg = (
                    f"Failed to parse /analyze request "
                    f"for AnalyzerEngine.analyze(). {e.args[0]}"
                )
                return jsonify(error=error_msg), 400
            except UnsupportedMediaType as e:
                return jsonify(error=e.description), 415
            except Exception as e:
                return jsonify(error=e.args[0]), 500

        @self.app.errorhandler(HTTPException)
        def http_exception(e):
            return jsonify(error=e.description), e.code



@pytest.fixture
def client():
    server = TestServer()
    server.app.testing = True
    with server.app.test_client() as client:
        yield client

def test_health(client):
    """Test the /health endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data.decode('utf-8') == 'Presidio Analyzer service is up'

def test_analyze(client):
    """Test the /analyze endpoint."""
    sample_data = {
        "text": "My name is Alex",
        "language": "en"
    }
    response = client.post('/analyze', json=sample_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

    sample_data = {
        "text": "There are no names.",
        "language": "en"
    }
    response = client.post('/analyze', json=sample_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)

def test_analyze_invalid_data(client):
    """Test the /analyze endpoint with invalid data."""
    response = client.post('/analyze', data="Invalid data")
    assert response.status_code == 415
    data = json.loads(response.data)
    assert "error" in data

def test_analyze_invalid_json(client):
    """Test the /analyze endpoint with invalid data."""
    response = client.post('/analyze', json={"invalid": "Some text"})
    assert response.status_code == 500
    data = json.loads(response.data)
    assert "error" in data


@pytest.mark.parametrize("sentence,language", [
    ("My name is Alex.", "en"),
    ("Je m’appelle Alex.", "fr"),
    ("Mi chiamo Alex.", "it"),
    ("Me llamo Alex", "es"),
    ("Mein Name ist Alex.", "de")
])
def test_analyze_person(client, sentence, language):
    """Test the /analyze endpoint."""
    sample_data = {
        "text": sentence,
        "language": language
    }
    response = client.post('/analyze', json=sample_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data)==1


@pytest.mark.parametrize("sentence,language", [
    ("Here is my email: alex.smith@gmail.com.", "en"),
    ("Voici mon email : alex.smith@gmail.com.", "fr"),
    ("Ecco la mia email: alex.smith@gmail.com.", "it"),
    ("Aquí tienes mi correo electrónico: alex.smith@gmail.com.", "es"),
    ("Hier ist meine E-Mail: alex.smith@gmail.com.", "de")
])
def test_analyze_email(client, sentence, language):
    """Test the /analyze endpoint."""
    sample_data = {
        "text": sentence,
        "language": language
    }
    response = client.post('/analyze', json=sample_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data)>=1


@pytest.mark.parametrize("sentence,language", [
    ("I will send you all the details of our meeting. We can then discuss about this in the Café titon in 34 Rue Titon, 75011 Paris, France.", "en"),
    ("Je vous enverrai tous les détails de notre réunion. Nous pourrons ensuite en discuter au Café Titon au 34 Rue Titon, 75011 Paris, France.", "fr"),
    ("Ti invierò tutti i dettagli del nostro incontro. Poi potremo discuterne al Café Titon in 34 Rue Titon, 75011 Parigi, Francia.", "it"),
    ("Te enviaré todos los detalles de nuestra reunión. Luego podremos hablar de esto en el Café Titon en 34 Rue Titon, 75011 París, Francia.", "es"),
    ("Ich werde Ihnen alle Details unseres Treffens zusenden. Dann können wir im Café Titon in der Rue Titon 34, 75011 Paris, Frankreich darüber sprechen.", "de")
])
def test_analyze_location(client, sentence, language):
    """Test the /analyze endpoint."""
    sample_data = {
        "text": sentence,
        "language": language
    }
    response = client.post('/analyze', json=sample_data)
    assert response.status_code == 200
    data = json.loads(response.data)
    assert isinstance(data, list)
    assert len(data)>=1