import frappe

def extend_validate(doc,method=None):
    if doc.price_list_rate and doc.selling == 1:
        update_item_price_in_item(doc,"selling")
    elif doc.price_list_rate and doc.buying == 1:
        update_item_price_in_item(doc,"buying")

def update_item_price_in_item(doc,type):
    item_price = frappe.get_value("Item",{"item_code" : doc.item_code},"standard_{}_rate".format(type))
    if item_price and item_price == doc.price_list_rate:
        return
    else:
        item_doc = frappe.get_doc("Item",{"item_code" : doc.item_code})
        if type == "selling":  
            item_doc.db_set("standard_selling_rate",doc.price_list_rate)
        else:
            item_doc.db_set("standard_buying_rate",doc.price_list_rate)
