import requests
import base64
import os

url = "http://139.167.56.10:3000/send"

headers = {
    "x-api-key": "MITHRAN_ERP_2026_x8K9mP2Q7L"
}

# -------------------------------------------------------
# Option 1: Send a local file as attachment
# Change this path to any real file on your machine
# -------------------------------------------------------
file_path = "test.pdf"   # <-- change to your file path

if os.path.exists(file_path):
    with open(file_path, "rb") as f:
        b64_data = base64.b64encode(f.read()).decode()

    data = {
        "number": "918012998375",
        "message": "Hello from Mithran ERP — attachment test",   # caption  shown under file
        "attachment": {
            "data": b64_data,
            "mimetype": "application/pdf",     # change if not PDF
            "filename": os.path.basename(file_path)
        }
    }

    print(f"Sending file: {file_path}")
    response = requests.post(url, headers=headers, json=data)
    print("Response:", response.text)

else:
    # -------------------------------------------------------
    # Option 2: No local file — send via URL instead
    # The Node server will download it automatically
    # -------------------------------------------------------
    print(f"File '{file_path}' not found — sending via URL instead")

    data = {
        "number": "919047621499",
        "message": "Hello from Mithran ERP — URL attachment test",
        "attachment": {
            "url": "https://www.w3.org/WAI/WCAG21/quickref/wcag-21-quick-reference.pdf",  # sample PDF URL
            "filename": "sample.pdf"
        }
    }

    response = requests.post(url, headers=headers, json=data)
    print("Response:", response.text)