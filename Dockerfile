# Use modular Weaviate image with OpenAI vectorizer support
FROM semitechnologies/weaviate:1.25.2-module

# Enable OpenAI text vectorizer module
ENV ENABLE_MODULES="text2vec-openai"

# Optional: dummy key — actual key should be set in Railway environment variables
ENV OPENAI_APIKEY="your-api-key-will-be-overridden-by-Railway"

# Optional port exposure
EXPOSE 8080
