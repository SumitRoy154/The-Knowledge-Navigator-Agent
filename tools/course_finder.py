import os
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv
from urllib.parse import urlparse, unquote
import re
import time
import html as html_lib

# Load environment variables
load_dotenv()

# Google Custom Search API configuration
GOOGLE_API_KEY = os.getenv("GOOGLE_SEARCH_API_KEY")
SEARCH_ENGINE_ID = os.getenv("GOOGLE_SEARCH_ENGINE_ID")

# If keys are missing, fall back to DuckDuckGo HTML scraping
USE_GOOGLE_CSE = bool(GOOGLE_API_KEY and SEARCH_ENGINE_ID)

class CourseFinder:
    """Real-time course search tool with web search fallback (Google CSE -> DuckDuckGo)"""

    def __init__(self):
        # Removed static entries; keep an empty local DB for future caching/extensions
        self.courses_db: Dict[str, List[Dict[str, Any]]] = self._initialize_course_database()

    def _initialize_course_database(self) -> Dict[str, List[Dict[str, Any]]]:
        """
        Local DB intentionally empty to force live searches.
        Keeps structure to support future caching or curated overrides.
        """
        return {}

    def _call_google_cse(self, query: str, num: int = 5) -> List[Dict[str, Any]]:
        """Call Google Custom Search API and return raw items (if configured)"""
        if not USE_GOOGLE_CSE:
            return []
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": GOOGLE_API_KEY,
            "cx": SEARCH_ENGINE_ID,
            "q": query,
            "num": min(max(1, int(num)), 10)
        }
        try:
            resp = requests.get(url, params=params, timeout=8)
            resp.raise_for_status()
            data = resp.json()
            return data.get("items", []) or []
        except Exception:
            return []

    def _call_duckduckgo(self, query: str, num: int = 5) -> List[Dict[str, Any]]:
        """
        Lightweight DuckDuckGo HTML search fallback (no API key required).
        Returns list of dicts with title, snippet, link similar to CSE items.
        """
        url = "https://html.duckduckgo.com/html/"
        params = {"q": query}
        headers = {"User-Agent": "knowledge-navigator-agent/1.0"}
        try:
            resp = requests.post(url, data=params, headers=headers, timeout=8)
            resp.raise_for_status()
            html = resp.text
        except Exception:
            return []

        # Find result blocks — best-effort parsing
        results = []
        # pattern finds <a ... class="result__a" href="...">title</a>
        a_matches = re.findall(r'(<a[^>]+class="[^"]*result__a[^"]*"[^>]*>.*?</a>)', html, flags=re.S)
        snippets = re.findall(r'<a[^>]+class="[^"]*result__snippet[^"]*"[^>]*>(.*?)</a>', html, flags=re.S)
        # If snippet pattern not present, attempt to collect brief text around link
        for i, a_html in enumerate(a_matches[:num]):
            # extract href
            href_m = re.search(r'href="([^"]+)"', a_html)
            title = re.sub(r'<.*?>', '', a_html).strip()
            title = html_lib.unescape(title)
            link = href_m.group(1) if href_m else ""
            snippet = html_lib.unescape(snippets[i].strip()) if i < len(snippets) else ""
            # Clean up link (DuckDuckGo returns /l/?kh=-1&uddg=encoded_url)
            # attempt to extract uddg param
            try:
                if "/l/?" in link and "uddg=" in link:
                    m = re.search(r"uddg=([^&]+)", link)
                    if m:
                        link = unquote(m.group(1))
            except Exception:
                pass
            results.append({"title": title, "snippet": snippet, "link": link})
        return results

    def _infer_platform_from_url(self, url: str) -> str:
        try:
            host = urlparse(url).netloc.lower()
            if "coursera.org" in host:
                return "Coursera"
            if "udemy.com" in host:
                return "Udemy"
            if "edx.org" in host:
                return "edX"
            if "linkedin.com" in host:
                return "LinkedIn Learning"
            if "freecodecamp.org" in host or "freecodecamp" in host:
                return "freeCodeCamp"
            if "codecademy.com" in host:
                return "Codecademy"
            if "pluralsight.com" in host:
                return "Pluralsight"
            if "khanacademy.org" in host:
                return "Khan Academy"
            return host.replace("www.", "")
        except Exception:
            return "Unknown"

    def _parse_snippet_for_price_rating_duration(self, snippet: str) -> Dict[str, Any]:
        out = {"price": "Varies", "rating": None, "duration_weeks": None}
        s = (snippet or "").lower()
        if "free" in s or "audit" in s:
            out["price"] = "Free"
        else:
            m = re.search(r"\$\s?\d{1,4}(?:\.\d{1,2})?", snippet)
            if m:
                out["price"] = m.group(0)
        m = re.search(r"(\d(?:\.\d)?)\s*(?:/5|stars|star|rating)", snippet)
        if m:
            try:
                out["rating"] = float(m.group(1))
            except Exception:
                out["rating"] = None
        m = re.search(r"(\d{1,2}\s*-\s*\d{1,2}\s*weeks)|(\d{1,2}\s*weeks)", snippet)
        if m:
            out["duration_weeks"] = m.group(0).replace(" ", "")
        return out

    def _determine_phase(self, text: str, level: str) -> str:
        s = (text or "").lower()
        if any(k in s for k in ["intro", "introduction", "beginner", "basics", "fundamentals"]):
            return "Phase I"
        if any(k in s for k in ["intermediate", "practical", "project", "application", "hands-on"]):
            return "Phase II"
        if any(k in s for k in ["advanced", "analysis", "deep", "advanced topics", "financial ratios"]):
            return "Phase III"
        if level and level.lower().startswith("begin"):
            return "Phase I"
        if level and level.lower().startswith("inter"):
            return "Phase II"
        return "Phase III"

    def _build_course_from_search_item(self, item: Dict[str, Any], level: str) -> Dict[str, Any]:
        # Support both CSE item shape and DuckDuckGo fallback item shape
        title = item.get("title") or item.get("htmlTitle") or item.get("titleNoFormatting") or ""
        snippet = item.get("snippet") or item.get("htmlSnippet") or item.get("snippet_text") or ""
        link = item.get("link") or item.get("formattedUrl") or item.get("link_text") or item.get("url") or ""
        platform = self._infer_platform_from_url(link)
        extra = self._parse_snippet_for_price_rating_duration(snippet)
        phase = self._determine_phase(snippet + " " + title, level)
        course = {
            "name": re.sub(r"\s+", " ", title).strip(),
            "platform": platform,
            "focus": re.sub(r"\s+", " ", snippet).strip(),
            "price": extra.get("price", "Varies"),
            "rating": extra.get("rating") or 0.0,
            "duration_weeks": extra.get("duration_weeks") or "Varies",
            "phase": phase,
            "level": (level or "Beginner").title(),
            "key_topics": snippet.strip(),
            "url": link
        }
        return course

    def search_online_courses(self, topic: str, level: str = "Beginner", max_results: int = 10) -> List[Dict[str, Any]]:
        """
        Live search for courses: prefer Google CSE when available, otherwise DuckDuckGo HTML fallback.
        Returns normalized list of course dicts (name, platform, focus, price, rating, duration_weeks, phase, level, key_topics, url).
        """
        topic_key = (topic or "").strip()
        if not topic_key:
            return []

        results: List[Dict[str, Any]] = []

        # 1) Try Google CSE if configured
        if USE_GOOGLE_CSE:
            query = f"{topic_key} {level} course site:coursera.org OR site:udemy.com OR site:edx.org OR site:linkedin.com OR site:freecodecamp.org OR site:codecademy.com OR site:pluralsight.com"
            items = self._call_google_cse(query, num=min(max_results, 10))
            for it in items:
                try:
                    results.append(self._build_course_from_search_item(it, level))
                except Exception:
                    continue
            time.sleep(0.1)

        # 2) If not enough results, use broader CSE query
        if len(results) < max_results and USE_GOOGLE_CSE:
            items = self._call_google_cse(f"{topic_key} {level} course", num=min(max_results * 2, 10))
            for it in items:
                try:
                    course = self._build_course_from_search_item(it, level)
                    if not any(course.get("url") == r.get("url") for r in results):
                        results.append(course)
                except Exception:
                    continue
            time.sleep(0.1)

        # 3) DuckDuckGo HTML fallback (no API key required)
        if len(results) < max_results:
            ddg_items = self._call_duckduckgo(f"{topic_key} {level} course", num=min(max_results * 2, 20))
            for it in ddg_items:
                try:
                    course = self._build_course_from_search_item({"title": it.get("title"), "snippet": it.get("snippet"), "link": it.get("link")}, level)
                    if not any(course.get("url") == r.get("url") for r in results):
                        results.append(course)
                except Exception:
                    continue
            time.sleep(0.1)

        # 4) Final fallback: local DB (empty by default)
        if not results and self.courses_db:
            for db_topic, courses in self.courses_db.items():
                if topic_key.lower() in db_topic.lower() or db_topic.lower() in topic_key.lower():
                    results.extend(courses)

        # Normalize ratings and ensure fields
        for r in results:
            if r.get("rating") is None:
                r["rating"] = 0.0
            else:
                try:
                    r["rating"] = float(r["rating"])
                except Exception:
                    r["rating"] = 0.0
            r.setdefault("price", "Varies")
            r.setdefault("duration_weeks", "Varies")
            r.setdefault("phase", self._determine_phase(r.get("focus", "") + " " + r.get("name", ""), level))
            r.setdefault("level", (level or "Beginner").title())

        # Sort by rating desc, then Phase I preference for Beginner
        results = sorted(results, key=lambda x: (x.get("rating", 0.0), 1 if x.get("phase") == "Phase I" else 0), reverse=True)

        # Deduplicate by url or name+platform
        seen = set()
        deduped = []
        for c in results:
            key = (c.get("url") or "").strip() or ((c.get("name", "") + "|" + c.get("platform", "")).lower())
            if key in seen:
                continue
            seen.add(key)
            deduped.append(c)
            if len(deduped) >= int(max_results):
                break

        return deduped

    def get_phase_one_courses(self, courses: List[Dict]) -> List[Dict]:
        """Filter and return only Phase I courses"""
        return [c for c in courses if c.get("phase") == "Phase I"]

    def get_all_topics(self) -> List[str]:
        """Get list of all available topics from local DB (web search is dynamic)"""
        return list(self.courses_db.keys())

# Create singleton instance
course_finder = CourseFinder()

def search_online_courses(topic: str, level: str = "Beginner", max_results: int = 10) -> List[Dict[str, Any]]:
    """Wrapper function for course search"""
    return course_finder.search_online_courses(topic, level, max_results)
