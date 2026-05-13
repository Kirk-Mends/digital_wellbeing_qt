# class WeeklyReportGenerator:
#     def generate(self, summary):
#         if summary is None:
#             return "No activity data available for this week."

#         total = summary["total_focus"]
#         deep_work = summary["deep_work"]
#         deep_reading = summary["deep_reading"]
#         focused_interaction = summary["focused_interaction"]
#         breaks = summary["breaks"]
#         avg_fatigue = summary["avg_fatigue"]
#         insights = summary["insights"]

#         # Build insights text
#         insights_text = "\n".join(f"• {i}" for i in insights)

#         return (
#             f"Here’s your weekly wellbeing summary:\n\n"
#             f"• Total focused minutes: **{total}**\n"
#             f"• Deep work minutes: **{deep_work}**\n"
#             f"• Deep reading minutes: **{deep_reading}**\n"
#             f"• Focused interaction minutes: **{focused_interaction}**\n"
#             f"• Breaks taken: **{breaks}**\n"
#             f"• Average fatigue level: **{avg_fatigue:.1f} / 100**\n\n"
#             f"Weekly Insights:\n{insights_text}\n\n"
#             f"Keep building healthy habits — small improvements add up."
#         )
















# class WeeklyReportGenerator:
#     def generate(self, summary):
#         if summary is None:
#             return "No activity data available for this week."

#         total = summary["total_focus"]
#         deep_work = summary["deep_work"]
#         deep_reading = summary["deep_reading"]
#         focused_interaction = summary["focused_interaction"]
#         breaks = summary["breaks"]
#         avg_fatigue = summary["avg_fatigue"]
#         max_fatigue = summary.get("max_fatigue", avg_fatigue)
#         insights = summary["insights"]

#         avg_fatigue_pct = f"{avg_fatigue:.1f}%"
#         max_fatigue_pct = f"{max_fatigue:.1f}%"

#         insights_html = "<br>".join(f"• {i}" for i in insights)

#         report = f"""
#         <div style="line-height: 1.35; font-size: 14px;">

#             <b>Here's your weekly wellbeing summary:</b><br>

#             • Total focused minutes: <b>{total:.1f}</b><br>
#             • Deep work minutes: <b>{deep_work:.1f}</b><br>
#             • Deep reading minutes: <b>{deep_reading:.1f}</b><br>
#             • Focused interaction minutes: <b>{focused_interaction:.1f}</b><br>
#             • Breaks taken: <b>{breaks}</b><br>
#             • Average fatigue level: <b>{avg_fatigue_pct}</b><br>
#             • Highest fatigue level: <b>{max_fatigue_pct}</b><br><br>

#             <div style="margin-top: 10px;">
#                 <b>Weekly Insights:</b><br>
#                 {insights_html}
#             </div>

#             <div style="margin-top: 12px;">
#                 Keep building healthy habits — small improvements add up.
#             </div>
#         </div>
#         """

#         return report











# class WeeklyReportGenerator:
#     def generate(self, summary):
#         if summary is None:
#             return "No activity data available for this week."

#         total = summary["total_focus"]
#         deep_work = summary["deep_work"]
#         deep_reading = summary["deep_reading"]
#         focused_interaction = summary["focused_interaction"]
#         breaks = summary["breaks"]
#         avg_fatigue = summary["avg_fatigue"]
#         max_fatigue = summary.get("max_fatigue", avg_fatigue)
#         insights = summary["insights"]

#         avg_fatigue_pct = f"{avg_fatigue:.1f}%"
#         max_fatigue_pct = f"{max_fatigue:.1f}%"

#         insights_html = "<br>".join(f"• {i}" for i in insights)

#         report = f"""
#         <div style="
#             font-family: 'Segoe UI', sans-serif;
#             font-size: 13px;
#             line-height: 1.55;
#             white-space: normal;
#         ">

#             <b style="font-size: 15px; font-weight: 600;">
#                 Here's your weekly wellbeing summary:
#             </b><br><br>

