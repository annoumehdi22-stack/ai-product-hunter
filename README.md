# 🕵️‍♂️ AI Product Hunter

An autonomous, multi-agent microservices pipeline that automates e-commerce product research, scraping, and AI analysis. 

## 🚀 Architecture & Workflow

This project replaces monolithic scripts with a scalable, Dockerized microservices architecture. It utilizes three specialized AI Agents collaborating via FastAPI, with a Streamlit frontend and Make.com webhook integrations.

1. **Agent 1 (The Navigator):** Receives the user prompt from the Streamlit UI and generates highly targeted search URLs.
2. **Agent 2 (The Scraper):** Navigates the web and extracts raw HTML using `undetected-chromedriver` running inside a headless Docker container. It bypasses bot-blocks and converts the raw data into clean Markdown using `markdownify`.
3. **Agent 3 (The Analyzer):** Processes the scraped Markdown data using Groq LLM to extract key insights, pricing, and product summaries.
4. **The Orchestrator:** The final structured data is sent via Webhooks to **Make.com**, which automatically logs the record into an **Airtable** database and sends a formatted alert to a **Slack** channel.

## 🛠️ Tech Stack

* **Backend:** Python, FastAPI (3 independent microservices)
* **Frontend:** Streamlit
* **Infrastructure:** Docker & Docker Compose (Headless Chromium configured)
* **Web Scraping:** Selenium, Undetected-Chromedriver, Markdownify
* **AI & LLM:** Groq API
* **Workflow Automation:** Make.com, Airtable, Slack API

## 🐳 How to Run Locally

1. Clone the repository:
   ```bash
   git clone [https://github.com/annoumehdi22-stack/ai-product-hunter.git](https://github.com/annoumehdi22-stack/ai-product-hunter.git)
   cd ai-product-hunter