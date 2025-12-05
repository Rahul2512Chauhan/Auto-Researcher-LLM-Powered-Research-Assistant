from pipelines.insight_extractor import extract_insights

def test_insights():
    text = "The paper introduces a new optimization technique that reduces training time by 40%."
    result = extract_insights(text)
    print(result)

test_insights()
