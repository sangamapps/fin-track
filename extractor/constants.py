from .reader.xls_reader import XlsReader
from .reader.table_reader import TableReader
from .reader.pdf_reader import PdfReader
from .extractors.hdfc_xls_as_extractor_v1 import HdfcXlsAccountStatementExtractorV1
from .extractors.sbi_xls_as_extractor_v1 import SbiXlsAccountStatementExtractorV1
from .extractors.axis_pdf_as_extractor_v1 import AxisPdfAccountStatementExtractorV1
from enum import Enum

class Extractor:
    def __init__(self, reader, extractor):
        self.reader = reader
        self.extractor = extractor

SBI_AS_XLS_V1_COLUMNS = [
    "Txn Date",
    "Value Date",
    "Description",
    "Ref No./Cheque No.",
    "Debit",
    "Credit",
    "Balance",
]

EXTRACTORS_MAP = {
    "HDFC_AS_XLS_V1": Extractor(XlsReader(), HdfcXlsAccountStatementExtractorV1()),
    "SBI_AS_XLS_V1": Extractor(TableReader(SBI_AS_XLS_V1_COLUMNS), SbiXlsAccountStatementExtractorV1()),
    "AXIS_AS_PDF_V1": Extractor(PdfReader(), AxisPdfAccountStatementExtractorV1()),
}

class GenericColumnNames(Enum):
    DATE = "date"
    DESCRIPTION = "description"
    DEBIT = "debit"
    CREDIT = "credit"
    BALANCE = "balance"

COLUMN_NAME_MAP = {
    # HDFC AS
    "Date": GenericColumnNames.DATE,
    "Narration": GenericColumnNames.DESCRIPTION,
    "Chq./Ref.No.": None,
    "Value Dt": None,
    "Withdrawal Amt.": GenericColumnNames.DEBIT,
    "Deposit Amt.": GenericColumnNames.CREDIT,
    "Closing Balance": GenericColumnNames.BALANCE,
    # SBI AS
    "Txn Date": GenericColumnNames.DATE,
    "Value Date": None,
    "Description": GenericColumnNames.DESCRIPTION,
    "Ref No./Cheque No.": None,
    "Debit": GenericColumnNames.DEBIT,
    "Credit": GenericColumnNames.CREDIT,
    "Balance": GenericColumnNames.BALANCE,
    # AXIS AS
    "Tran Date" : GenericColumnNames.DATE,
    "Chq No" : None,
    "Particulars" : GenericColumnNames.DESCRIPTION,
    "Debit" : GenericColumnNames.DEBIT,
    "Credit" : GenericColumnNames.CREDIT,
    "Balance" : GenericColumnNames.BALANCE,
    "Init.\nBr" : None,
}