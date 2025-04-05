# Use official Weaviate with text2vec-openai module
FROM semitechnologies/weaviate:1.25.2

ENV ENABLE_MODULES="text2vec-openai"
ENV OPENAI_APIKEY="your-api-key-will-be-overridden-by-Railway"

# Optional: expose port if needed (usually done by Railway automatically)
EXPOSE 8080


