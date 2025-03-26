import pdfplumber

class PdfReader:
    def get_json_data(self, file):
        data = []
        with pdfplumber.open(file) as pdf:
            pages = pdf.pages
        for page in pages:
            tables = page.extract_table()
            if tables:
                data.extend(tables)
        return data