import pytest
import json
from app import create_app

@pytest.fixture
def app():
    """Create and configure a test app."""
    app = create_app()
    app.config['TESTING'] = True
    return app

@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()

class TestPromptMatchingAPI:
    """Test cases for the Prompt Matching API."""
    
    def test_no_json_content_type(self, client):
        """Test request without JSON content type."""
        response = client.post('/api/match-prompt', data="not json")
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Content-Type must be application/json'
    
    def test_method_not_allowed(self, client):
        """Test unsupported HTTP methods."""
        response = client.get('/api/match-prompt')
        assert response.status_code == 405
        data = json.loads(response.data)
        assert 'Method not allowed' in data['error']
    
    def test_valid_prompt_1(self, client):
        """Test valid Prompt 1 matching."""
        payload = {
            "situation": "Commercial Auto",
            "level": "Structure",
            "file_type": "Summary Report",
            "data": "Test data"
        }
        response = client.post('/api/match-prompt', json=payload)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['matched_prompt'] == 'Prompt 1'
        assert data['status'] == 'success'
    
    def test_valid_prompt_2(self, client):
        """Test valid Prompt 2 matching."""
        payload = {
            "situation": "General Liability",
            "level": "Summarize",
            "file_type": "Deposition",
            "data": ""
        }
        response = client.post('/api/match-prompt', json=payload)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['matched_prompt'] == 'Prompt 2'
    
    def test_valid_prompt_3(self, client):
        """Test valid Prompt 3 matching."""
        payload = {
            "situation": "Commercial Auto",
            "level": "Summarize",
            "file_type": "Summons",
            "data": "Legal data"
        }
        response = client.post('/api/match-prompt', json=payload)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['matched_prompt'] == 'Prompt 3'
    
    def test_valid_prompt_4(self, client):
        """Test valid Prompt 4 matching."""
        payload = {
            "situation": "Workers Compensation",
            "level": "Structure",
            "file_type": "Medical Records",
            "data": "Medical data"
        }
        response = client.post('/api/match-prompt', json=payload)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['matched_prompt'] == 'Prompt 4'
    
    def test_valid_prompt_5(self, client):
        """Test valid Prompt 5 matching."""
        payload = {
            "situation": "Workers Compensation",
            "level": "Summarize",
            "file_type": "Summons",
            "data": "Legal document data"
        }
        response = client.post('/api/match-prompt', json=payload)
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['matched_prompt'] == 'Prompt 5'
    
    def test_missing_field(self, client):
        """Test missing data error."""
        payload = {
            "situation": "Commercial Auto",
            "level": "Structure",
            # missing file_type
            "data": "Test data"
        }
        response = client.post('/api/match-prompt', json=payload)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Missing Data'
    
    def test_empty_field(self, client):
        """Test empty field error."""
        payload = {
            "situation": "",
            "level": "Structure",
            "file_type": "Summary Report",
            "data": "Test data"
        }
        response = client.post('/api/match-prompt', json=payload)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Missing Data'
    
    def test_invalid_combination(self, client):
        """Test invalid prompt combination."""
        payload = {
            "situation": "Commercial Auto",
            "level": "Structure",
            "file_type": "Deposition",  # This combination doesn't exist
            "data": "Test data"
        }
        response = client.post('/api/match-prompt', json=payload)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Invalid Prompt'
    
    def test_invalid_situation(self, client):
        """Test invalid situation value."""
        payload = {
            "situation": "Invalid Situation",
            "level": "Structure",
            "file_type": "Summary Report",
            "data": "Test data"
        }
        response = client.post('/api/match-prompt', json=payload)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Invalid Prompt'
    
    def test_invalid_level(self, client):
        """Test invalid level value."""
        payload = {
            "situation": "Commercial Auto",
            "level": "Invalid Level",
            "file_type": "Summary Report",
            "data": "Test data"
        }
        response = client.post('/api/match-prompt', json=payload)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Invalid Prompt'
    
    def test_invalid_file_type(self, client):
        """Test invalid file_type value."""
        payload = {
            "situation": "Commercial Auto",
            "level": "Structure",
            "file_type": "Invalid File Type",
            "data": "Test data"
        }
        response = client.post('/api/match-prompt', json=payload)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['error'] == 'Invalid Prompt'