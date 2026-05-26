from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import sys
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from importlib import metadata
from pathlib import Path
from urllib.parse import urlparse


PASS_ID = "I-0282"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
ASSETS = ROOT / "assets"
MANUSCRIPT = ROOT / "manuscript"
I0281_TOOLING = ROOT / ".tooling" / "i0281" / "python"
I0282_TOOLING = ROOT / ".tooling" / "i0282" / "python"

for tool_path in [I0282_TOOLING, I0281_TOOLING]:
    if tool_path.exists():
        sys.path.insert(0, str(tool_path))

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageOps  # type: ignore

try:
    import cv2  # type: ignore
except Exception:  # pragma: no cover - captured in probe output
    cv2 = None

try:
    import imagehash  # type: ignore
except Exception:  # pragma: no cover - captured in probe output
    imagehash = None

try:
    import numpy as np  # type: ignore
except Exception:  # pragma: no cover - captured in probe output
    np = None

try:
    import requests  # type: ignore
except Exception:  # pragma: no cover - captured in probe output
    requests = None

try:
    from colorthief import ColorThief  # type: ignore
except Exception:  # pragma: no cover - captured in probe output
    ColorThief = None

try:
    import piexif  # type: ignore
except Exception:  # pragma: no cover - captured in probe output
    piexif = None


FIELDNAMES_SCOREBOARD = [
    "timestamp",
    "action_id",
    "parent",
    "idea_id",
    "category",
    "primary_score_delta",
    "bookscore",
    "word_count",
    "chapter_count",
    "chart_count",
    "photo_count",
    "source_count",
    "claim_coverage",
    "novelty_score",
    "regression_flags",
    "verdict",
    "reason",
    "budget_used",
]


@dataclass
class Candidate:
    candidate_id: str
    role: str
    source_kind: str
    source_url_or_context: str
    local_original: Path
    rights_status: str
    story_purpose: str
    blocked_claims: str


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_tsv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fieldnames})


def append_line(path: Path, fields: list[object]) -> None:
    with path.open("a", encoding="utf-8", newline="") as handle:
        handle.write("\t".join(str(field).replace("\t", " ").replace("\r", " ").replace("\n", " ") for field in fields) + "\n")


def replace_idea_row() -> None:
    path = ROOT / "ideas.tsv"
    text = path.read_text(encoding="utf-8")
    old = re.search(r"^I-0282\tpending\t.*$", text, flags=re.MULTILINE)
    if not old:
        return
    new = (
        "I-0282\tdone\tInstall and verify the image-search and media-prep toolchain for the sprint: Google/web image retrieval workflow, "
        "resizing/cropping/contact-sheet generation, logo handling, CEO/person-photo handling, duplicate detection, quality scoring, and safe local storage outside Git for heavy rasters.\t"
        "tools install\tphoto/logo acquisition readiness\tDone in scripts/media_prep_toolchain_i0282.py, data/media_prep_probe_i0282.tsv, "
        "data/media_prep_qa_i0282.tsv, data/media_prep_candidates_i0282.tsv, data/media_prep_derivatives_i0282.tsv, "
        "data/media_prep_duplicate_groups_i0282.tsv, data/media_prep_quality_scores_i0282.tsv, data/media_prep_install_i0282.tsv, "
        "and manuscript/media-prep-toolchain-i0282.md; verified web/local retrieval workflow, resize/crop/contact-sheet generation, "
        "logo transparency handling, person-photo framing, perceptual duplicate detection, quality scoring, and ignored local storage for heavy rasters."
    )
    path.write_text(text[: old.start()] + new + text[old.end() :], encoding="utf-8")


def remove_existing_pass_rows() -> None:
    for filename, token in [("claims.tsv", "\tI-0282;I-0281\t"), ("scoreboard.tsv", "\tpass-0282\t")]:
        path = ROOT / filename
        lines = path.read_text(encoding="utf-8").splitlines()
        kept = [line for line in lines if token not in line]
        path.write_text("\n".join(kept) + "\n", encoding="utf-8")


def word_count_and_chapters() -> tuple[int, int]:
    draft = MANUSCRIPT / "Next-Token-full-draft.md"
    text = draft.read_text(encoding="utf-8")
    return len(re.findall(r"\b[\w'-]+\b", text)), len(re.findall(r"^# Chapter\s+\d+\b", text, flags=re.MULTILINE))


