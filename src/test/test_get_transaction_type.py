from ..ofxstatement.plugins.qif import QIFParser
from quiffen.core.account import AccountType

other_transaction_type = 'OTHER'

expectations = {
    AccountType.CASH: 'CASH',
    AccountType.OTH_L: 'DEBIT',
    AccountType.BANK: other_transaction_type
}


def test_get_transaction_type():
    for transaction_type, expectation in expectations.items():
        assert QIFParser.get_transaction_type(transaction_type) == expectation