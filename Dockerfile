# Use modular Weaviate image with support for OpenAI module
FROM semitechnologies/weaviate:1.25.2-mod

# Enable the OpenAI text vectorization module
ENV ENABLE_MODULES="text2vec-openai"

# Optional: override with dummy key (actual set in Railway variables)
ENV OPENAI_APIKEY="your-api-key-will-be-overridden-by-Railway"

# Optional: expose port
EXPOSE 8080
