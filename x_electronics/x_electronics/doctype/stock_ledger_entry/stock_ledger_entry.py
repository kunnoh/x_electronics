# Copyright (c) 2026, Alvin Dereba and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StockLedgerEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		item: DF.Link
		quantity: DF.Float
		valuation_rate: DF.Currency
		value_difference: DF.Currency
		voucher_no: DF.Data | None
		voucher_type: DF.Data | None
		warehouse: DF.Link
	# end: auto-generated types

	pass
