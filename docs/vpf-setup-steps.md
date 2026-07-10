# Steps: Show Voluntary PF for Selected Employees

This is the exact path we used to successfully demonstrate voluntary PF (VPF) for some employees while others stay on mandatory PF only.

---

## Outcome

| Employee | Mandatory PF | Voluntary PF | Visible on salary slip |
|---|---|---|---|
| Employee with opt-in | ₹1,800 | ₹2,000 | **Provident Fund** + **Additional Provident Fund** |
| Employee without opt-in | ₹1,800 | — | **Provident Fund** only |

---

## Prerequisites

1. Company country = **India**
2. Apps installed: `frappe`, `erpnext`, `hrms`, `hrms_pf_india`
3. `bench migrate` completed after installing `hrms_pf_india`
4. Salary components exist:
   - **Provident Fund** (Component Type = Provident Fund)
   - **Additional Provident Fund** (Component Type = Additional Provident Fund) — created by the app

---

## Step 1 — Put mandatory PF in the Salary Structure (once for all)

1. Open **Salary Structure** (or create one, e.g. **Standard Monthly PF**).
2. Add earnings as needed (Basic, HRA, allowances, etc.).
3. Under **Deductions**, add:

| Field | Value |
|---|---|
| Salary Component | Provident Fund |
| Amount based on formula | Yes |
| Formula | `B * 0.12 if B <= 15000 else 1800` |
| Depends on Payment Days | No |

> Use this formula form. HRMS does **not** support `min()` in salary formulas.

4. Do **not** add **Additional Provident Fund** to the structure.
5. **Save** and **Submit** the structure.

**Why:** Mandatory PF is company-wide. Voluntary PF is per employee, not in the structure.

---

## Step 2 — Assign the structure to employees

1. Open **Salary Structure Assignment → New** for each employee.
2. Set:
   - Employee
   - Salary Structure = your structure from Step 1
   - From Date
   - Base (monthly CTC / base pay used by formulas)
   - Company / Currency
3. **Save** and **Submit**.

**Why:** VPF opt-in requires a submitted assignment. Without it, the Employee form will block enabling voluntary PF.

---

## Step 3 — Opt in voluntary PF only for selected employees

On each employee who wants VPF:

1. Open **Employee**.
2. Open section **Voluntary Provident Fund**.
3. Set:

| Field | Example |
|---|---|
| Opt for Voluntary PF | ✓ checked |
| Voluntary PF Amount | `2000` |
| Consent Date | e.g. `01-07-2026` |

4. **Save**.

**What happens automatically:**

- App validates amount > 0, consent date present, and salary structure assignment exists.
- App creates a submitted recurring **Additional Salary**:
  - Component = **Additional Provident Fund**
  - Amount = voluntary amount
  - Is Recurring = Yes

Employees who should **not** have VPF: leave **Opt for Voluntary PF** unchecked. No Additional Salary is created.

---

## Step 4 — Create / refresh the Salary Slip

1. Open **Salary Slip → New** (or use Payroll Entry).
2. Select the employee and payroll period.
3. **Save**.

### Expected result — employee WITH VPF

Deductions include:

- Provident Fund → mandatory (e.g. ₹1,800)
- **Additional Provident Fund** → voluntary (e.g. ₹2,000)
- Other deductions (e.g. Professional Tax)

### Expected result — employee WITHOUT VPF

Deductions include:

- Provident Fund → mandatory only
- **No** Additional Provident Fund row

---

## Step 5 — Verify Additional Salary (optional but useful in demos)

1. Open **Additional Salary**.
2. Filter by employee / component **Additional Provident Fund**.
3. Confirm a submitted recurring record exists only for opted-in employees.

---

## Step 6 — Print the payslip (demo)

1. Open the Salary Slip.
2. **Print** → format **Salary Slip Clean** (if installed via demo setup) or your company format.
3. Show earnings, deductions (including VPF row when opted in), and net pay.

---

## Changing or stopping VPF later

| Action | How |
|---|---|
| Change amount | Update **Voluntary PF Amount** on Employee → Save (app cancels/recreates Additional Salary) |
| Stop VPF | Uncheck **Opt for Voluntary PF** → Save (app disables Additional Salary) |
| Restart VPF | Check again, set amount + consent date → Save |

---

## Local demo shortcut (already done on `hrms-pf.localhost`)

```bash
bench --site hrms-pf.localhost execute hrms_pf_india.hrms_pf_india.setup.demo_payroll.setup_demo_payroll
```

This created:

- Sourav — VPF ₹2,000 (shows Additional Provident Fund on slip)
- Avishek — no VPF
- Structure **Standard Monthly PF**
- Sample slips + print format **Salary Slip Clean**

Full client walkthrough: [`client-demo-guide.md`](client-demo-guide.md)

---

## Production notes (`hrms-erp.ascratech.com`)

1. App is installed; Employee already has:
   - Opt for Voluntary PF
   - Voluntary PF Amount
   - Consent Date
2. Use an **existing** production Salary Structure that already has mandatory Provident Fund.
3. Ensure the PF formula uses the ₹15,000 ceiling pattern above (or your approved company formula).
4. For a demo employee:
   - Confirm Salary Structure Assignment exists
   - Opt in on Employee (checkbox + amount + consent)
   - Generate salary slip for the period
   - Show the extra **Additional Provident Fund** deduction row

Do **not** run the local demo payroll script on production unless you intentionally want demo employees/structure created there.

---

## Checklist before showing a client

- [ ] Mandatory PF visible on a non-VPF employee slip
- [ ] VPF employee has checkbox + amount + consent on Employee
- [ ] Additional Salary exists for that employee
- [ ] Salary slip shows **both** Provident Fund and Additional Provident Fund
- [ ] Net pay is lower by the VPF amount vs the same gross without VPF
- [ ] Print looks clean
