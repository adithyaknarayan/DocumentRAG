# Introduction

# Overview

Also for fun, I was recently looking into DIP (Dependency Inversion Principle), so I wanted to use this take-home as a sort of test bench to see how well that would work for this project. Overall, from what I understand we need a pipeline that looks like
```
interfaces (Abstract classes)  ← domain (embedding, chunking, DB)
     ↑                             ↑
application (ingestion, retrieval, generation)
     ↑
wiring / main
```
So more concrete diagram can be seen as,
![Architecture Layers](assets/Layers.png)

Here `application only depends on interfaces and domain, infra on application etc. Following this I'll try to build out the whole pipeline and hopefully have a clean ablation on the chunking/retreival stategy later down the line.

# A (very bare minmum) testing overview
If you're curious about how to use each component independently you can take a look at the files I used to test each chunk seperately in `tests/test_*`.

The overall flow is like
```
test_chunker.py -> test_embedder.py -> test_ingest.py -> test_retreival.py
```

This essentially outlines every step taken on the way to making the whole repository and how I broke down the components. Additionally for a more detailed explanation on how DIP layers were constructed, I go over each layer below starting from the Interface -> Domain -> Application Layer (where most of the orchestration happens) -> the main wiring loop.


# Domain Layer
## Vector DB
Now that the embedder and the chunking components have been build out, I'll work on the database component. For convenience I'll be sticking ot FAISS, but will still follow the DIP design principle and do a abstraction layer on top.

This layer is made of 


# Application Layer
## Ingestion
So for the first part, I'm thinking that we generate a pipeline that ingests all the given documents, chunks it and generates embeddings and stores it in a vectorDB. So the dependency would flow like
```
Ingestion -> {domain.chunk, domain.embed, domain.vector_db} -> {abstractions on each (stored in interfaces)}
```

Since this is a high level module, with DIP, I'll be putting this in applications as a service that orchestrates those components together.

## Retreival 

## Generation
