from PDF_Extractor import PDFExtractor
from pdfminer.high_level import extract_text
extractor = PDFExtractor("PDFExtractorTest.pdf")
text = extract_text("Simple_PDFExtracting/PDFExtractorTest.pdf")
print(text)
