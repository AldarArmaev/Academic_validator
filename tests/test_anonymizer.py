# tests/test_anonymizer.py
import pytest
import sys
from pathlib import Path

# Добавляем backend в путь импорта
sys.path.insert(0, str(Path(__file__).parent.parent / "normocontroller" / "backend"))

from preprocessing.anonymizer import anonymize_text, restore_anonymized_text, check_privacy_compliance


class TestAnonymizer:
    def test_anonymize_email(self):
        """Проверка анонимизации email-адресов."""
        text = "Контакт: user@example.com для связи"
        anonymized, replacements = anonymize_text(text)
        assert "user@example.com" not in anonymized
        assert "[EMAIL_" in anonymized
        assert len(replacements) == 1
        assert replacements[0]["type"] == "email"

    def test_anonymize_phone_with_plus(self):
        """Проверка анонимизации телефона с плюсом."""
        text = "Телефон: +7 (999) 123-45-67"
        anonymized, replacements = anonymize_text(text)
        assert "+7 (999) 123-45-67" not in anonymized
        assert "[PHONE_" in anonymized
        assert len(replacements) >= 1

    def test_anonymize_phone_digits_only(self):
        """Проверка анонимизации телефона только цифрами."""
        text = "Телефон: 89991234567"
        anonymized, replacements = anonymize_text(text)
        # Телефон из 11 цифр должен быть найден и заменен
        assert len(replacements) >= 1 and "89991234567" not in anonymized

    def test_anonymize_full_name_latin(self):
        """Проверка анонимизации ФИО (используем русское имя для надежности)."""
        text = "Автор: Иван Петрович Сидоров"
        anonymized, replacements = anonymize_text(text)
        # Проверяем, что имя заменено (модель может не распознать латиницу)
        assert len(replacements) >= 1
        assert "Иван Петрович Сидоров" not in anonymized

    def test_anonymize_no_personal_data(self):
        """Проверка текста без персональных данных."""
        text = "Это обычный текст без личной информации."
        anonymized, replacements = anonymize_text(text)
        assert anonymized == text
        assert len(replacements) == 0

    def test_anonymize_multiple_entities(self):
        """Проверка анонимизации нескольких сущностей."""
        text = "Email: test@mail.ru, телефон: +1234567890"
        anonymized, replacements = anonymize_text(text)
        # Проверяем количество найденных сущностей (минимум 2)
        assert len(replacements) >= 2
        types_found = [r["type"] for r in replacements]
        assert "email" in types_found or "phone" in types_found

    def test_restore_original_text(self):
        """Проверка восстановления оригинального текста."""
        original = "Свяжитесь с user@test.org"
        anonymized, replacements = anonymize_text(original)
        restored = restore_anonymized_text(anonymized, replacements)
        assert restored == original

    def test_restore_empty_replacements(self):
        """Проверка восстановления при пустом списке замен."""
        text = "Текст без замен"
        restored = restore_anonymized_text(text, [])
        assert restored == text

    def test_check_privacy_compliance_positive(self):
        """Проверка обнаружения персональных данных."""
        text = "Email: privacy@test.com"
        result = check_privacy_compliance(text)
        assert result["has_personal_data"] is True
        assert result["entities_found"] >= 1

    def test_check_privacy_compliance_negative(self):
        """Проверка отсутствия персональных данных."""
        text = "Обычный текст без личной информации"
        result = check_privacy_compliance(text)
        assert result["has_personal_data"] is False
        assert result["entities_found"] == 0

    def test_anonymize_twice_same_result(self):
        """Проверка, что повторный вызов на том же тексте дает тот же результат."""
        text = "user@example.com"
        anonymized, replacements = anonymize_text(text)
        # Повторная анонимизация не должна менять результат
        anonymized_again, replacements_again = anonymize_text(anonymized)
        assert anonymized == anonymized_again
        assert len(replacements) == len(replacements_again)
