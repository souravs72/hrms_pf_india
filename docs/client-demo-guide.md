# Voluntary Provident Fund (VPF) — Client Demo Guide

**Product:** HRMS PF India (extension for Frappe HRMS)  
**Demo site:** `hrms-pf.localhost`  
**Company:** Ascra Technology (India)

This guide is for walking a client through how mandatory PF and voluntary PF work, using the demo already set up on the local site.

---

## 1. What the client should understand (30 seconds)

| Topic | How it works |
|---|---|
| **Mandatory PF** | Configured once in the **Salary Structure**. Same rule for all employees. |
| **Voluntary PF (VPF)** | Employee opts in on their **Employee** form (checkbox + amount + consent date). |
| **Salary slip** | Mandatory PF always appears. If opted in, an extra **Additional Provident Fund** row is added. |
| **No duplicate work** | HR does not manually create Additional Salary for each VPF employee — the app syncs it. |

---

## 2. Demo accounts (already created)

| Employee | User | Monthly CTC (base) | VPF |
|---|---|---|---|
| **Sourav S** (`HR-EMP-00001`) | sourav@ascratech.com | ₹60,000 | Yes — ₹2,000 / month |
| **Avishek** (`HR-EMP-00002`) | avishek@clapgrow.com | ₹45,000 | No |

Both users have **Employee** + **Employee Self Service** roles.

**Login:** Administrator (or the employee users above).

---

## 3. Demo script (recommended order)

### Step A — Show the shared salary structure (mandatory PF)

1. Open **Salary Structure** → **Standard Monthly PF**
2. Point out **Earnings**:
   - Basic = 50% of base  
   - HRA = 40% of Basic  
   - Medical Allowance = ₹1,250  
   - Other Allowances = remainder  
3. Point out **Deductions**:
   - **Provident Fund** formula: `B * 0.12 if B <= 15000 else 1800`  
     → 12% of Basic, capped at the ₹15,000 wage ceiling (max ₹1,800)  
   - **Professional Tax** = ₹200  

**Talking point:** One structure for the company. Mandatory PF is not configured per employee.

---

### Step B — Show employee without VPF (Avishek)

1. Open **Employee** → **Avishek** (`HR-EMP-00002`)
2. Scroll to section **Voluntary Provident Fund**
3. Show: **Opt for Voluntary PF** is unchecked — amount and consent date are hidden
4. Open **Salary Slip** → `Sal Slip/HR-EMP-00002/00001`
5. Show deductions:
   - Provident Fund → ₹1,800  
   - Professional Tax → ₹200  
   - **No** Additional Provident Fund row  
6. Net pay ≈ ₹43,000  

**Talking point:** Default employees need zero extra setup for VPF.

---

### Step C — Show employee with VPF (Sourav)

1. Open **Employee** → **Sourav S** (`HR-EMP-00001`)
2. In **Voluntary Provident Fund**:
   - **Opt for Voluntary PF** ✓  
   - **Voluntary PF Amount** = ₹2,000  
   - **Consent Date** = 01-07-2026  
3. Open **Additional Salary** for this employee  
   - Recurring **Additional Provident Fund** = ₹2,000 (created automatically on save)  
4. Open **Salary Slip** → `Sal Slip/HR-EMP-00001/00001`
5. Show deductions:
   - Provident Fund → ₹1,800 (mandatory)  
   - Additional Provident Fund → ₹2,000 (voluntary)  
   - Professional Tax → ₹200  
6. Net pay ≈ ₹56,000  

**Talking point:** Opt-in on Employee → app creates Additional Salary → salary slip gets one extra row. Clean separation for EPFO reporting.

---

### Step D — Show the payslip print

1. On either salary slip, click **Print**
2. Select format **Salary Slip Clean** (default)
3. Show earnings, deductions, gross, net, and amount in words

**Talking point:** Client-ready payslip layout for sharing with employees.

---

### Step E — (Optional live change) Toggle VPF

1. Open Avishek’s Employee form  
2. Check **Opt for Voluntary PF**, enter amount (e.g. ₹1,000), set **Consent Date**, **Save**  
3. Show that a new **Additional Salary** is created  
4. Create / refresh a salary slip for the period — **Additional Provident Fund** appears  
5. Uncheck the opt-in and **Save** — Additional Salary is disabled  

---

## 4. Numbers cheat-sheet (for Q&A)

### Sourav — base ₹60,000

