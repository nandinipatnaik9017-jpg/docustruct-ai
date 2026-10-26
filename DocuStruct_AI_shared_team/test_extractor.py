from extractor import analyze_invoice

print("Testing invoice extraction...")

try:
    result = analyze_invoice("sample_invoice.pdf")
    print("\nExtracted invoice data:")
    print(result)
except Exception as e:
    print("Error:", e)