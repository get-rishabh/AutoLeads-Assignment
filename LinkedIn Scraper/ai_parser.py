"""
LinkedIn Profile Parser Module using Gemini AI
Uses LLM-based parsing for robust data extraction
"""

import os
import json
import time
from dotenv import load_dotenv
import google.generativeai as genai
from bs4 import BeautifulSoup
import re

# Load environment variables
load_dotenv()


class GeminiProfileParser:
    def __init__(self, driver):
        self.driver = driver
        
        # Get Gemini API key
        self.gemini_api_key = os.getenv('GEMINI_API_KEY')
        
        # Gemini is required for this parser
        if not self.gemini_api_key or self.gemini_api_key == 'your_gemini_key_here':
            raise ValueError(
                "GEMINI_API_KEY not found. "
                "This parser requires Gemini AI. "
                "Get FREE API key from: https://makersuite.google.com/app/apikey\n"
                "Add to .env file: GEMINI_API_KEY=your_key_here"
            )
        
        # Configure Gemini
        try:
            genai.configure(api_key=self.gemini_api_key)
            # Use gemini-1.5-pro for better extraction
            self.gemini_model = genai.GenerativeModel('gemini-2.5-pro')
            print("✅ Gemini AI configured (gemini-2.5-pro)")
        except Exception as e:
            raise ValueError(f"Failed to configure Gemini: {e}")
    
    def get_page_html(self):
        """Get the current page HTML"""
        return self.driver.page_source
    
    def html_to_clean_text(self, html_content):
        """Convert HTML to clean text using BeautifulSoup - focuses on visible profile content"""
        try:
            print("📄 Converting HTML to clean text...")
            
            # Parse HTML
            soup = BeautifulSoup(html_content, 'lxml')
            
            # Remove script and style tags FIRST (they contain JSON data we don't want)
            for element in soup(['script', 'style', 'noscript']):
                element.decompose()
            
            # Try to find the main profile content area
            # LinkedIn uses specific class names for profile sections
            main_content = None
            
            # Try to find main profile container
            profile_selectors = [
                soup.find('main'),
                soup.find('div', class_=lambda x: x and 'profile' in x.lower()),
                soup.find('section', class_=lambda x: x and 'profile' in x.lower()),
                soup.find('body')
            ]
            
            for selector in profile_selectors:
                if selector:
                    main_content = selector
                    break
            
            if not main_content:
                print("⚠️ Could not find main profile content, using body")
                main_content = soup.find('body')
            
            # Extract text from main content
            text = main_content.get_text(separator='\n', strip=True)
            
            # Clean up the text
            lines = []
            for line in text.split('\n'):
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Skip lines that are just numbers
                if line.isdigit():
                    continue
                
                # Skip very short lines (likely noise)
                if len(line) <= 2:
                    continue
                
                # Skip lines that look like JSON or code
                if line.startswith('{') or line.startswith('[') or 'urn:li:' in line:
                    continue
                
                # Skip lines with too many special characters (likely data structures)
                special_char_count = sum(1 for c in line if c in '{}[]":,')
                if special_char_count > len(line) * 0.3:  # More than 30% special chars
                    continue
                
                lines.append(line)
            
            clean_text = '\n'.join(lines)
            
            # Limit text size (Gemini has token limits)
            if len(clean_text) > 40000:
                print(f"⚠️ Text too long ({len(clean_text)} chars), truncating to 40000...")
                clean_text = clean_text[:40000]
            
            print(f"✅ Extracted clean text ({len(clean_text)} chars, {len(lines)} lines)")
            
            # Save a preview for debugging
            with open('debug_clean_preview.txt', 'w', encoding='utf-8') as f:
                f.write(clean_text[:3000])  # First 3000 chars only
            print("💾 Saved text preview to debug_clean_preview.txt")
            
            return clean_text
            
        except Exception as e:
            print(f"❌ HTML to text conversion error: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def extract_structured_data_with_gemini(self, clean_text, profile_url):
        """
        Extract structured data using Gemini AI directly from HTML text
        """
        try:
            print("🤖 Using Gemini AI for structured extraction...")
            
            # Create a more explicit prompt
            extraction_prompt = f"""You are a data extraction AI. Extract LinkedIn profile information from the text below.

IMPORTANT: You MUST return a valid JSON object with ALL these fields filled in (use the actual data from the profile):

{{
  "name": "Person's full name from the profile",
  "headline": "Professional headline (what they do)",
  "location": "City, State/Country",
  "about": "Summary/About section text",
  "current_position": "Current job title",
  "current_company": "Current company name",
  "experiences": [
    {{
      "title": "Job title",
      "company": "Company name",
      "duration": "Jan 2020 - Present"
    }}
  ],
  "educations": [
    {{
      "school": "University/School name",
      "degree": "Degree name",
      "field": "Field of study"
    }}
  ],
  "skills": ["skill1", "skill2", "skill3"]
}}

RULES:
- Extract ALL available information from the profile text
- For experiences: Include up to 5 most recent jobs
- For education: Include up to 3 schools
- For skills: Include up to 15 skills
- If a field is truly missing, use "N/A" for strings or [] for arrays
- Return ONLY the JSON object, no other text
- Do NOT use markdown code blocks
- Make sure the JSON is valid and parseable

PROFILE TEXT:
{clean_text[:20000]}

JSON OUTPUT:"""
            
            # Generate response with better generation config
            generation_config = {
                'temperature': 0.1,  # Lower temperature for more consistent output
                'top_p': 0.8,
                'top_k': 40,
                'max_output_tokens': 2048,
            }
            
            response = self.gemini_model.generate_content(
                extraction_prompt,
                generation_config=generation_config
            )
            
            # Handle complex responses properly
            try:
                # Try simple accessor first
                response_text = response.text.strip()
            except ValueError:
                # If simple accessor fails, manually extract from parts
                print("⚠️ Complex response detected, extracting from parts...")
                
                # Check if response was blocked
                if not response.candidates:
                    print("❌ No candidates in response - likely blocked by safety filters")
                    return None
                
                # Extract text from all parts
                parts_text = []
                for candidate in response.candidates:
                    if hasattr(candidate.content, 'parts'):
                        for part in candidate.content.parts:
                            if hasattr(part, 'text'):
                                parts_text.append(part.text)
                
                if not parts_text:
                    print("❌ No text found in response parts")
                    # Try to get the full response for debugging
                    with open('debug_gemini_full_response.txt', 'w', encoding='utf-8') as f:
                        f.write(str(response))
                    print("💾 Saved full response to debug_gemini_full_response.txt")
                    return None
                
                response_text = '\n'.join(parts_text).strip()
                print(f"✅ Extracted {len(parts_text)} parts from response")
            
            # Save raw response for debugging
            with open('debug_gemini_response.txt', 'w', encoding='utf-8') as f:
                f.write(response_text)
            print("💾 Saved Gemini response to debug_gemini_response.txt")
            
            # Clean up the response
            # Remove markdown code blocks
            if '```json' in response_text:
                response_text = response_text.split('```json')[1].split('```')[0].strip()
            elif '```' in response_text:
                response_text = response_text.split('```')[1].split('```')[0].strip()
            
            # Remove any text before the first {
            if '{' in response_text:
                response_text = response_text[response_text.index('{'):]
            
            # Remove any text after the last }
            if '}' in response_text:
                response_text = response_text[:response_text.rindex('}')+1]
            
            print(f"📝 Cleaned response (first 200 chars): {response_text[:200]}")
            
            # Parse JSON
            try:
                profile_data = json.loads(response_text)
            except json.JSONDecodeError as e:
                print(f"❌ JSON parse error: {e}")
                print(f"Trying to fix common JSON issues...")
                # Try to fix common issues
                response_text = response_text.replace("'", '"')  # Single quotes to double
                response_text = re.sub(r',(\s*[}\]])', r'\1', response_text)  # Trailing commas
                profile_data = json.loads(response_text)
            
            profile_data['profile_url'] = profile_url
            profile_data['success'] = True
            profile_data['error'] = None
            
            # Validate and set defaults ONLY if truly empty
            if not profile_data.get('experiences') or len(profile_data.get('experiences', [])) == 0:
                profile_data['experiences'] = [{'title': 'N/A', 'company': 'N/A', 'duration': 'N/A'}]
            
            if not profile_data.get('educations') or len(profile_data.get('educations', [])) == 0:
                profile_data['educations'] = [{'school': 'N/A', 'degree': 'N/A', 'field': 'N/A'}]
            
            if not profile_data.get('skills') or len(profile_data.get('skills', [])) == 0:
                profile_data['skills'] = ['N/A']
            
            # Print extracted data summary for debugging
            print(f"✅ Gemini extraction successful:")
            print(f"   Name: {profile_data.get('name', 'N/A')}")
            print(f"   Headline: {profile_data.get('headline', 'N/A')[:50]}...")
            print(f"   Location: {profile_data.get('location', 'N/A')}")
            print(f"   Experiences: {len(profile_data.get('experiences', []))}")
            print(f"   Educations: {len(profile_data.get('educations', []))}")
            print(f"   Skills: {len(profile_data.get('skills', []))}")
            
            return profile_data
            
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse Gemini response as JSON: {e}")
            print(f"Full response: {response_text}")
            # Save failed response for inspection
            with open('debug_gemini_failed.txt', 'w', encoding='utf-8') as f:
                f.write(f"Error: {e}\n\nResponse:\n{response_text}")
            return None
        except Exception as e:
            print(f"❌ Gemini extraction error: {e}")
            import traceback
            traceback.print_exc()
            
            # Save error details
            with open('debug_gemini_error.txt', 'w', encoding='utf-8') as f:
                f.write(f"Error: {e}\n\n")
                f.write("Traceback:\n")
                f.write(traceback.format_exc())
                f.write("\n\nClean text preview (first 1000 chars):\n")
                f.write(clean_text[:1000] if clean_text else "No clean text")
            print("💾 Saved error details to debug_gemini_error.txt")
            
            return None
    
    def extract_structured_data(self, clean_text, profile_url):
        """
        Extract structured data using Gemini AI
        """
        try:
            result = self.extract_structured_data_with_gemini(clean_text, profile_url)
            if result:
                return result
            print("⚠️ Gemini extraction failed")
            return {
                'profile_url': profile_url,
                'error': 'Gemini extraction failed',
                'success': False
            }
        except Exception as e:
            print(f"❌ Extraction error: {e}")
            return {
                'profile_url': profile_url,
                'error': str(e),
                'success': False
            }
    
    def parse_profile(self, profile_url):
        """
        Main parsing method using Gemini AI
        
        Returns:
            Dictionary containing all extracted profile data
        """
        try:
            print(f"\n{'='*60}")
            print("🚀 Using Gemini AI for LLM-based extraction")
            print(f"{'='*60}")
            
            # Wait for page to load
            time.sleep(2)
            
            # Get HTML content
            print("📄 Extracting page HTML...")
            html_content = self.get_page_html()
            
            # Convert to clean text
            clean_text = self.html_to_clean_text(html_content)
            
            if not clean_text or len(clean_text) < 100:
                return {
                    'profile_url': profile_url,
                    'error': 'Failed to extract text from HTML',
                    'success': False
                }
            
            # Save clean text for debugging
            with open('debug_clean_text.txt', 'w', encoding='utf-8') as f:
                f.write(clean_text)
            print("💾 Saved clean text to debug_clean_text.txt")
            
            # Extract structured data using Gemini
            profile_data = self.extract_structured_data(clean_text, profile_url)
            
            if not profile_data or not profile_data.get('success'):
                return {
                    'profile_url': profile_url,
                    'error': profile_data.get('error', 'Failed to extract structured data'),
                    'success': False
                }
            
            print(f"✅ Successfully parsed profile: {profile_data.get('name', 'Unknown')}")
            return profile_data
            
        except Exception as e:
            print(f"❌ Error parsing profile: {e}")
            import traceback
            traceback.print_exc()
            return {
                'profile_url': profile_url,
                'error': str(e),
                'success': False
            }

