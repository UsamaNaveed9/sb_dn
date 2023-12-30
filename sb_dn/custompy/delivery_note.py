from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today



@frappe.whitelist()
def make_stock_entry(doc,action):
	if doc.items[0].against_sales_order and doc.is_return == 0:
		new_doc = frappe.new_doc("Stock Entry")
		new_doc.stock_entry_type = "Material Transfer"
		new_doc.company = doc.company
		new_doc.set_posting_time = 1
		new_doc.posting_date = doc.posting_date
		new_doc.from_warehouse = doc.set_warehouse
		new_doc.to_warehouse = frappe.db.get_single_value("Stock Settings", "default_delivered_warehouse")
		for it in doc.items:
			row = new_doc.append("items",{})
			row.s_warehouse = doc.set_warehouse
			row.t_warehouse = frappe.db.get_single_value("Stock Settings", "default_delivered_warehouse")
			row.item_code = it.item_code
			row.qty = it.qty
			row.uom = it.uom
		new_doc.remarks = f"""This Material Transfer created on Delivery Note: {doc.name}""" 
		new_doc.save()
		new_doc.submit()
	elif doc.items[0].against_sales_order and doc.is_return == 1:
		new_doc = frappe.new_doc("Stock Entry")
		new_doc.stock_entry_type = "Material Transfer"
		new_doc.company = doc.company
		new_doc.set_posting_time = 1
		new_doc.posting_date = doc.posting_date
		new_doc.from_warehouse = frappe.db.get_single_value("Stock Settings", "default_delivered_warehouse")
		new_doc.to_warehouse = doc.set_warehouse
		for it in doc.items:
			row = new_doc.append("items",{})
			row.s_warehouse = frappe.db.get_single_value("Stock Settings", "default_delivered_warehouse")
			row.t_warehouse = doc.set_warehouse
			row.item_code = it.item_code
			row.qty = -(it.qty)
			row.uom = it.uom
		new_doc.remarks = f"""This Material Transfer created on Delivery Note Return: {doc.name}""" 
		new_doc.save()
		new_doc.submit()    
	
