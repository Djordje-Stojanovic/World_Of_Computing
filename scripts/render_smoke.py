from __future__ import annotations

import argparse
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path

import fitz


@dataclass(frozen=True)
class ImageSmokeSpec:
    path: Path
    label: str
    min_unique_colors: int = 8
    max_dark_ratio: float = 0.92
    min_mean_luma: float = 18.0
    min_colorfulness: float = 1.5


def smoke_rows(
    *,
    root: Path,
    prefix: str,
    text: str,
    required_text: list[str],
    image_specs: list[ImageSmokeSpec],
    artifacts: list[Path],
    max_unignored_bytes: int = 250_000,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    missing = [needle for needle in required_text if needle not in text]
    rows.append(
        {
            "check_id": f"{prefix}-TEXT",
            "evidence": f"required={len(required_text)}; missing={';'.join(missing) if missing else 'none'}",
            "result": "pass" if not missing else "fail",
            "notes": "Required guardrail strings survive PDF text extraction.",
        }
    )

    for spec in image_specs:
        stats = image_stats(spec.path)
        failed = []
        if stats["unique_colors"] < spec.min_unique_colors:
            failed.append("low_unique_colors")
        if stats["dark_ratio"] > spec.max_dark_ratio:
            failed.append("too_dark")
        if stats["mean_luma"] < spec.min_mean_luma:
            failed.append("low_mean_luma")
        if stats["colorfulness"] < spec.min_colorfulness:
            failed.append("low_colorfulness")
        rows.append(
            {
                "check_id": f"{prefix}-IMAGE-{spec.label}",
                "evidence": (
                    f"path={spec.path.as_posix()}; unique_colors={stats['unique_colors']}; "
                    f"dark_ratio={stats['dark_ratio']:.3f}; mean_luma={stats['mean_luma']:.1f}; "
                    f"colorfulness={stats['colorfulness']:.1f}"
                ),
                "result": "fail" if failed else "pass",
                "notes": "Image is rejected if it looks blank, near-black, monochrome, or missing expected figure colors."
                if not failed
                else f"Image smoke failure: {','.join(failed)}.",
            }
        )

    unignored = unignored_large_artifacts(root, artifacts, max_unignored_bytes)
    rows.append(
        {
            "check_id": f"{prefix}-ARTIFACTS",
            "evidence": f"max_unignored_bytes={max_unignored_bytes}; unignored_large={';'.join(unignored) if unignored else 'none'}",
            "result": "pass" if not unignored else "fail",
            "notes": "Rendered PDFs, PNGs, and text extracts must stay ignored when they are too large for source control.",
        }
    )
    return rows


def image_stats(path: Path) -> dict[str, float]:
    doc = fitz.open(path)
    page = doc[0]
    pix = page.get_pixmap(alpha=False)
    data = pix.samples
    stride = max(1, len(data) // (3 * 5000))
    colors: set[tuple[int, int, int]] = set()
    dark = 0
    luma_sum = 0.0
    color_sum = 0.0
    count = 0
    for idx in range(0, len(data), 3 * stride):
        if idx + 2 >= len(data):
            break
        r, g, b = data[idx], data[idx + 1], data[idx + 2]
        colors.add((r // 8, g // 8, b // 8))
        luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
        luma_sum += luma
        color_sum += abs(r - g) + abs(g - b) + abs(b - r)
        if luma < 24:
            dark += 1
        count += 1
    doc.close()
    if count == 0:
        return {"unique_colors": 0, "dark_ratio": 1.0, "mean_luma": 0.0, "colorfulness": 0.0}
    return {
        "unique_colors": float(len(colors)),
        "dark_ratio": dark / count,
        "mean_luma": luma_sum / count,
        "colorfulness": color_sum / count,
    }


def unignored_large_artifacts(root: Path, artifacts: list[Path], max_bytes: int) -> list[str]:
    large = [path for path in artifacts if path.exists() and path.stat().st_size > max_bytes]
    if not large:
        return []
    rels = [path.resolve().relative_to(root.resolve()).as_posix() for path in large]
    unignored: list[str] = []
    for rel in rels:
        proc = subprocess.run(
            ["git", "check-ignore", "-q", rel],
            cwd=root,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            unignored.append(rel)
    return unignored


def run_negative_self_test(root: Path) -> list[dict[str, str]]:
    with tempfile.TemporaryDirectory(prefix="render_smoke_negative_", dir=root) as tmp_name:
        tmp = Path(tmp_name)
        black_pdf = tmp / "black_page.pdf"
        large_artifact = tmp / "unignored-large.bin"

        doc = fitz.open()
        page = doc.new_page(width=72, height=72)
        page.draw_rect(page.rect, color=(0, 0, 0), fill=(0, 0, 0))
        doc.save(black_pdf)
        doc.close()

        large_artifact.write_bytes(b"x" * 64)

        return smoke_rows(
            root=root,
            prefix="NEGSMOKE",
            text="this text intentionally omits the required guardrail",
            required_text=["missing guardrail text"],
            image_specs=[
                ImageSmokeSpec(
                    black_pdf,
                    "BLACK",
                    min_unique_colors=2,
                    max_dark_ratio=0.5,
                    min_mean_luma=18.0,
                    min_colorfulness=0.1,
                )
            ],
            artifacts=[large_artifact],
            max_unignored_bytes=10,
        )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Render QA smoke helpers.")
    parser.add_argument(
        "--self-test-negative",
        action="store_true",
        help="Create temporary bad inputs and verify the smoke checks report failures.",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root for artifact checks.")
    args = parser.parse_args(argv)

    if not args.self_test_negative:
        parser.print_help()
        return 0

    rows = run_negative_self_test(args.root.resolve())
    for row in rows:
        print(f"{row['check_id']}\t{row['result']}\t{row['evidence']}\t{row['notes']}")

    expected_failures = {"NEGSMOKE-TEXT", "NEGSMOKE-IMAGE-BLACK", "NEGSMOKE-ARTIFACTS"}
    actual_failures = {row["check_id"] for row in rows if row["result"] == "fail"}
    missing = expected_failures - actual_failures
    if missing:
        print(f"negative self-test did not trigger expected failures: {','.join(sorted(missing))}", file=sys.stderr)
        return 1
    print("negative self-test passed: all expected failure classes were detected")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
