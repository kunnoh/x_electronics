# Copyright (c) 2026, Alvin Dereba and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import datetime

class StockEntry(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from x_electronics.x_electronics.doctype.stock_entry_item.stock_entry_item import StockEntryItem

		amended_from: DF.Link | None
		from_warehouse: DF.Link | None
		items: DF.Table[StockEntryItem]
		posting_datetime: DF.Date | None
		to_warehouse: DF.Link | None
		type: DF.Literal["Receipt", "Consume", "Transfer"]
	# end: auto-generated types

	def validate(self):
		self.remove_duplicate_items()
		self.set_posting_datetime()

	def remove_duplicate_items(self):
		if not self.get("items"):
			frappe.throw("Please add at least one item to the Stock Entry!")

		seen = {}
		uniq_rows = []

		for item in self.items:
			key = getattr(item, 'item', None)
			if key and key not in seen:
				seen[key] = True
				uniq_rows.append(item)

		# Replace child table with uniq entries
		self.set("items", uniq_rows)


	def set_posting_datetime(self):
		# set posting_date to current date if not specified
		if not self.posting_datetime:
			self.posting_datetime = datetime.strptime(frappe.utils.today(), "%Y-%m-%d").date()

		# ensure posting date is not in the future
		today = datetime.strptime(frappe.utils.today(), "%Y-%m-%d").date()

		# get date version of posting date string
		if isinstance(self.posting_datetime, str):
			self.posting_datetime = datetime.strptime(self.posting_datetime, "%Y-%m-%d").date()

		if self.posting_datetime > today:
			frappe.throw("Posting date cannot be in the future!")


