import base64
import os
from mistralai.client import Mistral
from dotenv import load_dotenv

load_dotenv("../../.env")


api_key = os.environ["MISTRAL_API_KEY"]

client = Mistral(api_key=api_key)


def encode_pdf(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode("utf-8")


ocr_response = client.ocr.process(
    model="mistral-ocr-latest",
    document={
        "type": "document_url",
        "document_url": f"data:application/pdf;base64,{encode_pdf('/Users/simon/dev/everything-training/src/mistral_ocr/data/simontest.pdf')}",
    },
    table_format="html",  # default is None
    # extract_header=True, # default is False
    # extract_footer=True, # default is False
    include_image_base64=True,
)

print(f"got response={ocr_response}")
