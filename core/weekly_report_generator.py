





# windows and mac version

# Changing the color for the titles to use qss

class WeeklyReportGenerator:
    def generate(self, summary, is_dark_mode=False, title_color="#1A1A1A"):
        # 1. ONLY t_primary uses the QSS color
        t_primary = title_color
        
        # 2. t_secondary remains the same (Gray/Slate)
        t_secondary = "rgba(228, 231, 242, 0.5)" if is_dark_mode else "#64748B"
        
        # 3. accent remains the same (Blue/Accent)
        accent = "#4DA3FF" if is_dark_mode else "#0057D9"
        
        focus_mins = f"{int(summary.get('total_focus', 0)):,}"
        fatigue = f"{float(summary.get('avg_fatigue', 0)):.1f}"

        # Corrected font-family to include ".AppleSystemUIFont" for Mac speed
        return f"""
        <div style="font-family: '.AppleSystemUIFont', 'Segoe UI', system-ui, sans-serif; line-height: 1.2;">
            <p style="color: {accent}; font-weight: 800; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">
                Weekly Report
            </p>

            <h1 style="color: {t_primary}; font-size: 32px; font-weight: 800; margin: 0 0 25px 0; letter-spacing: -1px;">
                Focus Intelligence
            </h1>

            <div style="margin-bottom: 30px;">
                <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Total Focus Time</p>
                <div style="color: {accent}; font-size: 64px; font-weight: 800; line-height: 1;">
                    {focus_mins} <span style="font-size: 20px; font-weight: 400; color: {t_secondary};">mins</span>
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
                <h3 style="color: {t_primary}; font-size: 15px; font-weight: 700; margin-bottom: 8px;">Executive Insights</h3>
                <p style="color: {t_secondary}; font-size: 14px; line-height: 1.5; font-style: italic; margin: 0;">
                    "{summary.get('insights', ['A steady, balanced week overall.'])[0]}"
                </p>
            </div>
        </div>
        """