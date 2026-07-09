# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe

ADDITIONAL_PF_COMPONENT = "Additional Provident Fund"
MANDATORY_PF_COMPONENT = "Provident Fund"


def ensure_pf_salary_components():
	_ensure_component(
		MANDATORY_PF_COMPONENT,
		component_type="Provident Fund",
		description="Mandatory employee EPF contribution (EPF Scheme 2026)",
	)
	_ensure_component(
		ADDITIONAL_PF_COMPONENT,
		component_type="Additional Provident Fund",
		description="Voluntary employee PF contribution (VPF) above statutory minimum",
		remove_if_zero_valued=1,
	)


def _ensure_component(name, component_type, description, remove_if_zero_valued=0):
	if frappe.db.exists("Salary Component", name):
		frappe.db.set_value(
			"Salary Component",
			name,
			{
				"component_type": component_type,
				"type": "Deduction",
				"exempted_from_income_tax": 1,
				"remove_if_zero_valued": remove_if_zero_valued,
			},
		)
		return

	doc = frappe.get_doc(
		{
			"doctype": "Salary Component",
			"salary_component": name,
			"salary_component_abbr": _abbr(name),
			"type": "Deduction",
			"description": description,
			"exempted_from_income_tax": 1,
			"remove_if_zero_valued": remove_if_zero_valued,
			"depends_on_payment_days": 0,
		}
	)
	doc.insert(ignore_permissions=True)

	if frappe.db.has_column("Salary Component", "component_type"):
		frappe.db.set_value("Salary Component", name, "component_type", component_type)


def _abbr(name):
	existing = {
		"Provident Fund": "PF",
		"Additional Provident Fund": "APF",
	}
	return existing.get(name, "".join(word[0] for word in name.split())[:10].upper())
