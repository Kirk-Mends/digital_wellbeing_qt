






# mac and windows version

# Changed the title color
class MonthlyReportGenerator:
    # Added title_color argument to match the Page's refresh call
    def generate(self, summary, last_summary=None, is_dark_mode=True, title_color="#1A1A1A"):
        if summary is None:
            return "No activity data available for this month."

        # 1. LINKED: t_primary now pulls directly from the QSS Title Color
        t_primary = title_color
        
        # 2. CONSTANT: These stay as the standard theme colors for readability
        t_secondary = "rgba(228, 231, 242, 0.5)" if is_dark_mode else "#64748B"
        accent = "#4DA3FF" if is_dark_mode else "#0057D9"
        
        # Formatting
        total_focus = f"{int(summary.get('total_focus', 0)):,}"
        fatigue = f"{float(summary.get('avg_fatigue', 0)):.1f}"
        
        # Trend Logic
        comparison_html = ""
        if last_summary:
            def get_change_ui(curr, prev):
                if prev == 0: return "—"
                val = ((curr - prev) / prev) * 100
                color = "#2ECC71" if val >= 0 else "#E74C3C"
                arrow = "↑" if val >= 0 else "↓"
                return f"<span style='color: {color}; font-weight: 700;'>{arrow} {abs(val):.1f}%</span>"

            comparison_html = f"""
            <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'};">
                <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px;">Trend vs Last Month</p>
                <div style="color: {t_primary}; font-size: 13px; font-weight: 600;">
                    Focus: {get_change_ui(summary.get('total_focus', 0), last_summary.get('total_focus', 0))} 
                    <span style="color: {t_secondary}; margin: 0 10px;">|</span> 
                    Fatigue: {get_change_ui(summary.get('avg_fatigue', 0), last_summary.get('avg_fatigue', 0))}
                </div>
            </div>
            """

        # Corrected font-family to include ".AppleSystemUIFont" for Mac speed
        return f"""
        <div style="font-family: '.AppleSystemUIFont', 'Segoe UI', system-ui, sans-serif; line-height: 1.2; padding-bottom: 40px;">
            <p style="color: {accent}; font-weight: 800; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">
                Monthly Report
            </p>

            <h1 style="color: {t_primary}; font-size: 32px; font-weight: 800; margin: 0 0 25px 0; letter-spacing: -1px;">
                Monthly Progress
            </h1>

            <div style="margin-bottom: 30px;">
                <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Total Monthly Focus</p>
                <div style="color: {accent}; font-size: 64px; font-weight: 800; line-height: 1;">
                    {total_focus} <span style="font-size: 20px; font-weight: 400; color: {t_secondary};">mins</span>
                </div>
            </div>

            <div style="display: flex; gap: 40px; margin-bottom: 30px;">
                <div>
                    <p style="color: {t_secondary}; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 2px;">Breaks</p>
                    <p style="color: {t_primary}; font-size: 22px; font-weight: 700; margin: 0;">{summary.get('breaks', 0)}</p>
                </div>
                <div>
                    <p style="color: {t_secondary}; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 2px;">Avg Fatigue</p>
                    <p style="color: {t_primary}; font-size: 22px; font-weight: 700; margin: 0;">{fatigue}%</p>
                </div>
            </div>

            <div style="border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'}; padding-top: 20px;">
                <h3 style="color: {t_primary}; font-size: 15px; font-weight: 700; margin-bottom: 10px;">Executive Insights</h3>
                <ul style="color: {t_secondary}; font-size: 14px; line-height: 1.5; margin: 0; padding-left: 18px;">
                    {"".join(f"<li style='margin-bottom: 6px;'>{i}</li>" for i in summary.get('insights', []))}
                </ul>
            </div>

            {comparison_html}
        </div>
        """