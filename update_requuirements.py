# def clean_requirements(input_file, output_file):
#     with open(input_file, "r") as infile:
#         lines = infile.readlines()

#     cleaned_lines = [line for line in lines if "@" not in line]

#     with open(output_file, "w") as outfile:
#         outfile.writelines(cleaned_lines)

# if __name__ == "__main__":
#     input_file = "requirements.txt"
#     output_file = "requirements_cleaned.txt"
#     clean_requirements(input_file, output_file)
#     print(f"Cleaned requirements saved to {output_file}")


import ssl
print(ssl.OPENSSL_VERSION)
