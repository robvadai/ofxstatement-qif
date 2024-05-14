import logging
from decimal import Decimal
from typing import Dict, Optional, Iterable, Tuple

from ofxstatement.parser import StatementParser
from ofxstatement.plugin import Plugin
from ofxstatement.statement import (StatementLine,
                                    generate_transaction_id)
from quiffen import Qif
from quiffen.core.account import AccountType
from quiffen.core.transaction import Transaction

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('QIF')


class QIFPlugin(Plugin):
    """QIF file parser"""

    def get_parser(self, filename: str) -> "QIFParser":
        return QIFParser(path=filename)


class QIFParser(StatementParser):
    """QIF statement parser"""

    path: str
    separator: str
    day_first: bool
    encoding: str
    account_name: str

    # 0-based csv column mapping to StatementLine field
    mappings: Dict[str, int] = {}

    def __init__(
        self,
        path: str,
        separator: str = '\n',
        day_first: bool = False,
        encoding: str = 'utf-8',
        account_name: str = 'Quiffen Default Account'
    ) -> None:
        """Return a class instance of QIFParser

        Parameters
        ----------
        path : Union[FilePath, str]
            The path to the QIF file.
        separator : str, default='\n'
            The line separator for the QIF file. This probably won't need
            changing.
        day_first : bool, default=False
            Whether the day or month comes first in the date.
        encoding : str, default='utf-8'
            The encoding of the QIF file.
        """
        super().__init__()
        self.path = path
        self.separator = separator
        self.day_first = day_first
        self.encoding = encoding
        self.account_name = account_name

    @staticmethod
    def get_transaction_type(account_type: AccountType) -> str:
        if account_type == AccountType.CASH:
            return 'CASH'
        elif account_type == AccountType.OTH_L:
            return 'DEBIT'
        else:
            return 'OTHER'

    def split_records(self) -> Iterable[Tuple[AccountType, Transaction]]:
        qif = Qif.parse(self.path, self.separator, self.day_first, self.encoding)
        if self.account_name in qif.accounts:
            account = qif.accounts[self.account_name]
            return ((account_type, transaction) for account_type, transactions in account.transactions.items() for transaction in transactions)
        return []

    def parse_record(self, line: [AccountType, Transaction]) -> Optional[StatementLine]:
        statement_line = StatementLine(
            date=line[1].date,
            memo=line[1].memo,
            amount=Decimal(line[1].amount),
        )

        statement_line.id = generate_transaction_id(statement_line)
        statement_line.date_user = line[1].date
        statement_line.trntype = self.get_transaction_type(line[0])
        statement_line.payee = line[1].payee

        return statement_line