#             <div style="margin-left: 4px; margin-bottom: 12px;">
#                 • Total focused minutes: <b>{total:.1f}</b><br>
#                 • Deep work minutes: <b>{deep_work:.1f}</b><br>
#                 • Deep reading minutes: <b>{deep_reading:.1f}</b><br>
#                 • Focused interaction minutes: <b>{focused_interaction:.1f}</b><br>
#                 • Breaks taken: <b>{breaks}</b><br>
#                 • Average fatigue level: <b>{avg_fatigue_pct}</b><br>
#                 • Highest fatigue level: <b>{max_fatigue_pct}</b>
#             </div>

#             <b style="font-weight: 600;">Weekly Insights:</b><br>

#             <div style="margin-left: 4px; margin-top: 6px; margin-bottom: 12px;">
#                 {insights_html}
#             </div>

#             <div style="font-size: 13px;">
#                 Keep building healthy habits — small improvements add up.
#             </div>

#         </div>
#         """

#         return report










# 25th march
# class WeeklyReportGenerator:
#     def generate(self, summary):
#         if not summary:
#             return """
#             <div style='text-align: center; padding: 40px; font-family: sans-serif;'>
#                 <h3 style='color: #888;'>No activity data available</h3>
#                 <p>Start your first session to generate insights.</p>
#             </div>
#             """

#         # --- DATA CLEANING ---
#         def fmt_num(val):
#             return f"{int(val):,}" # Removes .0 and adds commas (Executive Style)

#         metrics = []
        
#         # Only add metrics if they have value (Crucial for Apple Review/Premium feel)
#         if summary.get("total_focus", 0) > 0:
#             metrics.append(f"• Total focused minutes: <b style='color: #0057D9;'>{fmt_num(summary['total_focus'])}</b>")
        
#         if summary.get("deep_work", 0) > 0:
#             metrics.append(f"• Deep work: <b>{fmt_num(summary['deep_work'])}m</b>")
            
#         if summary.get("deep_reading", 0) > 0:
#             metrics.append(f"• Deep reading: <b>{fmt_num(summary['deep_reading'])}m</b>")

#         if summary.get("focused_interaction", 0) > 0:
#             metrics.append(f"• Collaboration: <b>{fmt_num(summary['focused_interaction'])}m</b>")

#         metrics.append(f"• Breaks taken: <b>{summary.get('breaks', 0)}</b>")

#         # Fatigue Logic
#         avg_fatigue = summary.get("avg_fatigue", 0)
#         metrics.append(f"• Average fatigue level: <b>{avg_fatigue:.1f}%</b>")

#         metrics_html = "<br>".join(metrics)
        
#         # Insights Logic
#         insights = summary.get("insights", [])
#         if not insights:
#             insights_html = "• Your behavioral patterns are stabilizing. Keep consistent."
#         else:
#             insights_html = "<br>".join(f"• {i}" for i in insights)

#         # --- PREMIUM HTML TEMPLATE ---
#         report = f"""
#         <div style="
#             font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
#             font-size: 14px;
#             line-height: 1.6;
#             color: #2c3e50;
#         ">
#             <div style="margin-bottom: 20px;">
#                 <span style="color: #0057D9; font-weight: 800; font-size: 10px; letter-spacing: 1px; text-transform: uppercase;">
#                     Weekly Performance Brief
#                 </span>
#                 <h2 style="margin-top: 5px; font-weight: 700; font-size: 18px; color: #1a1a1a;">
#                     Here's your wellbeing summary:
#                 </h2>
#             </div>

#             <div style="
#                 background-color: rgba(0, 87, 217, 0.03); 
#                 border-left: 3px solid #0057D9;
#                 padding: 15px 20px;
#                 margin-bottom: 25px;
#                 border-radius: 0 8px 8px 0;
#             ">
#                 {metrics_html}
#             </div>

#             <h3 style="font-size: 15px; font-weight: 700; margin-bottom: 10px; color: #1a1a1a;">
#                 Executive Insights
#             </h3>

#             <div style="margin-bottom: 25px; color: #444;">
#                 {insights_html}
#             </div>

#             <hr style="border: 0; border-top: 1px solid #eee; margin-bottom: 20px;">

#             <div style="font-size: 12px; color: #888; font-style: italic;">
#                 "Keep building healthy habits — small improvements add up."
#             </div>
#         </div>
#         """
#         return report













