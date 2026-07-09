# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe
from frappe.utils import flt

from hrms_pf_india.hrms_pf_india.constants import (
	EPF_EMPLOYEE_RATE,
	PF_CONTRIBUTION_STATUTORY,
	PF_CONTRIBUTION_VOLUNTARY_FIXED,
	PF_CONTRIBUTION_VOLUNTARY_FULL_BASIC,
	STATUTORY_WAGE_CEILING,
)

MANDATORY_PF_CAP = flt(STATUTORY_WAGE_CEILING * EPF_EMPLOYEE_RATE)


def get_pf_wages(employee):
	"""PF wage base from the latest submitted salary structure assignment."""
	if not employee:
		return 0

	return flt(
		frappe.db.get_value(
			"Salary Structure Assignment",
			{"employee": employee, "docstatus": 1},
			"base",
			order_by="from_date desc",
		)
	)


def calculate_pf_breakup(employee_doc, pf_wages=None):
	pf_wages = flt(pf_wages if pf_wages is not None else get_pf_wages(employee_doc.name))
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
	contribution_type = employee_doc.get("pf_contribution_type") or PF_CONTRIBUTION_STATUTORY
	if contribution_type == PF_CONTRIBUTION_STATUTORY:
		return 0

	if contribution_type == PF_CONTRIBUTION_VOLUNTARY_FIXED:
		return flt(employee_doc.get("voluntary_pf_amount"))

	if contribution_type == PF_CONTRIBUTION_VOLUNTARY_FULL_BASIC:
		if pf_wages <= STATUTORY_WAGE_CEILING:
			return 0
		mandatory_pf = mandatory_pf if mandatory_pf is not None else calculate_mandatory_pf(pf_wages)
		return flt(max(0, pf_wages * EPF_EMPLOYEE_RATE - mandatory_pf))

	return 0
