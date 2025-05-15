# Technical Decisions

This document outlines the technical decisions made for the Marhinovirus Agent project, explaining the rationale behind each choice.

## Vector Database: ChromaDb

### Why ChromaDb?
1. **Performance**
   - Optimized for fast similarity searches
   - Uses efficient indexing structures (HNSW - Hierarchical Navigable Small World)
   - Provides quick retrieval of relevant information, leading to faster agent responses

2. **Simplicity**
   - Easy to set up and use
   - Minimal configuration required
   - Works well out of the box for small to medium-sized collections

3. **Features**
   - Supports metadata filtering
   - Built-in persistence
   - Good integration with Python ecosystem
   - Efficient memory usage

4. **Scalability**
   - Can handle collections of various sizes
   - Suitable for our current needs (single PDF) and future expansion
   - Good performance even with larger document collections

### Alternatives Considered
- **PgVector**: More complex setup, requires PostgreSQL
- **Qdrant**: More features than needed for our use case
- **Milvus**: Overkill for our current scale
- **Pinecone**: Managed service, not needed for our self-hosted solution

## Embedder: SentenceTransformerEmbedder

### Why SentenceTransformerEmbedder?
1. **Semantic Understanding**
   - Uses state-of-the-art transformer models
   - Captures semantic meaning, not just keywords
   - Understands context and nuance in text

2. **Quality**
   - Produces high-quality embeddings
   - Good at understanding medical terminology
   - Maintains semantic relationships between concepts

3. **Local Processing**
   - Runs entirely locally
   - No API costs or dependencies
   - No internet connection required
   - Better privacy and data security

4. **Performance**
   - Optimized for inference
   - Good balance of speed and quality
   - Efficient memory usage

### Alternatives Considered
- **OpenAIEmbedder**: Requires API key and internet connection
- **HuggingFaceEmbedder**: More complex setup, potentially slower
- **CohereEmbedder**: Requires API key and internet connection

## Image Support and Limitations

### Current Limitations
1. **Text-Only Processing**
   - Current setup only processes text content from PDFs
   - Images in PDFs are not analyzed or indexed
   - No visual content understanding

2. **Embedding Limitations**
   - SentenceTransformerEmbedder cannot process images
   - No visual feature extraction capabilities
   - Limited to text-based semantic search

### Potential Solutions for Image Support
1. **Multi-Modal Embedding**
   - Add CLIP or similar vision-language model
   - Process both text and images
   - Create unified embeddings for mixed content

2. **Hybrid Processing Pipeline**
   - Extract images from PDFs separately
   - Process images with vision models
   - Process text with SentenceTransformer
   - Store both types of embeddings in ChromaDb

3. **Metadata Enhancement**
   - Store image references in metadata
   - Link images to relevant text content
   - Enable image retrieval based on text queries

### Future Image Support Considerations
1. **Model Selection**
   - CLIP for general image understanding
   - Medical-specific vision models for better domain understanding
   - Multi-modal models for combined text-image processing

2. **Storage Optimization**
   - Efficient storage of image embeddings
   - Caching strategies for frequently accessed images
   - Compression techniques for large image collections

3. **Query Processing**
   - Support for image-based queries
   - Combined text-image search capabilities
   - Relevance scoring for mixed content

## Combined Benefits

The combination of ChromaDb and SentenceTransformerEmbedder provides:

1. **Efficient Information Retrieval**
   - Fast and accurate search through the knowledge base
   - Good semantic understanding of queries
   - Relevant information retrieval

2. **Quality Responses**
   - Better context understanding
   - More accurate answers
   - Ability to handle complex medical queries

3. **Privacy and Security**
   - All processing done locally
   - No external API dependencies
   - Complete control over data

4. **Cost-Effective**
   - No API costs
   - No external service dependencies
   - Efficient resource usage

## Future Considerations

1. **Scaling**
   - Current setup can handle growth in document collection
   - May need to adjust parameters for larger collections
   - Can easily switch to alternative solutions if needed

2. **Performance Optimization**
   - Can tune embedding model parameters
   - Can adjust ChromaDb indexing parameters
   - Can implement caching if needed

3. **Feature Expansion**
   - Current setup supports adding more features
   - Can implement additional filtering capabilities
   - Can add more sophisticated search features 

## Image Support and Limitations

### Current Limitations
1. **Text-Only Processing**
   - Current setup only processes text content from PDFs
   - Images in PDFs are not analyzed or indexed
   - No visual content understanding

2. **Embedding Limitations**
   - SentenceTransformerEmbedder cannot process images
   - No visual feature extraction capabilities
   - Limited to text-based semantic search

### Potential Solutions for Image Support
1. **Multi-Modal Embedding**
   - Add CLIP or similar vision-language model
   - Process both text and images
   - Create unified embeddings for mixed content

2. **Hybrid Processing Pipeline**
   - Extract images from PDFs separately
   - Process images with vision models
   - Process text with SentenceTransformer
   - Store both types of embeddings in ChromaDb

3. **Metadata Enhancement**
   - Store image references in metadata
   - Link images to relevant text content
   - Enable image retrieval based on text queries

### Future Image Support Considerations
1. **Model Selection**
   - CLIP for general image understanding
   - Medical-specific vision models for better domain understanding
   - Multi-modal models for combined text-image processing

2. **Storage Optimization**
   - Efficient storage of image embeddings
   - Caching strategies for frequently accessed images
   - Compression techniques for large image collections

3. **Query Processing**
   - Support for image-based queries
   - Combined text-image search capabilities
   - Relevance scoring for mixed content