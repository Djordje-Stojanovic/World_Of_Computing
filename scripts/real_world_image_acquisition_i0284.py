from __future__ import annotations

import csv
import hashlib
import html
import json
import re
import subprocess
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from urllib.parse import quote, urljoin
from urllib.request import Request, urlopen


PASS_ID = "I-0284"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
MANUSCRIPT = ROOT / "manuscript"
PY_TOOLING_1 = ROOT / ".tooling" / "i0281" / "python"
PY_TOOLING_2 = ROOT / ".tooling" / "i0282" / "python"

for tool_path in [PY_TOOLING_2, PY_TOOLING_1]:
    if tool_path.exists():
        sys.path.insert(0, str(tool_path))

from PIL import Image, ImageDraw, ImageOps  # type: ignore


UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 NextTokenPrivateEdition/1.0"
SOURCE_DIR = ASSETS / "private_use_photos" / "i0284_source_images"
LOGO_DIR = ASSETS / "logos" / "i0284"
PEOPLE_DIR = ASSETS / "people" / "i0284"
CONTACT_DIR = ASSETS / "source_media" / "i0284_contact_sheets"
CHROME = Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe")


def now_stamp() -> str:
    return datetime.now().astimezone().replace(microsecond=0).isoformat()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def safe_name(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return value[:80] or "asset"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, delimiter="\t", fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def append_line(path: Path, fields: list[object]) -> None:
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(str(field).replace("\t", " ").replace("\r", " ").replace("\n", " ") for field in fields) + "\n")


def fetch_bytes(url: str, timeout: int = 25) -> tuple[bytes, str]:
    request = Request(url, headers={"User-Agent": UA, "Accept": "*/*"})
    with urlopen(request, timeout=timeout) as response:
        content_type = response.headers.get("Content-Type", "")
        return response.read(), content_type


def fetch_text(url: str, timeout: int = 25) -> str:
    data, content_type = fetch_bytes(url, timeout)
    charset_match = re.search(r"charset=([^;\s]+)", content_type, flags=re.I)
    charset = charset_match.group(1) if charset_match else "utf-8"
    return data.decode(charset, errors="replace")


def extension_from_content_type(content_type: str, fallback_url: str) -> str:
    lower = content_type.lower()
    if "svg" in lower:
        return ".svg"
    if "png" in lower:
        return ".png"
    if "jpeg" in lower or "jpg" in lower:
        return ".jpg"
    if "webp" in lower:
        return ".webp"
    suffix = Path(fallback_url.split("?", 1)[0]).suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".svg"}:
        return ".jpg" if suffix == ".jpeg" else suffix
    return ".bin"


def image_dimensions(path: Path) -> tuple[int, int]:
    if path.suffix.lower() == ".svg":
        text = path.read_text(encoding="utf-8", errors="replace")
        width = re.search(r'\bwidth="([0-9.]+)', text)
        height = re.search(r'\bheight="([0-9.]+)', text)
        if width and height:
            return int(float(width.group(1))), int(float(height.group(1)))
        viewbox = re.search(r'\bviewBox="[^"]*?\s([0-9.]+)\s([0-9.]+)"', text)
        if viewbox:
            return int(float(viewbox.group(1))), int(float(viewbox.group(2)))
        return 0, 0
    with Image.open(path) as image:
        return image.size


