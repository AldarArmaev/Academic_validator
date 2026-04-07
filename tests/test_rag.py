# tests/test_rag.py
import pytest
import sys
from pathlib import Path

# Добавляем backend в путь импорта
sys.path.insert(0, str(Path(__file__).parent.parent / "normocontroller" / "backend"))

from contour_b.rag import RAGSystem


class TestRAGSystem:
    def test_rag_init_empty(self):
        """Проверка инициализации RAG системы с пустым списком документов."""
        rag = RAGSystem()
        assert hasattr(rag, 'documents')
        assert isinstance(rag.documents, list)
        assert len(rag.documents) == 0

    def test_add_documents_increases_count(self):
        """Проверка, что добавление документов увеличивает счётчик."""
        rag = RAGSystem()
        initial_count = len(rag.documents)
        rag.add_documents([{"text": "Тестовый документ", "metadata": {"source": "test"}}])
        assert len(rag.documents) > initial_count

    def test_add_documents_preserves_fields(self):
        """Проверка, что добавленные документы сохраняют поля."""
        rag = RAGSystem()
        doc = {"text": "Сохранённый текст", "metadata": {"key": "value"}}
        rag.add_documents([doc])
        assert rag.documents[0]["text"] == "Сохранённый текст"
        assert rag.documents[0]["metadata"]["key"] == "value"

    def test_retrieve_returns_list(self):
        """Проверка, что retrieve возвращает список."""
        rag = RAGSystem()
        result = rag.retrieve("запрос")
        assert isinstance(result, list)

    def test_retrieve_top_k_respected(self):
        """Проверка соблюдения параметра top_k."""
        rag = RAGSystem()
        # Добавляем несколько документов
        for i in range(10):
            rag.add_documents([{"text": f"Документ {i}", "metadata": {"id": i}}])
        result = rag.retrieve("запрос", top_k=3)
        assert isinstance(result, list)
        assert len(result) <= 3

    def test_retrieve_empty_without_documents(self):
        """Проверка, что retrieve возвращает пустой список без документов."""
        rag = RAGSystem()
        result = rag.retrieve("любой запрос")
        assert result == []

    def test_generate_answer_returns_string(self):
        """Проверка, что generate_answer возвращает строку."""
        rag = RAGSystem()
        result = rag.generate_answer("вопрос", [])
        assert isinstance(result, str)

    def test_generate_answer_not_empty(self):
        """Проверка, что generate_answer возвращает непустую строку."""
        rag = RAGSystem()
        result = rag.generate_answer("вопрос", [])
        assert len(result) > 0
