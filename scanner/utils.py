import hashlib
import math
import string

def get_file_hashes(file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        md5 = hashlib.md5(content).hexdigest()
        sha256 = hashlib.sha256(content).hexdigest()
    return md5, sha256

def calculate_entropy(data):
    if not data:
        return 0
    entropy = 0
    for x in set(data):
        p_x = data.count(x) / len(data)
        entropy -= p_x * math.log2(p_x)
    return round(entropy, 2)

def extract_strings(binary_data):
    return [s.decode() for s in binary_data.split(b'\x00') if len(s) > 4 and all(chr(c) in string.printable for c in s)]

def scan_file(file_path):
    with open(file_path, 'rb') as f:
        binary = f.read()

    entropy = calculate_entropy(binary.decode('latin-1', errors='ignore'))
    strings_found = extract_strings(binary)

    suspicious_keywords = ['powershell', 'base64', 'eval', 'cmd.exe', 'wget', 'curl']
    flagged = [s for s in strings_found if any(k in s.lower() for k in suspicious_keywords)]

    verdict = 'Malicious' if entropy > 7.5 and flagged else 'Suspicious' if flagged else 'Safe'

    return {
        "entropy": entropy,
        "suspicious_strings": flagged[:10],
        "verdict": verdict
    }
