from src.domain.chunk import SentenceChunker
from src.domain.embed import SentenceTransformerEmbedder

sentence = """
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

"""

chunker = SentenceChunker(1)
embedder = SentenceTransformerEmbedder()
test_chunks = chunker.chunk_text(sentence)

# now generate embeddings for 1 example
texts = [chunk['text'] for chunk in test_chunks]
metadatas = [chunk['metadata'] for chunk in test_chunks]

embeddings = embedder.embed_batch(texts)

breakpoint()