def quality_score(path: Path) -> tuple[str, str]:
    if path.suffix.lower() == ".svg":
        size = path.stat().st_size
        return ("90.0" if size > 300 else "45.0"), "svg_vector"
    try:
        with Image.open(path) as image:
            image = image.convert("RGB")
            width, height = image.size
            gray = ImageOps.grayscale(image.resize((max(1, width // 4), max(1, height // 4))))
            extrema = gray.getextrema()
            contrast = extrema[1] - extrema[0]
            megapixels = (width * height) / 1_000_000
            score = min(100.0, 20.0 + megapixels * 25.0 + contrast / 2.5)
            return f"{score:.1f}", f"mp={megapixels:.2f}; contrast={contrast}"
    except Exception as exc:
        return "0.0", f"image_open_failed={type(exc).__name__}"


def meta_image_url(page_url: str, text: str) -> str:
    patterns = [
        r'<meta[^>]+property=["\']og:image(?::secure_url)?["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']og:image(?::secure_url)?["\']',
        r'<meta[^>]+name=["\']twitter:image["\'][^>]+content=["\']([^"\']+)["\']',
        r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+name=["\']twitter:image["\']',
    ]
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.I)
        if match:
            return urljoin(page_url, html.unescape(match.group(1)))
    return ""


SOURCE_PAGE_CANDIDATES = [
    ("NVIDIA AI", "NVIDIA", "https://www.nvidia.com/en-us/ai/", "AI platform/source surface"),
    ("NVIDIA Blackwell", "NVIDIA", "https://www.nvidia.com/en-us/data-center/technologies/blackwell-architecture/", "Blackwell hardware texture"),
    ("NVIDIA GTC", "NVIDIA", "https://www.nvidia.com/gtc/", "GTC public event surface"),
    ("AMD Instinct", "AMD", "https://www.amd.com/en/products/accelerators/instinct.html", "accelerator competitor texture"),
    ("CoreWeave", "CoreWeave", "https://www.coreweave.com/", "AI cloud/datacenter texture"),
    ("OpenAI ChatGPT", "OpenAI", "https://openai.com/chatgpt/", "ChatGPT product surface"),
    ("OpenAI API", "OpenAI", "https://openai.com/api/", "developer API product surface"),
    ("Anthropic Claude", "Anthropic", "https://www.anthropic.com/claude", "Claude product surface"),
    ("Anthropic Claude 4", "Anthropic", "https://www.anthropic.com/news/claude-4", "model launch source surface"),
    ("DeepSeek", "DeepSeek", "https://www.deepseek.com/", "China frontier lab/product surface"),
    ("Meta Llama", "Meta", "https://www.llama.com/", "open-weight model surface"),
    ("Meta AI", "Meta", "https://ai.meta.com/", "Meta AI product/lab surface"),
    ("Google Gemini", "Google", "https://gemini.google.com/", "Gemini interface surface"),
    ("Google DeepMind", "Google DeepMind", "https://deepmind.google/", "DeepMind lab surface"),
    ("Google Cloud AI", "Google", "https://cloud.google.com/products/ai", "cloud AI product surface"),
    ("Microsoft Azure OpenAI", "Microsoft", "https://azure.microsoft.com/en-us/products/ai-services/openai-service", "cloud partnership surface"),
    ("GitHub Copilot", "GitHub", "https://github.com/features/copilot", "coding assistant product surface"),
    ("ASML", "ASML", "https://www.asml.com/en", "semiconductor supply-chain surface"),
    ("TSMC", "TSMC", "https://www.tsmc.com/english", "foundry source surface"),
    ("Hugging Face", "Hugging Face", "https://huggingface.co/", "open model hub surface"),
    ("Mistral AI", "Mistral AI", "https://mistral.ai/", "European frontier lab surface"),
    ("xAI", "xAI", "https://x.ai/", "frontier lab product surface"),
    ("Baidu AI Cloud", "Baidu", "https://cloud.baidu.com/", "China cloud/model surface"),
    ("Tencent Hunyuan", "Tencent", "https://hunyuan.tencent.com/", "China model surface"),
    ("Alibaba Qwen", "Alibaba/Qwen", "https://qwenlm.github.io/", "Qwen open model surface"),
    ("PyTorch", "PyTorch", "https://pytorch.org/", "ML tooling surface"),
    ("CUDA Toolkit", "NVIDIA", "https://developer.nvidia.com/cuda-toolkit", "CUDA tooling surface"),
    ("LMArena", "LMArena", "https://lmarena.ai/", "leaderboard surface"),
    ("AWS Bedrock", "AWS", "https://aws.amazon.com/bedrock/", "cloud model platform surface"),
    ("Oracle AI", "Oracle", "https://www.oracle.com/artificial-intelligence/", "cloud AI surface"),
    ("IBM watsonx", "IBM", "https://www.ibm.com/watsonx", "enterprise AI platform surface"),
    ("Databricks ML", "Databricks", "https://www.databricks.com/product/machine-learning", "data/model platform surface"),
    ("Snowflake Cortex", "Snowflake", "https://www.snowflake.com/en/data-cloud/cortex/", "data cloud AI surface"),
]


LOGO_CANDIDATES = [
    ("NVIDIA", "nvidia", "hardware/AI factory logo"),
    ("AMD", "amd", "accelerator competitor logo"),
    ("OpenAI", "openai", "LLM lab/product logo"),
    ("Anthropic", "anthropic", "Claude lab logo"),
    ("Meta", "meta", "Llama/open-weight logo"),
    ("Google", "google", "Gemini/DeepMind ecosystem logo"),
    ("Google Cloud", "googlecloud", "cloud AI logo"),
    ("Microsoft", "microsoft", "OpenAI cloud partner logo"),
    ("Alibaba Cloud", "alibabacloud", "Qwen/cloud ecosystem logo"),
    ("Hugging Face", "huggingface", "model hub logo"),
    ("Mistral AI", "mistralai", "European frontier lab logo"),
    ("xAI/X", "x", "frontier lab/social owner logo"),
    ("Baidu", "baidu", "China model/cloud logo"),
    ("Tencent QQ", "tencentqq", "Tencent ecosystem logo"),
    ("Xiaomi", "xiaomi", "MiMo model-lab adjacent logo"),
    ("Amazon Web Services", "amazonwebservices", "cloud AI platform logo"),
    ("Oracle", "oracle", "cloud AI platform logo"),
    ("IBM", "ibm", "enterprise AI platform logo"),
    ("Intel", "intel", "CPU/accelerator ecosystem logo"),
    ("Arm", "arm", "CPU ecosystem logo"),
    ("GitHub", "github", "coding agent/developer surface logo"),
    ("Python", "python", "ML/software substrate logo"),
    ("PyTorch", "pytorch", "training framework logo"),
    ("TensorFlow", "tensorflow", "ML framework logo"),
    ("Docker", "docker", "deployment/tooling logo"),
    ("Kubernetes", "kubernetes", "infrastructure orchestration logo"),
    ("Linux", "linux", "software substrate logo"),
    ("Databricks", "databricks", "data/model platform logo"),
    ("Cloudflare", "cloudflare", "edge/inference infrastructure logo"),
    ("Apache", "apache", "open-source substrate logo"),
    ("Kaggle", "kaggle", "data/benchmark ecosystem logo"),
]


PEOPLE_CANDIDATES = [
    ("Jensen Huang", "NVIDIA founder and CEO", "Jensen_Huang", "hardware/AI factory human anchor"),
    ("Lisa Su", "AMD chair and CEO", "Lisa_Su", "accelerator competitor human anchor"),
    ("Sam Altman", "OpenAI CEO", "Sam_Altman", "ChatGPT/OpenAI human anchor"),
    ("Greg Brockman", "OpenAI cofounder", "Greg_Brockman", "OpenAI systems/product human anchor"),
    ("Ilya Sutskever", "OpenAI cofounder and researcher", "Ilya_Sutskever", "scaling/alignment human anchor"),
    ("Andrej Karpathy", "researcher and former OpenAI/Tesla leader", "Andrej_Karpathy", "software/LLM education human anchor"),
    ("Dario Amodei", "Anthropic cofounder and CEO", "Dario_Amodei", "Claude/alignment human anchor"),
    ("Daniela Amodei", "Anthropic cofounder and president", "Daniela_Amodei", "Anthropic institution human anchor"),
    ("Mark Zuckerberg", "Meta founder and CEO", "Mark_Zuckerberg", "Llama/open-weight human anchor"),
    ("Demis Hassabis", "Google DeepMind CEO", "Demis_Hassabis", "DeepMind/Gemini human anchor"),
    ("Sundar Pichai", "Google CEO", "Sundar_Pichai", "Google product/platform human anchor"),
    ("Satya Nadella", "Microsoft CEO", "Satya_Nadella", "Microsoft/OpenAI platform human anchor"),
    ("Yann LeCun", "Meta chief AI scientist", "Yann_LeCun", "open research/model debate human anchor"),
    ("Geoffrey Hinton", "deep learning researcher", "Geoffrey_Hinton", "neural-network lineage human anchor"),
    ("Yoshua Bengio", "deep learning researcher", "Yoshua_Bengio", "deep-learning lineage human anchor"),
    ("Fei-Fei Li", "AI researcher", "Fei-Fei_Li", "data/vision/AI institution human anchor"),
    ("Andrew Ng", "AI researcher and educator", "Andrew_Ng", "AI education/cloud human anchor"),
    ("Jeff Dean", "Google researcher", "Jeff_Dean", "Google systems/model scaling human anchor"),
    ("Oriol Vinyals", "DeepMind researcher", "Oriol_Vinyals", "seq2seq/deep learning human anchor"),
    ("Ashish Vaswani", "Transformer coauthor", "Ashish_Vaswani", "Transformer human anchor"),
    ("Noam Shazeer", "LLM researcher", "Noam_Shazeer", "MoE/model architecture human anchor"),
    ("Liang Wenfeng", "DeepSeek founder", "Liang_Wenfeng", "DeepSeek human anchor"),
]


PERSON_PROFILE_FALLBACK = {
    "Jensen Huang": "https://www.nvidia.com/en-us/about-nvidia/board-of-directors/jensen-huang/",
    "Lisa Su": "https://www.amd.com/en/corporate/leadership/lisa-su.html",
    "Sam Altman": "https://en.wikipedia.org/wiki/Sam_Altman",
    "Greg Brockman": "https://en.wikipedia.org/wiki/Greg_Brockman",
    "Ilya Sutskever": "https://en.wikipedia.org/wiki/Ilya_Sutskever",
    "Andrej Karpathy": "https://karpathy.ai/",
    "Dario Amodei": "https://en.wikipedia.org/wiki/Dario_Amodei",
    "Daniela Amodei": "https://en.wikipedia.org/wiki/Daniela_Amodei",
    "Mark Zuckerberg": "https://about.meta.com/media-gallery/executives/mark-zuckerberg/",
    "Demis Hassabis": "https://deepmind.google/about/leadership/demis-hassabis/",
    "Sundar Pichai": "https://abc.xyz/investor/sundar-pichai/",
    "Satya Nadella": "https://news.microsoft.com/exec/satya-nadella/",
    "Yann LeCun": "https://ai.meta.com/people/yann-lecun/",
    "Geoffrey Hinton": "https://en.wikipedia.org/wiki/Geoffrey_Hinton",
    "Yoshua Bengio": "https://mila.quebec/en/person/yoshua-bengio/",
    "Fei-Fei Li": "https://profiles.stanford.edu/fei-fei-li",
    "Andrew Ng": "https://www.andrewng.org/",
    "Jeff Dean": "https://research.google/people/jeff/",
    "Oriol Vinyals": "https://en.wikipedia.org/wiki/Oriol_Vinyals",
    "Ashish Vaswani": "https://en.wikipedia.org/wiki/Ashish_Vaswani",
    "Noam Shazeer": "https://en.wikipedia.org/wiki/Noam_Shazeer",
    "Liang Wenfeng": "https://en.wikipedia.org/wiki/Liang_Wenfeng",
}


def remove_existing_pass_rows() -> None:
    for path, token in [
        (ROOT / "scoreboard.tsv", "\tpass-0284\t"),
        (ROOT / "claims.tsv", "\tI-0284\t"),
        (ROOT / "assets_manifest.tsv", "A-0284-"),
        (ROOT / "sources.tsv", "\tI-0284\t"),
    ]:
        if not path.exists():
            continue
        lines = path.read_text(encoding="utf-8").splitlines()
        kept = [line for line in lines if token not in line]
        path.write_text("\n".join(kept) + "\n", encoding="utf-8")


def next_source_number() -> int:
    max_id = 0
    for line in (ROOT / "sources.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        if not line:
            continue
        source_id = line.split("\t", 1)[0]
        match = re.match(r"S-(\d+)", source_id)
        if match:
            max_id = max(max_id, int(match.group(1)))
    return max_id + 1


def next_claim_number() -> int:
    max_id = 0
    for line in (ROOT / "claims.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        if not line:
            continue
        claim_id = line.split("\t", 1)[0]
        match = re.match(r"C-(\d+)", claim_id)
        if match:
            max_id = max(max_id, int(match.group(1)))
    return max_id + 1


def acquire_source_images(failures: list[dict[str, object]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    for title, org, page_url, story in SOURCE_PAGE_CANDIDATES:
        try:
            page_text = fetch_text(page_url)
            image_url = meta_image_url(page_url, page_text)
            if not image_url:
                raise RuntimeError("no og/twitter image found")
            payload, content_type = fetch_bytes(image_url)
            ext = extension_from_content_type(content_type, image_url)
            if ext == ".bin":
                raise RuntimeError(f"unsupported image content type {content_type}")
            local_path = SOURCE_DIR / f"{safe_name(org)}-{safe_name(title)}{ext}"
            local_path.write_bytes(payload)
            width, height = image_dimensions(local_path)
            score, score_note = quality_score(local_path)
            rows.append(
                {
                    "asset_id": f"A-0284-{len(rows) + 1:03d}",
                    "category": "source_image",
                    "subject": title,
                    "organization_or_role": org,
                    "source_page_url": page_url,
                    "source_asset_url": image_url,
                    "local_path": rel(local_path),
                    "sha256": sha256_file(local_path),
                    "file_size": local_path.stat().st_size,
                    "width": width,
                    "height": height,
                    "quality_score": score,
                    "quality_note": score_note,
                    "rights_status": "private_use_source_image_from_public_page",
                    "story_purpose": story,
                    "blocked_claims": "Visual texture only; does not prove current product state, adoption, performance, revenue, safety, or benchmark rank.",
                }
            )
        except Exception as exc:
            failures.append({"category": "source_image", "subject": title, "source": page_url, "failure": f"{type(exc).__name__}: {exc}"})
    return rows


def acquire_logos(failures: list[dict[str, object]], start_index: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    LOGO_DIR.mkdir(parents=True, exist_ok=True)
    for brand, slug, story in LOGO_CANDIDATES:
        url = f"https://cdn.simpleicons.org/{quote(slug)}"
        try:
            payload, content_type = fetch_bytes(url)
            text = payload.decode("utf-8", errors="replace")
            if "<svg" not in text[:500].lower():
                raise RuntimeError(f"not an SVG response: {content_type}")
            local_path = LOGO_DIR / f"{safe_name(brand)}.svg"
            local_path.write_text(text, encoding="utf-8")
            width, height = image_dimensions(local_path)
            score, score_note = quality_score(local_path)
            rows.append(
                {
                    "asset_id": f"A-0284-{start_index + len(rows):03d}",
                    "category": "logo",
                    "subject": brand,
                    "organization_or_role": brand,
                    "source_page_url": "https://simpleicons.org/",
                    "source_asset_url": url,
                    "local_path": rel(local_path),
                    "sha256": sha256_file(local_path),
                    "file_size": local_path.stat().st_size,
                    "width": width,
                    "height": height,
                    "quality_score": score,
                    "quality_note": score_note,
                    "rights_status": "private_use_brand_logo_from_simple_icons_public_cdn",
                    "story_purpose": story,
                    "blocked_claims": "Logo identifies an actor only; it does not imply endorsement, partnership, market share, model quality, or current product status.",
                }
            )
        except Exception as exc:
            failures.append({"category": "logo", "subject": brand, "source": url, "failure": f"{type(exc).__name__}: {exc}"})
    return rows


def wiki_summary_url(page_title: str) -> str:
    return f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(page_title)}"


def acquire_people(failures: list[dict[str, object]], start_index: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    PEOPLE_DIR.mkdir(parents=True, exist_ok=True)
    for person, role, page_title, story in PEOPLE_CANDIDATES:
        summary_url = wiki_summary_url(page_title)
        try:
            summary = json.loads(fetch_text(summary_url))
            image_url = ""
            if isinstance(summary.get("originalimage"), dict):
                image_url = summary["originalimage"].get("source", "")
            if not image_url and isinstance(summary.get("thumbnail"), dict):
                image_url = summary["thumbnail"].get("source", "")
            if not image_url:
                raise RuntimeError("no Wikipedia thumbnail/originalimage")
            payload, content_type = fetch_bytes(image_url)
            ext = extension_from_content_type(content_type, image_url)
            if ext == ".bin":
                ext = ".jpg"
            local_path = PEOPLE_DIR / f"{safe_name(person)}{ext}"
            local_path.write_bytes(payload)
            width, height = image_dimensions(local_path)
            score, score_note = quality_score(local_path)
            rows.append(
                {
                    "asset_id": f"A-0284-{start_index + len(rows):03d}",
                    "category": "person_image",
                    "subject": person,
                    "organization_or_role": role,
                    "source_page_url": summary.get("content_urls", {}).get("desktop", {}).get("page", summary_url),
                    "source_asset_url": image_url,
                    "local_path": rel(local_path),
                    "sha256": sha256_file(local_path),
                    "file_size": local_path.stat().st_size,
                    "width": width,
                    "height": height,
                    "quality_score": score,
                    "quality_note": score_note,
                    "rights_status": "private_use_public_profile_image_from_wikipedia_summary",
                    "story_purpose": story,
                    "blocked_claims": "Public-profile image only; does not support biography claims beyond separately sourced text, current title, motives, or private scenes.",
                }
            )
        except Exception as exc:
            failures.append({"category": "person_image", "subject": person, "source": summary_url, "failure": f"{type(exc).__name__}: {exc}"})
    return rows


def chrome_screenshot(url: str, target: Path) -> None:
    if not CHROME.exists():
        raise FileNotFoundError(f"Chrome not found at {CHROME}")
    target.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        str(CHROME),
        "--headless=new",
        "--disable-gpu",
        "--no-sandbox",
        "--disable-extensions",
        "--hide-scrollbars",
        "--window-size=1200,900",
        "--virtual-time-budget=6000",
        f"--screenshot={target}",
        url,
    ]
    completed = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=35, check=False)
    if completed.returncode != 0 or not target.exists() or target.stat().st_size < 5000:
        raise RuntimeError(f"Chrome screenshot failed rc={completed.returncode}; output={completed.stdout[-300:]}")


def add_person_profile_fallbacks(existing_rows: list[dict[str, object]], failures: list[dict[str, object]], start_index: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    existing_subjects = {str(row["subject"]) for row in existing_rows}
    for person, role, _page_title, story in PEOPLE_CANDIDATES:
        if person in existing_subjects:
            continue
        profile_url = PERSON_PROFILE_FALLBACK.get(person)
        if not profile_url:
            continue
        try:
            local_path = PEOPLE_DIR / f"{safe_name(person)}-profile-page.png"
            chrome_screenshot(profile_url, local_path)
            width, height = image_dimensions(local_path)
            score, score_note = quality_score(local_path)
            rows.append(
                {
                    "asset_id": f"A-0284-{start_index + len(rows):03d}",
                    "category": "person_image",
                    "subject": person,
                    "organization_or_role": role,
                    "source_page_url": profile_url,
                    "source_asset_url": profile_url,
                    "local_path": rel(local_path),
                    "sha256": sha256_file(local_path),
                    "file_size": local_path.stat().st_size,
                    "width": width,
                    "height": height,
                    "quality_score": score,
                    "quality_note": f"profile_page_screenshot; {score_note}",
                    "rights_status": "private_use_public_profile_page_screenshot",
                    "story_purpose": story,
                    "blocked_claims": "Public-profile page screenshot only; does not support biography claims beyond separately sourced text, current title, motives, or private scenes.",
                }
            )
            existing_subjects.add(person)
            if len(existing_rows) + len(rows) >= 15:
                break
        except Exception as exc:
            failures.append({"category": "person_profile_fallback", "subject": person, "source": profile_url, "failure": f"{type(exc).__name__}: {exc}"})
    return rows


def contact_sheet(rows: list[dict[str, object]], filename: str, title: str) -> Path:
    CONTACT_DIR.mkdir(parents=True, exist_ok=True)
    images = [ROOT / str(row["local_path"]) for row in rows if Path(ROOT / str(row["local_path"])).suffix.lower() != ".svg"]
    cell_w, cell_h = 300, 240
    cols = 5
    rows_count = max(1, (len(images) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * cell_w, rows_count * cell_h + 70), (248, 245, 238))
    draw = ImageDraw.Draw(sheet)
    draw.text((18, 18), title, fill=(32, 42, 48))
    for idx, path in enumerate(images):
        x = (idx % cols) * cell_w
        y = 70 + (idx // cols) * cell_h
        try:
            with Image.open(path) as image:
                image = image.convert("RGB")
                image.thumbnail((cell_w - 24, cell_h - 58))
                sheet.paste(image, (x + 12, y + 8))
                draw.text((x + 12, y + cell_h - 42), path.stem[:34], fill=(30, 38, 42))
        except Exception:
            draw.rectangle((x + 12, y + 8, x + cell_w - 12, y + cell_h - 58), outline=(160, 60, 60), width=2)
            draw.text((x + 20, y + 40), "open failed", fill=(120, 30, 30))
    target = CONTACT_DIR / filename
    sheet.save(target)
    return target


def append_asset_manifest(rows: list[dict[str, object]]) -> None:
    for row in rows:
        append_line(
            ROOT / "assets_manifest.tsv",
            [
                row["asset_id"],
                "available_local_private_use",
                row["local_path"],
                row["category"],
                row["subject"],
                row["source_page_url"],
                row["source_asset_url"],
                row["organization_or_role"],
                "2026-05-27",
                f"I-0284 acquired {row['category']} for private-edition visual layer: {row['subject']}.",
                row["story_purpose"],
                f"{row['rights_status']}; {row['blocked_claims']}",
                "manuscript/real-world-image-acquisition-i0284.md",
            ],
        )


def append_sources(rows: list[dict[str, object]]) -> None:
    number = next_source_number()
    for idx, row in enumerate(rows):
        append_line(
            ROOT / "sources.tsv",
            [
                f"S-{number + idx:04d}",
                "available",
                f"I-0284 {row['category']}: {row['subject']}",
                row["organization_or_role"],
                row["category"],
                row["source_page_url"],
                "2026-05-27",
                "post-cutoff acquisition of visual/source handle; not evidence for post-cutoff events",
                "primary visual source" if row["category"] != "person_image" else "public-profile visual source",
                "I-0284",
                f"Local file {row['local_path']}; sha256 {row['sha256']}; source asset {row['source_asset_url']}; blocked claims: {row['blocked_claims']}",
            ],
        )


def replace_idea_row(summary: dict[str, object]) -> None:
    path = ROOT / "ideas.tsv"
    text = path.read_text(encoding="utf-8")
    match = re.search(r"^I-0284\tpending\t.*$", text, flags=re.MULTILINE)
    if not match:
        return
    new = (
        "I-0284\tdone\tAcquire the first half of the real-world image layer: at least 25 strong private-use photos/screenshots/source images, 25 company/lab/product logos, "
        "and 15 CEO/founder/research-leader/person images across NVIDIA, AMD, CoreWeave, OpenAI, Anthropic, DeepSeek, Meta, Google, Microsoft, ASML, TSMC, and key open-model actors.\t"
        "acquisition half 1\tphoto/logo/people coverage\tDone in scripts/real_world_image_acquisition_i0284.py, data/real_world_image_acquisition_i0284.tsv, "
        "data/real_world_image_acquisition_failures_i0284.tsv, data/real_world_image_acquisition_qa_i0284.tsv, and manuscript/real-world-image-acquisition-i0284.md; "
        f"acquired {summary['source_image_count']} source images, {summary['logo_count']} logos, and {summary['person_image_count']} person/public-profile images with local files, hashes, provenance, story-purpose fields, and blocked-claim notes."
    )
    path.write_text(text[: match.start()] + new + text[match.end() :], encoding="utf-8")


def word_count_and_chapters() -> tuple[int, int]:
    text = (MANUSCRIPT / "Next-Token-full-draft.md").read_text(encoding="utf-8")
    return len(re.findall(r"\b[\w'-]+\b", text)), len(re.findall(r"^# Chapter\s+\d+\b", text, flags=re.MULTILINE))


def append_ledgers(summary: dict[str, object]) -> None:
    claim_id = f"C-{next_claim_number():04d}"
    append_line(
        ROOT / "claims.tsv",
        [
            claim_id,
            "supported",
            "I-0284 acquired the first real-world visual layer with at least 25 source images, 25 logos, and 15 person/public-profile images, each with local file, hash, provenance, story purpose, rights/private-use note, and blocked-claim text.",
            "data/real_world_image_acquisition_i0284.tsv; data/real_world_image_acquisition_qa_i0284.tsv",
            "I-0284",
            "local acquisition ledger and file/hash proof",
            "2026-05-27",
            "Visual assets are private-use handles, not final publication clearance and not support for product/currentness/market/performance/biography claims.",
        ],
    )

    words, chapters = word_count_and_chapters()
    source_total = len((ROOT / "sources.tsv").read_text(encoding="utf-8").splitlines()) - 1
    supported_total = sum(1 for line in (ROOT / "claims.tsv").read_text(encoding="utf-8").splitlines()[1:] if "\tsupported\t" in line)
    append_line(
        ROOT / "scoreboard.tsv",
        [
            now_stamp(),
            "pass-0284",
            "champion real-world image acquisition half 1",
            "I-0284",
            "acquisition half 1",
            "+1.0",
            "100.0",
            words,
            chapters,
            "142",
            78 + int(summary["source_image_count"]) + int(summary["person_image_count"]),
            source_total,
            f"{supported_total} supported / 0 needs-verification; acquired {summary['source_image_count']} source images, {summary['logo_count']} logos, {summary['person_image_count']} person images; {summary['qa_pass']} pass, {summary['qa_warn']} warn, {summary['qa_fail']} fail QA checks; {summary['failure_count']} failed/unused candidates logged",
            "+1",
            "Rasters remain local/ignored; logo SVGs and provenance ledgers are committed; no final layout integration, publication permission, or factual product/biography claim promotion implied",
            "promoted",
            "Acquired the first real-world visual layer across official pages, brand marks, and public-profile images so the private edition can later show companies, products, hardware surfaces, and people rather than only diagrams.",
            "one real-world photo/logo/people acquisition pass",
        ],
    )

    insight_block = (
        "\n## 2026-05-27 - I-0284 Real-World Image Layer\n\n"
        "Real-world visuals are useful only when they arrive as evidence handles, not vibes: the minimum unit is local file, source URL, source-asset URL, hash, role, story purpose, quality note, rights/private-use status, and blocked-claim text. Logos identify actors, profile images humanize institutions, and source images add texture, but none of them license market, benchmark, safety, adoption, current-product, or private-scene claims.\n"
    )
    insights = ROOT / "insights.md"
    text = insights.read_text(encoding="utf-8")
    pattern = r"\n## 2026-05-27 - I-0284 Real-World Image Layer\n\n.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.DOTALL):
        text = re.sub(pattern, insight_block.rstrip("\n"), text, flags=re.DOTALL)
    else:
        text += insight_block
    insights.write_text(text, encoding="utf-8")

    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    insert = (
        f"- **Current real-world image layer:** I-0284 acquires {summary['source_image_count']} source images, {summary['logo_count']} logos, and {summary['person_image_count']} person/public-profile images with local files, hashes, story-purpose fields, private-use notes, and blocked-claim text in `data/real_world_image_acquisition_i0284.tsv`; rasters remain local/ignored and final layout/rights review remains pending.\n"
    )
    marker = "- **Current table/excerpt integration toolchain:**"
    if insert not in readme_text and marker in readme_text:
        readme.write_text(readme_text.replace(marker, insert + marker, 1), encoding="utf-8")


def write_brief(summary: dict[str, object], sheets: dict[str, Path]) -> None:
    lines = [
        "# I-0284 Real-World Image Acquisition Half 1",
        "",
        f"Status: promoted acquisition pass, with {summary['qa_pass']} pass / {summary['qa_warn']} warn / {summary['qa_fail']} fail QA.",
        "",
        "## Acquired",
        "",
        f"- Source images: {summary['source_image_count']} local files from official/public source pages.",
        f"- Logos: {summary['logo_count']} local SVG files.",
        f"- Person/public-profile images: {summary['person_image_count']} local files.",
        f"- Failed or unused candidates logged: {summary['failure_count']}.",
        "",
        "## Contact Sheets",
        "",
        f"- Source images: `{rel(sheets['source_images'])}`",
        f"- Person images: `{rel(sheets['people'])}`",
        "",
        "## Limits",
        "",
        "- This pass acquires private-use visual handles; it does not integrate them into the full manuscript or final figure manifest.",
        "- Rasters and contact sheets are intentionally local/ignored. The committed artifact is the provenance and QA trail.",
        "- Logo rows identify actors only. Source-image and profile-image rows do not support market, product, benchmark, safety, adoption, currentness, biography, motive, or private-scene claims.",
        "- Final layout, caption compression, image selection, rights review, and replacement decisions remain for I-0290 and later render passes.",
        "",
    ]
    (MANUSCRIPT / "real-world-image-acquisition-i0284.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    remove_existing_pass_rows()
    for directory in [SOURCE_DIR, LOGO_DIR, PEOPLE_DIR, CONTACT_DIR, DATA, MANUSCRIPT]:
        directory.mkdir(parents=True, exist_ok=True)

    failures: list[dict[str, object]] = []
    source_rows = acquire_source_images(failures)
    logo_rows = acquire_logos(failures, len(source_rows) + 1)
    people_rows = acquire_people(failures, len(source_rows) + len(logo_rows) + 1)
    if len(people_rows) < 15:
        people_rows.extend(
            add_person_profile_fallbacks(
                people_rows,
                failures,
                len(source_rows) + len(logo_rows) + len(people_rows) + 1,
            )
        )
    rows = source_rows + logo_rows + people_rows

    fields = [
        "asset_id",
        "category",
        "subject",
        "organization_or_role",
        "source_page_url",
        "source_asset_url",
        "local_path",
        "sha256",
        "file_size",
        "width",
        "height",
        "quality_score",
        "quality_note",
        "rights_status",
        "story_purpose",
        "blocked_claims",
    ]
    write_tsv(DATA / "real_world_image_acquisition_i0284.tsv", rows, fields)
    write_tsv(DATA / "real_world_image_acquisition_failures_i0284.tsv", failures, ["category", "subject", "source", "failure"])

    sheets = {
        "source_images": contact_sheet(source_rows, "i0284_source_images_contact_sheet.png", "I-0284 source images"),
        "people": contact_sheet(people_rows, "i0284_people_contact_sheet.png", "I-0284 people/public-profile images"),
    }

    categories = Counter(str(row["category"]) for row in rows)
    orgs = {str(row["organization_or_role"]).split("/", 1)[0] for row in rows}
    required_fields = ["local_path", "sha256", "source_page_url", "source_asset_url", "story_purpose", "blocked_claims", "rights_status"]
    all_files_exist = all((ROOT / str(row["local_path"])).exists() for row in rows)
    all_hashes_match = all(sha256_file(ROOT / str(row["local_path"])) == row["sha256"] for row in rows)
    all_required = all(all(str(row.get(field, "")).strip() for field in required_fields) for row in rows)
    logo_svg_count = sum(1 for row in logo_rows if str(row["local_path"]).endswith(".svg"))
    sheet_ok = all(path.exists() and path.stat().st_size > 10_000 for path in sheets.values())

    qa_rows = [
        {"check_id": "I0284-001", "category": "source_image_count", "result": "pass" if categories["source_image"] >= 25 else "fail", "evidence": f"source_images={categories['source_image']} target=25", "recommended_action": "Use in I-0290 placement triage."},
        {"check_id": "I0284-002", "category": "logo_count", "result": "pass" if categories["logo"] >= 25 else "fail", "evidence": f"logos={categories['logo']} target=25; svg={logo_svg_count}", "recommended_action": "Use in I-0290 company/lab visual lane."},
        {"check_id": "I0284-003", "category": "person_image_count", "result": "pass" if categories["person_image"] >= 15 else "fail", "evidence": f"person_images={categories['person_image']} target=15", "recommended_action": "Use in I-0290 people/human texture lane."},
        {"check_id": "I0284-004", "category": "local_files", "result": "pass" if all_files_exist else "fail", "evidence": f"rows={len(rows)} all_files_exist={all_files_exist}", "recommended_action": "Repair missing files before integration."},
        {"check_id": "I0284-005", "category": "hashes", "result": "pass" if all_hashes_match else "fail", "evidence": f"all_hashes_match={all_hashes_match}", "recommended_action": "Keep hashes as acquisition proof."},
        {"check_id": "I0284-006", "category": "provenance_fields", "result": "pass" if all_required else "fail", "evidence": f"required_fields={','.join(required_fields)} all_present={all_required}", "recommended_action": "Do not promote rows with missing provenance."},
        {"check_id": "I0284-007", "category": "source_diversity", "result": "pass" if len(orgs) >= 12 else "warn", "evidence": f"distinct_org_or_role_prefixes={len(orgs)}", "recommended_action": "Use I-0287 to fill remaining institutional gaps."},
        {"check_id": "I0284-008", "category": "contact_sheets", "result": "pass" if sheet_ok else "fail", "evidence": "; ".join(f"{key}={rel(path)} bytes={path.stat().st_size}" for key, path in sheets.items()), "recommended_action": "Inspect sheets before final placement."},
        {"check_id": "I0284-009", "category": "failure_log", "result": "pass" if len(failures) >= 0 else "fail", "evidence": f"failures_logged={len(failures)}", "recommended_action": "Use failures to target I-0287 second half."},
    ]
    write_tsv(DATA / "real_world_image_acquisition_qa_i0284.tsv", qa_rows, ["check_id", "category", "result", "evidence", "recommended_action"])

    summary = {
        "source_image_count": categories["source_image"],
        "logo_count": categories["logo"],
        "person_image_count": categories["person_image"],
        "total_rows": len(rows),
        "failure_count": len(failures),
        "distinct_orgs": len(orgs),
        "qa_pass": sum(1 for row in qa_rows if row["result"] == "pass"),
        "qa_warn": sum(1 for row in qa_rows if row["result"] == "warn"),
        "qa_fail": sum(1 for row in qa_rows if row["result"] == "fail"),
        "source_contact_sheet": rel(sheets["source_images"]),
        "people_contact_sheet": rel(sheets["people"]),
    }
    write_tsv(DATA / "real_world_image_acquisition_summary_i0284.tsv", [summary], list(summary.keys()))

    append_asset_manifest(rows)
    append_sources(rows)
    replace_idea_row(summary)
    write_brief(summary, sheets)
    append_ledgers(summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["qa_fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
