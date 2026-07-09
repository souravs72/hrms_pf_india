# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe
from frappe.utils import flt

STATUTORY_WAGE_CEILING = 15000
EPF_EMPLOYEE_RATE = 0.12
MANDATORY_PF_CAP = flt(STATUTORY_WAGE_CEILING * EPF_EMPLOYEE_RATE)


def get_pf_wages(employee_doc):
	"""Best-effort PF wage base from active salary structure assignment."""
	assignment = frappe.db.get_value(
		"Salary Structure Assignment",
		{"employee": employee_doc.name, "docstatus": 1},
		"base",
		order_by="from_date desc",
	)
	return flt(assignment)


def calculate_pf_breakup(employee_doc, pf_wages=None):
	pf_wages = flt(pf_wages if pf_wages is not None else get_pf_wages(employee_doc))
	mandatory = calculate_mandatory_pf(pf_wages)
	voluntary = calculate_voluntary_pf(employee_doc, pf_wages, mandatory)
	return {
		"pf_wages": pf_wages,
		"mandatory_pf": mandatory,
		"voluntary_pf": voluntary,
		"total_employee_pf": flt(mandatory + voluntary),
	}


def calculate_mandatory_pf(pf_wages):
	return flt(min(pf_wages, STATUTORY_WAGE_CEILING) * EPF_EMPLOYEE_RATE)


def calculate_voluntary_pf(employee_doc, pf_wages, mandatory_pf=None):
	contribution_type = employee_doc.get("pf_contribution_type") or "Statutory Minimum"
	if contribution_type == "Statutory Minimum":
		return 0

	if contribution_type == "Voluntary Fixed Amount":
		return flt(employee_doc.get("voluntary_pf_amount"))

	if contribution_type == "Voluntary on Full Basic":
		if pf_wages <= STATUTORY_WAGE_CEILING:
			return 0
		mandatory_pf = mandatory_pf if mandatory_pf is not None else calculate_mandatory_pf(pf_wages)
		return flt(max(0, pf_wages * EPF_EMPLOYEE_RATE - mandatory_pf))

	return 0
