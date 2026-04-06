"""FastAPI приложение для системы проверки учебных работ 'Нормоконтролёр'."""

import os
import tempfile
import uuid
from datetime import datetime, timedelta
from typing import List

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse

from schemas import (
    ValidationReport,
    ReportSummary,
    ReportError,
    ErrorLocation
)
from contour_a.format_checker import validate_format

app = FastAPI(
    title="Нормоконтролёр API",
    description="Система автоматической проверки учебных работ на соответствие требованиям",
    version="1.0.0"
)


@app.get("/health")
async def health_check():
    """Проверка работоспособности сервиса."""
    return {"status": "ok"}


@app.post("/validate/format", response_model=ValidationReport)
async def validate_format_endpoint(file: UploadFile = File(...)):
    """Проверка форматирования документа.
    
    Принимает .docx файл и возвращает отчёт о найденных ошибках форматирования.
    """
    # Проверка расширения файла
    if not file.filename.lower().endswith('.docx'):
        raise HTTPException(
            status_code=400,
            detail="Только файлы формата .docx поддерживаются"
        )
    
    # Сохранение временного файла
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
            content = await file.read()
            tmp_file.write(content)
            tmp_path = tmp_file.name
        
        # Запуск проверки
        report = validate_format(tmp_path)
        
        return report
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка при обработке файла: {str(e)}"
        )
    
    finally:
        # Удаление временного файла
        if 'tmp_path' in locals():
            try:
                os.unlink(tmp_path)
            except:
                pass


@app.post("/validate/semantic", response_model=ValidationReport)
async def validate_semantic_endpoint(file: UploadFile = File(...)):
    """Семантическая проверка документа (заглушка).
    
    В будущих версиях будет выполнять проверку стиля, цитирования
    и содержания с использованием RAG и LLM.
    """
    # Заглушка: возвращает пустой отчёт
    return ValidationReport(
        doc_id=str(uuid.uuid4()),
        session_expires_at=datetime.utcnow() + timedelta(hours=24),
        summary=ReportSummary(
            total_errors=0,
            formatting=0,
            style=0,
            citations=0
        ),
        errors=[]
    )


@app.post("/validate", response_model=ValidationReport)
async def validate_full_endpoint(file: UploadFile = File(...)):
    """Полная проверка документа (форматирование + семантика) (заглушка).
    
    В будущих версиях будет объединять результаты Контур А и Контур Б.
    """
    # Заглушка: возвращает пустой отчёт
    return ValidationReport(
        doc_id=str(uuid.uuid4()),
        session_expires_at=datetime.utcnow() + timedelta(hours=24),
        summary=ReportSummary(
            total_errors=0,
            formatting=0,
            style=0,
            citations=0
        ),
        errors=[]
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
