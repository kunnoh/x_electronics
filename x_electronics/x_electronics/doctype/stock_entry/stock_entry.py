# Copyright (c) 2026, Alvin Dereba and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class StockEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from x_electronics.x_electronics.doctype.stock_entry_item.stock_entry_item import StockEntryItem

		amended_from: DF.Link | None
		from_warehouse: DF.Link | None
		table_zuen: DF.Table[StockEntryItem]
		to_warehouse: DF.Link | None
		type: DF.Literal["Receipt", "Consume", "Transfer"]
	# end: auto-generated types

	pass
