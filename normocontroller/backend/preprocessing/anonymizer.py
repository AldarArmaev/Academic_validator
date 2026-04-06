"""Модуль анонимизации текста для защиты персональных данных."""

import re
from typing import List, Dict, Any


def anonymize_text(text: str) -> tuple[str, List[Dict[str, Any]]]:
    """Анонимизирует текст, заменяя персональные данные на плейсхолдеры.
    
    Args:
        text: Исходный текст
        
    Returns:
        Кортеж из:
            - анонимизированный текст
            - список заменённых сущностей
    """
    replacements = []
    
    # Паттерны для поиска персональных данных
    patterns = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\+?\d[\d\s\-\(\)]{7,}\d',
        "full_name": r'\b[A-Z][a-z]+\s+[A-Z][a-z]+\s+[A-Z][a-z]+\b',
    }
    
    anonymized_text = text
    
    for entity_type, pattern in patterns.items():
        matches = list(re.finditer(pattern, anonymized_text))
        for i, match in enumerate(matches):
            original = match.group()
            placeholder = f"[{entity_type.upper()}_{i}]"
            anonymized_text = anonymized_text.replace(original, placeholder, 1)
            replacements.append({
                "type": entity_type,
                "original": original,
                "placeholder": placeholder,
                "position": match.start()
            })
    
    return anonymized_text, replacements


def restore_anonymized_text(text: str, replacements: List[Dict[str, Any]]) -> str:
    """Восстанавливает оригинальный текст из анонимизированного.
    
    Args:
        text: Анонимизированный текст
        replacements: Список заменённых сущностей
        
    Returns:
        Оригинальный текст
    """
    restored_text = text
    for replacement in replacements:
        restored_text = restored_text.replace(
            replacement["placeholder"],
            replacement["original"]
        )
    return restored_text


def check_privacy_compliance(text: str) -> Dict[str, Any]:
    """Проверяет текст на наличие персональных данных.
    
    Args:
        text: Текст для проверки
        
    Returns:
        Словарь с результатами проверки
    """
    _, replacements = anonymize_text(text)
    
    return {
        "has_personal_data": len(replacements) > 0,
        "entities_found": len(replacements),
        "entity_types": list(set(r["type"] for r in replacements)),
        "details": replacements
    }