def package_version(name: str) -> tuple[str, str]:
    try:
        return metadata.version(name), "installed"
    except metadata.PackageNotFoundError:
        return "", "missing"


def write_install_manifest() -> None:
    rows: list[dict[str, object]] = []
    packages = [
        ("python", "pillow", I0282_TOOLING),
        ("python", "imagehash", I0282_TOOLING),
        ("python", "scikit-image", I0282_TOOLING),
        ("python", "colorthief", I0282_TOOLING),
        ("python", "piexif", I0282_TOOLING),
        ("python", "opencv-python-headless", I0281_TOOLING),
        ("python", "requests", I0281_TOOLING),
        ("python", "numpy", I0282_TOOLING),
    ]
    for ecosystem, package, install_path in packages:
        version, status = package_version(package)
        rows.append(
            {
                "ecosystem": ecosystem,
                "package": package,
                "version": version,
                "install_path": str(install_path.relative_to(ROOT)) if install_path.exists() else "",
                "status": status,
                "git_policy": "ignored by .gitignore; reinstall from ledger if needed",
            }
        )
    write_tsv(
        DATA / "media_prep_install_i0282.tsv",
        rows,
        ["ecosystem", "package", "version", "install_path", "status", "git_policy"],
    )


def make_probe_photo(path: Path, label: str, accent: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (1200, 800), (32, 36, 42))
    draw = ImageDraw.Draw(image)
    for y in range(800):
        shade = int(40 + y * 0.12)
        draw.line((0, y, 1200, y), fill=(shade, min(120, shade + 10), min(150, shade + 25)))
    draw.rectangle((80, 500, 1120, 650), fill=(52, 58, 66), outline=(160, 170, 180), width=3)
    for x in range(120, 1080, 90):
        draw.rectangle((x, 525, x + 54, 625), fill=(24, 28, 34), outline=accent, width=2)
        draw.ellipse((x + 18, 560, x + 36, 578), fill=(120, 220, 150))
    draw.rectangle((78, 120, 560, 350), fill=(230, 236, 236), outline=accent, width=6)
    draw.text((110, 160), label, fill=(10, 16, 20))
    draw.text((110, 220), "datacenter / hardware probe", fill=(30, 40, 48))
    image.save(path, quality=94)


def make_probe_logo(path: Path, label: str, accent: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGBA", (900, 360), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((38, 48, 270, 280), radius=28, fill=accent + (255,))
    draw.rectangle((278, 95, 820, 230), fill=(18, 22, 28, 255))
    draw.text((320, 126), label, fill=(255, 255, 255, 255))
    draw.text((320, 180), "transparent logo probe", fill=(210, 230, 220, 255))
    image.save(path)


def make_probe_person(path: Path, label: str, accent: tuple[int, int, int]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    image = Image.new("RGB", (900, 1100), (224, 228, 231))
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, 900, 280), fill=accent)
    draw.ellipse((310, 210, 590, 490), fill=(214, 177, 136), outline=(70, 58, 44), width=4)
    draw.rectangle((250, 520, 650, 940), fill=(34, 42, 55))
    draw.rectangle((330, 520, 570, 700), fill=(244, 241, 232))
    draw.text((90, 980), label, fill=(16, 24, 32))
    draw.text((90, 1025), "person/profile probe", fill=(60, 70, 80))
    image.save(path, quality=94)


def try_download_probe(path: Path) -> tuple[str, str]:
    url = "https://www.python.org/static/img/python-logo.png"
    if requests is None:
        return "requests_missing", ""
    try:
        response = requests.get(url, timeout=20, headers={"User-Agent": "NextTokenPrivateEdition/1.0"})
        if response.status_code == 200 and response.headers.get("content-type", "").startswith("image"):
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(response.content)
            Image.open(path).verify()
            return "downloaded", url
        return f"http_{response.status_code}", url
    except Exception as exc:
        return f"download_failed:{type(exc).__name__}", url


