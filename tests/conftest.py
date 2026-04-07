"""Фикстуры для тестов проекта Normocontroller."""

import pytest
from pathlib import Path
from docx import Document
import json

# Базовый путь к фикстурам
FIXTURES_DIR = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixture_path():
    """Возвращает функцию для получения пути к файлу в fixtures/."""
    def _get_path(name: str) -> Path:
        return FIXTURES_DIR / name
    return _get_path


@pytest.fixture
def rules():
    """Загружает university_rules.json."""
    rules_path = Path(__file__).parent.parent / "backend" / "university_rules.json"
    with open(rules_path, "r", encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def correct_doc(fixture_path):
    """Загружает correct.docx как объект Document."""
    doc_path = fixture_path("correct.docx")
    return Document(doc_path)
