import re

def parse_mcq_questions(text: str) -> list[dict]:
    """يحلل النص لاستخراج أسئلة MCQ."""
    questions = []
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    current_question = None
    current_options = []
    
    q_patterns = [
        re.compile(r'^(\d+[\.\-]|السؤال\s+\d+[:\.\-]|Question\s+\d+[:\.\-])', re.IGNORECASE),
        re.compile(r'^(السؤال\s+الثاني|السؤال\s+الأول|السؤال\s+الثالث)[:\.\-]', re.IGNORECASE)
    ]
    o_pattern = re.compile(r'^([أ-يA-Za-z])[\)\.]')

    for line in lines:
        is_q = any(p.match(line) for p in q_patterns)
        if is_q:
            if current_question and current_options:
                questions.append({"question": current_question, "options": current_options, "correct_option_id": 0})
            
            q_text = line
            for p in q_patterns:
                q_text = p.sub('', q_text).strip()
            current_question = q_text
            current_options = []
            continue
            
        o_match = o_pattern.match(line)
        if o_match and current_question is not None:
            label = o_match.group(1)
            content = o_pattern.sub('', line).strip()
            current_options.append(f"{label}) {content}")
            continue
            
        if current_question is not None:
            if not current_options:
                current_question += " " + line
            else:
                current_options[-1] += " " + line

    if current_question and current_options:
        questions.append({"question": current_question, "options": current_options, "correct_option_id": 0})

    return questions