| Component | Amount |
|---|---|
| Basic | ₹30,000 |
| HRA | ₹12,000 |
| Medical Allowance | ₹1,250 |
| Other Allowances | ₹16,750 |
| **Gross** | **₹60,000** |
| Provident Fund (mandatory) | ₹1,800 |
| Additional Provident Fund (VPF) | ₹2,000 |
| Professional Tax | ₹200 |
| **Total deduction** | **₹4,000** |
| **Net** | **₹56,000** |

### Avishek — base ₹45,000

| Component | Amount |
|---|---|
| Basic | ₹22,500 |
| HRA | ₹9,000 |
| Medical Allowance | ₹1,250 |
| Other Allowances | ₹12,250 |
| **Gross** | **₹45,000** |
| Provident Fund (mandatory) | ₹1,800 |
| Professional Tax | ₹200 |
| **Total deduction** | **₹2,000** |
| **Net** | **₹43,000** |

---

## 5. Quick links (local desk)

| What | Path |
|---|---|
| Salary Structure | `/app/salary-structure/Standard%20Monthly%20PF` |
| Sourav (with VPF) | `/app/employee/HR-EMP-00001` |
| Avishek (no VPF) | `/app/employee/HR-EMP-00002` |
| Sourav slip | `/app/salary-slip/Sal%20Slip/HR-EMP-00001/00001` |
| Avishek slip | `/app/salary-slip/Sal%20Slip/HR-EMP-00002/00001` |
| Print format | `/app/print-format/Salary%20Slip%20Clean` |
| Additional Salary list | `/app/additional-salary` |
| PF report | `/app/query-report/Provident%20Fund%20Deductions` |

---

## 6. How the product works (for technical stakeholders)

```
Salary Structure
  └── Provident Fund (mandatory formula for everyone)
        ↓
Employee form
  └── Opt for Voluntary PF + Amount + Consent Date
        ↓
App syncs recurring Additional Salary
  └── Component: Additional Provident Fund
        ↓
Salary Slip
  ├── Provident Fund          ← from structure
  └── Additional Provident Fund ← from Additional Salary (only if opted in)
```

### Employee fields (app)

| Field | Purpose |
|---|---|
| Opt for Voluntary PF | Checkbox to enable VPF |
| Voluntary PF Amount | Monthly voluntary amount |
| Consent Date | Required when opted in |

### What HRMS still owns

- Mandatory PF formula and salary structure  
- Payroll entry / salary slip generation  
- Provident Fund Deductions report  
- Journal / bank entries  

### What this app adds

- Clean opt-in UI on Employee  
- Auto-create / update / disable Additional Salary for VPF  
- Validation (amount > 0, consent date, salary structure assignment required)

---

## 7. Production checklist (after go-live)

- [ ] Company country = **India**
- [ ] App `hrms_pf_india` installed and migrated
- [ ] Salary Structure has mandatory PF with ₹15,000 ceiling formula  
  (`B * 0.12 if B <= 15000 else 1800` — note: `min()` is not available in HRMS formulas)
- [ ] Do **not** put voluntary PF in the structure
- [ ] Salary Structure Assignment exists for each employee **before** enabling VPF
- [ ] Employee **Provident Fund Account** (UAN) filled where needed
- [ ] For VPF employees: checkbox + amount + consent date
- [ ] Run **Provident Fund Deductions** report monthly for remittance

---

## 8. Reset / recreate local demo

```bash
bench --site hrms-pf.localhost execute hrms_pf_india.hrms_pf_india.setup.demo_payroll.setup_demo_payroll
```

Safe to re-run: updates structure, employees, VPF flags, slips, and print format.

---

## 9. Client FAQ

**Q: Can each employee choose a different VPF amount?**  
Yes. Amount is per employee on the Employee form.

**Q: Does the employer have to match VPF?**  
No. Matching is optional under EPF rules. This app only handles the employee voluntary deduction.

**Q: Will VPF mix into mandatory PF on the slip?**  
No. They appear as separate rows and separate columns in the PF report.

**Q: What if someone stops VPF?**  
Uncheck **Opt for Voluntary PF** and save. The recurring Additional Salary is disabled; future slips won’t include it.

**Q: Do we need a custom salary structure per VPF employee?**  
No. One shared structure + per-employee opt-in is enough.

---

*Aligned with app `hrms_pf_india` (checkbox + amount + consent). Demo data on site `hrms-pf.localhost`.*
