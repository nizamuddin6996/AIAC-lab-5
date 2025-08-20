# Script to collect user data from the console

# Collect user data
name = input("Enter your name: ")
age = input("Enter your age: ")
email = input("Enter your email: ")

# Display collected data
print("\nCollected Data:")
print(f"Name: {name}")
print(f"Age: {age}")
print(f"Email: {email}")

# --- Data Protection & Anonymization Comments ---
# 1. Avoid storing sensitive data in plain text files.
# 2. Use hashing (e.g., hashlib) to anonymize names/emails if storage is required.
# 3. Remove or mask personally identifiable information (PII) before sharing data.
# 4. Use secure storage solutions (e.g., encrypted databases) for sensitive data.
# 5. Always comply with data protection regulations (e.g., GDPR).