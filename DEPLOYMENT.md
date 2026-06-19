# ShelfEye: Zero-Install Cloud Development & Deployment Guide

To build, manage, and deploy ShelfEye without installing a single file on your local machine, you will use **GitHub Codespaces** (a secure, cloud-hosted development environment running entirely in your browser) and **Streamlit Community Cloud** (for serverless deployment).

---

## ☁️ The Zero-Install Architecture

Instead of setting up local development tools, your entire workflow lives completely in the cloud:
* **GitHub** hosts your remote source code repository.
* **GitHub Codespaces** provides a browser-based VS Code environment to write, edit, and test code.
* **Streamlit Community Cloud** pulls code directly from your repository to provision and build the web interface.

---

## 🛠️ Step 1: Initialize Your Remote Repository

1. Go to **GitHub.com** and log in to your account.
2. Click the **New** button to initialize a new repository.
3. Name the repository exactly: `ShelfEye`.
4. Set the visibility status to **Public** or **Private** depending on your portfolio needs.
5. Check the box to **Add a README file**.
6. Select **Python** from the `.gitignore` template dropdown list.
7. Click **Create repository**.

---

## 💻 Step 2: Boot Up Your Cloud IDE (GitHub Codespaces)

1. Inside your newly created repository page, click the green **Code** button.
2. Select the **Codespaces** tab from the dropdown menu.
3. Click **Create codespace on main**.
4. A full cloud instance of Visual Studio Code will open inside a new browser tab. This isolated container environment has Python pre-installed on remote cloud servers.

---

## 📁 Step 3: Scaffold Your Directory Structure

Open the terminal pane at the bottom of your browser-based Codespaces window, paste this single command string, and press **Enter** to generate the standardized folder architecture:

```bash
mkdir src && touch src/app.py src/config.py src/engine.py src/llm_client.py requirements.txt .env
