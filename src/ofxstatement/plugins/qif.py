from typing import Dict, Optional, Any, Iterable, List, TextIO
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
import logging

from ofxstatement.plugin import Plugin
from ofxstatement.parser import StatementParser
from ofxstatement.statement import (Statement, StatementLine,
                                    generate_transaction_id, TRANSACTION_TYPES)

from quiffen import Qif, QifDataType
from quiffen.core.account import AccountType
from quiffen.core.transaction import Transaction
import decimal

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger('Santander')

class QIFParser(StatementParser):
    """QIF statement parser"""

    path: TextIO  # file input stream
    day_first: bool
    account_name: str

    # 0-based csv column mapping to StatementLine field
    mappings: Dict[str, int] = {}

    def __init__(
        self,
        path: TextIO,
        day_first: bool = False,
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

        Returns
        -------
        Qif
            A Qif object containing all the data in the QIF file.
        """
        super().__init__()
        self.path = path
        self.day_first = day_first
        self.account_name = account_name

    @staticmethod
    def get_transaction_type(account_type: AccountType) -> Optional[str]:
        return 'CASH' if account_type == AccountType.CASH else None

    def split_records(self) -> Iterable[[AccountType, Transaction]]:
        qif = Qif.parse(self.path, day_first=self.day_first)
        if self.account_name in qif.accounts:
            account = qif.accounts[self.account_name]
            return [ (account_type, transaction) for account_type, transactions in account.transactions.items() for transaction in transactions ]
        return []

    def parse_record(self, line: [AccountType, Transaction]) -> Optional[StatementLine]:
        statement_line = StatementLine(
            id = None,
            date = line[1].date,
            memo = line[1].memo,
            amount = Decimal(line[1].amount),
        )

        statement_line.id = generate_transaction_id(statement_line)
        statement_line.date_user = line[1].date
        statement_line.trntype = self.get_transaction_type(line[0])
        statement_line.payee = line[1].payee

        return statement_line
