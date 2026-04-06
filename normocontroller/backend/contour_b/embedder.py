"""Модуль для создания эмбеддингов текста."""

from typing import List


class Embedder:
    """Класс для генерации векторных представлений текста.
    
    Для MVP используется заглушка. В будущем будет интегрирован
    с реальной моделью (например, sentence-transformers).
    """
    
    def __init__(self, model_name: str = "default"):
        self.model_name = model_name
    
    def embed(self, text: str) -> List[float]:
        """Создаёт эмбеддинг для текста.
        
        Args:
            text: Текст для векторизации
            
        Returns:
            Список чисел, представляющих вектор
        """
        # Заглушка: возвращает фиктивный вектор
        return [0.0] * 768
    
    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Создаёт эмбеддинги для списка текстов.
        
        Args:
            texts: Список текстов для векторизации
            
        Returns:
            Список векторов
        """
        return [self.embed(text) for text in texts]
