from __future__ import annotations

from pathlib import Path
from datetime import datetime
import base64


def _xor_encrypt(data: bytes, key: bytes) -> bytes:
	"""Encrypt/decrypt bytes using XOR with a repeating key."""
	if not key:
		raise ValueError("Encryption key must not be empty.")
	key_len = len(key)
	return bytes(b ^ key[i % key_len] for i, b in enumerate(data))


def collect_and_save_student_details(output_directory: str | Path = ".", filename: str | None = None) -> Path:
	"""Prompt for student details (name, age, email) and save them to a new text file.

	Args:
		output_directory: Directory where the file will be created. Defaults to current directory.
		filename: Optional explicit filename. If not provided, a timestamped filename is generated.

	Returns:
		Path: The path to the file that was created.
	"""

	def prompt_non_empty(prompt_text: str) -> str:
		while True:
			value = input(prompt_text).strip()
			if value:
				return value
			print("Value cannot be empty. Please try again.")

	def prompt_age(prompt_text: str) -> int:
		while True:
			value = input(prompt_text).strip()
			if value.isdigit():
				age_value = int(value)
				if 0 <= age_value <= 150:
					return age_value
			print("Please enter a valid age between 0 and 150.")

	def prompt_email(prompt_text: str) -> str:
		while True:
			email_value = input(prompt_text).strip()
			# Minimal sanity checks; not a full RFC validation
			if "@" in email_value and "." in email_value.split("@")[-1]:
				return email_value
			print("Please enter a valid email address (e.g., name@example.com).")

	student_name = prompt_non_empty("Enter student name: ")
	age = prompt_age("Enter student age: ")
	email = prompt_email("Enter student email: ")

	output_dir_path = Path(output_directory)
	output_dir_path.mkdir(parents=True, exist_ok=True)

	generated_filename = filename or f"student_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
	file_path = output_dir_path / generated_filename

	contents = [
		"Student Details",
		"================",
		f"Name:  {student_name}",
		f"Age:   {age}",
		f"Email: {email}",
	]

	plaintext = "\n".join(contents) + "\n"
	file_path.write_text(plaintext, encoding="utf-8")

	# Also create an encrypted copy using a user-provided key
	encryption_key = prompt_non_empty("Enter encryption key to create encrypted file: ")
	encrypted_bytes = _xor_encrypt(plaintext.encode("utf-8"), encryption_key.encode("utf-8"))
	encrypted_b64 = base64.b64encode(encrypted_bytes).decode("ascii")
	encrypted_path = file_path.with_name(f"{file_path.stem}_encrypted{file_path.suffix}")
	encrypted_path.write_text(encrypted_b64 + "\n", encoding="utf-8")

	print(f"Saved student details to: {file_path}")
	print(f"Saved encrypted student details to: {encrypted_path}")
	return file_path


if __name__ == "__main__":
	collect_and_save_student_details()


