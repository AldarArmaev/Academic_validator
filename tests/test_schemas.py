# tests/test_schemas.py
import pytest
from datetime import datetime, timedelta
from pydantic import ValidationError
import sys
from pathlib import Path

# Добавляем backend в путь импорта
sys.path.insert(0, str(Path(__file__).parent.parent / "normocontroller" / "backend"))

from schemas import ErrorLocation, ReportError, ReportSummary, ValidationReport


class TestErrorLocation:
    def test_error_location_valid(self):
        """Проверка создания валидного ErrorLocation."""
        location = ErrorLocation(
            page=1,
            paragraph_index=5,
            chapter="Введение"
        )
        assert location.page == 1
        assert location.paragraph_index == 5
        assert location.chapter == "Введение"

    def test_error_location_chapter_optional(self):
        """Проверка, что chapter является необязательным полем."""
        location = ErrorLocation(
            page=2,
            paragraph_index=10
        )
        assert location.page == 2
        assert location.paragraph_index == 10
        assert location.chapter is None


class TestReportError:
    def test_report_error_valid(self):
        """Проверка создания валидного ReportError."""
        error = ReportError(
            id="error_001",
            type="formatting",
            severity="error",
            location=ErrorLocation(page=1, paragraph_index=0),
            fragment="Неверный шрифт",
            rule="Шрифт должен быть Times New Roman",
            found_value="Arial",
            expected_value="Times New Roman",
            recommendation="Измените шрифт на Times New Roman"
        )
        assert error.id == "error_001"
        assert error.type == "formatting"
        assert error.severity == "error"
        assert error.fragment == "Неверный шрифт"

    def test_report_error_invalid_type(self):
        """Проверка отклонения недопустимого типа ошибки."""
        with pytest.raises(ValidationError):
            ReportError(
                id="error_002",
                type="invalid_type",
                severity="error",
                location=ErrorLocation(page=1, paragraph_index=0),
                fragment="Тест",
                rule="Правило",
                found_value="Значение",
                expected_value="Ожидаемое",
                recommendation="Рекомендация"
            )

    def test_report_error_invalid_severity(self):
        """Проверка отклонения недопустимой серьёзности ошибки."""
        with pytest.raises(ValidationError):
            ReportError(
                id="error_003",
                type="formatting",
                severity="critical",
                location=ErrorLocation(page=1, paragraph_index=0),
                fragment="Тест",
                rule="Правило",
                found_value="Значение",
                expected_value="Ожидаемое",
                recommendation="Рекомендация"
            )


class TestReportSummary:
    def test_report_summary_counts(self):
        """Проверка подсчёта ошибок в сводке."""
        summary = ReportSummary(
            total_errors=10,
            formatting=5,
            style=3,
            citations=2
        )
        assert summary.total_errors == 10
        assert summary.formatting == 5
        assert summary.style == 3
        assert summary.citations == 2


class TestValidationReport:
    def test_validation_report_has_doc_id(self):
        """Проверка наличия doc_id в отчёте."""
        report = ValidationReport(
            doc_id="test-doc-123",
            session_expires_at=datetime.utcnow() + timedelta(hours=24),
            summary=ReportSummary(
                total_errors=0,
                formatting=0,
                style=0,
                citations=0
            ),
            errors=[]
        )
        assert report.doc_id == "test-doc-123"
        assert isinstance(report.created_at, datetime)

    def test_validation_report_session_expires(self):
        """Проверка времени истечения сессии."""
        expires_at = datetime.utcnow() + timedelta(hours=48)
        report = ValidationReport(
            doc_id="test-doc-456",
            session_expires_at=expires_at,
            summary=ReportSummary(
                total_errors=0,
                formatting=0,
                style=0,
                citations=0
            ),
            errors=[]
        )
        assert report.session_expires_at == expires_at
        # Проверяем, что сессия ещё не истекла
        assert report.session_expires_at > datetime.utcnow()
