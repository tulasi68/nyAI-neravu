"""Rules layer: statutory checks applied alongside the learned model.

Section 138 NI Act timeline (verify against current law before relying on it):
  1. Cheque presented within its validity (3 months from date of cheque).
  2. Demand notice sent within 30 days of receiving the bank's return memo.
  3. Drawer has 15 days from receipt of notice to pay.
  4. Complaint filed within 1 month after those 15 days expire.
Any broken step usually means the complaint fails on limitation or maintainability.
This is decision support for a judge, not a ruling.
"""
from datetime import date, timedelta


def months_after(d: date, n: int) -> date:
    y, m = divmod(d.month - 1 + n, 12)
    y, m = d.year + y, m + 1
    day = min(d.day, [31, 29 if y % 4 == 0 and (y % 100 or y % 400 == 0) else 28,
                      31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1])
    return date(y, m, day)


def check_section_138(cheque_date, presented, return_memo, notice_sent, notice_received, complaint_filed):
    issues = []
    if presented > months_after(cheque_date, 3):
        issues.append("Cheque presented after its 3-month validity.")
    if notice_sent > return_memo + timedelta(days=30):
        issues.append("Demand notice sent more than 30 days after the return memo.")
    payment_deadline = notice_received + timedelta(days=15)
    complaint_deadline = months_after(payment_deadline, 1)
    if complaint_filed <= payment_deadline:
        issues.append("Complaint filed before the 15-day payment period ended (premature).")
    elif complaint_filed > complaint_deadline:
        issues.append(f"Complaint filed after the limitation date ({complaint_deadline}).")
    return {"statutory_ok": not issues, "issues": issues}


if __name__ == "__main__":
    ok = check_section_138(date(2025, 1, 10), date(2025, 2, 1), date(2025, 2, 5),
                           date(2025, 2, 20), date(2025, 2, 22), date(2025, 3, 20))
    late = check_section_138(date(2025, 1, 10), date(2025, 2, 1), date(2025, 2, 5),
                             date(2025, 4, 1), date(2025, 4, 3), date(2025, 6, 30))
    print(ok)
    print(late)
