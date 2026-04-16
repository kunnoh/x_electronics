import frappe
from frappe import _

def create_ledger_entries(doc, method=None):
	frappe.log("Submitting Stock Entry......................")
	frappe.log(doc)

	if doc.docstatus != 1:
		return

	for item in doc.items:
		if doc.type == "Receipt" and doc.to_warehouse:
			create_entry(
				item=item,
				warehouse=doc.to_warehouse,
				actual_quantity=item.quantity,
				incoming_rate=item.valuation_rate,
				voucher_type= "Stock Entry",
				voucher_no=doc.name,
                posting_datetime=doc.posting_datetime,
			)
		elif doc.type == "Consume" and doc.from_warehouse:
			create_entry(
				item=item,
				warehouse=doc.from_warehouse,
				actual_quantity=item.quantity,
				incoming_rate=item.valuation_rate,
				voucher_type= "Stock Entry",
				voucher_no=doc.name,
                posting_datetime=doc.posting_datetime,
			)
		elif doc.type == "Transfer":
			# Outbound entry
			if doc.to_warehouse:
				create_entry(
					item=item,
					warehouse=doc.from_warehouse,
					actual_quantity=-1*item.quantity, # Negative for source
					incoming_rate=item.valuation_rate,
					voucher_type= "Stock Entry",
					voucher_no=doc.name,
	                posting_datetime=doc.posting_datetime,
				)

			# Inbound entry
			if doc.from_warehouse:
				create_entry(
					item=item,
					warehouse=doc.to_warehouse,
					actual_quantity=item.quantity, # Positive for target
					incoming_rate=item.valuation_rate,
					voucher_type= "Stock Entry",
					voucher_no=doc.name,
	                posting_datetime=doc.posting_datetime,
				)

def create_entry(
    item,
    warehouse,
    actual_quantity,
    incoming_rate,
    voucher_type,
    voucher_no,
    posting_datetime,
):
    """Create a single stateless stock ledger entry"""
    sle = frappe.new_doc("Stock Ledger Entry")
    sle.item = item.item
    sle.warehouse = warehouse
    sle.actual_quantity = actual_quantity
    sle.incoming_rate = incoming_rate if actual_quantity > 0 else 0
    sle.voucher_type = voucher_type
    sle.voucher_no = voucher_no
    sle.voucher_detail_no = item.name
    sle.posting_datetime = posting_datetime
    sle.transaction_uom = item.uom
    sle.insert()

def delete_ledger_entries(doc, method=None):
    """Delete stateless stock ledger entries when document is cancelled"""
    if doc.docstatus != 2:  # 2 means cancelled
        return

    frappe.db.delete(
        "Stock Ledger Entry",
        {"voucher_type": doc.doctype, "voucher_no": doc.name},
    )
