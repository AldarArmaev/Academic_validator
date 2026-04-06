from datetime import datetime
from typing import Literal, List, Optional
from pydantic import BaseModel, Field


class ErrorLocation(BaseModel):
    """Местоположение ошибки в документе."""
    page: int = Field(..., description="Номер страницы")
    paragraph_index: int = Field(..., description="Индекс абзаца на странице")
    chapter: Optional[str] = Field(None, description="Название главы/раздела")


class ReportError(BaseModel):
    """Описание найденной ошибки."""
    id: str = Field(..., description="Уникальный идентификатор ошибки")
    type: Literal["formatting", "style", "citation_check"] = Field(
        ..., description="Тип ошибки"
    )
    severity: Literal["error", "warning", "info"] = Field(
        ..., description="Серьёзность ошибки"
    )
    location: ErrorLocation = Field(..., description="Местоположение ошибки")
    fragment: str = Field(..., description="Фрагмент текста с ошибкой")
    rule: str = Field(..., description="Описание нарушенного правила")
    found_value: str = Field(..., description="Найденное значение")
    expected_value: str = Field(..., description="Ожидаемое значение")
    recommendation: str = Field(..., description="Рекомендация по исправлению")


class ReportSummary(BaseModel):
    """Сводная статистика по отчёту."""
    total_errors: int = Field(..., description="Общее количество ошибок")
    formatting: int = Field(..., description="Ошибки форматирования")
    style: int = Field(..., description="Стилистические ошибки")
    citations: int = Field(..., description="Проблемы с цитированием")


class ValidationReport(BaseModel):
    """Полный отчёт о проверке документа."""
    doc_id: str = Field(..., description="Идентификатор документа")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Время создания отчёта")
    session_expires_at: datetime = Field(..., description="Время истечения сессии")
    summary: ReportSummary = Field(..., description="Сводная статистика")
    errors: List[ReportError] = Field(default_factory=list, description="Список ошибок")
