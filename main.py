import os
import shutil
import zipfile
import sys
import patcher

def cleanup():
    if os.path.exists('data/ipa.zip'):
        os.remove('data/ipa.zip')
    if os.path.exists('data/ipa'):
        shutil.rmtree('data/ipa')
    if os.path.exists('data'):
        shutil.rmtree('data')

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <IP>")
        return

    ip = sys.argv[1]

    if len(ip) > 27:
        print("ERROR: IP too long")
        return

    if not os.path.exists("ipa.ipa"):
        print("ERROR: ipa.ipa not found in repo root")
        return

    print(f"[INFO] Using IP: {ip}")

    os.makedirs("data", exist_ok=True)

    shutil.copyfile("ipa.ipa", "data/ipa.zip")

    print("[INFO] Extracting IPA")
    with zipfile.ZipFile("data/ipa.zip", 'r') as zip_ref:
        zip_ref.extractall("data/ipa")

    binary_path = "./data/ipa/Payload/minecraftearthtf.app/minecraftearthtf"

    if not patcher.hex_bytes_in_file(
        "68747470733A2F2F6C6F6361746F722E6D6365736572762E6E6574",
        binary_path
    ):
        print("[ERROR] File appears encrypted or unsupported")
        cleanup()
        return

    print("[INFO] Patching...")

    patcher.patch_app_name()
    patcher.remove_drm()
    patcher.remove_useless_files()
    patcher.patch_ip(ip)
    patcher.patch_sunset_time()

    print("[INFO] Repacking IPA")
    patcher.zip_folder_contents("data/ipa/", "patched.ipa")

    print("[SUCCESS] Done! Output: patched.ipa")

    cleanup()

if __name__ == "__main__":
    main()
