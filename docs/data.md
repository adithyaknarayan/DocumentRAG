# Data Review
To start with I wanted to review what the data looked like. I was curious about this since this would influence the chunking strategy that I use+other components of the pipeline.

To start with, I did a simple review (a super general one) using: https://medium.com/@sahin.samia/mastering-document-chunking-strategies-for-retrieval-augmented-generation-rag-c9c16785efc7

Overall, I want the system to be modular so that I can add in more chunking strategies down the line to run a small ablation.

## Observations
1. Most of the documents seems to have titled paragraphs like the following. Interestingly, in quite a few cases, the paragraph title provides concrete information on what the pragraph is likely to address.
'''
INTRODUCTION
AS A RULE grain is the first crop grown on newly cultivated land, but few irrigated farms can be made to pay if perma- nently devoted to it. Hence in well-established irrigated sections, grain is grown only as a secondary crop in a rotation, or to utilize land with water supplies insufficient to mature more remunerative crops.
'''

2. I'm unsure if sentence chunking is a good idea here since we have the semantics contained in titled paragraphs. So having looked at the previously linked article it seems likely that paragraph level embeddings might be a better idea.

3. Also might use sliding windows in the even that context needs to be preserved across chunks since the same context can be refered to in multiple places.