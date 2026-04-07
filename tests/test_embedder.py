# tests/test_embedder.py
import pytest
import sys
from pathlib import Path

# Добавляем backend в путь импорта
sys.path.insert(0, str(Path(__file__).parent.parent / "normocontroller" / "backend"))

from contour_b.embedder import Embedder


class TestEmbedder:
    def test_embed_returns_list(self):
        """Проверка, что embed возвращает список."""
        embedder = Embedder()
        result = embedder.embed("тестовый текст")
        assert isinstance(result, list)

    def test_embed_vector_length(self):
        """Проверка длины вектора (384 для MiniLM модели)."""
        embedder = Embedder()
        result = embedder.embed("тестовый текст")
        # Для MVP используется заглушка с вектором размера 768
        # В будущем будет 384 для paraphrase-multilingual-MiniLM-L12-v2
        assert len(result) in [384, 768]

    def test_embed_all_floats(self):
        """Проверка, что все элементы вектора - числа с плавающей точкой."""
        embedder = Embedder()
        result = embedder.embed("тестовый текст")
        for value in result:
            assert isinstance(value, float)

    def test_embed_batch_returns_list_of_lists(self):
        """Проверка, что embed_batch возвращает список списков."""
        embedder = Embedder()
        texts = ["текст 1", "текст 2", "текст 3"]
        result = embedder.embed_batch(texts)
        assert isinstance(result, list)
        for vec in result:
            assert isinstance(vec, list)

    def test_embed_batch_length_matches_input(self):
        """Проверка, что количество векторов совпадает с количеством входных текстов."""
        embedder = Embedder()
        texts = ["первый", "второй", "третий", "четвёртый"]
        result = embedder.embed_batch(texts)
        assert len(result) == len(texts)

    def test_embed_empty_string(self):
        """Проверка обработки пустой строки."""
        embedder = Embedder()
        result = embedder.embed("")
        assert isinstance(result, list)

    def test_embed_batch_empty_list(self):
        """Проверка обработки пустого списка."""
        embedder = Embedder()
        result = embedder.embed_batch([])
        assert isinstance(result, list)
        assert len(result) == 0
