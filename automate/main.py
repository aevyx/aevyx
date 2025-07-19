import requests
from bs4 import BeautifulSoup
import html

USERNAME = "xyz_aevyx"
URL = f"https://www.hackerrank.com/{USERNAME}"


def fetch_profile_data():
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept-Language": "en-US,en;q=0.9"
    }

    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    data = {
        "name": USERNAME.capitalize(),
        "username": USERNAME,
        "badges": 0,
        "certificates": 0,
        "avatar": "user_logo.svg"
    }

    meta_name = soup.find("meta", property="og:title")
    if meta_name and meta_name.get("content"):
        name_parts = meta_name["content"].split(" | ")
        if name_parts and name_parts[0].strip().lower() != USERNAME.lower():
            data["name"] = name_parts[0].strip().replace("-", " ")

    meta_avatar = soup.find("meta", property="og:image")
    if meta_avatar and meta_avatar.get("content") !='https://hrcdn.net/og/default.jpg':
        data["avatar"] = meta_avatar["content"]

    badge_divs = soup.find_all("div", class_="hacker-badge")
    data["badges"] = len(badge_divs)

    cert_links = soup.find_all("a", href=lambda href: href and "certificate" in href)
    data["certificates"] = len(cert_links)

    return data


def wrap_text(text, max_length=30):
    words = text.split()
    lines = []
    current = ""

    for word in words:
        if len(current + " " + word) <= max_length:
            current += " " + word if current else word
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def generate_svg(data):
    name_lines = wrap_text(data["name"], 22)

    name_svg = "\n".join(
        f'<tspan x="90" dy="{20 if i else 0}" class="fade-in" style="animation-delay:{i * 0.1 + 0.3}s">{html.escape(line)}</tspan>'
        for i, line in enumerate(name_lines)
    )

    name_height = 40 + len(name_lines) * 20
    stats_y = name_height + 45
    stars_y = stats_y + 20
    svg_height = stars_y + 60

    logo_url ='hackerrank_logo.svg'

    def render_star(x, filled):
        opacity = "1" if filled else "0.3"
        return f'''
        <polygon points="{x},0 {x+4},10 {x+12},10 {x+5},18 {x+7},30 {x},23 {x-7},30 {x-5},18 {x-12},10 {x-4},10"
                 fill="#6445ff" opacity="{opacity}" transform="translate(0,{stars_y}) scale(0.8, 0.7)" />'''

    stars_svg = "\n".join(render_star(50 + i * 30, i < 3) for i in range(5))


    content = f"""<svg width="460" height="{svg_height}" xmlns="http://www.w3.org/2000/svg">
  <style>
    .title {{ font: 700 20px Verdana; fill: black; }}
    .subtitle {{ font: 14px Verdana; fill: black; }}
    .stat {{ font: 16px Verdana; fill: black; }}
    .fade-in {{
      opacity: 0;
      animation: fadeIn 0.6s ease-out forwards;
    }}
    .slide-in {{
      transform: translateX(-10px);
      opacity: 0;
      animation: slideIn 0.6s ease-out forwards;
    }}
    @keyframes fadeIn {{ to {{ opacity: 1; }} }}
    @keyframes slideIn {{ to {{ transform: translateX(0); opacity: 1; }} }}
    @keyframes popIn {{ to {{ transform: scale(1); }} }}
  </style>

  <!-- Background -->
  <rect width="100%" height="100%" rx="15" fill="#ffffff" />

  <!-- Top-right HackerRank logo -->
  <image href="{logo_url}" x="415" y="10" width="30" height="30" />

  <!-- Avatar -->
  <image href="{html.escape(data['avatar'])}" x="20" y="20" width="60" height="60"
         clip-path="circle(30px at 30px 30px)" />

  <!-- Name -->
  <text x="90" y="40" class="title">{name_svg}</text>

  <!-- Username -->
  <text x="90" y="{name_height}" class="subtitle fade-in" style="animation-delay: 0.5s">@{html.escape(data['username'])}</text>

  <!-- Stats -->
  <text x="20" y="{stats_y}" class="stat slide-in" style="animation-delay: 0.6s">🏅 Badges: {html.escape(str(data['badges']))}</text>
  <text x="200" y="{stats_y}" class="stat slide-in" style="animation-delay: 0.7s">📜 Certificates: {html.escape(str(data['certificates']))}</text>

  <!-- Star Rating -->
  {stars_svg}

  <text x="90" y="40" class="title"></text>

</svg>"""

    with open("automate/card.svg", "w", encoding="utf-8") as f:
        f.write(content)


if __name__ == "__main__":
    profile_data = fetch_profile_data()
    generate_svg(profile_data)
