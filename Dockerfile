# Use the official Weaviate image that supports modules
FROM semitechnologies/weaviate:1.25.2

# Enable the text2vec-openai module
ENV ENABLE_MODULES="text2vec-openai"

# Set the OpenAI API key (ensure this is set securely in your environment)
ENV OPENAI_APIKEY="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"

# Expose the default Weaviate port
EXPOSE 8080

# Start Weaviate
CMD ["./weaviate"]
