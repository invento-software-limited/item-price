import frappe


def extend_validate(doc, method=None):
    # For Create And Update Item Price
    if doc.standard_selling_rate:
        item_price_update_or_create(doc, "selling")

    if doc.standard_buying_rate:
        item_price_update_or_create(doc, "buying")


def item_price_update_or_create(doc, type):
    field_name = "standard_{}_rate".format(type)
    price_list = frappe.db.get_single_value("{} Settings".format(type).capitalize(), "{}_price_list".format(type))
    if not price_list:
        price_list = "Standard {}".format(type.capitalize())

    if frappe.db.exists("Item Price", {"item_code": doc.item_code, "{}".format(type): 1, "price_list": price_list}):
        if doc.get(field_name) != frappe.get_value("Item Price",
                                                   {"item_code": doc.get("item_code"), "{}".format(type): 1,
                                                    "price_list": price_list}, "price_list_rate"):
            price_doc = frappe.get_doc("Item Price", {"item_code": doc.get("item_code"), "{}".format(type): 1,
                                                      "price_list": price_list})
            price_doc.price_list_rate = doc.get(field_name)
            price_doc.flags.ignore_validate = True
            price_doc.save()
    else:
        doc.db_set("standard_{}_rate".format(type), doc.get(field_name))
        new_price = frappe.new_doc("Item Price")
        new_price.item_code = doc.get("item_code")
        new_price.price_list = price_list if price_list else "Standard {}".format(type.capitalize())
        new_price.price_list_rate = doc.get(field_name)
        new_price.uom = doc.stock_uom
        if type == "selling":
            new_price.selling = 1
        else:
            new_price.buying = 1
        new_price.save()
