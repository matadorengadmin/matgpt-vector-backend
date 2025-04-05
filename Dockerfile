# Use official modular Weaviate image with OpenAI vectorizer support
FROM semitechnologies/weaviate:1.25.3-mod

# These are required, but values will be injected securely by Railway at runtime
ENV ENABLE_MODULES=text2vec-openai
ENV OPENAI_APIKEY=will-be-set-in-Railway

# Expose Weaviate port (Railway does this automatically)
EXPOSE 8080
