# from swiftshadow import QuickProxy
# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api.proxies import GenericProxyConfig

# # 1. Get Proxy from SwiftShadow
# proxy_url = QuickProxy(countries=["US"], protocol="http").as_string()
# # proxy_url is "http://52.188.28.218:3128"
# print(f"Obtained Proxy: {proxy_url}")

# # If the proxy is http, ensure the https_url is also set for consistency
# # by replacing the scheme if necessary, or just reusing the string.
# # Since the GenericProxyConfig requires a separate entry, we'll strip the scheme for the config.

# # 2. Create the GenericProxyConfig object
# proxy_config = GenericProxyConfig(
#     http_url=proxy_url,
#     # https_url=proxy_url.replace("http://", "https://"), # Best practice: adjust scheme for HTTPS
# )

# # 3. Create the API instance with the proxy configuration
# ytt_api = YouTubeTranscriptApi(
#     proxy_config=proxy_config
# )

# VIDEO_ID = 'bmtI7Bv8Ap4'

# # 4. Call the instance method fetch()
# try:
#     transcript_list = ytt_api.fetch(VIDEO_ID) # Call fetch() on the instance (ytt_api)
#     print("\n✅ Transcript downloaded successfully using Instance method (GenericProxyConfig).")
#     # ... rest of your processing
# except Exception as e:
#     print(f"\n❌ Error: {e}")









# from swiftshadow.classes import ProxyInterface
# from youtube_transcript_api import YouTubeTranscriptApi
# from youtube_transcript_api.proxies import GenericProxyConfig
# from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled

# VIDEO_ID = 'bmtI7Bv8Ap4'
# PREFERRED_LANGUAGES = ['en', 'a.en']
# MAX_ATTEMPTS = 5

# # Initialize the SwiftShadow Proxy Manager
# # We'll manually rotate by calling .rotate()
# # Note: Ensure countries and protocol match your proxy requirements
# swift_proxy_manager = ProxyInterface(countries=["US"], protocol="http", autoRotate=False)

# for attempt in range(1, MAX_ATTEMPTS + 1):
#     print(f"\n--- Attempt {attempt} ---")

#     # 1. Rotate the proxy for a fresh IP
#     if attempt > 1:
#         swift_proxy_manager.rotate()
    
#     # Get the current proxy string from the manager
#     try:
#         current_proxy_object = swift_proxy_manager.get()
#         proxy_string = current_proxy_object.as_string()
#         print(f"Obtained Proxy: {proxy_string}")
        
#     except Exception as e:
#         print(f"❌ Failed to get proxy from swiftshadow: {e}")
#         continue
    
#     # 2. Configure the GenericProxyConfig
#     # We only set the http_url to prevent the SSL/ProxyError, 
#     # as the unauthenticated proxy from swiftshadow often doesn't handle HTTPS tunneling.
#     try:
#         proxy_config = GenericProxyConfig(
#             http_url=proxy_string,
#             # Do NOT set https_url unless you have a working HTTPS-compatible proxy URL
#         )
        
#         # 3. Create a new YouTubeTranscriptApi instance with the proxy config
#         ytt_api = YouTubeTranscriptApi(
#             proxy_config=proxy_config,
#             # languages=PREFERRED_LANGUAGES
#         )
        
#         # 4. Attempt to download the transcript using the fetch() method
#         transcript_list = ytt_api.fetch(VIDEO_ID)
        
#         # 5. Success handling
#         full_transcript = " ".join([item['text'] for item in transcript_list])
#         print("-" * 50)
#         print(f"✅ Transcript Downloaded Successfully on attempt {attempt}!")
#         print(f"Transcript Snippet (First 500 characters):\n{full_transcript[:500]}...")
#         print("-" * 50)
#         break # Exit the loop on success

#     except (NoTranscriptFound, TranscriptsDisabled) as e:
#         # NoTranscriptFound here usually means YouTube successfully received the request 
#         # but is still blocking the proxy IP or no transcript is available.
#         print(f"❌ Failed: IP is likely blocked or no transcript available. Rotating proxy...")
#     except Exception as e:
#         print(f"❌ An unexpected error occurred: {e}")
        
# if attempt == MAX_ATTEMPTS and 'full_transcript' not in locals():
#     print("\n\nFailed to download transcript after all attempts. You must use a more robust, high-rotation residential proxy solution.")




from swiftshadow.classes import ProxyInterface
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.proxies import GenericProxyConfig
from youtube_transcript_api._errors import NoTranscriptFound, TranscriptsDisabled
import requests # Import requests to catch connection-related errors

VIDEO_ID = 'bmtI7Bv8Ap4'
PREFERRED_LANGUAGES = ['en', 'a.en']
MAX_ATTEMPTS = 10 # Increase attempts to account for bad proxies

# Initialize the SwiftShadow Proxy Manager
swift_proxy_manager = ProxyInterface(countries=["US"], protocol="http", autoRotate=False)

for attempt in range(1, MAX_ATTEMPTS + 1):
    print(f"\n--- Attempt {attempt} ---")

    # 1. Rotate the proxy for a fresh IP
    if attempt > 1:
        swift_proxy_manager.rotate()
    
    # Get the current proxy string
    try:
        proxy_string = swift_proxy_manager.get().as_string()
        print(f"Obtained Proxy: {proxy_string}")
        
    except Exception as e:
        print(f"❌ Failed to get proxy from swiftshadow: {e}")
        continue # Skip to the next attempt if we can't get a proxy
    
    # 2. Configure the GenericProxyConfig
    try:
        # Only set http_url to prevent SSL/ProxyError with unauthenticated proxies
        proxy_config = GenericProxyConfig(
            http_url=proxy_string,
        )
        
        # 3. Create a new YouTubeTranscriptApi instance with the proxy config
        ytt_api = YouTubeTranscriptApi(
            proxy_config=proxy_config,
            # languages=PREFERRED_LANGUAGES
        )
        
        # 4. Attempt to download the transcript using the fetch() method
        transcript_list = ytt_api.fetch(VIDEO_ID)
        
        # 5. Success handling
        full_transcript = " ".join([item['text'] for item in transcript_list])
        print("-" * 50)
        print(f"✅ Transcript Downloaded Successfully on attempt {attempt}!")
        print(f"Transcript Snippet (First 500 characters):\n{full_transcript[:500]}...")
        print("-" * 50)
        break # Exit the loop on success

    # --- ENHANCED ERROR HANDLING ---
    except (requests.exceptions.ProxyError, requests.exceptions.ConnectionError, requests.exceptions.Timeout) as e:
        # This catches the ConnectTimeoutError and other connection failures.
        print(f"❌ Connection/Proxy Error: The proxy {proxy_string} is unreachable or timed out. Rotating...")
        # continue (Implicitly continues to the next loop iteration)
        
    except (NoTranscriptFound, TranscriptsDisabled) as e:
        # This catches the YouTube IP block error.
        print(f"❌ YouTube Blocked Error: IP is blocked or no transcript available. Rotating...")
        # continue (Implicitly continues to the next loop iteration)

    except Exception as e:
        print(f"❌ An unexpected error occurred: {type(e).__name__} - {e}")
        # continue (Implicitly continues to the next loop iteration)
        
if attempt == MAX_ATTEMPTS and 'full_transcript' not in locals():
    print("\n\nFailed to download transcript after all attempts.")
    print("Recommendation: Swiftshadow's quick proxies are unreliable for consistent scraping. Consider a dedicated, high-rotation residential proxy service.")