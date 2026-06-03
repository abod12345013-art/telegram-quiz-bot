from utils.question_parser import parse_mcq_questions

def test_parser():
    test_text = """
    1. What is the capital of Iraq?
    A) Basra
    B) Mosul
    C) Baghdad
    D) Erbil

    السؤال الثاني: ما هي عاصمة السعودية؟
    أ) جدة
    ب) الرياض
    ج) مكة
    د) الدمام
    """
    
    questions = parse_mcq_questions(test_text)
    
    print(f"تم العثور على {len(questions)} سؤال.")
    for i, q in enumerate(questions, 1):
        print(f"\nالسؤال {i}: {q['question']}")
        print("الخيارات:")
        for opt in q['options']:
            print(f"  - {opt}")

if __name__ == "__main__":
    test_parser()
