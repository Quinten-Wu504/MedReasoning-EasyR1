import os
import subprocess
import requests

GITHUB_USERNAME = "Quinten-Wu504"
LOCAL_FOLDER = "/opt/dlami/nvme/wujinxuan/EasyR1"
TOKEN = os.getenv("GITHUB_TOKEN") 
REPO_NAME = "MedReasoning-EasyR1"
DESCRIPTION = "Specific-Modified EasyR1 for our MedReasoning Project."

url = f"https://api.github.com/repos/{GITHUB_USERNAME}/{REPO_NAME}"
headers = {"Authorization": f"token {TOKEN}"}
response = requests.get(url, headers=headers)

if response.status_code == 404:
    print(f"仓库不存在，正在创建：{REPO_NAME}")
    data = {"name": REPO_NAME, "description": DESCRIPTION, "private": False}
    create_resp = requests.post(f"https://api.github.com/user/repos", headers=headers, json=data)
    if create_resp.status_code == 201:
        print("仓库创建成功")
    else:
        print("创建失败:", create_resp.text)
        exit(1)
else:
    print("仓库已存在，将直接推送")

os.chdir(LOCAL_FOLDER)

if not os.path.exists(os.path.join(LOCAL_FOLDER, ".git")):
    subprocess.run(["git", "init"])
    subprocess.run(["git", "branch", "-M", "main"])

subprocess.run(["git", "add", "."])
subprocess.run(["git", "commit", "-m", "Initial commit"], check=False)

remote_url = f"https://{GITHUB_USERNAME}:{TOKEN}@github.com/{GITHUB_USERNAME}/{REPO_NAME}.git"
subprocess.run(["git", "remote", "set-url", "origin", remote_url], check=False)
subprocess.run(["git", "remote", "add", "origin", remote_url], check=False)
subprocess.run(["git", "push", "-u", "origin", "main", "--force"])

print(f"上传完成，仓库地址：https://github.com/{GITHUB_USERNAME}/{REPO_NAME}")