# class WeeklyReportGenerator:
#     def generate(self, summary, is_dark_mode=False):
#         if not summary:
#             return "<p style='color: gray; text-align: center;'>No data available.</p>"

#         # --- DYNAMIC THEME COLORS ---
#         # Crucial for Premium Dark Mode visibility
#         text_primary = "#FFFFFF" if is_dark_mode else "#1A1A1A"
#         text_secondary = "#AAAAAA" if is_dark_mode else "#444444"
#         bg_accent = "rgba(77, 163, 255, 0.1)" if is_dark_mode else "rgba(0, 87, 217, 0.03)"
#         accent_color = "#4DA3FF" if is_dark_mode else "#0057D9"

#         def fmt_num(val):
#             return f"{int(val):,}"

#         metrics = []
#         if summary.get("total_focus", 0) > 0:
#             metrics.append(f"• Total focused minutes: <b style='color: {accent_color};'>{fmt_num(summary['total_focus'])}</b>")
        
#         metrics.append(f"• Breaks taken: <b>{summary.get('breaks', 0)}</b>")
#         metrics.append(f"• Average fatigue level: <b>{summary.get('avg_fatigue', 0):.1f}%</b>")

#         metrics_html = "<br>".join(metrics)
#         insights_html = "<br>".join(f"• {i}" for i in summary.get("insights", ["A steady, balanced week overall."]))

#         return f"""
#         <div style="font-family: sans-serif; font-size: 14px; line-height: 1.6; color: {text_primary};">
#             <div style="margin-bottom: 20px;">
#                 <span style="color: {accent_color}; font-weight: 800; font-size: 10px; letter-spacing: 1px; text-transform: uppercase;">
#                     Verified AI Insights
#                 </span>
#                 <h2 style="margin-top: 5px; font-weight: 700; font-size: 20px; color: {text_primary};">
#                     Here's your weekly wellbeing summary:
#                 </h2>
#             </div>

#             <div style="background-color: {bg_accent}; border-left: 4px solid {accent_color}; padding: 15px 20px; margin-bottom: 25px; border-radius: 0 8px 8px 0;">
#                 {metrics_html}
#             </div>

#             <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 10px;">Executive Insights</h3>
#             <div style="color: {text_secondary}; margin-bottom: 25px;">
#                 {insights_html}
#             </div>

#             <hr style="border: 0; border-top: 1px solid {accent_color}33; margin-bottom: 20px;">
#             <div style="font-size: 12px; color: {text_secondary}; font-style: italic;">
#                 "Keep building healthy habits — small improvements add up."
#             </div>
#         </div>
#         """
    





# class WeeklyReportGenerator:
#     def generate(self, summary, is_dark_mode=False):
#         if not summary:
#             return "<p style='text-align: center; opacity: 0.5;'>No data available.</p>"

#         def fmt_num(val):
#             try:
#                 return f"{int(float(val)):,}"
#             except:
#                 return str(val)

#         # Build Data Points
#         metrics = []
#         if summary.get("total_focus", 0) > 0:
#             # We use 'color: inherit' or specific semantic classes
#             metrics.append(f"• Total focused minutes: <b class='accent-text'>{fmt_num(summary['total_focus'])}</b>")
        
#         metrics.append(f"• Breaks taken: <b>{summary.get('breaks', 0)}</b>")
#         metrics.append(f"• Average fatigue level: <b>{summary.get('avg_fatigue', 0):.1f}%</b>")

#         metrics_html = "<br>".join(metrics)
#         insights_html = "".join([f"<div style='margin-bottom: 8px; opacity: 0.8;'>• {i}</div>" for i in summary.get("insights", ["A steady, balanced week overall."])])

#         # No hex codes here. We use inline-styles that respect the parent container's color.
#         return f"""
#         <div style="font-family: 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6;">
#             <div style="margin-bottom: 25px;">
#                 <span class="accent-text" style="font-weight: 800; font-size: 10px; letter-spacing: 1.2px; text-transform: uppercase;">
#                     Verified AI Insights
#                 </span>
#                 <h2 style="margin-top: 8px; font-weight: 700; font-size: 22px;">
#                     Weekly Wellbeing Summary
#                 </h2>
#             </div>

