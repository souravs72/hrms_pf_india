# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT
"""One-shot local demo setup: employees, salary structure, slips, print format.

Run:
  bench --site hrms-pf.localhost execute hrms_pf_india.hrms_pf_india.setup.demo_payroll.setup_demo_payroll
"""

from __future__ import annotations

import frappe
from frappe.utils import add_days, get_first_day, get_last_day, getdate, today

COMPANY = "Ascra Technology"
CURRENCY = "INR"
STRUCTURE_NAME = "Standard Monthly PF"
PRINT_FORMAT_NAME = "Salary Slip Clean"

DEMO_EMPLOYEES = [
	{
		"user": "sourav@ascratech.com",
		"first_name": "Sourav",
		"last_name": "S",
		"gender": "Male",
		"date_of_birth": "1995-01-15",
		"date_of_joining": "2024-04-01",
		"department": "Management - AT",
		"designation": "Business Analyst",
		"base": 60000,
		"opt_vpf": 1,
		"vpf_amount": 2000,
		"consent_date": "2026-07-01",
	},
	{
		"user": "avishek@clapgrow.com",
		"first_name": "Avishek",
		"last_name": "",
		"gender": "Male",
		"date_of_birth": "1994-06-20",
		"date_of_joining": "2024-06-01",
		"department": "Operations - AT",
		"designation": "Associate",
		"base": 45000,
		"opt_vpf": 0,
		"vpf_amount": 0,
		"consent_date": None,
	},
]


def setup_demo_payroll():
	frappe.flags.in_install = False
	_ensure_components()
	_ensure_holiday_list()
	_ensure_print_format()
	structure = _ensure_salary_structure()

	employees = []
	for row in DEMO_EMPLOYEES:
		emp = _ensure_employee(row)
		_ensure_assignment(emp, structure, row["base"])
		_apply_vpf(emp, row)
		employees.append(emp)

	slips = []
	for emp in employees:
		slips.append(_ensure_salary_slip(emp.name))

	frappe.db.commit()
	return {
		"company": COMPANY,
		"salary_structure": structure,
		"employees": [e.name for e in employees],
		"salary_slips": slips,
		"print_format": PRINT_FORMAT_NAME,
	}


def _ensure_holiday_list():
	from frappe.utils import getdate

	year = getdate(today()).year
	name = f"India Holidays {year}"
	if not frappe.db.exists("Holiday List", name):
		doc = frappe.get_doc(
			{
				"doctype": "Holiday List",
				"holiday_list_name": name,
				"from_date": f"{year}-01-01",
				"to_date": f"{year}-12-31",
				"weekly_off": "Sunday",
			}
		)
		doc.get_weekly_off_dates()
		doc.flags.ignore_permissions = True
		doc.insert()

	frappe.db.set_value("Company", COMPANY, "default_holiday_list", name)
	return name


def _ensure_components():
	components = [
		{
			"salary_component": "Other Allowances",
			"salary_component_abbr": "OA",
			"type": "Earning",
			"is_tax_applicable": 1,
			"depends_on_payment_days": 0,
		},
		{
			"salary_component": "Medical Allowance",
			"salary_component_abbr": "MA",
			"type": "Earning",
			"is_tax_applicable": 1,
			"depends_on_payment_days": 0,
		},
	]
	for values in components:
		name = values["salary_component"]
		if frappe.db.exists("Salary Component", name):
			frappe.db.set_value("Salary Component", name, "depends_on_payment_days", values["depends_on_payment_days"])
			continue
		doc = frappe.get_doc({"doctype": "Salary Component", **values})
		doc.flags.ignore_permissions = True
		doc.insert()

	# Formula-driven rows must not also depend on payment days on the component master
	for name in ("House Rent Allowance", "Other Allowances", "Medical Allowance", "Professional Tax"):
		if frappe.db.exists("Salary Component", name):
			frappe.db.set_value("Salary Component", name, "depends_on_payment_days", 0)

	if frappe.db.has_column("Salary Component", "component_type"):
		frappe.db.set_value("Salary Component", "Provident Fund", "component_type", "Provident Fund")
		if frappe.db.exists("Salary Component", "Additional Provident Fund"):
			frappe.db.set_value(
				"Salary Component",
				"Additional Provident Fund",
				"component_type",
				"Additional Provident Fund",
			)
		if frappe.db.exists("Salary Component", "Professional Tax"):
			frappe.db.set_value("Salary Component", "Professional Tax", "component_type", "Professional Tax")


