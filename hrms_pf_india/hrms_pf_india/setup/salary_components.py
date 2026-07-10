# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe
from frappe import _

ADDITIONAL_PF_COMPONENT = "Additional Provident Fund"


def ensure_pf_salary_components():
	"""Ensure the Additional Provident Fund deduction component exists for VPF."""
	if not frappe.db.has_column("Salary Component", "component_type"):
		frappe.throw(_("Salary Component field `component_type` is missing."))

	if frappe.db.exists("Salary Component", ADDITIONAL_PF_COMPONENT):
		frappe.db.set_value(
			"Salary Component",
			ADDITIONAL_PF_COMPONENT,
			{
				"component_type": "Additional Provident Fund",
				"type": "Deduction",
				"exempted_from_income_tax": 1,
				"remove_if_zero_valued": 1,
				"depends_on_payment_days": 0,
			},
		)
		return

	doc = frappe.get_doc(
		{
			"doctype": "Salary Component",
			"salary_component": ADDITIONAL_PF_COMPONENT,
			"salary_component_abbr": "APF",
			"component_type": "Additional Provident Fund",
			"type": "Deduction",
			"exempted_from_income_tax": 1,
			"remove_if_zero_valued": 1,
			"depends_on_payment_days": 0,
		}
	)
	doc.flags.ignore_permissions = True
	doc.insert(ignore_if_duplicate=True)
