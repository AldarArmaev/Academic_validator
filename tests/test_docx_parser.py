# tests/test_docx_parser.py
import pytest
import sys
from pathlib import Path

# Добавляем backend в путь импорта
sys.path.insert(0, str(Path(__file__).parent.parent / "normocontroller" / "backend"))

from preprocessing.docx_parser import parse_docx, extract_text_from_docx


class TestDocxParser:
    def test_parse_docx_returns_paragraphs(self, fixture_path):
        """Проверка, что parse_docx возвращает абзацы."""
        result = parse_docx(str(fixture_path("correct.docx")))
        assert "paragraphs" in result
        assert isinstance(result["paragraphs"], list)
        assert len(result["paragraphs"]) > 0

    def test_parse_docx_paragraph_has_required_keys(self, fixture_path):
        """Проверка, что каждый абзац имеет требуемые ключи."""
        result = parse_docx(str(fixture_path("correct.docx")))
        for para in result["paragraphs"]:
            assert "text" in para
            assert "style" in para
            assert "runs_count" in para

    def test_parse_docx_returns_metadata(self, fixture_path):
        """Проверка, что parse_docx возвращает метаданные."""
        result = parse_docx(str(fixture_path("correct.docx")))
        assert "metadata" in result
        assert isinstance(result["metadata"], dict)
        assert "total_paragraphs" in result["metadata"]
        assert "total_pages" in result["metadata"]

    def test_parse_docx_total_pages_positive(self, fixture_path):
        """Проверка, что количество страниц положительное."""
        result = parse_docx(str(fixture_path("correct.docx")))
        assert result["metadata"]["total_pages"] >= 1

    def test_extract_text_returns_string(self, fixture_path):
        """Проверка, что extract_text_from_docx возвращает строку."""
        text = extract_text_from_docx(str(fixture_path("correct.docx")))
        assert isinstance(text, str)

    def test_extract_text_not_empty(self, fixture_path):
        """Проверка, что извлечённый текст не пустой."""
        text = extract_text_from_docx(str(fixture_path("correct.docx")))
        assert len(text) > 0

    def test_estimate_pages_multipage(self, fixture_path):
        """Проверка оценки количества страниц для многостраничного документа."""
        # Используем parse_docx вместо несуществующей estimate_pages
        result = parse_docx(str(fixture_path("all_violations.docx")))
        total_pages = result["metadata"]["total_pages"]
        # Документ должен содержать минимум 2 страницы
        assert total_pages >= 2

    def test_parse_invalid_path_raises(self, fixture_path):
        """Проверка, что неверный путь вызывает исключение."""
        with pytest.raises(Exception):
            parse_docx("/nonexistent/path/to/file.docx")
