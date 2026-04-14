# Copyright (c) 2026, Alvin Dereba and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class Product(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		description: DF.Text | None
		item_code: DF.Data
		item_name: DF.Data
		uom: DF.Literal["Kgs", "Metres", "Boxes", "Pieces", "Packets"]
		valuation_rate: DF.Float
	# end: auto-generated types

	pass
