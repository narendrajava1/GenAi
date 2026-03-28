# run this once to create a sample PDF
from fpdf import FPDF

pdf = FPDF()
pdf.add_page()
pdf.set_font("Arial", size=12)

content = """
Nara Chandrababu Naidu Profile

Nara Chandrababu Naidu, commonly known as CBN, was born on 20 April 1950.
He is currently serving as the Chief Minister of Andhra Pradesh since 2024.
He holds the record of longest-serving Chief Minister in the political history of Telugu states.
He is the national president of the Telugu Desam Party (TDP).

Education:
He obtained his B.A. degree in 1972 from Sri Venkateswara Arts College, Tirupati.
He earned a master degree in Economics from Sri Venkateswara University.

Political Career:
Naidu began his political journey as a confidant of Sanjay Gandhi.
He was elected to the Andhra Pradesh state legislative assembly in 1978.
He later joined the TDP, founded by his father-in-law N. T. Rama Rao (NTR).
He served as Chief Minister from 1995 to 2004.
In the 2024 elections, TDP made a comeback securing 164 seats.

Technology Vision:
During his tenure he was hailed as the Hi-tech Chief Minister.
He plans to launch India first drone taxis.
He aims to build 5.5 GW of data centers in Andhra Pradesh.
He partnered with IBM to skill 1 lakh youngsters in AI and cybersecurity.
"""

for line in content.split("\n"):
    pdf.cell(200, 10, txt=line, ln=True)

pdf.output("cbn.pdf")
print("✅ cbn.pdf created!")
# ```
#
# Add `fpdf` to Pipfile and run this once to generate your test PDF.
#
# ---

# 📄 Single PDF → Chunks → Embeddings
# → FAISS Vector Store → Retriever
# → LLM → Answer