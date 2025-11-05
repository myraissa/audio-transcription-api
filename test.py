import pytest
import requests
import os
from requests_mock import Mocker

API_URL = "http://localhost:8000"

# Fixture for the audio file path
@pytest.fixture
def audio_file_path():
    return r"C:\Users\myrai\OneDrive\Bureau\test-speech-to-text\engl_audio.mp3"

# Fixture for the video file path (replace with actual path when available)
@pytest.fixture
def video_file_path():
    return r"C:\Users\myrai\OneDrive\Bureau\test-speech-to-text\engl.mp4"  # Replace with your video file path

def test_health_check_success(requests_mock: Mocker):
    requests_mock.get(f"{API_URL}/", json={"status": "ok"})
    response = requests.get(f"{API_URL}/")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_transcribe_audio_file(audio_file_path, requests_mock: Mocker):
    # Ensure the audio file exists
    assert os.path.exists(audio_file_path), f"Audio file {audio_file_path} not found"

    # Mock the API response
    fake_result = {
        "success": True,
        "text": "hello world",  # Adjust based on expected transcription
        "detected_language": "English",
        "language_code": "en",
        "word_count": 2,
    }
    requests_mock.post(f"{API_URL}/transcribe", json=fake_result)

    # Read the actual audio file
    with open(audio_file_path, "rb") as audio_file:
        files = {"file": ("engl_audio.mp3", audio_file, "audio/mpeg")}
        response = requests.post(f"{API_URL}/transcribe", files=files)

    assert response.status_code == 200
    assert response.json()["success"]
    assert response.json()["detected_language"] == "English"
    assert response.json()["language_code"] == "en"

def test_transcribe_video_file(video_file_path, requests_mock: Mocker):
    # Ensure the video file exists
    assert os.path.exists(video_file_path), f"Video file {video_file_path} not found"

    # Mock the API response
    fake_result = {
        "success": True,
        "text": "hello world",  # Adjust based on expected transcription
        "detected_language": "English",
        "language_code": "en",
        "word_count": 2,
    }
    requests_mock.post(f"{API_URL}/transcribe", json=fake_result)

    # Read the actual video file
    with open(video_file_path, "rb") as video_file:
        files = {"file": ("sample_video.mp4", video_file, "video/mp4")}
        response = requests.post(f"{API_URL}/transcribe", files=files)

    assert response.status_code == 200
    assert response.json()["success"]
    assert response.json()["detected_language"] == "English"
    assert response.json()["language_code"] == "en"