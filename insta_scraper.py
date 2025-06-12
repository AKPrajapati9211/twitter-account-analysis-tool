import requests
import os
from PIL import Image
from io import BytesIO

def scrape_instagram_images(username, sessionid, max_images=10):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",

        "Cookie": f"sessionid={sessionid};"
    }

    url = f"https://www.instagram.com/api/v1/users/web_profile_info/?username={username}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch profile: {response.status_code}")
        print("Response:", response.text)
        return

    try:
        user_data = response.json()['data']['user']
        posts = user_data['edge_owner_to_timeline_media']['edges']
    except Exception as e:
        print("❌ Failed to parse Instagram JSON:", e)
        return

    save_dir = f"scraped_images/{username}"
    os.makedirs(save_dir, exist_ok=True)

    for i, post in enumerate(posts[:max_images]):
        image_url = post['node']['display_url']
        print(f"📥 Downloading image {i+1}: {image_url}")
        try:
            img_data = requests.get(image_url, headers=headers).content
            img = Image.open(BytesIO(img_data))
            img.save(f"{save_dir}/{username}_{i+1}.jpg")
        except Exception as e:
            print(f"⚠️ Could not download image {i+1}: {e}")

    print(f"✅ Done! Images saved in {save_dir}")

if __name__ == "__main__":
    import getpass

    username = input("📸 Instagram username to scrape: ")
    sessionid = getpass.getpass("🔑 Paste your Instagram sessionid: ")

    scrape_instagram_images(username, sessionid)