def _ensure_salary_structure():
	if frappe.db.exists("Salary Structure", STRUCTURE_NAME):
		doc = frappe.get_doc("Salary Structure", STRUCTURE_NAME)
		if doc.docstatus == 0:
			doc.submit()
		return doc.name

	payment_account = frappe.db.get_value(
		"Account",
		{"company": COMPANY, "account_type": "Bank", "is_group": 0},
		"name",
	) or frappe.db.get_value("Account", {"company": COMPANY, "name": ["like", "Payroll Payable%"]}, "name")

	doc = frappe.get_doc(
		{
			"doctype": "Salary Structure",
			"name": STRUCTURE_NAME,
			"company": COMPANY,
			"currency": CURRENCY,
			"payroll_frequency": "Monthly",
			"is_active": "Yes",
			"payment_account": payment_account,
			"earnings": [
				{
					"salary_component": "Basic",
					"abbr": "B",
					"amount_based_on_formula": 1,
					"formula": "base * 0.50",
					"depends_on_payment_days": 1,
				},
				{
					"salary_component": "House Rent Allowance",
					"abbr": "HRA",
					"amount_based_on_formula": 1,
					"formula": "B * 0.40",
					"depends_on_payment_days": 0,
				},
				{
					"salary_component": "Medical Allowance",
					"abbr": "MA",
					"amount": 1250,
					"amount_based_on_formula": 0,
					"depends_on_payment_days": 0,
				},
				{
					"salary_component": "Other Allowances",
					"abbr": "OA",
					"amount_based_on_formula": 1,
					"formula": "base - B - HRA - MA",
					"depends_on_payment_days": 0,
				},
			],
			"deductions": [
				{
					"salary_component": "Provident Fund",
					"abbr": "PF",
					"amount_based_on_formula": 1,
					# Statutory employee PF: 12% of Basic, capped at ₹15,000 wage ceiling
					"formula": "B * 0.12 if B <= 15000 else 1800",
					"depends_on_payment_days": 0,
				},
				{
					"salary_component": "Professional Tax",
					"abbr": "PT",
					"amount": 200,
					"amount_based_on_formula": 0,
					"depends_on_payment_days": 0,
				},
			],
		}
	)
	doc.flags.ignore_permissions = True
	doc.insert()
	doc.submit()
	return doc.name


def _ensure_employee(row):
	_prepare_user(row["user"])

	existing = frappe.db.get_value("Employee", {"user_id": row["user"]}, "name")
	if existing:
		emp = frappe.get_doc("Employee", existing)
	else:
		emp = frappe.get_doc(
			{
				"doctype": "Employee",
				"first_name": row["first_name"],
				"last_name": row["last_name"] or None,
				"company": COMPANY,
				"status": "Active",
				"gender": row["gender"],
				"date_of_birth": row["date_of_birth"],
				"date_of_joining": row["date_of_joining"],
				"department": row["department"] if frappe.db.exists("Department", row["department"]) else None,
				"designation": row["designation"] if frappe.db.exists("Designation", row["designation"]) else None,
				"user_id": row["user"],
				"create_user_permission": 1,
				"prefered_contact_email": "Company Email",
				"company_email": row["user"],
				"prefered_email": row["user"],
			}
		)
		emp.flags.ignore_permissions = True
		emp.insert()

	# India PF account placeholder (UAN-style)
	if frappe.db.has_column("Employee", "provident_fund_account") and not emp.get("provident_fund_account"):
		emp.db_set("provident_fund_account", f"100{emp.name[-4:].zfill(4)}123456", update_modified=False)

	return emp


def _prepare_user(email):
	user = frappe.get_doc("User", email)
	changed = False
	if user.user_type != "System User":
		user.user_type = "System User"
		changed = True
	for role in ("Employee", "Employee Self Service"):
		if not any(r.role == role for r in user.roles):
			user.append("roles", {"role": role})
			changed = True
	if changed:
		user.flags.ignore_permissions = True
		user.save()


