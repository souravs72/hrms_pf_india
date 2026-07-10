# Steps: Enable Voluntary PF for Selected Employees

Use this when most employees stay on mandatory PF and only some opt into voluntary PF (VPF).

---

## Outcome

| Employee | Mandatory PF | Voluntary PF | On salary slip |
|---|---|---|---|
| Opted in | From Salary Structure | Fixed monthly amount | **Provident Fund** + **Additional Provident Fund** |
| Not opted in | From Salary Structure | — | **Provident Fund** only |

---

## Prerequisites

1. Company country = **India**
2. Apps installed: Frappe, ERPNext, HRMS, and `hrms_pf_india`
3. Migrate completed after installing the app
4. Salary components:
   - **Provident Fund** (Component Type = Provident Fund)
   - **Additional Provident Fund** (Component Type = Additional Provident Fund) — ensured by the app

---

## Step 1 — Mandatory PF in the Salary Structure

1. Open or create a **Salary Structure**.
2. Configure earnings as required (Basic, HRA, allowances, etc.).
3. Under **Deductions**, add:

| Field | Value |
|---|---|
| Salary Component | Provident Fund |
| Amount based on formula | Yes |
| Formula | `B * 0.12 if B <= 15000 else 1800` |
| Depends on Payment Days | No |

> Use this form. HRMS does not support `min()` in salary formulas.

4. Do **not** add **Additional Provident Fund** to the structure.
5. Save and submit.

---

## Step 2 — Assign the structure

1. Create a **Salary Structure Assignment** for each employee.
2. Set employee, structure, from date, base pay, company, and currency.
3. Save and submit.

VPF opt-in requires a submitted assignment.

---

## Step 3 — Opt in only for selected employees

On each employee who wants VPF:

1. Open **Employee**.
2. Open **Voluntary Provident Fund**.
3. Set:

| Field | Purpose |
|---|---|
| Opt for Voluntary PF | Enable VPF |
| Voluntary PF Amount | Monthly voluntary amount |
| Consent Date | Required when opted in |

4. Save.

The app then:

- Validates amount, consent date, and salary structure assignment
- Creates a submitted recurring **Additional Salary** for **Additional Provident Fund**

Leave the checkbox unchecked for employees without VPF.

---

## Step 4 — Create the Salary Slip

1. Create a **Salary Slip** (or use Payroll Entry) for the period.
2. Save and review deductions.

**With VPF:** Provident Fund + Additional Provident Fund (+ other deductions)  
**Without VPF:** Provident Fund only (+ other deductions)

---

## Step 5 — Optional checks

1. **Additional Salary** — recurring Additional Provident Fund exists only for opted-in employees.
2. **Print** — confirm the payslip shows the VPF row when applicable.
3. **Provident Fund Deductions** report — mandatory and additional PF appear separately.

---

## Change or stop VPF later

| Action | How |
|---|---|
| Change amount | Update Voluntary PF Amount on Employee → Save |
| Stop VPF | Uncheck Opt for Voluntary PF → Save |
| Restart VPF | Check again, set amount and consent date → Save |

---

## Go-live checklist

- [ ] Company country is India
- [ ] `hrms_pf_india` installed and migrated
- [ ] Mandatory PF formula uses the ₹15,000 ceiling pattern (or your approved formula)
- [ ] Voluntary PF is not in the Salary Structure
- [ ] Salary Structure Assignment exists before enabling VPF
- [ ] Provident Fund Account (UAN) filled on employees where needed
- [ ] Opted-in employees have checkbox, amount, and consent date
- [ ] Sample slips reviewed for one opted-in and one non-opted employee
