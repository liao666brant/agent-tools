#!/usr/bin/env python3
"""Tests for skill-doctor report rendering."""

import base64
import io
import json
import re
import tempfile
import unittest
import webbrowser
from contextlib import redirect_stdout
from pathlib import Path
from unittest.mock import patch

import render_report as renderer


class ReportRendererTests(unittest.TestCase):
    def render(self, title: str = "Agent 技能质量报告") -> str:
        return renderer.render_page({
            "title": title,
            "generated_at": "2026-08-25T08:00:00+08:00",
            "harness": "codex",
            "scores": {
                "efficiency": 0.75,
                "code_quality": 0.93,
                "skill_coverage": 0.74,
                "overall": 0.82,
            },
            "cta_url": "https://warp.dev/factories/request-access",
        })

    def test_code_diffs_follow_os_theme(self) -> None:
        bundle = renderer.embedded_diffs_script()

        self.assertTrue('themeType:"system"' in bundle)
        self.assertTrue(
            'theme:{dark:"pierre-dark",light:"pierre-light"}' in bundle,
        )

    def test_report_follows_os_theme_and_keeps_monospace_diffs(self) -> None:
        page = self.render().split("<script>", 1)[0]

        for contract in (
            '<meta name="color-scheme" content="light dark">',
            "@media (prefers-color-scheme: dark)",
            "--page-bg: #0f0d14",
            "background: var(--surface)",
            "--mono-font: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace",
            "--diffs-font-family: var(--mono-font)",
            "--diffs-header-font-family: var(--mono-font)",
        ):
            with self.subTest(contract=contract):
                self.assertTrue(contract in page, contract)

    def test_factories_footer_keeps_cta_with_sticky_position(self) -> None:
        page = self.render().split("<script>", 1)[0]

        self.assertTrue(".factories-footer { position: sticky; bottom: 16px;" in page)
        footer = re.search(
            r'<div class="stamp-row row factories-footer">(.*)', page, re.DOTALL,
        )
        self.assertIsNotNone(footer)
        if footer is not None:
            self.assertTrue('class="stamp-name"' in footer.group(1))
            self.assertTrue(
                'href="https://warp.dev/factories/request-access"' in footer.group(1),
            )

    def test_generated_timestamp_formats_utc_and_naive_values(self) -> None:
        cases = (
            ("2026-08-27T22:06:10.421941+00", "2026年8月27日 22:06 UTC"),
            ("2026-08-25T00:00:00Z", "2026年8月25日 00:00 UTC"),
            ("2026-08-25T08:00:00+08:00", "2026年8月25日 00:00 UTC"),
            ("2026-08-25T08:00:00", "2026年8月25日 08:00"),
            ("not-a-date", "not-a-date"),
            ("", ""),
            (None, ""),
        )

        for value, expected in cases:
            with self.subTest(value=value):
                self.assertEqual(renderer.format_generated_at(value), expected)

    def test_report_displays_formatted_timestamp(self) -> None:
        page = self.render().split("<script>", 1)[0]

        self.assertTrue("2026年8月25日 00:00 UTC" in page)
        self.assertFalse("2026-08-25T08:00:00+08:00" in page)

    def test_open_option_preserves_report_path(self) -> None:
        report_path = str(Path("report folder") / "report.json")

        args = renderer.parse_args([report_path, "--open"])

        self.assertEqual(args.report_path, report_path)
        self.assertTrue(args.open_browser)

    def test_browser_open_is_opt_in(self) -> None:
        args = renderer.parse_args([])

        self.assertEqual(args.report_path, "./skill-doctor-report/report.json")
        self.assertFalse(args.open_browser)

    def test_open_report_uses_default_browser_with_file_uri(self) -> None:
        report_path = Path("report folder") / "report.html"

        with patch("webbrowser.open", return_value=True) as browser_open:
            opened = renderer.open_report(report_path)

        self.assertTrue(opened)
        browser_open.assert_called_once_with(report_path.absolute().as_uri(), new=2)

    def test_open_report_returns_false_when_browser_cannot_open(self) -> None:
        for failure in (OSError("no browser"), webbrowser.Error("no browser")):
            with self.subTest(failure=type(failure).__name__):
                with patch("webbrowser.open", side_effect=failure):
                    self.assertFalse(renderer.open_report(Path("report.html")))

    def test_share_card_keeps_attribution_and_score_data(self) -> None:
        script = self.render().rsplit("<script>", 1)[1]
        encoded = re.search(r"var CARD = (.*);", script)
        self.assertIsNotNone(encoded)
        if encoded is not None:
            card = json.loads(encoded.group(1))
            self.assertEqual(card["eyebrow"], "skill-doctor")
            self.assertEqual(card["stamp"][1], "warp.dev/skill-doctor")
            self.assertIn("/skill-doctor", card["stamp"][0])
            self.assertEqual([value for _, value in card["bars"]], [75, 93, 74])
        self.assertTrue("text('# ' + CARD.eyebrow" in script)

    def test_metric_animation_preserves_values_and_reduced_motion(self) -> None:
        page = self.render().split("<script>", 1)[0]

        for contract in (
            "animation: skill-doctor-fill 700ms",
            "from { transform: scaleX(0); }",
            "to { transform: scaleX(1); }",
            "width:75%;--metric-delay:180ms",
            "width:93%;--metric-delay:290ms",
            "width:74%;--metric-delay:400ms",
            "@media (prefers-reduced-motion: reduce)",
            ".bar-fill { animation: none; }",
        ):
            with self.subTest(contract=contract):
                self.assertTrue(contract in page, contract)

    def test_report_preserves_cjk_mobile_layout(self) -> None:
        page = self.render()

        for contract in (
            '<html lang="zh-CN">',
            '<meta name="viewport" content="width=device-width, initial-scale=1">',
            "@media (max-width: 480px)",
            "Intl.Segmenter('zh-CN'",
            "document.querySelectorAll('.natural-wrap')",
        ):
            with self.subTest(contract=contract):
                self.assertTrue(contract in page, contract)

    def test_headings_use_natural_breaks_and_allow_flex_shrink(self) -> None:
        page = self.render("跨宿主技能质量与长中文标题换行验证报告").split("<script>", 1)[0]

        self.assertIn('<h1 class="natural-wrap">', page)
        self.assertEqual(page.count('<h2 class="natural-wrap">'), 2)
        self.assertRegex(page, r"\.title-row h1 \{[^}]*min-width: 0;")

    def test_footer_copy_uses_natural_breaks_inside_shrinkable_flex(self) -> None:
        page = self.render().split("<script>", 1)[0]

        self.assertRegex(page, r'<div class="stamp">.*?</svg><div class="natural-wrap">')
        self.assertRegex(page, r"\.stamp \{[^}]*min-width: 0;")
        self.assertRegex(page, r"\.stamp > div \{[^}]*min-width: 0;")

    def test_report_escapes_html_and_script_delimiters(self) -> None:
        title = "字符样例 </script> <b>标题</b> & \"引号\""

        page = self.render(title)

        self.assertTrue("&lt;/script&gt; &lt;b&gt;标题&lt;/b&gt;" in page)
        self.assertTrue("<\\/script>" in page)
        self.assertEqual(page.count("</script>"), 2)

    def test_diff_fallback_and_payload_preserve_original_content(self) -> None:
        diff = "--- a/SKILL.md\n+++ b/SKILL.md\n@@ -1 +1 @@\n-旧内容\n+字符 <示例> & 文本\n"

        rendered = renderer.render_diff(diff, 'proposed/<示例>".md')

        payload = re.search(r'data-diff="([^"]+)"', rendered)
        self.assertIsNotNone(payload)
        if payload is not None:
            self.assertEqual(base64.b64decode(payload.group(1)).decode("utf-8"), diff)
        self.assertIn("&lt;示例&gt; &amp; 文本", rendered)
        self.assertIn('data-filename="&lt;示例&gt;&quot;.md"', rendered)

    def test_main_writes_report_before_opening_browser(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            report_path = Path(temp_dir) / "report.json"
            report_path.write_text('{"scores": {"overall": 0.7}}', encoding="utf-8")
            output = io.StringIO()
            out_path = report_path.with_name("report.html")

            def open_existing_report(path: Path) -> bool:
                self.assertEqual(path, out_path)
                self.assertTrue(path.is_file())
                return True

            with redirect_stdout(output), patch.object(
                renderer, "open_report", side_effect=open_existing_report, create=True,
            ) as browser_open:
                renderer.main([str(report_path), "--open"])

            self.assertTrue(out_path.is_file())
            self.assertIn(out_path.absolute().as_uri(), output.getvalue())
            browser_open.assert_called_once_with(out_path)


if __name__ == "__main__":
    unittest.main()