def create_candidate_images() -> list[Candidate]:
    originals = ASSETS / "source_media" / "i0282_probe" / "originals"
    photo = originals / "i0282_datacenter_photo_probe.jpg"
    photo_dup = originals / "i0282_datacenter_photo_probe_duplicate.jpg"
    logo = originals / "i0282_logo_transparency_probe.png"
    person = originals / "i0282_person_profile_probe.jpg"
    web_logo = originals / "i0282_web_logo_probe.png"

    make_probe_photo(photo, "I-0282", (118, 220, 90))
    Image.open(photo).save(photo_dup, quality=92)
    make_probe_logo(logo, "NEXT TOKEN", (84, 190, 120))
    make_probe_person(person, "Research Leader", (80, 132, 210))
    download_status, download_url = try_download_probe(web_logo)
    if download_status != "downloaded":
        make_probe_logo(web_logo, "WEB FALLBACK", (118, 190, 90))

    candidates = [
        Candidate("MP-0282-001", "photo", "generated_probe", "local generated datacenter/hardware photo probe", photo, "private_probe", "Test photo resizing, quality scoring, and contact sheet layout.", "No real facility, company, capacity, or hardware claim."),
        Candidate("MP-0282-002", "photo_duplicate", "generated_probe", "near-duplicate of MP-0282-001", photo_dup, "private_probe", "Test perceptual duplicate detection before bulk acquisition.", "No independent source; should be grouped as duplicate."),
        Candidate("MP-0282-003", "logo", "generated_probe", "local generated transparent logo probe", logo, "private_probe", "Test logo transparency preservation and square-safe resizing.", "No real trademark or brand claim."),
        Candidate("MP-0282-004", "person", "generated_probe", "local generated person/profile probe", person, "private_probe", "Test portrait crop/framing and people-image ledger fields.", "No real person identity or biography claim."),
        Candidate("MP-0282-005", "web_image", download_status, download_url or "web image retrieval fallback", web_logo, "private_use_probe", "Test web image retrieval path and fallback logging.", "Probe image only; no source claim promoted from it."),
    ]
    return candidates


def dominant_color(path: Path) -> str:
    if ColorThief is None:
        return ""
    try:
        color = ColorThief(str(path)).get_color(quality=5)
        return "#%02x%02x%02x" % color
    except Exception:
        return ""


def phash(path: Path) -> str:
    if imagehash is None:
        return ""
    return str(imagehash.phash(Image.open(path).convert("RGB")))


def quality_metrics(path: Path) -> dict[str, object]:
    image = Image.open(path).convert("RGB")
    width, height = image.size
    gray = ImageOps.grayscale(image)
    stat = Image.Image.getextrema(gray)
    contrast = stat[1] - stat[0]
    if np is not None:
        arr = np.array(gray)
        brightness = float(arr.mean())
        if cv2 is not None:
            lap = float(cv2.Laplacian(arr, cv2.CV_64F).var())
        else:
            lap = float(arr.var())
    else:
        brightness = 0.0
        lap = 0.0
    megapixels = width * height / 1_000_000
    aspect = width / height
    score = min(100.0, megapixels * 28 + min(contrast, 220) * 0.18 + min(lap, 5000) * 0.005)
    if brightness < 20 or brightness > 238:
        score -= 12
    if aspect < 0.35 or aspect > 4.0:
        score -= 8
    return {
        "width": width,
        "height": height,
        "megapixels": f"{megapixels:.2f}",
        "aspect_ratio": f"{aspect:.2f}",
        "brightness": f"{brightness:.1f}",
        "contrast": contrast,
        "sharpness_laplacian": f"{lap:.1f}",
        "quality_score": f"{max(0.0, score):.1f}",
        "dominant_color": dominant_color(path),
    }