def _ensure_assignment(employee, structure, base):
	existing = frappe.db.get_value(
		"Salary Structure Assignment",
		{"employee": employee.name, "salary_structure": structure, "docstatus": 1},
		"name",
	)
	if existing:
		frappe.db.set_value("Salary Structure Assignment", existing, "base", base)
		return existing

	from_date = employee.date_of_joining or "2024-04-01"
	doc = frappe.get_doc(
		{
			"doctype": "Salary Structure Assignment",
			"employee": employee.name,
			"salary_structure": structure,
			"from_date": from_date,
			"company": COMPANY,
			"currency": CURRENCY,
			"base": base,
			"variable": 0,
		}
	)
	doc.flags.ignore_permissions = True
	doc.insert()
	doc.submit()
	return doc.name


def _apply_vpf(employee, row):
	if not frappe.db.has_column("Employee", "opt_for_voluntary_pf"):
		return

	employee.reload()
	employee.opt_for_voluntary_pf = 1 if row.get("opt_vpf") else 0
	employee.voluntary_pf_amount = row.get("vpf_amount") or 0
	employee.pf_consent_date = row.get("consent_date")
	employee.flags.ignore_permissions = True
	employee.save()


def _ensure_salary_slip(employee):
	start = get_first_day(today())
	end = get_last_day(today())

	existing = frappe.db.get_value(
		"Salary Slip",
		{"employee": employee, "start_date": start, "end_date": end, "docstatus": ["<", 2]},
		"name",
	)
	if existing:
		doc = frappe.get_doc("Salary Slip", existing)
		if doc.docstatus == 0:
			doc.flags.ignore_permissions = True
			doc.save()
		return doc.name

	doc = frappe.get_doc(
		{
			"doctype": "Salary Slip",
			"employee": employee,
			"company": COMPANY,
			"posting_date": today(),
			"payroll_frequency": "Monthly",
			"start_date": start,
			"end_date": end,
			"currency": CURRENCY,
		}
	)
	doc.flags.ignore_permissions = True
	doc.insert()
	doc.save()
	return doc.name


def _ensure_print_format():
	html = _print_format_html()
	if frappe.db.exists("Print Format", PRINT_FORMAT_NAME):
		doc = frappe.get_doc("Print Format", PRINT_FORMAT_NAME)
		doc.html = html
		doc.custom_format = 1
		doc.print_format_type = "Jinja"
		doc.doc_type = "Salary Slip"
		doc.standard = "No"
		doc.disabled = 0
		doc.flags.ignore_permissions = True
		doc.save()
	else:
		doc = frappe.get_doc(
			{
				"doctype": "Print Format",
				"name": PRINT_FORMAT_NAME,
				"doc_type": "Salary Slip",
				"module": "Payroll",
				"standard": "No",
				"custom_format": 1,
				"print_format_type": "Jinja",
				"html": html,
			}
		)
		doc.flags.ignore_permissions = True
		doc.insert()

	# Default print format for Salary Slip on this site
	frappe.make_property_setter(
		{
			"doctype": "Salary Slip",
			"doctype_or_field": "DocType",
			"property": "default_print_format",
			"value": PRINT_FORMAT_NAME,
			"property_type": "Data",
		},
		is_system_generated=False,
		validate_fields_for_doctype=False,
	)


