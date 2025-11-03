from reportlab.lib.pagesizes import LETTER
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def make_sample_statement(path="samples/sample_statement.pdf"):
    c = canvas.Canvas(path, pagesize=LETTER)
    width, height = LETTER

    # --- Header ---
    c.setFont("Helvetica-Bold", 18)
    c.drawString(1 * inch, height - 1 * inch, "CHASE Card Services")

    c.setFont("Helvetica", 10)
    c.drawString(1 * inch, height - 1.3 * inch, "Customer Service: 1-800-935-9935")
    c.drawString(1 * inch, height - 1.5 * inch, "Account ending in 9876")

    # --- Statement Info ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1 * inch, height - 2 * inch, "Statement Period: January 1, 2025 to January 31, 2025")
    c.drawString(1 * inch, height - 2.3 * inch, "Payment Due Date: February 21, 2025")
    c.drawString(1 * inch, height - 2.6 * inch, "New Balance: $1,234.56")

    # --- Transactions header ---
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1 * inch, height - 3.2 * inch, "Transactions")

    # --- Transaction table ---
    c.setFont("Helvetica", 10)
    y = height - 3.5 * inch
    transactions = [
        ("01/03/25", "Starbucks Los Angeles CA", "-5.67"),
        ("01/10/25", "Amazon Marketplace", "-45.90"),
        ("01/15/25", "Spotify Subscription", "-9.99"),
        ("01/21/25", "Payment Received - Thank You", "100.00")
    ]
    c.drawString(1 * inch, y, "Date        Description                               Amount")
    y -= 0.2 * inch
    for date, desc, amt in transactions:
        c.drawString(1 * inch, y, date)
        c.drawString(2 * inch, y, desc)
        c.drawRightString(width - 1 * inch, y, amt)
        y -= 0.25 * inch

    # --- Footer ---
    c.setFont("Helvetica-Oblique", 8)
    c.drawString(1 * inch, 0.75 * inch, "This is a synthetic statement for testing parser functionality.")
    c.save()
    print(f"✅ Created sample statement at: {path}")

if __name__ == "__main__":
    make_sample_statement()
