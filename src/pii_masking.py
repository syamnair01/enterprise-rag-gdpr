## PII Masking Module. 
## Masks common PII patterns to reduce GDPR risk before embedding or retrieval.

import re

def mask_pii(text: str) -> str:
    """
    Masks common PII patterns to reduce GDPR risk
    before embedding or retrieval.
    """
    text = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL]', text)
    text = re.sub(r'\b\d{10,}\b', '[PHONE]', text)
    return text
