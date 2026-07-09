# Copyright (c) 2026, Ascra Technologies and contributors
# License: MIT

import frappe
from frappe.tests.utils import FrappeTestCase

from hrms_pf_india.hrms_pf_india.constants import PF_CONTRIBUTION_STATUTORY, PF_CONTRIBUTION_VOLUNTARY_FIXED
from hrms_pf_india.hrms_pf_india.utils.pf_calculator import (
	calculate_mandatory_pf,
	calculate_pf_breakup,
	calculate_voluntary_pf,
)


class TestPFCalculator(FrappeTestCase):
	def test_mandatory_pf_at_ceiling(self):
		self.assertEqual(calculate_mandatory_pf(15000), 1800)
		self.assertEqual(calculate_mandatory_pf(60000), 1800)

	def test_mandatory_pf_below_ceiling(self):
		self.assertEqual(calculate_mandatory_pf(10000), 1200)

	def test_voluntary_fixed_amount(self):
		doc = frappe._dict(
			pf_contribution_type=PF_CONTRIBUTION_VOLUNTARY_FIXED,
			voluntary_pf_amount=2500,
		)
		self.assertEqual(calculate_voluntary_pf(doc, 60000), 2500)

	def test_voluntary_full_basic(self):
		doc = frappe._dict(pf_contribution_type="Voluntary on Full Basic")
		breakup = calculate_pf_breakup(doc, pf_wages=60000)
		self.assertEqual(breakup["mandatory_pf"], 1800)
		self.assertEqual(breakup["voluntary_pf"], 5400)
		self.assertEqual(breakup["total_employee_pf"], 7200)

	def test_statutory_only_has_no_voluntary(self):
		doc = frappe._dict(pf_contribution_type=PF_CONTRIBUTION_STATUTORY)
		breakup = calculate_pf_breakup(doc, pf_wages=60000)
		self.assertEqual(breakup["voluntary_pf"], 0)
		self.assertEqual(breakup["total_employee_pf"], 1800)

	def test_voluntary_full_basic_below_ceiling(self):
		doc = frappe._dict(pf_contribution_type="Voluntary on Full Basic")
		breakup = calculate_pf_breakup(doc, pf_wages=12000)
		self.assertEqual(breakup["mandatory_pf"], 1440)
		self.assertEqual(breakup["voluntary_pf"], 0)

	def test_zero_wages_returns_zero_mandatory(self):
		self.assertEqual(calculate_mandatory_pf(0), 0)