#             <div class="stats-box" style="padding: 22px; margin-bottom: 30px; border-radius: 8px; border-left: 3px solid;">
#                 {metrics_html}
#             </div>

#             <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 12px; ">Executive Insights</h3>
#             <div style="margin-bottom: 30px;">
#                 {insights_html}
#             </div>

#             <hr style="border: 0; border-top: 1px solid; opacity: 0.1; margin-bottom: 20px;">
#             <div style="font-size: 12px; opacity: 0.6; font-style: italic;">
#                 "Keep building healthy habits — small improvements add up."
#             </div>
#         </div>
#         """












# class WeeklyReportGenerator:
#     def generate(self, summary, is_dark_mode=False):
#         if not summary:
#             return "<p style='text-align: center; opacity: 0.5;'>No data available.</p>"

#         # Explicitly defining the color for the tags that were defaulting to black
#         heading_color = "#E4E7F2" if is_dark_mode else "#1A1A1A"

#         def fmt_num(val):
#             try:
#                 return f"{int(float(val)):,}"
#             except:
#                 return str(val)

#         metrics = []
#         if summary.get("total_focus", 0) > 0:
#             metrics.append(f"• Total focused minutes: <b class='accent-text'>{fmt_num(summary['total_focus'])}</b>")
        
#         metrics.append(f"• Breaks taken: <b>{summary.get('breaks', 0)}</b>")
#         metrics.append(f"• Average fatigue level: <b>{summary.get('avg_fatigue', 0):.1f}%</b>")

#         metrics_html = "<br>".join(metrics)
#         insights_html = "".join([f"<div style='margin-bottom: 8px; opacity: 0.8;'>• {i}</div>" for i in summary.get("insights", ["A steady, balanced week overall."])])

#         return f"""
#         <div style="font-family: 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6;">
#             <div style="margin-bottom: 25px;">
#                 <span class="accent-text" style="font-weight: 800; font-size: 10px; letter-spacing: 1.2px; text-transform: uppercase;">
#                     Verified AI Insights
#                 </span>
#                 <h2 style="margin-top: 8px; font-weight: 700; font-size: 18px; color: {heading_color};">
#                     Weekly Wellbeing Summary
#                 </h2>
#             </div>

#             <div class="stats-box" style="padding: 22px; margin-bottom: 30px; border-radius: 8px; border-left: 3px solid;">
#                 {metrics_html}
#             </div>

#             <h3 style="font-size: 16px; font-weight: 700; margin-bottom: 12px; color: {heading_color};">Executive Insights</h3>
#             <div style="margin-bottom: 30px;">
#                 {insights_html}
#             </div>

#             <hr style="border: 0; border-top: 1px solid; opacity: 0.1; margin-bottom: 20px;">
#             <div style="font-size: 12px; opacity: 0.6; font-style: italic;">
#                 "Keep building healthy habits — small improvements add up."
#             </div>
#         </div>
#         """





















# class WeeklyReportGenerator:
#     def generate(self, summary, is_dark_mode=False):
#         t_primary = "#FFFFFF" if is_dark_mode else "#1A1A1A"
#         t_secondary = "rgba(255,255,255,0.6)" if is_dark_mode else "#64748B"
#         accent = "#4DA3FF" if is_dark_mode else "#0057D9"

#         # "Hero" Metric Design
#         focus_mins = f"{int(summary.get('total_focus', 0)):,}"
        
#         return f"""
#         <div style="font-family: 'Segoe UI', sans-serif; padding: 10px;">
#             <div style="margin-bottom: 30px; text-align: left;">
#                 <span style="color: {accent}; font-weight: 800; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase;">
#                     Weekly Analysis
#                 </span>
#                 <h1 style="color: {t_primary}; font-size: 28px; margin-top: 8px; font-weight: 800; letter-spacing: -0.5px;">
#                     Focus Intelligence
#                 </h1>
#             </div>

#             <div style="background: {accent}15; border-radius: 14px; padding: 25px; margin-bottom: 30px; border: 1px solid {accent}30;">
#                 <div style="color: {t_secondary}; font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
#                     Total Focus Time
#                 </div>
#                 <div style="color: {accent}; font-size: 42px; font-weight: 800; margin: 5px 0;">
#                     {focus_mins} <span style="font-size: 18px; font-weight: 400; color: {t_secondary};">mins</span>
#                 </div>
#             </div>

