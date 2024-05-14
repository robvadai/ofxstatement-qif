import tempfile
from datetime import datetime
from decimal import Decimal

import pytest
from ofxstatement.ui import UI
from src.ofxstatement.plugins.qif import QIFPlugin

qif_file_contents = """!Type:Oth L
D30/03/2024
T-1080.00
PTRANSFER REFERENCE                                                                        , 1080.00
^
D20/04/2024
T-2.75
PFOREIGN CURRENCY CONVERSION FEE                                                           , 2.75
^
D10/03/2024
T1200.00
PFASTER PAYMENTS RECEIPT                                                                   , 1200.00
^"""

expected_currency_usd = "USD"


@pytest.mark.integration
def test_parse_qif_file():

    plugin = QIFPlugin(UI(), {"day-first": True, "currency": "USD"})

    with tempfile.NamedTemporaryFile(delete_on_close=False, suffix=".qif") as fp:
        fp.writelines([f"{line}\n".encode() for line in qif_file_contents.splitlines()])
        fp.close()

        parser = plugin.get_parser(fp.name)
        statement = parser.parse()

        assert len(statement.lines) == 3

        first_line = statement.lines[0]
        assert first_line.date == datetime(2024, 3, 30)
        assert first_line.date_user == datetime(2024, 3, 30)
        assert first_line.amount == Decimal(-1080)
        assert first_line.trntype == 'DEBIT'
        assert first_line.currency.symbol == expected_currency_usd
        assert first_line.payee == "TRANSFER REFERENCE                                                                        , 1080.00"

        second_line = statement.lines[1]
        assert second_line.date == datetime(2024, 4, 20)
        assert second_line.date_user == datetime(2024, 4, 20)
        assert second_line.amount == Decimal(-2.75)
        assert second_line.trntype == 'DEBIT'
        assert second_line.currency.symbol == expected_currency_usd
        assert second_line.payee == "FOREIGN CURRENCY CONVERSION FEE                                                           , 2.75"

        third_line = statement.lines[2]
        assert third_line.date == datetime(2024, 3, 10)
        assert third_line.date_user == datetime(2024, 3, 10)
        assert third_line.amount == Decimal(1200)
        assert third_line.trntype == 'DEBIT'
        assert third_line.currency.symbol == expected_currency_usd
        assert third_line.payee == "FASTER PAYMENTS RECEIPT                                                                   , 1200.00"