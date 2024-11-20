import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def scrape_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("user-agent=Mozilla/5.0")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)
        html_content = driver.page_source
        return html_content
    except Exception as e:
        st.error(f"Error occurred: {e}")
        return None
    finally:
        driver.quit()

def format_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')

    # Add viewport meta tag for responsiveness
    viewport_meta = soup.new_tag("meta", attrs={"name": "viewport", "content": "width=device-width, initial-scale=1.0"})
    if soup.head:
        soup.head.insert(0, viewport_meta)
    else:
        # Create a head tag if it doesn't exist
        head = soup.new_tag("head")
        head.insert(0, viewport_meta)
        soup.insert(0, head)
    
    return soup.prettify()



# Streamlit application
st.set_page_config(layout="wide")  # Set layout to wide to use full screen width

st.title("Clone Website")

url_input = st.text_input("Enter a website URL:", "")

if st.button("Get Code"):
    if url_input:
        with st.spinner("Fetching website content..."):
            html_content = scrape_with_selenium(url_input)
        
        if html_content:
            formatted_html = format_html(html_content)

            # Display download option for formatted HTML
            st.download_button(
                label="Download Code",
                data=formatted_html,
                file_name="code.html",
                mime="text/html",
            )
            
            # Display live preview spanning the full width of the screen
            st.subheader("Live Preview")
            st.components.v1.html(
                html_content,
                height=600,  # Adjust height as needed
                scrolling=True,
            )
    else:
        st.warning("Please enter a valid URL.")