#             <div style="display: flex; margin-bottom: 30px;">
#                 <div style="margin-right: 40px;">
#                     <div style="color: {t_secondary}; font-size: 11px; font-weight: 600;">BREAKS</div>
#                     <div style="color: {t_primary}; font-size: 20px; font-weight: 700;">{summary.get('breaks', 0)}</div>
#                 </div>
#                 <div>
#                     <div style="color: {t_secondary}; font-size: 11px; font-weight: 600;">AVG FATIGUE</div>
#                     <div style="color: {t_primary}; font-size: 20px; font-weight: 700;">{summary.get('avg_fatigue', 0)}%</div>
#                 </div>
#             </div>

#             <h3 style="color: {t_primary}; font-size: 16px; font-weight: 700; margin-bottom: 12px; border-top: 1px solid {t_primary}15; padding-top: 20px;">
#                 Executive Insights
#             </h3>
#             <p style="color: {t_secondary}; font-size: 14px; line-height: 1.6; font-style: italic;">
#                 "A steady, balanced week overall. Your focus endurance is improving."
#             </p>
#         </div>
#         """





# class WeeklyReportGenerator:
#     def generate(self, summary, is_dark_mode=False):
#         t_primary = "#E4E7F2" if is_dark_mode else "#1A1A1A"
#         t_secondary = "rgba(228, 231, 242, 0.5)" if is_dark_mode else "#64748B"
#         accent = "#4DA3FF" if is_dark_mode else "#0057D9"
        
#         # --- THE FIX: Round the fatigue and format focus minutes ---
#         focus_mins = f"{int(summary.get('total_focus', 0)):,}"
#         fatigue = f"{float(summary.get('avg_fatigue', 0)):.1f}"

#         return f"""
#         <div style="font-family: 'Segoe UI', system-ui, sans-serif;">
#             <p style="color: {accent}; font-weight: 800; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 30px;">
#                 Weekly Report
#             </p>

#             <h1 style="color: {t_primary}; font-size: 32px; font-weight: 800; margin-bottom: 40px; letter-spacing: -1px;">
#                 Focus Intelligence
#             </h1>

#             <div style="margin-bottom: 40px;">
#                 <p style="color: {t_secondary}; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">Total Focus Time</p>
#                 <div style="color: {accent}; font-size: 64px; font-weight: 800; line-height: 1;">
#                     {focus_mins} <span style="font-size: 24px; font-weight: 400; color: {t_secondary};">mins</span>
#                 </div>
#             </div>

#             <div style="margin-bottom: 30px;">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Breaks</p>
#                 <p style="color: {t_primary}; font-size: 24px; font-weight: 700; margin: 0;">{summary.get('breaks', 0)}</p>
#             </div>

#             <div style="margin-bottom: 40px;">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Avg Fatigue</p>
#                 <p style="color: {t_primary}; font-size: 24px; font-weight: 700; margin: 0;">{fatigue}%</p>
#             </div>

#             <div style="border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'}; padding-top: 30px;">
#                 <h3 style="color: {t_primary}; font-size: 16px; font-weight: 700; margin-bottom: 10px;">Executive Insights</h3>
#                 <p style="color: {t_secondary}; font-size: 15px; line-height: 1.6; font-style: italic; margin: 0;">
#                     "{summary.get('insights', ['A steady, balanced week overall. Your focus endurance is improving.'])[0]}"
#                 </p>
#             </div>
#         </div>
#         """











# Closed the margin small

# class WeeklyReportGenerator:
#     def generate(self, summary, is_dark_mode=False):
#         t_primary = "#E4E7F2" if is_dark_mode else "#1A1A1A"
#         t_secondary = "rgba(228, 231, 242, 0.5)" if is_dark_mode else "#64748B"
#         accent = "#4DA3FF" if is_dark_mode else "#0057D9"
        
#         # --- THE FIX: Round the fatigue and format focus minutes ---
#         focus_mins = f"{int(summary.get('total_focus', 0)):,}"
#         fatigue = f"{float(summary.get('avg_fatigue', 0)):.1f}"

