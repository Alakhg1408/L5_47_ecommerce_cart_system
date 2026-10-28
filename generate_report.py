#!/usr/bin/env python3
"""
Render report.html to PDF using Google Chrome headless.
"""
import subprocess
import sys
import os

def main():
    chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    repo_dir = "/Users/alakhgupta/L5_47_ecommerce_cart_system-1"
    html_file = os.path.join(repo_dir, "report.html")
    pdf_primary = os.path.join(repo_dir, "Static_Code_Analysis_Report_PES2UG24CS051.pdf")
    pdf_secondary = os.path.join(repo_dir, "PES2UG24CS051_Lab5_Report.pdf")
    pdf_downloads = "/Users/alakhgupta/Downloads/PES2UG24CS051_Lab5_Report.pdf"

    if not os.path.exists(html_file):
        print(f"Error: {html_file} does not exist.")
        sys.exit(1)

    cmd = [
        chrome_path,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={pdf_primary}",
        "--no-pdf-header-footer",
        html_file
    ]

    print("Running Google Chrome to generate PDF...")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print("Chrome error:", result.stderr)
        sys.exit(1)

    print(f"Successfully generated: {pdf_primary}")

    # Copy to alternate locations for ease of access and submission
    subprocess.run(["cp", pdf_primary, pdf_secondary], check=True)
    print(f"Copied to: {pdf_secondary}")
    subprocess.run(["cp", pdf_primary, pdf_downloads], check=True)
    print(f"Copied to: {pdf_downloads}")

if __name__ == "__main__":
    main()
