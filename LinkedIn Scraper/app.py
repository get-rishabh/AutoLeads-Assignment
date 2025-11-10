"""
LinkedIn Profile Scraper - Streamlit App
Main application interface
"""

import streamlit as st
import pandas as pd
from scraper import LinkedInScraper
import os
from datetime import datetime
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Page configuration
st.set_page_config(
    page_title="LinkedIn Profile Scraper",
    page_icon="🔍",
    layout="wide"
)

# Initialize session state
if 'scraper' not in st.session_state:
    st.session_state.scraper = None

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

if 'scraped_data' not in st.session_state:
    st.session_state.scraped_data = None

if 'browser_opened' not in st.session_state:
    st.session_state.browser_opened = False

# Removed use_llama state - now only uses Gemini AI


def format_profile_data_for_csv(results):
    """Format scraped profile data for CSV export"""
    formatted_data = []
    
    for result in results:
        if result.get('success', False):
            # Flatten experience data
            exp_list = result.get('experiences', [])
            experience_str = ""
            if exp_list:
                experience_str = " | ".join([
                    f"{exp.get('title', 'N/A')} at {exp.get('company', 'N/A')} ({exp.get('duration', 'N/A')})"
                    for exp in exp_list
                ])
            
            # Flatten education data
            edu_list = result.get('educations', [])
            education_str = ""
            if edu_list:
                education_str = " | ".join([
                    f"{edu.get('school', 'N/A')} - {edu.get('degree', 'N/A')} - {edu.get('field', 'N/A')}"
                    for edu in edu_list
                ])
            
            # Flatten skills
            skills_list = result.get('skills', [])
            skills_str = ", ".join(skills_list) if skills_list else "N/A"
            
            formatted_data.append({
                'Name': result.get('name', 'N/A'),
                'Headline': result.get('headline', 'N/A'),
                'Location': result.get('location', 'N/A'),
                'About': result.get('about', 'N/A'),
                'Current Position': result.get('current_position', 'N/A'),
                'Current Company': result.get('current_company', 'N/A'),
                'Experience': experience_str,
                'Education': education_str,
                'Skills': skills_str,
                'Profile URL': result.get('profile_url', 'N/A')
            })
        else:
            # Add error entry
            formatted_data.append({
                'Name': 'ERROR',
                'Headline': 'N/A',
                'Location': 'N/A',
                'About': result.get('error', 'Unknown error'),
                'Current Position': 'N/A',
                'Current Company': 'N/A',
                'Experience': 'N/A',
                'Education': 'N/A',
                'Skills': 'N/A',
                'Profile URL': result.get('profile_url', 'N/A')
            })
    
    return formatted_data


# Main UI
st.title("🔍 LinkedIn Profile Scraper")

# Check for API keys
gemini_api_key = os.getenv('GEMINI_API_KEY')

if not gemini_api_key or gemini_api_key == 'your_gemini_key_here':
    st.error("""
    🔑 **Gemini API Key Required!**
    
    This scraper uses Google's Gemini AI for LLM-based parsing.
    
    **Setup:**
    1. Get FREE API key from: https://makersuite.google.com/app/apikey
    2. Create a `.env` file in the project root
    3. Add: `GEMINI_API_KEY=your_actual_key_here`
    4. Restart the app
    
    **Why Gemini?**
    - ✅ FREE (generous free tier)
    - ✅ Better extraction (90%+ accuracy)
    - ✅ No LlamaParse dependency issues
    
    **Alternative:** Set environment variable `GEMINI_API_KEY`
    """)
    st.stop()
else:
    st.success("✅ Gemini AI configured (Google's LLM)")

# Warning banner
st.warning("""
⚠️ **Important Warnings:**
- Use only with throwaway/test accounts
- Recommended for educational purposes only
- LinkedIn actively detects and blocks scrapers
""")

# Create output directory if it doesn't exist
if not os.path.exists('output'):
    os.makedirs('output')

# Sidebar for instructions
with st.sidebar:
    st.header("📖 Instructions")
    st.markdown("""
    ### How to Use:
    
    1. **Login to LinkedIn**
       - Click "Open Browser & Login"
       - Manually log into your LinkedIn account
       - Complete any security checks
       - Click "Confirm Login" when done
    
    2. **Enter Profile URLs**
       - Paste LinkedIn profile URLs
       - One URL per line
       - Example: `https://www.linkedin.com/in/username/`
    
    3. **Start Scraping**
       - Click "Start Scraping"
       - Wait for completion (LLM processing takes longer)
       - Download CSV results
    
    ### 🤖 Using Gemini AI:
    - **AI-based parsing** - Highly robust
    - Understands content semantically
    - Not affected by HTML changes
    - ~10-15 seconds per profile
    
    ### Tips:
    - Scrape 5-10 profiles at a time
    - Wait between scraping sessions
    - Use test account only
    - Be patient - LLM processing takes time
    """)
    
    st.divider()
    st.caption("Built with Streamlit & Selenium")


# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    st.header("Step 1: LinkedIn Authentication")
    
    if not st.session_state.logged_in:
        if st.button("🌐 Open Browser & Login to LinkedIn", type="primary", use_container_width=True):
            with st.spinner("Opening browser for manual login..."):
                try:
                    st.session_state.scraper = LinkedInScraper()
                    st.session_state.scraper.open_linkedin_for_login()
                    st.session_state.browser_opened = True
                    st.success("✅ Browser opened! Please log in manually in the browser window.")
                    st.info("👉 After logging in, click 'Confirm Login' button below")
                except Exception as e:
                    st.error(f"Error opening browser: {e}")
        
        if st.session_state.browser_opened:
            st.divider()
            if st.button("✔️ Confirm Login (Click after you've logged in)", use_container_width=True):
                with st.spinner("Checking login status..."):
                    try:
                        if st.session_state.scraper.check_login_status():
                            st.session_state.logged_in = True
                            st.success("🎉 Successfully logged in to LinkedIn!")
                            st.rerun()
                        else:
                            st.error("❌ Could not verify login. Please make sure you're logged in and try again.")
                    except Exception as e:
                        st.error(f"Error verifying login: {e}")
    else:
        st.success("✅ Logged in to LinkedIn")
        
        if st.button("🔄 Logout & Close Browser", use_container_width=True):
            if st.session_state.scraper:
                st.session_state.scraper.close()
            st.session_state.scraper = None
            st.session_state.logged_in = False
            st.session_state.browser_opened = False
            st.session_state.scraped_data = None
            st.rerun()

with col2:
    st.metric("Status", "Logged In ✓" if st.session_state.logged_in else "Not Logged In", 
              delta="Ready" if st.session_state.logged_in else "Login Required")


# Step 2: Scraping section (only shown when logged in)
if st.session_state.logged_in:
    st.divider()
    st.header("Step 2: Scrape Profiles")
    
    # Input for profile URLs
    profile_urls_input = st.text_area(
        "Enter LinkedIn Profile URLs (one per line)",
        height=150,
        placeholder="https://www.linkedin.com/in/username1/\nhttps://www.linkedin.com/in/username2/\nhttps://www.linkedin.com/in/username3/"
    )
    
    # Parse URLs
    profile_urls = [url.strip() for url in profile_urls_input.split('\n') if url.strip()]
    
    if profile_urls:
        st.info(f"📋 {len(profile_urls)} profile(s) to scrape")
        
        # Validate URLs
        invalid_urls = [url for url in profile_urls if 'linkedin.com/in/' not in url]
        if invalid_urls:
            st.warning(f"⚠️ {len(invalid_urls)} invalid URL(s) detected. Make sure URLs contain 'linkedin.com/in/'")
    
    # Info about parsing method
    st.info("🤖 Using Gemini AI for intelligent data extraction (~10-15 seconds per profile)")
    
    col_a, col_b = st.columns([1, 1])
    
    with col_a:
        if st.button("🚀 Start Scraping", type="primary", use_container_width=True, disabled=len(profile_urls) == 0):
            if profile_urls:
                # Create progress containers
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                try:
                    results = []
                    total = len(profile_urls)
                    
                    def update_progress(current, total, url):
                        progress = current / total
                        progress_bar.progress(progress)
                        status_text.text(f"Scraping {current}/{total}: {url[:50]}...")
                    
                    # Scrape profiles using Gemini AI
                    results = st.session_state.scraper.scrape_multiple_profiles(
                        profile_urls,
                        progress_callback=update_progress
                    )
                    
                    progress_bar.progress(1.0)
                    status_text.text("✅ Scraping completed!")
                    
                    # Store results
                    st.session_state.scraped_data = results
                    
                    # Show success message
                    successful = sum(1 for r in results if r.get('success', False))
                    failed = total - successful
                    
                    st.success(f"🎉 Scraping completed! {successful} successful, {failed} failed")
                    
                except Exception as e:
                    st.error(f"Error during scraping: {e}")
                    status_text.text("❌ Scraping failed")

# Step 3: Results and Download
if st.session_state.scraped_data:
    st.divider()
    st.header("Step 3: Results & Download")
    
    # Format data for display
    formatted_data = format_profile_data_for_csv(st.session_state.scraped_data)
    df = pd.DataFrame(formatted_data)
    
    # Display preview
    st.subheader("📊 Preview of Scraped Data")
    st.dataframe(df, use_container_width=True, height=300)
    
    # Show detailed view in expander
    with st.expander("🔍 View Detailed Raw Data"):
        for idx, result in enumerate(st.session_state.scraped_data, 1):
            st.markdown(f"### Profile {idx}: {result.get('name', 'N/A')}")
            st.json(result)
    
    # Download section
    col_x, col_y, col_z = st.columns([1, 1, 1])
    
    with col_x:
        # Generate CSV
        csv = df.to_csv(index=False)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"linkedin_profiles_{timestamp}.csv"
        
        st.download_button(
            label="📥 Download CSV",
            data=csv,
            file_name=filename,
            mime="text/csv",
            use_container_width=True,
            type="primary"
        )
    
    with col_y:
        # Save to output folder
        if st.button("💾 Save to Output Folder", use_container_width=True):
            try:
                output_path = os.path.join('output', filename)
                df.to_csv(output_path, index=False)
                st.success(f"✅ Saved to: {output_path}")
            except Exception as e:
                st.error(f"Error saving file: {e}")
    
    with col_z:
        if st.button("🗑️ Clear Results", use_container_width=True):
            st.session_state.scraped_data = None
            st.rerun()
    
    # Statistics
    st.divider()
    st.subheader("📈 Statistics")
    
    stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
    
    with stat_col1:
        st.metric("Total Profiles", len(st.session_state.scraped_data))
    
    with stat_col2:
        successful = sum(1 for r in st.session_state.scraped_data if r.get('success', False))
        st.metric("Successful", successful)
    
    with stat_col3:
        failed = len(st.session_state.scraped_data) - successful
        st.metric("Failed", failed)
    
    with stat_col4:
        success_rate = (successful / len(st.session_state.scraped_data) * 100) if st.session_state.scraped_data else 0
        st.metric("Success Rate", f"{success_rate:.1f}%")


# Footer
st.divider()
st.caption("⚠️ Disclaimer: This tool is for educational purposes only. Scraping LinkedIn violates their Terms of Service. Use at your own risk.")

