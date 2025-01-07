from presidio_analyzer import AnalyzerEngine

# Set up the engine, loads the NLP module (spaCy model by default) and other PII recognizers
analyzer = AnalyzerEngine()


my_text = """
My phone number is 212-555-5555. However my new french phone number is 212-666-5576.
"""
# Call analyzer to get results
results = analyzer.analyze(text=my_text,
                           entities=["PHONE_NUMBER"],
                           language='en')
print(results)
# the output is a RecognizerResult.