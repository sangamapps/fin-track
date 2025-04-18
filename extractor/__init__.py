from .constants import EXTRACTORS_MAP, COLUMN_NAME_MAP, GenericColumnNames
from model.transaction import Transaction, TransactionType


def extract(extractor, file):
    extractor_obj = EXTRACTORS_MAP[extractor]
    json_data = extractor_obj.reader.get_json_data(file)
    transactions = extractor_obj.extractor.get_transactions(json_data)
    transactions = rename_columns(transactions)
    return transactions


def convert_to_generic_column_name(column_name):
    return COLUMN_NAME_MAP[column_name] if column_name in COLUMN_NAME_MAP else None


def convert_to_float(column_value):
    if type(column_value) in [int, float]:
        return column_value
    if column_value is None or (type(column_value) is str and column_value.strip() == ""):
        return 0.0
    column_value = column_value.replace(",", "")
    return float(column_value)


def process_column_value(generic_column_name, column_value):
    if generic_column_name == GenericColumnNames.DATE:
        return column_value
    elif generic_column_name == GenericColumnNames.DEBIT:
        return convert_to_float(column_value)
    elif generic_column_name == GenericColumnNames.CREDIT:
        return convert_to_float(column_value)
    elif generic_column_name == GenericColumnNames.BALANCE:
        return convert_to_float(column_value)
    else:
        if type(column_value) is str:
            return column_value.strip()
        return column_value
    
def get_transaction_type(transaction):
    if transaction[GenericColumnNames.CREDIT.value] > 0:
        return TransactionType.CREDIT.value
    return TransactionType.DEBIT.value
    
def get_transaction_amount(transaction):
    if transaction[GenericColumnNames.CREDIT.value] > 0:
        return transaction[GenericColumnNames.CREDIT.value]
    return transaction[GenericColumnNames.DEBIT.value]


def rename_columns(transactions):
    processed_transactions = []
    for transaction in transactions:
        processed_transaction = {}
        for column_name in transaction:
            generic_column_name = convert_to_generic_column_name(column_name)
            if not generic_column_name:
                continue
            processed_transaction[generic_column_name.value] = process_column_value(
                generic_column_name, transaction[column_name]
            )
        processed_transaction[Transaction.KEY_TYPE] = get_transaction_type(processed_transaction)
        processed_transaction[Transaction.KEY_AMOUNT] = get_transaction_amount(processed_transaction)
        processed_transaction[Transaction.KEY_EXCLUDE_FROM_TOTALS] = 0
        processed_transaction[Transaction.KEY_APPLIED_RULES] = {}
        processed_transaction[Transaction.KEY_COMMENTS] = ""
        processed_transactions.append(processed_transaction)
    return processed_transactions
