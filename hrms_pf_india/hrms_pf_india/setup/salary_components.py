# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe
from frappe import _

ADDITIONAL_PF_COMPONENT = "Additional Provident Fund"
MANDATORY_PF_COMPONENT = "Provident Fund"

_COMPONENT_ABBR = {
	MANDATORY_PF_COMPONENT: "PF",
	ADDITIONAL_PF_COMPONENT: "APF",
}


def ensure_pf_salary_components():
	if not frappe.db.has_column("Salary Component", "component_type"):
		frappe.throw(_("Salary Component field `component_type` is missing."))

	_ensure_component(MANDATORY_PF_COMPONENT, component_type="Provident Fund")
	_ensure_component(
		ADDITIONAL_PF_COMPONENT,
		component_type="Additional Provident Fund",
		remove_if_zero_valued=1,
	)


def _ensure_component(name, component_type, remove_if_zero_valued=0):
	values = {
		"component_type": component_type,
		"type": "Deduction",
		"exempted_from_income_tax": 1,
		"remove_if_zero_valued": remove_if_zero_valued,
		"depends_on_payment_days": 0,
	}

	if frappe.db.exists("Salary Component", name):
		frappe.db.set_value("Salary Component", name, values)
		return

	doc = frappe.get_doc(
		{
			"doctype": "Salary Component",
			"salary_component": name,
			"salary_component_abbr": _COMPONENT_ABBR.get(name, name[:10].upper()),
			**values,
		}
	)
	doc.flags.ignore_permissions = True
	doc.insert(ignore_if_duplicate=True)
