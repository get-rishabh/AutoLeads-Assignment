"""
LinkedIn Profile Scraper Module
Uses Selenium with undetected-chromedriver to avoid bot detection
"""

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import random
import sys


class LinkedInScraper:
    def __init__(self):
        self.driver = None
        self.is_logged_in = False
        
    def init_driver(self):
        """Initialize undetected Chrome driver"""
        options = uc.ChromeOptions()
        # Keep browser open and visible for manual login
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--start-maximized')
        
        # Additional stealth options
        options.add_argument('--disable-blink-features=AutomationControlled')
        
        self.driver = uc.Chrome(options=options)
        return self.driver
    
    def open_linkedin_for_login(self):
        """Open LinkedIn login page for manual authentication"""
        if not self.driver:
            self.init_driver()
        
        self.driver.get('https://www.linkedin.com/login')
        return True
    
    def check_login_status(self):
        """Check if user is logged into LinkedIn"""
        try:
            # Check if we're on feed page or can access feed
            current_url = self.driver.current_url
            if 'feed' in current_url or 'mynetwork' in current_url or 'in/' in current_url:
                self.is_logged_in = True
                return True
            
            # Try to navigate to feed to verify login
            self.driver.get('https://www.linkedin.com/feed/')
            time.sleep(2)
            
            current_url = self.driver.current_url
            if 'feed' in current_url:
                self.is_logged_in = True
                return True
            
            return False
        except Exception as e:
            print(f"Error checking login status: {e}")
            return False
    
    def human_like_delay(self, min_seconds=2, max_seconds=5):
        """Add random delay to mimic human behavior"""
        time.sleep(random.uniform(min_seconds, max_seconds))
    
    def smooth_scroll(self):
        """Scroll page smoothly to load dynamic content"""
        try:
            # Initial wait for page load
            time.sleep(2)
            
            # Scroll down in multiple passes to trigger lazy loading
            for scroll_pass in range(3):  # Multiple passes to ensure all content loads
                # Get current page height
                last_height = self.driver.execute_script("return document.body.scrollHeight")
                
                # Scroll in increments
                scroll_pause_time = random.uniform(0.8, 1.5)
                scroll_increment = 400
                
                current_position = 0
                while current_position < last_height:
                    current_position += scroll_increment
                    self.driver.execute_script(f"window.scrollTo({{top: {current_position}, behavior: 'smooth'}});")
                    time.sleep(scroll_pause_time)
                    
                    # Check if new content loaded
                    new_height = self.driver.execute_script("return document.body.scrollHeight")
                    if new_height > last_height:
                        last_height = new_height
                
                # Pause at bottom
                time.sleep(1)
            
            # Scroll back to top smoothly
            self.driver.execute_script("window.scrollTo({top: 0, behavior: 'smooth'});")
            time.sleep(1)
            
        except Exception as e:
            print(f"Error during scrolling: {e}")
    
    def navigate_to_profile(self, profile_url):
        """Navigate to a LinkedIn profile URL"""
        try:
            print(f"Navigating to: {profile_url}")
            self.driver.get(profile_url)
            
            # Wait for initial page load
            self.human_like_delay(4, 6)
            
            # Check for CAPTCHA or login redirect
            current_url = self.driver.current_url
            if 'checkpoint' in current_url or 'authwall' in current_url:
                return False, "CAPTCHA or authentication required"
            
            if 'login' in current_url:
                return False, "Redirected to login - session may have expired"
            
            # Wait for profile content to load
            try:
                # Wait for the main profile section to be present
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "h1"))
                )
            except:
                print("Warning: Profile may not have loaded completely")
            
            # Scroll to load all dynamic content
            print("Scrolling to load all content...")
            self.smooth_scroll()
            
            print("Profile page loaded successfully")
            return True, "Success"
            
        except Exception as e:
            print(f"Error navigating to profile: {e}")
            return False, str(e)
    
    def extract_profile_data(self, profile_url):
        """
        Extract profile data from current page using Gemini AI
        Returns dictionary with profile information
        
        Args:
            profile_url: LinkedIn profile URL
        """
        # Navigate to profile
        print(f"\n{'='*60}")
        print(f"Starting extraction for: {profile_url}")
        print(f"{'='*60}")
        
        success, message = self.navigate_to_profile(profile_url)
        if not success:
            print(f"❌ Failed to navigate: {message}")
            return {
                'profile_url': profile_url,
                'error': message,
                'success': False
            }
        
        # Parse the profile using Gemini AI
        print("Starting profile data extraction...")
        
        try:
            from ai_parser import GeminiProfileParser
            parser = GeminiProfileParser(self.driver)
        except ImportError as e:
            print(f"❌ Failed to import AI parser: {e}")
            print("   Make sure ai_parser.py exists and Gemini API key is configured.")
            return {
                'profile_url': profile_url,
                'error': f'AI parser import failed: {e}',
                'success': False
            }
        
        profile_data = parser.parse_profile(profile_url)
        
        if profile_data.get('success'):
            print(f"✅ Successfully extracted data for: {profile_data.get('name', 'Unknown')}")
        else:
            print(f"❌ Failed to extract data: {profile_data.get('error', 'Unknown error')}")
        
        return profile_data
    
    def scrape_multiple_profiles(self, profile_urls, progress_callback=None):
        """
        Scrape multiple LinkedIn profiles using Gemini AI
        
        Args:
            profile_urls: List of LinkedIn profile URLs
            progress_callback: Optional callback function for progress updates
        
        Returns:
            List of dictionaries containing profile data
        """
        results = []
        total = len(profile_urls)
        
        for idx, url in enumerate(profile_urls, 1):
            if progress_callback:
                progress_callback(idx, total, url)
            
            profile_data = self.extract_profile_data(url)
            results.append(profile_data)
            
            # Add delay between profiles to avoid detection
            if idx < total:
                self.human_like_delay(6, 10)  # Longer delay for AI processing
        
        return results
    
    def close(self):
        """Close the browser"""
        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None
            self.is_logged_in = False