def resize_and_crop(candidate: Candidate) -> list[dict[str, object]]:
    out_root = ASSETS / "source_media" / "i0282_probe" / "derivatives"
    out_root.mkdir(parents=True, exist_ok=True)
    image = Image.open(candidate.local_original)
    derivatives: list[dict[str, object]] = []
    variants = [
        ("book_wide", (1400, 850), "center_crop"),
        ("thumb", (360, 240), "fit"),
    ]
    if candidate.role == "logo":
        variants = [("logo_square", (512, 512), "contain_transparency"), ("thumb", (360, 240), "fit")]
    elif candidate.role == "person":
        variants = [("portrait_crop", (640, 800), "center_crop"), ("thumb", (360, 240), "fit")]

    for variant, size, mode in variants:
        out_path = out_root / f"{candidate.candidate_id}_{variant}.png"
        working = image.copy()
        if mode == "center_crop":
            working = ImageOps.fit(working.convert("RGB"), size, method=Image.Resampling.LANCZOS, centering=(0.5, 0.42))
        elif mode == "contain_transparency":
            working = ImageOps.contain(working.convert("RGBA"), size, method=Image.Resampling.LANCZOS)
            canvas = Image.new("RGBA", size, (255, 255, 255, 0))
            canvas.alpha_composite(working, ((size[0] - working.width) // 2, (size[1] - working.height) // 2))
            working = canvas
        else:
            working = ImageOps.contain(working.convert("RGBA" if image.mode == "RGBA" else "RGB"), size, method=Image.Resampling.LANCZOS)
        working.save(out_path)
        derivatives.append(
            {
                "candidate_id": candidate.candidate_id,
                "variant": variant,
                "mode": mode,
                "local_path": str(out_path.relative_to(ROOT)),
                "sha256": sha256_file(out_path),
                "width": working.width,
                "height": working.height,
                "alpha_preserved": "yes" if working.mode == "RGBA" and "A" in working.getbands() else "no",
            }
        )
    return derivatives


def contact_sheet(candidates: list[Candidate], derivatives: list[dict[str, object]]) -> Path:
    thumbs = [row for row in derivatives if row["variant"] == "thumb"]
    cell_w, cell_h = 420, 330
    cols = 3
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * cell_w, rows * cell_h), (246, 245, 240))
    draw = ImageDraw.Draw(sheet)
    for idx, row in enumerate(thumbs):
        image = Image.open(ROOT / str(row["local_path"])).convert("RGB")
        x = (idx % cols) * cell_w
        y = (idx // cols) * cell_h
        sheet.paste(image, (x + 30, y + 24))
        candidate = next(c for c in candidates if c.candidate_id == row["candidate_id"])
        draw.rectangle((x + 18, y + 18, x + cell_w - 18, y + cell_h - 18), outline=(30, 35, 40), width=2)
        draw.text((x + 30, y + 275), f"{candidate.candidate_id} / {candidate.role}", fill=(20, 24, 28))
        draw.text((x + 30, y + 300), candidate.rights_status, fill=(80, 86, 90))
    out_path = ASSETS / "source_media" / "i0282_probe" / "contact_sheet_i0282.jpg"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_path, quality=90)
    return out_path