def _print_format_html():
	return """
<style>
  .payslip { font-family: Helvetica, Arial, sans-serif; color: #1f2937; font-size: 12px; line-height: 1.45; }
  .company-name { font-size: 20px; font-weight: 700; }
  .doc-title { font-size: 14px; font-weight: 700; text-transform: uppercase; letter-spacing: 1px; text-align: right; }
  .meta { color: #6b7280; margin-top: 2px; }
  .rule { border: 0; border-top: 2px solid #111827; margin: 12px 0 16px; }
  .info, .money, .totals { width: 100%; border-collapse: collapse; }
  .info th { text-align: left; width: 18%; color: #6b7280; font-weight: 500; padding: 5px 6px; }
  .info td { text-align: left; font-weight: 600; padding: 5px 6px; width: 32%; }
  .section-title { font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; color: #374151; margin: 14px 0 6px; }
  .money th { background: #f3f4f6; text-align: left; padding: 8px; border-bottom: 1px solid #e5e7eb; }
  .money td { padding: 7px 8px; border-bottom: 1px solid #f3f4f6; }
  .money .amt, .totals .value { text-align: right; white-space: nowrap; }
  .totals td { padding: 8px; }
  .totals .label { color: #4b5563; }
  .net-row td { background: #111827; color: #fff; font-size: 13px; font-weight: 700; }
  .words { margin-top: 12px; padding: 10px 12px; background: #f9fafb; border: 1px solid #e5e7eb; }
  .sign-table { width: 100%; margin-top: 48px; }
  .sign-table td { width: 45%; text-align: center; color: #6b7280; border-top: 1px solid #d1d5db; padding-top: 8px; }
  .sign-spacer { width: 10%; border: 0 !important; }
</style>

<div class="payslip">
  <table class="info">
    <tr>
      <td colspan="2">
        <div class="company-name">{{ doc.company }}</div>
        <div class="meta">Payslip for {{ frappe.format(doc.start_date, {"fieldtype":"Date"}) }} – {{ frappe.format(doc.end_date, {"fieldtype":"Date"}) }}</div>
      </td>
      <td colspan="2">
        <div class="doc-title">Salary Slip</div>
        <div class="meta" style="text-align:right;">{{ doc.name }}</div>
      </td>
    </tr>
  </table>
  <hr class="rule">

  <table class="info">
    <tr>
      <th>Employee</th><td>{{ doc.employee_name }} ({{ doc.employee }})</td>
      <th>Department</th><td>{{ doc.department or "—" }}</td>
    </tr>
    <tr>
      <th>Designation</th><td>{{ doc.designation or "—" }}</td>
      <th>Payment Days</th><td>{{ doc.payment_days }} / {{ doc.total_working_days }}</td>
    </tr>
  </table>

  <div class="section-title">Earnings</div>
  <table class="money">
    <thead><tr><th>Component</th><th class="amt">Amount ({{ doc.currency }})</th></tr></thead>
    <tbody>
      {% for row in doc.earnings %}
        {% if row.amount %}
        <tr>
          <td>{{ row.salary_component }}</td>
          <td class="amt">{{ frappe.format(row.amount, {"fieldtype":"Currency", "options": doc.currency}) }}</td>
        </tr>
        {% endif %}
      {% endfor %}
    </tbody>
  </table>

  <div class="section-title">Deductions</div>
  <table class="money">
    <thead><tr><th>Component</th><th class="amt">Amount ({{ doc.currency }})</th></tr></thead>
    <tbody>
      {% for row in doc.deductions %}
        {% if row.amount %}
        <tr>
          <td>{{ row.salary_component }}</td>
          <td class="amt">{{ frappe.format(row.amount, {"fieldtype":"Currency", "options": doc.currency}) }}</td>
        </tr>
        {% endif %}
      {% endfor %}
    </tbody>
  </table>

  <table class="totals">
    <tr>
      <td class="label">Gross Pay</td>
      <td class="value">{{ frappe.format(doc.gross_pay, {"fieldtype":"Currency", "options": doc.currency}) }}</td>
    </tr>
    <tr>
      <td class="label">Total Deduction</td>
      <td class="value">{{ frappe.format(doc.total_deduction, {"fieldtype":"Currency", "options": doc.currency}) }}</td>
    </tr>
    <tr class="net-row">
      <td>Net Pay</td>
      <td class="value">{{ frappe.format(doc.rounded_total or doc.net_pay, {"fieldtype":"Currency", "options": doc.currency}) }}</td>
    </tr>
  </table>

  {% if doc.total_in_words %}
  <div class="words"><strong>In words:</strong> {{ doc.total_in_words }}</div>
  {% endif %}

  <table class="sign-table">
    <tr>
      <td>Employee Signature</td>
      <td class="sign-spacer"></td>
      <td>Authorized Signatory</td>
    </tr>
  </table>
</div>
""".strip()