#         return f"""
#         <div style="font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.2;">
#             <p style="color: {accent}; font-weight: 800; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">
#                 Weekly Report
#             </p>

#             <h1 style="color: {t_primary}; font-size: 32px; font-weight: 800; margin: 0 0 25px 0; letter-spacing: -1px;">
#                 Focus Intelligence
#             </h1>

#             <div style="margin-bottom: 30px;">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Total Focus Time</p>
#                 <div style="color: {accent}; font-size: 64px; font-weight: 800; line-height: 1;">
#                     {focus_mins} <span style="font-size: 20px; font-weight: 400; color: {t_secondary};">mins</span>
#                 </div>
#             </div>

#             <div style="display: flex; gap: 40px; margin-bottom: 30px;">
#                 <div>
#                     <p style="color: {t_secondary}; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 2px;">Breaks</p>
#                     <p style="color: {t_primary}; font-size: 22px; font-weight: 700; margin: 0;">{summary.get('breaks', 0)}</p>
#                 </div>
#                 <div>
#                     <p style="color: {t_secondary}; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 2px;">Avg Fatigue</p>
#                     <p style="color: {t_primary}; font-size: 22px; font-weight: 700; margin: 0;">{fatigue}%</p>
#                 </div>
#             </div>

#             <div style="border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'}; padding-top: 20px;">
#                 <h3 style="color: {t_primary}; font-size: 15px; font-weight: 700; margin-bottom: 8px;">Executive Insights</h3>
#                 <p style="color: {t_secondary}; font-size: 14px; line-height: 1.5; font-style: italic; margin: 0;">
#                     "{summary.get('insights', ['A steady, balanced week overall. Your focus endurance is improving.'])[0]}"
#                 </p>
#             </div>
#         </div>
#         """
















# # Changing the color for the titles to use qss

# class WeeklyReportGenerator:
#     def generate(self, summary, is_dark_mode=False, title_color="#1A1A1A"):
#         # 1. ONLY t_primary uses the QSS color
#         t_primary = title_color
        
#         # 2. t_secondary remains the same (Gray/Slate)
#         t_secondary = "rgba(228, 231, 242, 0.5)" if is_dark_mode else "#64748B"
        
#         # 3. accent remains the same (Blue/Accent)
#         accent = "#4DA3FF" if is_dark_mode else "#0057D9"
        
#         focus_mins = f"{int(summary.get('total_focus', 0)):,}"
#         fatigue = f"{float(summary.get('avg_fatigue', 0)):.1f}"

#         return f"""
#         <div style="font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.2;">
#             <p style="color: {accent}; font-weight: 800; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">
#                 Weekly Report
#             </p>

#             <h1 style="color: {t_primary}; font-size: 32px; font-weight: 800; margin: 0 0 25px 0; letter-spacing: -1px;">
#                 Focus Intelligence
#             </h1>

#             <div style="margin-bottom: 30px;">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Total Focus Time</p>
#                 <div style="color: {accent}; font-size: 64px; font-weight: 800; line-height: 1;">
#                     {focus_mins} <span style="font-size: 20px; font-weight: 400; color: {t_secondary};">mins</span>
#                 </div>
#             </div>

#             <div style="display: flex; gap: 40px; margin-bottom: 30px;">
#                 <div>
#                     <p style="color: {t_secondary}; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 2px;">Breaks</p>
#                     <p style="color: {t_primary}; font-size: 22px; font-weight: 700; margin: 0;">{summary.get('breaks', 0)}</p>
#                 </div>
#                 <div>
#                     <p style="color: {t_secondary}; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 2px;">Avg Fatigue</p>
#                     <p style="color: {t_primary}; font-size: 22px; font-weight: 700; margin: 0;">{fatigue}%</p>
#                 </div>
#             </div>

#             <div style="border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'}; padding-top: 20px;">
#                 <h3 style="color: {t_primary}; font-size: 15px; font-weight: 700; margin-bottom: 8px;">Executive Insights</h3>
#                 <p style="color: {t_secondary}; font-size: 14px; line-height: 1.5; font-style: italic; margin: 0;">
#                     "{summary.get('insights', ['A steady, balanced week overall.'])[0]}"
#                 </p>
#             </div>
#         </div>
#         """








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