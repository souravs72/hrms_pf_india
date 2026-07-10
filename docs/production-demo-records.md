# Production Demo Records

How voluntary PF was demonstrated on the live HRMS site using real company payroll data.

Slips were left in **Draft** so accounting / payroll submission is not affected.

---

## The three documents to open

| # | DocType | Purpose |
|---|---|---|
| 1 | **Additional Salary** | Recurring voluntary PF created by the app after Employee opt-in |
| 2 | **Salary Slip** (with VPF) | Shows **Provident Fund** + **Additional Provident Fund** |
| 3 | **Salary Slip** (without VPF) | Control employee — mandatory PF only, no Additional Provident Fund row |

On the production site these are:

| # | DocType | Document |
|---|---|---|
| 1 | Additional Salary | `HR-ADS-26-07-00003` (Additional Provident Fund, ₹2,000, recurring) |
| 2 | Salary Slip (with VPF) | `Sal Slip/HR-EMP-00036/00003` — July 2026 Draft |
| 3 | Salary Slip (without VPF) | `Sal Slip/HR-EMP-00041/00002` — July 2026 Draft |

Employee setup used:

- Opted in: existing employee on **Voluntary PF Salary Structure** (base from live assignment)
- Control: existing employee on **New 25-26** with VPF left off

Search in Desk:

- **Additional Salary** → filter Salary Component = Additional Provident Fund, July 2026
- **Salary Slip** → filter period Start Date = 01-07-2026, status Draft

---

## How this was achieved (real-world path)

### Prerequisites already on production

- Company country = India
- App `hrms_pf_india` installed and migrated
- Existing salary structures with **Provident Fund** deductions
- Active employees with submitted **Salary Structure Assignment**

### Step A — Working days for the demo period

Salary Slip needs a holiday list that covers the payroll month.

1. Created **Holiday List** for calendar year 2026 (weekly off: Sunday).
2. Set that holiday list on the two demo employees.

Without this, slip creation fails with “set a default Holiday List”.

### Step B — Document 1: Additional Salary (VPF)

On an active employee who already had a submitted assignment to a structure that includes mandatory Provident Fund:

1. Open **Employee** → section **Voluntary Provident Fund**
2. Check **Opt for Voluntary PF**
3. Set **Voluntary PF Amount** = 2000
4. Set **Consent Date** = first day of the demo month
5. Save

**Result:** App creates a submitted recurring **Additional Salary**:

- Salary Component = Additional Provident Fund  
- Is Recurring = Yes  
- Amount = 2000  

No manual Additional Salary entry was required.

### Step C — Document 2: Salary Slip with VPF

1. **Salary Slip → New**
2. Select the opted-in employee
3. Period = full demo month (monthly)
4. Save (leave as **Draft**)

**Result:** Deductions include:

- Provident Fund (from Salary Structure)
- **Additional Provident Fund** (from Additional Salary)
- Other structure deductions (e.g. Professional Tax / Income Tax) as applicable

### Step D — Document 3: Salary Slip without VPF

1. Pick a second active employee on a normal structure
2. Confirm **Opt for Voluntary PF** is unchecked
3. Create the same month’s Salary Slip as Draft

**Result:** Provident Fund appears; **Additional Provident Fund does not**.

---

## What to show in a client meeting

1. Open the opted-in **Employee** — checkbox, amount, consent date.  
2. Open **Additional Salary** — prove the app synced it.  
3. Open the **with-VPF** slip — point to the extra Additional Provident Fund row.  
4. Open the **without-VPF** slip — same process, no voluntary row.  
5. Optional: Print the with-VPF slip.

---

## Safety notes

- Demo salary slips are **Draft** — do not submit unless payroll intends to post them.
- Only two existing employees were used; no fake company or fake CTC masters were invented beyond a 2026 holiday list.
- Changing Voluntary PF Amount on Employee cancels/recreates Additional Salary (amount is not editable on submitted Additional Salary).
- To stop the demo VPF later: uncheck **Opt for Voluntary PF** on the employee and save.

---

## Related guides

- [vpf-setup-steps.md](vpf-setup-steps.md) — generic setup steps  
- [user-guide.md](user-guide.md) — product behaviour and demo narrative  