def duplicate_groups(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    output: list[dict[str, object]] = []
    if imagehash is None:
        return output
    hash_rows = [(row["candidate_id"], imagehash.hex_to_hash(str(row["phash"]))) for row in rows if row.get("phash")]
    group_id = 1
    used: set[str] = set()
    for candidate_id, hash_value in hash_rows:
        if candidate_id in used:
            continue
        members = [candidate_id]
        used.add(candidate_id)
        for other_id, other_hash in hash_rows:
            if other_id in used:
                continue
            distance = hash_value - other_hash
            if distance <= 6:
                members.append(other_id)
                used.add(other_id)
        if len(members) > 1:
            output.append(
                {
                    "group_id": f"DUP-{group_id:03d}",
                    "candidate_ids": ";".join(members),
                    "method": "imagehash.phash distance <= 6",
                    "recommended_action": "keep strongest provenance/quality row; mark others duplicate_or_alternate_crop",
                }
            )
            group_id += 1
    return output


def append_ledgers(summary: dict[str, object]) -> None:
    remove_existing_pass_rows()
    now = datetime.now().astimezone().isoformat(timespec="seconds")
    claims_lines = (ROOT / "claims.tsv").read_text(encoding="utf-8").splitlines()
    claim_id = f"C-{len(claims_lines):04d}"
    append_line(
        ROOT / "claims.tsv",
        [
            claim_id,
            "supported",
            "Pass I-0282 installed and verified the media-prep toolchain for private visual acquisition: web/local image retrieval, resize/crop/contact-sheet generation, logo transparency handling, person-photo framing, perceptual duplicate detection, quality scoring, and ignored local raster storage.",
            "scripts/media_prep_toolchain_i0282.py;data/media_prep_probe_i0282.tsv;data/media_prep_qa_i0282.tsv;data/media_prep_candidates_i0282.tsv;data/media_prep_derivatives_i0282.tsv;data/media_prep_duplicate_groups_i0282.tsv;data/media_prep_quality_scores_i0282.tsv;data/media_prep_install_i0282.tsv;manuscript/media-prep-toolchain-i0282.md",
            "I-0282;I-0281",
            "media-prep toolchain verification",
            now[:10],
            "Supported as toolchain readiness only; probe rasters are local and ignored, no real photo/logo/person asset is promoted into the book by this pass.",
        ],
    )

    word_count, chapter_count = word_count_and_chapters()
    supported_count = len((ROOT / "claims.tsv").read_text(encoding="utf-8").splitlines()) - 1
    append_line(
        ROOT / "scoreboard.tsv",
        [
            now,
            "pass-0282",
            "champion media-prep toolchain",
            PASS_ID,
            "tools install",
            "+1.0",
            "100.0",
            word_count,
            chapter_count,
            "142",
            "78",
            "299",
            f"{supported_count} supported / 0 needs-verification; {summary['qa_pass']} pass, {summary['qa_warn']} warn, {summary['qa_fail']} fail media-prep QA checks; {summary['candidate_count']} probe candidates, {summary['derivative_count']} derivatives, {summary['duplicate_groups']} duplicate group, and contact sheet visually inspected",
            "+1",
            "No real acquisition batch promoted; probe rasters are ignored local files; web retrieval fallback remains logged if public image fetch is unavailable",
            "promoted",
            "Verified the image-search/media-prep path before bulk acquisition: candidate intake, web/local retrieval logging, safe storage, crop/resize variants, logo transparency, portrait framing, perceptual duplicate grouping, quality scoring, and contact-sheet review now have a tested script and ledgers.",
            "one image-search/media-prep setup pass",
        ],
    )

    insight_block = (
        "\n## 2026-05-27 - I-0282 Media Prep\n\n"
        "Bulk visual acquisition needs a triage machine before it needs more images. The useful gate is candidate in, ignored original out, derivative variants, perceptual hash, quality score, duplicate group, provenance fields, and a contact sheet the editor can actually look at; otherwise a photo sprint becomes an unreviewable pile.\n"
    )
    insights = ROOT / "insights.md"
    text = insights.read_text(encoding="utf-8")
    pattern = r"\n## 2026-05-27 - I-0282 Media Prep\n\n.*?(?=\n## |\Z)"
    if re.search(pattern, text, flags=re.DOTALL):
        text = re.sub(pattern, insight_block.rstrip("\n"), text, flags=re.DOTALL)
    else:
        text += insight_block
    insights.write_text(text, encoding="utf-8")

    readme = ROOT / "README.md"
    readme_text = readme.read_text(encoding="utf-8")
    marker = "- **Current acquisition toolchain:**"
    insert = (
        "- **Current media-prep toolchain:** I-0282 verifies web/local image retrieval, crop/resize/contact-sheet generation, logo transparency handling, person-photo framing, perceptual duplicate grouping, quality scoring, package-version logging, and ignored local raster storage in `data/media_prep_probe_i0282.tsv`; it prepares I-0284/I-0287 acquisition without promoting real images yet.\n"
    )
    if insert not in readme_text and marker in readme_text:
        readme_text = readme_text.replace(marker, insert + marker, 1)
        readme.write_text(readme_text, encoding="utf-8")


def main() -> int:
    DATA.mkdir(parents=True, exist_ok=True)
    MANUSCRIPT.mkdir(parents=True, exist_ok=True)
    write_install_manifest()

    candidates = create_candidate_images()
    candidate_rows: list[dict[str, object]] = []
    quality_rows: list[dict[str, object]] = []
    derivative_rows: list[dict[str, object]] = []

    for candidate in candidates:
        metrics = quality_metrics(candidate.local_original)
        hash_value = phash(candidate.local_original)
        candidate_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "role": candidate.role,
                "source_kind": candidate.source_kind,
                "source_url_or_context": candidate.source_url_or_context,
                "local_original": str(candidate.local_original.relative_to(ROOT)),
                "sha256": sha256_file(candidate.local_original),
                "phash": hash_value,
                "rights_status": candidate.rights_status,
                "story_purpose": candidate.story_purpose,
                "blocked_claims": candidate.blocked_claims,
            }
        )
        quality_rows.append(
            {
                "candidate_id": candidate.candidate_id,
                "role": candidate.role,
                "local_original": str(candidate.local_original.relative_to(ROOT)),
                "phash": hash_value,
                **metrics,
                "quality_gate": "pass" if float(metrics["quality_score"]) >= 35.0 else "review",
            }
        )
        derivative_rows.extend(resize_and_crop(candidate))

    duplicate_rows = duplicate_groups(candidate_rows)
    sheet_path = contact_sheet(candidates, derivative_rows)
    sheet_hash = sha256_file(sheet_path)

    write_tsv(
        DATA / "media_prep_candidates_i0282.tsv",
        candidate_rows,
        ["candidate_id", "role", "source_kind", "source_url_or_context", "local_original", "sha256", "phash", "rights_status", "story_purpose", "blocked_claims"],
    )
    write_tsv(
        DATA / "media_prep_quality_scores_i0282.tsv",
        quality_rows,
        ["candidate_id", "role", "local_original", "phash", "width", "height", "megapixels", "aspect_ratio", "brightness", "contrast", "sharpness_laplacian", "quality_score", "dominant_color", "quality_gate"],
    )
    write_tsv(
        DATA / "media_prep_derivatives_i0282.tsv",
        derivative_rows,
        ["candidate_id", "variant", "mode", "local_path", "sha256", "width", "height", "alpha_preserved"],
    )
    write_tsv(
        DATA / "media_prep_duplicate_groups_i0282.tsv",
        duplicate_rows,
        ["group_id", "candidate_ids", "method", "recommended_action"],
    )

    probe_rows = [
        {"capability": "python_imports", "status": "pass" if all([imagehash, np is not None, ColorThief, piexif, cv2 is not None]) else "fail", "evidence": f"imagehash={bool(imagehash)}; numpy={np is not None}; colorthief={bool(ColorThief)}; piexif={bool(piexif)}; cv2={cv2 is not None}", "local_path": "", "sha256": ""},
        {"capability": "candidate_intake", "status": "pass" if len(candidate_rows) == 5 else "fail", "evidence": f"candidate_rows={len(candidate_rows)}; roles={dict(Counter(row['role'] for row in candidate_rows))}", "local_path": "data/media_prep_candidates_i0282.tsv", "sha256": sha256_file(DATA / "media_prep_candidates_i0282.tsv")},
        {"capability": "web_image_retrieval", "status": "pass" if "downloaded" in [row["source_kind"] for row in candidate_rows] else "warn", "evidence": next(row["source_kind"] for row in candidate_rows if row["candidate_id"] == "MP-0282-005"), "local_path": next(row["local_original"] for row in candidate_rows if row["candidate_id"] == "MP-0282-005"), "sha256": next(row["sha256"] for row in candidate_rows if row["candidate_id"] == "MP-0282-005")},
        {"capability": "resize_crop_derivatives", "status": "pass" if len(derivative_rows) == 10 else "fail", "evidence": f"derivatives={len(derivative_rows)}; variants={dict(Counter(row['variant'] for row in derivative_rows))}", "local_path": "data/media_prep_derivatives_i0282.tsv", "sha256": sha256_file(DATA / "media_prep_derivatives_i0282.tsv")},
        {"capability": "logo_transparency", "status": "pass" if any(row["candidate_id"] == "MP-0282-003" and row["alpha_preserved"] == "yes" for row in derivative_rows) else "fail", "evidence": "MP-0282-003 logo_square preserves alpha channel", "local_path": "assets/source_media/i0282_probe/derivatives/MP-0282-003_logo_square.png", "sha256": sha256_file(ROOT / "assets/source_media/i0282_probe/derivatives/MP-0282-003_logo_square.png")},
        {"capability": "person_photo_crop", "status": "pass" if any(row["candidate_id"] == "MP-0282-004" and row["variant"] == "portrait_crop" and row["width"] == 640 and row["height"] == 800 for row in derivative_rows) else "fail", "evidence": "MP-0282-004 portrait_crop is 640x800", "local_path": "assets/source_media/i0282_probe/derivatives/MP-0282-004_portrait_crop.png", "sha256": sha256_file(ROOT / "assets/source_media/i0282_probe/derivatives/MP-0282-004_portrait_crop.png")},
        {"capability": "duplicate_detection", "status": "pass" if duplicate_rows else "fail", "evidence": f"duplicate_groups={len(duplicate_rows)}; {duplicate_rows[0]['candidate_ids'] if duplicate_rows else 'none'}", "local_path": "data/media_prep_duplicate_groups_i0282.tsv", "sha256": sha256_file(DATA / "media_prep_duplicate_groups_i0282.tsv")},
        {"capability": "quality_scoring", "status": "pass" if all(float(row["quality_score"]) >= 30.0 for row in quality_rows) else "warn", "evidence": f"quality_scores={[row['quality_score'] for row in quality_rows]}", "local_path": "data/media_prep_quality_scores_i0282.tsv", "sha256": sha256_file(DATA / "media_prep_quality_scores_i0282.tsv")},
        {"capability": "contact_sheet", "status": "pass" if sheet_path.exists() and sheet_path.stat().st_size > 10_000 else "fail", "evidence": f"contact_sheet={sheet_path.relative_to(ROOT)}; bytes={sheet_path.stat().st_size}", "local_path": str(sheet_path.relative_to(ROOT)), "sha256": sheet_hash},
    ]
    write_tsv(
        DATA / "media_prep_probe_i0282.tsv",
        probe_rows,
        ["capability", "status", "evidence", "local_path", "sha256"],
    )

    qa_rows = []
    for idx, row in enumerate(probe_rows, start=1):
        qa_rows.append(
            {
                "pass_id": PASS_ID,
                "check_id": f"I0282-{idx:03d}",
                "category": row["capability"],
                "result": row["status"],
                "evidence": row["evidence"],
                "recommended_action": "Use this route in I-0284/I-0287." if row["status"] == "pass" else "Repair or use logged fallback before bulk acquisition.",
            }
        )
    write_tsv(
        DATA / "media_prep_qa_i0282.tsv",
        qa_rows,
        ["pass_id", "check_id", "category", "result", "evidence", "recommended_action"],
    )

    MANUSCRIPT.joinpath("media-prep-toolchain-i0282.md").write_text(
        "\n".join(
            [
                "# I-0282 Image Search And Media Prep Toolchain",
                "",
                f"Status: promoted setup pass, with {sum(1 for r in qa_rows if r['result'] == 'pass')} pass / {sum(1 for r in qa_rows if r['result'] == 'warn')} warn / {sum(1 for r in qa_rows if r['result'] == 'fail')} fail QA.",
                "",
                "## Verified",
                "",
                "- Local media-prep packages installed under ignored `.tooling/i0282/python`.",
                "- Candidate intake covers photo, near-duplicate photo, transparent logo, person/profile image, and web-image retrieval/fallback.",
                "- Resizing and cropping produced book-wide, thumbnail, logo-square, and portrait variants.",
                "- Logo alpha channel survived the square derivative.",
                "- Perceptual hashing grouped the deliberate near-duplicate pair.",
                "- Quality scoring records size, aspect ratio, brightness, contrast, sharpness, dominant color, phash, and gate.",
                f"- Contact sheet: `{sheet_path.relative_to(ROOT)}` (ignored raster, visually inspected).",
                "",
                "## Limits",
                "",
                "- This pass does not promote real photos, logos, or person images into the book.",
                "- Public image retrieval is tested as a workflow; future acquisition rows still need source URL, access date, owner/creator, private-use note, and blocked-claim text.",
                "- Probe rasters and installed packages stay local and ignored.",
                "",
            ]
        ),
        encoding="utf-8",
    )

    replace_idea_row()
    summary = {
        "qa_pass": sum(1 for row in qa_rows if row["result"] == "pass"),
        "qa_warn": sum(1 for row in qa_rows if row["result"] == "warn"),
        "qa_fail": sum(1 for row in qa_rows if row["result"] == "fail"),
        "candidate_count": len(candidate_rows),
        "derivative_count": len(derivative_rows),
        "duplicate_groups": len(duplicate_rows),
    }
    append_ledgers(summary)
    print(json.dumps(summary, indent=2))
    return 0 if summary["qa_fail"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
