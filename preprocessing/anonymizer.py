"""Module for anonymizing personal data in text."""

import re
from typing import Tuple, List, Dict

from natasha import NamesExtractor, OrganisationExtractor, MorphVocab, Doc


def anonymize_text(text: str) -> Tuple[str, List[Dict]]:
    """
    Replace personal data with placeholders.
    
    Args:
        text: Input text to anonymize.
        
    Returns:
        Tuple of (anonymized_text, list of replacements).
        Each replacement: {"type": str, "original": str, "placeholder": str, "position": int}.
    """
    replacements = []
    anonymized = text
    
    # Email regex
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    
    # Phone regex: +7, 8, or 11 digits
    phone_pattern = r'(?:\+7|8|\d{11})[\s\-]?(?:\(\d{3}\)|\d{3})[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}'
    
    # Counters for placeholders
    email_count = 0
    phone_count = 0
    name_count = 0
    org_count = 0
    
    # Extract entities using Natasha
    morph_vocab = MorphVocab()
    names_extractor = NamesExtractor(morph_vocab)
    org_extractor = OrganisationExtractor(morph_vocab)
    
    doc = Doc(text)
    try:
        doc.extract_names(names_extractor)
        doc.extract_orgs(org_extractor)
    except Exception:
        pass
    
    # Find all PER and ORG entities
    entities = []
    spans = doc.spans if doc.spans else []
    for span in spans:
        if span.type == 'PER':
            entities.append((span.start, span.stop, span.text, 'FULL_NAME'))
        elif span.type == 'ORG':
            entities.append((span.start, span.stop, span.text, 'ORG'))
    
    # Sort by position (reverse order to replace from end to start)
    entities.sort(key=lambda x: x[0], reverse=True)
    
    # Process emails
    for match in re.finditer(email_pattern, anonymized):
        email_count += 1
        placeholder = f"[EMAIL_{email_count}]"
        replacements.append({
            "type": "email",
            "original": match.group(),
            "placeholder": placeholder,
            "position": match.start()
        })
    
    # Process phones
    for match in re.finditer(phone_pattern, anonymized):
        phone_count += 1
        placeholder = f"[PHONE_{phone_count}]"
        replacements.append({
            "type": "phone",
            "original": match.group(),
            "placeholder": placeholder,
            "position": match.start()
        })
    
    # Process names and orgs (reverse order to maintain positions)
    for start, stop, entity_text, entity_type in entities:
        if entity_type == 'FULL_NAME':
            name_count += 1
            placeholder = f"[FULL_NAME_{name_count}]"
            replacements.append({
                "type": "full_name",
                "original": entity_text,
                "placeholder": placeholder,
                "position": start
            })
        elif entity_type == 'ORG':
            org_count += 1
            placeholder = f"[DEPARTMENT_{org_count}]"
            replacements.append({
                "type": "org",
                "original": entity_text,
                "placeholder": placeholder,
                "position": start
            })
    
    # Sort replacements by position for consistent ordering
    replacements.sort(key=lambda x: x["position"])
    
    # Apply replacements (reverse order to preserve positions)
    result = anonymized
    for repl in sorted(replacements, key=lambda x: x["position"], reverse=True):
        result = result[:repl["position"]] + repl["placeholder"] + result[repl["position"] + len(repl["original"]):]
    
    return result, replacements


def restore_anonymized_text(text: str, replacements: List[Dict]) -> str:
    """
    Restore original text from anonymized version using replacements list.
    
    Args:
        text: Anonymized text.
        replacements: List of replacement dictionaries.
        
    Returns:
        Restored original text.
    """
    result = text
    # Sort by position descending to replace from end to start
    for repl in sorted(replacements, key=lambda x: x["position"], reverse=True):
        placeholder = repl["placeholder"]
        original = repl["original"]
        pos = repl["position"]
        # Find placeholder in text and replace
        if placeholder in result:
            idx = result.find(placeholder)
            result = result[:idx] + original + result[idx + len(placeholder):]
    return result


def check_privacy_compliance(text: str) -> Dict:
    """
    Check if text contains personal data.
    
    Args:
        text: Input text to check.
        
    Returns:
        Dict with keys: has_personal_data (bool), entities_found (int).
    """
    _, replacements = anonymize_text(text)
    has_personal_data = len(replacements) > 0
    entities_found = len(replacements)
    
    return {
        "has_personal_data": has_personal_data,
        "entities_found": entities_found
    }
