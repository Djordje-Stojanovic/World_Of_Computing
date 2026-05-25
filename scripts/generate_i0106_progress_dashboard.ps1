$ErrorActionPreference = 'Stop'

$chapters = @(
  [pscustomobject]@{chapter=1; title='The Shock'; file=''; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=2; title='Before the Transformer'; file='manuscript/01-before-the-transformer.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=3; title='Attention Catches Fire'; file='manuscript/02-attention-catches-fire.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=4; title='The Scaling Bet'; file='manuscript/03-scaling-bet.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=5; title='GPT-1 to GPT-3: The Door Opens'; file='manuscript/05-gpt-1-to-gpt-3-door-opens.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=6; title='Alignment Enters the Product'; file='manuscript/06-alignment-enters-product.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=7; title='ChatGPT: The Interface Event'; file='manuscript/07-chatgpt-interface-event.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=8; title='Microsoft, OpenAI, and the Cloud Bargain'; file=''; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=9; title='Google and DeepMind Wake the Sleeping Giant'; file=''; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=10; title='Meta, Llama, and the Open-Weight Shock'; file='manuscript/10-meta-llama-open-weight-shock.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=11; title='The Chinese Frontier'; file='manuscript/11-chinese-frontier-open-models.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=12; title='Europe, xAI, and the Rest of the Frontier'; file=''; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=13; title='Benchmarks, Arenas, and the Mirage of Rank'; file='manuscript/13-model-rankings-appendix.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=14; title='NVIDIA and CUDA: The Moat Under the Moat'; file=''; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=15; title='GTC 2026: The AI Factory Sells Itself'; file='manuscript/15-gtc-2026-ai-factory-sells-itself.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=16; title='Datacenters, Power, and the Physical Internet'; file='manuscript/16-speed-to-power.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=17; title='Data, Tokens, and the Library Problem'; file=''; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=18; title='Tools, Retrieval, and the Agent Turn'; file=''; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=19; title='Code as the Second Native Language'; file=''; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=20; title='Claude Code and the Industrialization of Pair Programming'; file='manuscript/20-claude-code-industrialized-pair-programming.md'; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=21; title='Reasoning, Test-Time Compute, and the New Scaling Axis'; file=''; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=22; title='The Economics of Intelligence on Tap'; file=''; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=23; title='Failure Modes, Truth, and Trust'; file=''; target_min=4200; target_max=4800},
  [pscustomobject]@{chapter=24; title='Next Token'; file=''; target_min=4200; target_max=4800}
)

$assets = Import-Csv assets_manifest.tsv -Delimiter "`t"
$claims = Import-Csv claims.tsv -Delimiter "`t"

$rows = foreach ($c in $chapters) {
  $exists = $c.file -and (Test-Path $c.file)
  $text = if ($exists) { Get-Content -Raw $c.file } else { '' }
  $words = if ($exists) { ($text | Measure-Object -Word).Words } else { 0 }
  $cuePattern = '(?<![A-Z0-9])(?:S|C|A|SNAP|N[0-9]+|CH[0-9]+Q)-[0-9]{1,12}'
  $sourceCues = if ($exists) { [regex]::Matches($text, $cuePattern).Count } else { 0 }
  $sourceDensity = if ($sourceCues -gt 0) { [math]::Round($words / $sourceCues, 1) } else { '' }
  $usedIn = if ($exists) { @($assets | Where-Object { $_.used_in -like "*$($c.file)*" }) } else { @() }
  $visuals = @($usedIn | Where-Object { $_.asset_type -match 'svg|diagram|chart|card|map|schematic|visual' }).Count
  $photos = @($usedIn | Where-Object { $_.asset_type -match 'photo|screenshot|png|render|extracted_slide' }).Count
  $claimRows = if ($exists) { @($claims | Where-Object { $_.location -like "*$($c.file)*" }).Count } else { 0 }
  $blockers = if ($exists) { @($claims | Where-Object { $_.location -like "*$($c.file)*" -and $_.status -ne 'supported' }).Count } else { 0 }
  $wordGap = [math]::Max(0, $c.target_min - $words)
  $sourceState = if (-not $exists) { 'missing draft' } elseif ($sourceCues -eq 0) { 'no inline cues' } elseif ($sourceDensity -ge 150 -and $sourceDensity -le 250) { 'target band' } elseif ($sourceDensity -lt 150) { 'dense/possibly cluttered' } else { 'sparse' }
  $nextAction = if (-not $exists) { 'draft chapter + capture sources' } elseif ($words -lt 3000) { 'expand to full chapter' } elseif (($visuals + $photos) -lt 3) { 'add visual/photo package' } elseif ($sourceDensity -gt 250) { 'add/normalize sources' } elseif ($blockers -gt 0) { 'retire blockers' } else { 'continuity/prose polish' }
  $completion = [math]::Round((([math]::Min($words, $c.target_min) / $c.target_min) * 0.55 + ([math]::Min(($visuals + $photos), 3) / 3) * 0.20 + $(if ($sourceCues -gt 0) { 1 } else { 0 }) * 0.15 + $(if ($claimRows -gt 0) { 1 } else { 0 }) * 0.10) * 100, 0)

  [pscustomobject]@{
    chapter=$c.chapter
    title=$c.title
    status=$(if ($exists) { 'drafted' } else { 'missing' })
    file=$(if ($exists) { $c.file } else { 'missing' })
    words=$words
    target_min=$c.target_min
    word_gap=$wordGap
    source_cues=$sourceCues
    words_per_cue=$sourceDensity
    source_state=$sourceState
    visuals=$visuals
    photos_or_screens=$photos
    claim_rows=$claimRows
    open_blocker_rows=$blockers
    weighted_chapter_percent=$completion
    next_action=$nextAction
  }
}

$rows | ConvertTo-Csv -Delimiter "`t" -NoTypeInformation | ForEach-Object { $_ -replace '"', '' } | Set-Content data/full_book_progress_dashboard_i0106.tsv -Encoding UTF8

$totalWords = ($rows | Measure-Object words -Sum).Sum
$scoreRows = Import-Csv scoreboard.tsv -Delimiter "`t" -Header timestamp,pass_id,parent,idea_id,category,delta_score,bookscore,word_count,chapter_count,chart_count,photo_count,source_count,claim_coverage,novelty,open_blockers,verdict,reason,scope
$latestLedgerWords = [int](($scoreRows | Where-Object { $_.word_count -match '^[0-9]+$' } | Select-Object -Last 1).word_count)
$drafted = @($rows | Where-Object status -eq 'drafted').Count
$missing = 24 - $drafted
$totalVisuals = @($assets | Where-Object { $_.asset_type -match 'svg|diagram|chart|card|map|schematic|visual|render|screenshot|photo|png|extracted_slide' }).Count
$totalPhotoSlots = @($assets | Where-Object { $_.asset_type -match 'photo|screenshot|png|render|extracted_slide' }).Count
$supportedClaims = @($claims | Where-Object status -eq 'supported').Count
$needClaims = @($claims | Where-Object status -ne 'supported').Count
$wordPct = [math]::Round(($totalWords / 100000) * 100, 1)
$chapterPct = [math]::Round(($drafted / 24) * 100, 1)
$visualPct = [math]::Round(($totalVisuals / 80) * 100, 1)
$photoPct = [math]::Round(($totalPhotoSlots / 50) * 100, 1)
$claimPct = [math]::Round(($supportedClaims / ($supportedClaims + $needClaims)) * 100, 1)
$publishable = [math]::Round(($wordPct * 0.22 + $chapterPct * 0.22 + [math]::Min($visualPct, 100) * 0.16 + [math]::Min($photoPct, 100) * 0.12 + $claimPct * 0.18 + 55 * 0.10), 0)
$bestseller = [math]::Round($publishable * 0.72, 0)

$constraints = @(
  [pscustomobject]@{metric='ledger_total_words'; current=$latestLedgerWords; target='100000-120000'; percent_to_minimum=[math]::Round(($latestLedgerWords / 100000) * 100, 1); gap=[math]::Max(0, 100000 - $latestLedgerWords); note='scoreboard total includes chapter drafts plus useful sidecar/spine manuscript work'},
  [pscustomobject]@{metric='words_to_minimum'; current=$totalWords; target='100000-120000'; percent_to_minimum=$wordPct; gap=[math]::Max(0, 100000 - $totalWords); note='mapped main-draft word count; does not count sidecar audits or outline prose'},
  [pscustomobject]@{metric='drafted_main_chapters'; current=$drafted; target='24 exactly'; percent_to_minimum=$chapterPct; gap=$missing; note='chapter shells with substantial mapped manuscript files'},
  [pscustomobject]@{metric='charts_diagrams_visuals'; current=$totalVisuals; target='80-100'; percent_to_minimum=$visualPct; gap=[math]::Max(0, 80 - $totalVisuals); note='all manifest visual-like assets; many are source/claim cards, not final art'},
  [pscustomobject]@{metric='photos_screenshots_slots'; current=$totalPhotoSlots; target='50-60'; percent_to_minimum=$photoPct; gap=[math]::Max(0, 50 - $totalPhotoSlots); note='major weak spot; current photo-like slots are mostly GTC slide renders'},
  [pscustomobject]@{metric='claim_rows_supported'; current=$supportedClaims; target='zero unsupported before done-enough'; percent_to_minimum=$claimPct; gap=$needClaims; note='unsupported rows still active; new prose must not raise this debt'}
)
$constraints | ConvertTo-Csv -Delimiter "`t" -NoTypeInformation | ForEach-Object { $_ -replace '"', '' } | Set-Content data/full_book_constraint_gaps_i0106.tsv -Encoding UTF8

$weak = $rows | Sort-Object @{Expression='weighted_chapter_percent';Ascending=$true}, @{Expression='chapter';Ascending=$true} | Select-Object -First 10
$md = [System.Collections.Generic.List[string]]::new()
$md.Add('# Full-Book Progress Dashboard')
$md.Add('')
$md.Add('Status pass: I-0106, generated 2026-05-25 from manuscript files, ledgers, and asset manifest.')
$md.Add('')
$md.Add('## Executive Read')
$md.Add('')
$md.Add("- Minimum-word progress: $wordPct% ($totalWords / 100,000 words; gap $([math]::Max(0, 100000 - $totalWords))).")
$md.Add("- Total loop-ledger words: $([math]::Round(($latestLedgerWords / 100000) * 100, 1))% ($latestLedgerWords / 100,000 words), but not all of that is cleanly placed in the 24-chapter spine yet.")
$md.Add("- Drafted-chapter progress: $chapterPct% ($drafted / 24 substantial chapter drafts; $missing missing).")
$md.Add("- Visual progress: $visualPct% ($totalVisuals / 80 visual-like manifest assets; gap $([math]::Max(0, 80 - $totalVisuals))).")
$md.Add("- Photo/screenshot progress: $photoPct% ($totalPhotoSlots / 50 photo-like slots; gap $([math]::Max(0, 50 - $totalPhotoSlots))).")
$md.Add("- Claim-ledger support: $claimPct% ($supportedClaims supported / $needClaims open or needs-verification rows).")
$md.Add('')
$md.Add("Working estimate: about $publishable% of the way to a publishable, professionally serious book; about $bestseller% of the way to the much harder Chip War / Thinking Machine / Isaacson-class commercial-awards target. The gap is not only volume. It is missing chapters, broader visual/photo reporting, and whole-book narrative continuity.")
$md.Add('')
$md.Add('## Weakest Chapter Targets')
$md.Add('')
$md.Add('| Rank | Ch. | Chapter | Status | Words | Visuals | Photos | Source state | Weighted % | Next action |')
$md.Add('|---:|---:|---|---|---:|---:|---:|---|---:|---|')
$rank = 1
foreach ($w in $weak) {
  $md.Add("| $rank | $($w.chapter) | $($w.title) | $($w.status) | $($w.words) | $($w.visuals) | $($w.photos_or_screens) | $($w.source_state) | $($w.weighted_chapter_percent)% | $($w.next_action) |")
  $rank++
}
$md.Add('')
$md.Add('## Immediate Steering')
$md.Add('')
$md.Add("- The book is no longer just an outline: the loop ledger has $latestLedgerWords committed words, while $totalWords words are already cleanly mapped into planned main chapters.")
$md.Add('- It is not close to award-ready yet: twelve mapped main chapters are still missing substantial drafts, the photo/screenshot layer is severely underbuilt, and the current visual set is too dependent on diagrams and NVIDIA/GTC-derived material.')
$md.Add('- The highest-return next moves are full chapter drafts for the missing Microsoft/OpenAI, Google/DeepMind, Europe/xAI/Mistral, data/tokens, tools/RAG/agents, coding agents, reasoning, economics, failure/trust, and final synthesis chapters; in parallel, a non-NVIDIA source/photo/screenshot acquisition pass should diversify the asset base.')
$md.Add('')
$md.Add('## Files')
$md.Add('')
$md.Add('- `data/full_book_progress_dashboard_i0106.tsv` - chapter-level dashboard.')
$md.Add('- `data/full_book_constraint_gaps_i0106.tsv` - hard-constraint gap table.')
$md.Add('- Best current mini pre-taste for a reader: `manuscript/07-chatgpt-interface-event.md`, followed by `manuscript/15-gtc-2026-ai-factory-sells-itself.md` for the more visual industrial chapter voice.')
$md | Set-Content manuscript/00-full-book-progress-dashboard.md -Encoding UTF8
Copy-Item manuscript/00-full-book-progress-dashboard.md champion/00-full-book-progress-dashboard.md -Force

Write-Output "Generated I-0106 dashboard: $totalWords words, $drafted drafted chapters, $totalVisuals visuals, $totalPhotoSlots photo-like slots."
