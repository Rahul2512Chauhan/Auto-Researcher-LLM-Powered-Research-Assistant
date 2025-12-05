from agents.question_generator import generate_research_questions

def test_questions():
    text = "The paper proposes a new self-supervised learning method for multimodal alignment."
    result = generate_research_questions(text)
    print(result)

test_questions()
