import streamlit as st
import requests
import time

st.set_page_config(page_title="AI Product Hunter", page_icon="🕵️‍♂️", layout="centered")

st.title("🕵️‍♂️ AI Product Hunter - Dashboard")
st.markdown("🚀 Automation kamla: L-pipeline ghadi y-doz rasso mn A tal Z. T9der t-7bess l-khedma f ay we9t b l-bouton **'Stop'** l-fou9 3la l-imen.")

col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input("Smya dyal l-produit (ex: Gaming Mouse):")
with col2:
    category = st.text_input("Catégorie (ex: Electronics):")

if st.button("🚀 Lancer l'Agent Hunter (Auto-Pilot)"):
    if product_name and category:
        try:
            # ==========================================
            # ETAPE 1: AGENT 1 (URL GENERATOR)
            # ==========================================
            with st.spinner("🕵️‍♂️ Agent 1 kay-9ad l-lien dyal s-search..."):
                api_url_agent1 = "http://agent1:8001/api/v1/generate-url"
                res1 = requests.post(api_url_agent1, json={"product_name": product_name, "category": category})
                
                if res1.status_code == 200:
                    data1 = res1.json()
                    if data1.get("status") == "success":
                        target_url = data1.get("generated_url")
                        if not target_url: 
                            target_url = f"https://www.aliexpress.com/wholesale?SearchText={product_name.replace(' ', '+')}"
                        
                        st.success("✅ Agent 1 nj7!")
                        st.info(f"🔗 L-lien li t-crea: {target_url}")
                        
                        # ========= L-FORSSA DYAL STOP =========
                        st.warning("⏱️ Ghadi n-dozo l Scraping mn hna 8 tawanin... Ila ban lik l-lien ghalat, wrek 3la 'Stop' l-fou9 3la limen 🛑")
                        time.sleep(8) 
                        # ======================================
                    else:
                        st.error(f"❌ Agent 1 Error: {data1.get('message')}")
                        st.stop()
                else:
                    st.error(f"❌ Agent 1 Server Error: {res1.status_code}")
                    st.stop()

            # ==========================================
            # ETAPE 2: AGENT 2 (SCRAPER)
            # ==========================================
            with st.spinner("⏳ Agent 2 (Scraper) bda l-khedma... tsena chi chwiya."):
                api_url_agent2 = "http://agent2:8000/api/v1/ai-hunt"
                res2 = requests.post(api_url_agent2, json={"category_url": target_url})
                
                if res2.status_code == 200:
                    data2 = res2.json()
                    if data2.get("status") == "error":
                        st.error(f"❌ Agent 2 Error: {data2.get('message')}")
                        st.stop()
                        
                    extracted_list = data2.get("extracted_products", [])
                    st.success(f"🎉 Agent 2 sala l-scraping! L9a {len(extracted_list)} produits.")
                    
                    # ========= PAUSE BACH Y-BRD GROQ =========
                    st.warning("⏳ Kan-tsnaw 15 seconds bach n-rtahou w ma-n-blokiwch Groq...")
                    time.sleep(15)
                    # =========================================
                else:
                    st.error(f"❌ Agent 2 Server Error: {res2.status_code}")
                    st.stop()

            # ==========================================
            # ETAPE 3: AGENT 3 (DATA ANALYZER)
            # ==========================================
            if len(extracted_list) > 0:
                with st.spinner("🧠 Agent 3 (Analyzer) kay-9ra d-data..."):
                    api_url_agent3 = "http://agent3:8002/api/v1/analyze"
                    res3 = requests.post(api_url_agent3, json={"products": extracted_list})
                    
                    if res3.status_code == 200:
                        data3 = res3.json()
                        if data3.get("status") == "success":
                            st.success("✨ Agent 3 sala l-tahlil!")
                            st.info(data3.get("summary"))
                            st.balloons()
                            
                            # ==========================================
                            # ETAPE 4: MAKE.COM
                            # ==========================================
                            with st.spinner("🚀 Kan-sifto d-data l Make.com..."):
                                make_webhook_url = "https://hook.eu2.make.com/lc2r9rxru4oh6o7eolowddxin34d9j8v" # Bdl hadi b r-rabit dyalk
                                
                                make_payload = {
                                    "product_search": product_name,
                                    "category": category,
                                    "total_products": len(extracted_list),
                                    "ai_summary": data3.get("summary"),
                                    "products": extracted_list
                                }
                                
                                make_res = requests.post(make_webhook_url, json=make_payload)
                                if make_res.status_code == 200:
                                    st.success("✅ D-data wslat l Make.com b naja7!")
                                else:
                                    st.error(f"❌ Make.com Webhook rfed t-talab: {make_res.status_code}")
                        else:
                            st.error(f"❌ Agent 3 Error: {data3.get('message')}")
                    else:
                        st.error(f"❌ Agent 3 Server Error: {res3.status_code}")
            else:
                st.warning("⚠️ Agent 2 ma-jbed 7ta produit, Agent 3 ma-3ndo may-dir.")
                
        except requests.exceptions.ConnectionError as e:
            st.error(f"🔌 Mochkil f l-ittissal: Chi serveur mn les Agents tafi.\n\n*Tafassil:* {e}")
        except Exception as e:
            st.error(f"⚠️ W9e3 mochkil 3am f Streamlit: {e}")
    else:
        st.warning("⚠️ D-dekhel s-smya w l-categorie b jouj 3afak.")