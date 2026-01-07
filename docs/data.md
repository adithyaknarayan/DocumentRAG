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


## Sentence Chunking
For example when chunking the above by sentence we get:
```
{'text': 'NTRODUCTION\nAS A RULE grain is the first crop grown on newly cultivated land, but few irrigated farms can be made to pay if perma- nently devoted to it.', 'metadata': {'chunk_index': 0, 'sentence_start': 0, 'sentence_end': 1, 'num_sentences': 1}}
```

So maybe we need a better strategy here. Similarly when it comes to the tabular(ish) data it has a tendency to pick up information from the next sections paragraph.

```
FARM PRACTICES UNDER CORN-BORER CONDITIONS
By Jesse W. Tapp, Agricultural Economist, and Grorce W. Couuier, Assistant Agricultural Economist, age i Farm Management and Costs, ‘Bureau of Agricultural Economics, and C. ARNOLD, Farm Management Demonstrator, Ohio State University

CONTENTS
Character of the problem in different areas - 3
    Methods of harvesting corn - 5
    Usual methods of preparing cornland - 6
Labor and power required by control practices - 8    
    How to handle stubble ground - 8
    How to handle stalk ground - 10
    How to reduce barn-lot clean-up - 14
When to do control work - 14
    Control-work calendar - 16
    Changes in cropping systems - 16

THE EUROPEAN CORN BORER has become well established at the edge of the Corn Belt, in northern Ohio, northeastern Indiana, and eastern Michigan. In a limited number of fields in Ohio and Michigan the borer was responsible for some commercial damage to the 1926 and 1927 corn crops. In the adjoining counties in the Province of Ontario the data of the Ontario Department of Agriculture show that the acreage of corn was reduced about 71 per cent from 1923 to 1927 on account of corn-borer damage. In 1927 slight infestations were found in eastern Corn-Belt areas considerably south and west of the 1926 infested area. (Fig.1.) A joint committee of the American Association of Economic Entomologists, the Ameri- can Society of Agronomy, and the American Society of Agricultural Engineers has aavank the opinion that “it will be impossible to eradicate the borer or even to prevent its spread to corn-growing areas not yet infested.”

```
```
{'text': 'FARM PRACTICES UNDER CORN-BORER CONDITIONS\nBy Jesse W. Tapp, Agricultural Economist, and Grorce W. Couuier, Assistant Agricultural Economist, age i Farm Management and Costs, ‘Bureau of Agricultural Economics, and C. ARNOLD, Farm Management Demonstrator, Ohio State University\n\nCONTENTS\nCharacter of the problem in different areas - 3\n    Methods of harvesting corn - 5\n    Usual methods of preparing cornland - 6\nLabor and power required by control practices - 8    \n    How to handle stubble ground - 8\n    How to handle stalk ground - 10\n    How to reduce barn-lot clean-up - 14\nWhen to do control work - 14\n    Control-work calendar - 16\n    Changes in cropping systems - 16\n\nTHE EUROPEAN CORN BORER has become well established at the edge of the Corn Belt, in northern Ohio, northeastern Indiana, and eastern Michigan.', 'metadata': {'chunk_index': 0, 'sentence_start': 0, 'sentence_end': 1, 'num_sentences': 1}}
```