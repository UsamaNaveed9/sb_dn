from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today



@frappe.whitelist()
def make_stock_entry(doc,action):
	if doc.items[0].sales_order and doc.items[0].delivery_note:
		new_doc = frappe.new_doc("Stock Entry")
		new_doc.stock_entry_type = "Material Issue"
		new_doc.company = doc.company
		new_doc.set_posting_time = 1
		new_doc.posting_date = doc.posting_date
		new_doc.from_warehouse = frappe.db.get_single_value("Stock Settings", "default_delivered_warehouse")
		for it in doc.items:
			row = new_doc.append("items",{})
			row.s_warehouse = frappe.db.get_single_value("Stock Settings", "default_delivered_warehouse")
			row.item_code = it.item_code
			row.qty = it.qty
			row.uom = it.uom
		new_doc.remarks = f"""This Material Issue created on Sales Invoice: {doc.name}""" 
		new_doc.save()
		new_doc.submit()
