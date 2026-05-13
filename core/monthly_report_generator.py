# class MonthlyReportGenerator:
#     def generate(self, summary, last_summary=None):
#         if summary is None:
#             return "No activity data available for this month."

#         # Current month values
#         total = summary["total_focus"]
#         deep_work = summary["deep_work"]
#         deep_reading = summary["deep_reading"]
#         focused_interaction = summary["focused_interaction"]
#         breaks = summary["breaks"]
#         avg_fatigue = summary["avg_fatigue"]
#         insights = summary["insights"]

#         insights_text = "\n".join(f"• {i}" for i in insights)

#         # ---------------------------------------------------------
#         # MONTH-TO-MONTH COMPARISON (if last month exists)
#         # ---------------------------------------------------------
#         comparison_text = ""

#         if last_summary:
#             last_total = last_summary["total_focus"]
#             last_deep_work = last_summary["deep_work"]
#             last_fatigue = last_summary["avg_fatigue"]

#             def pct_change(current, previous):
#                 if previous == 0:
#                     return None
#                 return ((current - previous) / previous) * 100

#             total_change = pct_change(total, last_total)
#             deep_work_change = pct_change(deep_work, last_deep_work)
#             fatigue_change = pct_change(avg_fatigue, last_fatigue)

#             def format_change(label, value):
#                 if value is None:
#                     return f"• {label}: no comparison available"
#                 arrow = "↑" if value > 0 else "↓"
#                 return f"• {label}: {arrow} {abs(value):.1f}%"

#             comparison_text = (
#                 "\nMonth‑to‑Month Comparison:\n"
#                 f"{format_change('Total focus time', total_change)}\n"
#                 f"{format_change('Deep work time', deep_work_change)}\n"
#                 f"{format_change('Average fatigue', fatigue_change)}\n"
#             )

#         # ---------------------------------------------------------
#         # FINAL REPORT TEXT
#         # ---------------------------------------------------------
#         report = (
#             f"Here’s your monthly wellbeing summary:\n\n"
#             f"• Total focused minutes: **{total}**\n"
#             f"• Deep work minutes: **{deep_work}**\n"
#             f"• Deep reading minutes: **{deep_reading}**\n"
#             f"• Focused interaction minutes: **{focused_interaction}**\n"
#             f"• Breaks taken: **{breaks}**\n"
#             f"• Average fatigue level: **{avg_fatigue:.1f} / 100**\n\n"
#             f"Monthly Insights:\n{insights_text}\n"
#         )

#         if comparison_text:
#             report += f"\n{comparison_text}\n"

#         report += "Keep building healthy habits — steady progress leads to long‑term wellbeing."

#         return report











# class MonthlyReportGenerator:
#     def generate(self, summary, last_summary=None):
#         if summary is None:
#             return "No activity data available for this month."

#         # Current month values
#         total = summary["total_focus"]
#         deep_work = summary["deep_work"]
#         deep_reading = summary["deep_reading"]
#         focused_interaction = summary["focused_interaction"]
#         breaks = summary["breaks"]
#         avg_fatigue = summary["avg_fatigue"]
#         insights = summary["insights"]

#         # Convert fatigue to percentage
#         avg_fatigue_pct = f"{avg_fatigue:.1f}%"

#         # Build insights HTML
#         insights_html = "<br>".join(f"• {i}" for i in insights)

#         # ---------------------------------------------------------
#         # MONTH‑TO‑MONTH COMPARISON
#         # ---------------------------------------------------------
#         comparison_html = ""

#         if last_summary:
#             last_total = last_summary["total_focus"]
#             last_deep_work = last_summary["deep_work"]
#             last_fatigue = last_summary["avg_fatigue"]

#             def pct_change(current, previous):
#                 if previous == 0:
#                     return None
#                 return ((current - previous) / previous) * 100

#             total_change = pct_change(total, last_total)
#             deep_work_change = pct_change(deep_work, last_deep_work)
#             fatigue_change = pct_change(avg_fatigue, last_fatigue)

#             def format_change(label, value):
#                 if value is None:
#                     return f"• {label}: no comparison available"
#                 arrow = "↑" if value > 0 else "↓"
#                 return f"• {label}: {arrow} {abs(value):.1f}%"

#             comparison_html = (
#                 "<div style='margin-top: 24px;'>"
#                 "<b>Month‑to‑Month Comparison:</b><br>"
#                 f"{format_change('Total focus time', total_change)}<br>"
#                 f"{format_change('Deep work time', deep_work_change)}<br>"
#                 f"{format_change('Average fatigue', fatigue_change)}<br>"
#                 "</div>"
#             )

#         # ---------------------------------------------------------
#         # FINAL REPORT (HTML)
#         # ---------------------------------------------------------
#         report = f"""
# <div style="line-height: 1.35; font-size: 14px;">

#     <b>Here’s your monthly wellbeing summary:</b><br>

#     • Total focused minutes: <b>{total:.1f}</b><br>
#     • Deep work minutes: <b>{deep_work:.1f}</b><br>
#     • Deep reading minutes: <b>{deep_reading:.1f}</b><br>
#     • Focused interaction minutes: <b>{focused_interaction:.1f}</b><br>
#     • Breaks taken: <b>{breaks}</b><br>
#     • Average fatigue level: <b>{avg_fatigue_pct}</b><br>

#     <div style="margin-top: 10px;">
#         <b>Monthly Insights:</b><br>
#         {insights_html}
#     </div>

#     {comparison_html}

#     <div style="margin-top: 10px;">
#         Keep building healthy habits — steady progress leads to long‑term wellbeing.
#     </div>

# </div>
# """

#         return report
















# class MonthlyReportGenerator:
#     def generate(self, summary, last_summary=None):
#         if summary is None:
#             return "No activity data available for this month."

#         # Current month values
#         total = summary["total_focus"]
#         deep_work = summary["deep_work"]
#         deep_reading = summary["deep_reading"]
#         focused_interaction = summary["focused_interaction"]
#         breaks = summary["breaks"]
#         avg_fatigue = summary["avg_fatigue"]
#         insights = summary["insights"]

#         avg_fatigue_pct = f"{avg_fatigue:.1f}%"
#         insights_html = "<br>".join(f"• {i}" for i in insights)

#         # Month‑to‑month comparison
#         comparison_html = ""
#         if last_summary:
#             last_total = last_summary["total_focus"]
#             last_deep_work = last_summary["deep_work"]
#             last_fatigue = last_summary["avg_fatigue"]

#             def pct_change(current, previous):
#                 if previous == 0:
#                     return None
#                 return ((current - previous) / previous) * 100

#             total_change = pct_change(total, last_total)
#             deep_work_change = pct_change(deep_work, last_deep_work)
#             fatigue_change = pct_change(avg_fatigue, last_fatigue)

#             def format_change(label, value):
#                 if value is None:
#                     return f"• {label}: no comparison available"
#                 arrow = "↑" if value > 0 else "↓"
#                 return f"• {label}: {arrow} {abs(value):.1f}%"

#             comparison_html = (
#                 "<div style='margin-top: 14px;'>"
#                 "<b>Month‑to‑Month Comparison:</b><br>"
#                 f"{format_change('Total focus time', total_change)}<br>"
#                 f"{format_change('Deep work time', deep_work_change)}<br>"
#                 f"{format_change('Average fatigue', fatigue_change)}<br>"
#                 "</div>"
#             )

#         # Final report
#         report = f"""
# <div style="
#     font-family: 'Segoe UI', sans-serif;
#     font-size: 13px;
#     line-height: 1.55;
#     white-space: normal;
# ">

#     <b style="font-size: 15px; font-weight: 600;">
#         Here’s your monthly wellbeing summary:
#     </b><br><br>

#     <div style="margin-left: 4px; margin-bottom: 12px;">
#         • Total focused minutes: <b>{total:.1f}</b><br>
#         • Deep work minutes: <b>{deep_work:.1f}</b><br>
#         • Deep reading minutes: <b>{deep_reading:.1f}</b><br>
#         • Focused interaction minutes: <b>{focused_interaction:.1f}</b><br>
#         • Breaks taken: <b>{breaks}</b><br>
#         • Average fatigue level: <b>{avg_fatigue_pct}</b>
#     </div>

#     <b style="font-weight: 600;">Monthly Insights:</b><br>

#     <div style="margin-left: 4px; margin-top: 6px; margin-bottom: 12px;">
#         {insights_html}
#     </div>

#     {comparison_html}

#     <div style="margin-top: 14px; font-size: 13px;">
#         Keep building healthy habits — steady progress leads to long‑term wellbeing.
#     </div>

# </div>
# """

#         return report










# 253h March


# class MonthlyReportGenerator:
#     def generate(self, summary, last_summary=None, is_dark_mode=True):
#         if summary is None:
#             return "No activity data available for this month."

#         # Colors
#         accent = "#4DA3FF" if is_dark_mode else "#0057D9"
#         dim_text = "#94A3B8" if is_dark_mode else "#64748B"
        
#         total = summary["total_focus"]
#         avg_fatigue_pct = f"{summary['avg_fatigue']:.1f}%"
#         insights_html = "".join(f"<li style='margin-bottom: 8px;'>{i}</li>" for i in summary["insights"])

#         # Month-to-Month Logic
#         comparison_html = ""
#         if last_summary:
#             def get_change_ui(curr, prev):
#                 if prev == 0: return ""
#                 val = ((curr - prev) / prev) * 100
#                 color = "#2ECC71" if val >= 0 else "#E74C3C"
#                 arrow = "↑" if val >= 0 else "↓"
#                 return f"<span style='color: {color}; font-weight: 700;'> {arrow} {abs(val):.1f}%</span>"

#             comparison_html = f"""
#                 <div style="margin-top: 25px; padding-top: 15px; border-top: 1px solid rgba(150,150,150,0.1);">
#                     <b style="color: {accent}; letter-spacing: 1px; font-size: 10px; text-transform: uppercase;">
#                         Trend vs Last Month
#                     </span></b><br>
#                     <div style="margin-top: 8px; font-size: 13px;">
#                         • Focus Volume: {get_change_ui(total, last_summary['total_focus'])}<br>
#                         • Fatigue Levels: {get_change_ui(summary['avg_fatigue'], last_summary['avg_fatigue'])}
#                     </div>
#                 </div>
#             """

#         return f"""
#         <div style="font-family: 'Segoe UI', sans-serif; line-height: 1.6;">
#             <div style="color: {accent}; font-weight: 800; font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 12px;">
#                 Monthly Analysis
#             </div>
            
#             <div style="font-size: 24px; font-weight: 800; margin-bottom: 20px;">
#                 Monthly Progress Summary
#             </div>

#             <div style="margin-bottom: 10px; color: {dim_text}; font-size: 11px; font-weight: 700; text-transform: uppercase;">
#                 Total Monthly Focus
#             </div>
#             <div style="font-size: 36px; font-weight: 800; color: {accent}; margin-bottom: 5px;">
#                 {int(total):,} <span style="font-size: 18px; color: {dim_text}; font-weight: 400;">mins</span>
#             </div>

#             <div style="font-size: 14px; margin-top: 20px;">
#                 • Average Fatigue: <b>{avg_fatigue_pct}</b><br>
#                 • Total Breaks: <b>{summary['breaks']}</b>
#             </div>

#             <div style="margin-top: 30px;">
#                 <b style="font-size: 16px; font-weight: 700;">Executive Insights</b>
#                 <ul style="margin-top: 10px; padding-left: 18px; font-size: 13px;">
#                     {insights_html}
#                 </ul>
#             </div>

#             {comparison_html}
#         </div>
#         """










# Its a bit thin

# class MonthlyReportGenerator:
#     def generate(self, summary, last_summary=None, is_dark_mode=True):
#         if summary is None:
#             return "No activity data available for this month."

#         # Refined Color Palette
#         accent = "#4DA3FF" if is_dark_mode else "#0057D9"
#         dim_text = "#94A3B8" if is_dark_mode else "#64748B"
#         border_color = "rgba(148, 163, 184, 0.1)"
        
#         total = summary["total_focus"]
#         avg_fatigue_pct = f"{summary['avg_fatigue']:.1f}%"
#         insights_html = "".join(f"<li style='margin-bottom: 10px; font-weight: 300;'>{i}</li>" for i in summary["insights"])

#         # Month-to-Month Logic (Streamlined)
#         comparison_html = ""
#         if last_summary:
#             def get_change_ui(curr, prev):
#                 if prev == 0: return ""
#                 val = ((curr - prev) / prev) * 100
#                 color = "#2ECC71" if val >= 0 else "#E74C3C"
#                 arrow = "↑" if val >= 0 else "↓"
#                 # Updated to thinner weights for the trend
#                 return f"<span style='color: {color}; font-weight: 500; letter-spacing: 0px;'> {arrow} {abs(val):.1f}%</span>"

#             comparison_html = f"""
#                 <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid {border_color};">
#                     <div style="color: {dim_text}; letter-spacing: 2px; font-size: 9px; text-transform: uppercase; font-weight: 600; margin-bottom: 12px;">
#                         Trend vs Last Month
#                     </div>
#                     <div style="font-size: 13px; font-weight: 300; letter-spacing: 0.3px; line-height: 2;">
#                         Focus Volume: {get_change_ui(total, last_summary['total_focus'])}<br>
#                         Fatigue Levels: {get_change_ui(summary['avg_fatigue'], last_summary['avg_fatigue'])}
#                     </div>
#                 </div>
#             """

#         return f"""
#         <div style="font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif; line-height: 1.5; color: {'#FFFFFF' if is_dark_mode else '#1A1A1A'};">
#             <div style="color: {accent}; font-weight: 600; font-size: 9px; letter-spacing: 2.5px; text-transform: uppercase; margin-bottom: 8px;">
#                 Monthly Analysis
#             </div>
            
#             <div style="font-size: 28px; font-weight: 300; letter-spacing: -0.5px; margin-bottom: 25px;">
#                 Monthly Progress
#             </div>

#             <div style="margin-bottom: 5px; color: {dim_text}; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px;">
#                 Total Focus Volume
#             </div>
#             <div style="font-size: 42px; font-weight: 200; color: {accent}; margin-bottom: 15px; letter-spacing: -1px;">
#                 {int(total):,} <span style="font-size: 16px; color: {dim_text}; font-weight: 300; letter-spacing: 0px;">mins</span>
#             </div>

#             <div style="font-size: 13px; font-weight: 300; margin-top: 20px; border-left: 1px solid {accent}; padding-left: 15px; line-height: 1.8;">
#                 Average Fatigue: <span style="font-weight: 500;">{avg_fatigue_pct}</span><br>
#                 Total Breaks: <span style="font-weight: 500;">{summary['breaks']}</span>
#             </div>

#             <div style="margin-top: 35px;">
#                 <div style="font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 1.5px; color: {dim_text}; margin-bottom: 15px;">
#                     Executive Insights
#                 </div>
#                 <ul style="margin-top: 10px; padding-left: 15px; font-size: 13px; color: {dim_text if is_dark_mode else '#444'};">
#                     {insights_html}
#                 </ul>
#             </div>

#             {comparison_html}
#         </div>
#         """









# same as weekly

# class MonthlyReportGenerator:
#     def generate(self, summary, last_summary=None, is_dark_mode=True):
#         if summary is None:
#             return "No activity data available for this month."

#         # Colors - Matched to Weekly's exact logic
#         t_primary = "#E4E7F2" if is_dark_mode else "#1A1A1A"
#         t_secondary = "rgba(228, 231, 242, 0.5)" if is_dark_mode else "#64748B"
#         accent = "#4DA3FF" if is_dark_mode else "#0057D9"
        
#         # Formatting
#         total_focus = f"{int(summary.get('total_focus', 0)):,}"
#         fatigue = f"{float(summary.get('avg_fatigue', 0)):.1f}"
        
#         # Comparison Logic
#         comparison_html = ""
#         if last_summary:
#             def get_change_ui(curr, prev):
#                 if prev == 0: return ""
#                 val = ((curr - prev) / prev) * 100
#                 color = "#2ECC71" if val >= 0 else "#E74C3C"
#                 arrow = "↑" if val >= 0 else "↓"
#                 return f"<span style='color: {color}; font-weight: 700;'>{arrow} {abs(val):.1f}%</span>"

#             comparison_html = f"""
#             <div style="margin-top: 40px; padding-top: 30px; border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'};">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 12px; letter-spacing: 1px;">Trend vs Last Month</p>
#                 <div style="color: {t_primary}; font-size: 14px; font-weight: 600; line-height: 1.8;">
#                     Focus Volume: {get_change_ui(summary['total_focus'], last_summary['total_focus'])}<br>
#                     Fatigue Levels: {get_change_ui(summary['avg_fatigue'], last_summary['avg_fatigue'])}
#                 </div>
#             </div>
#             """

#         return f"""
#         <div style="font-family: 'Segoe UI', system-ui, sans-serif; background: transparent;">
#             <p style="color: {accent}; font-weight: 800; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 30px;">
#                 Monthly Report
#             </p>

#             <h1 style="color: {t_primary}; font-size: 32px; font-weight: 800; margin-bottom: 40px; letter-spacing: -1px;">
#                 Monthly Progress
#             </h1>

#             <div style="margin-bottom: 40px;">
#                 <p style="color: {t_secondary}; font-size: 12px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px;">Total Monthly Focus</p>
#                 <div style="color: {accent}; font-size: 64px; font-weight: 800; line-height: 1;">
#                     {total_focus} <span style="font-size: 24px; font-weight: 400; color: {t_secondary};">mins</span>
#                 </div>
#             </div>

#             <div style="display: flex; gap: 40px; margin-bottom: 40px;">
#                 <div>
#                     <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Avg Fatigue</p>
#                     <p style="color: {t_primary}; font-size: 24px; font-weight: 700; margin: 0;">{fatigue}%</p>
#                 </div>
#                 <div>
#                     <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Breaks</p>
#                     <p style="color: {t_primary}; font-size: 24px; font-weight: 700; margin: 0;">{summary.get('breaks', 0)}</p>
#                 </div>
#             </div>

#             <div style="border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'}; padding-top: 30px;">
#                 <h3 style="color: {t_primary}; font-size: 16px; font-weight: 700; margin-bottom: 10px;">Executive Insights</h3>
#                 <ul style="color: {t_secondary}; font-size: 15px; line-height: 1.6; margin: 0; padding-left: 18px;">
#                     {"".join(f"<li style='margin-bottom: 8px;'>{i}</li>" for i in summary.get('insights', []))}
#                 </ul>
#             </div>

#             {comparison_html}
#         </div>
#         """
















# class MonthlyReportGenerator:
#     def generate(self, summary, last_summary=None, is_dark_mode=True):
#         if summary is None:
#             return "No activity data available for this month."

#         # Colors - Consistent with Weekly
#         t_primary = "#E4E7F2" if is_dark_mode else "#1A1A1A"
#         t_secondary = "rgba(228, 231, 242, 0.5)" if is_dark_mode else "#64748B"
#         accent = "#4DA3FF" if is_dark_mode else "#0057D9"
        
#         # Formatting
#         total_focus = f"{int(summary.get('total_focus', 0)):,}"
#         fatigue = f"{float(summary.get('avg_fatigue', 0)):.1f}"
        
#         # Trend Logic
#         comparison_html = ""
#         if last_summary:
#             def get_change_ui(curr, prev):
#                 if prev == 0: return ""
#                 val = ((curr - prev) / prev) * 100
#                 color = "#2ECC71" if val >= 0 else "#E74C3C"
#                 arrow = "↑" if val >= 0 else "↓"
#                 return f"<span style='color: {color}; font-weight: 700;'>{arrow} {abs(val):.1f}%</span>"

#             comparison_html = f"""
#             <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'};">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px;">Trend vs Last Month</p>
#                 <div style="color: {t_primary}; font-size: 14px; font-weight: 600;">
#                     Focus: {get_change_ui(summary['total_focus'], last_summary['total_focus'])} | 
#                     Fatigue: {get_change_ui(summary['avg_fatigue'], last_summary['avg_fatigue'])}
#                 </div>
#             </div>
#             """

#         return f"""
#         <div style="font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.2;">
#             <p style="color: {accent}; font-weight: 800; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">
#                 Monthly Report
#             </p>

#             <h1 style="color: {t_primary}; font-size: 32px; font-weight: 800; margin: 0 0 25px 0; letter-spacing: -1px;">
#                 Monthly Progress
#             </h1>

#             <div style="margin-bottom: 30px;">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Total Monthly Focus</p>
#                 <div style="color: {accent}; font-size: 64px; font-weight: 800; line-height: 1;">
#                     {total_focus} <span style="font-size: 20px; font-weight: 400; color: {t_secondary};">mins</span>
#                 </div>
#             </div>

#             <div style="display: flex; gap: 30px; margin-bottom: 30px;">
#                 <div>
#                     <p style="color: {t_secondary}; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 2px;">Avg Fatigue</p>
#                     <p style="color: {t_primary}; font-size: 22px; font-weight: 700; margin: 0;">{fatigue}%</p>
#                 </div>
#                 <div>
#                     <p style="color: {t_secondary}; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 2px;">Breaks</p>
#                     <p style="color: {t_primary}; font-size: 22px; font-weight: 700; margin: 0;">{summary.get('breaks', 0)}</p>
#                 </div>
#             </div>

#             <div style="border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'}; padding-top: 20px;">
#                 <h3 style="color: {t_primary}; font-size: 15px; font-weight: 700; margin-bottom: 10px;">Executive Insights</h3>
#                 <ul style="color: {t_secondary}; font-size: 14px; line-height: 1.5; margin: 0; padding-left: 18px;">
#                     {"".join(f"<li style='margin-bottom: 6px;'>{i}</li>" for i in summary.get('insights', []))}
#                 </ul>
#             </div>

#             {comparison_html}
#         </div>
#         """












# # This is also perfect
# class MonthlyReportGenerator:
#     def generate(self, summary, last_summary=None, is_dark_mode=True):
#         if summary is None:
#             return "No activity data available for this month."

#         # Colors - Consistent with Weekly
#         t_primary = "#E4E7F2" if is_dark_mode else "#1A1A1A"
#         t_secondary = "rgba(228, 231, 242, 0.5)" if is_dark_mode else "#64748B"
#         accent = "#4DA3FF" if is_dark_mode else "#0057D9"
        
#         # Formatting
#         total_focus = f"{int(summary.get('total_focus', 0)):,}"
#         fatigue = f"{float(summary.get('avg_fatigue', 0)):.1f}"
        
#         # Trend Logic
#         comparison_html = ""
#         if last_summary:
#             def get_change_ui(curr, prev):
#                 if prev == 0: return ""
#                 val = ((curr - prev) / prev) * 100
#                 color = "#2ECC71" if val >= 0 else "#E74C3C"
#                 arrow = "↑" if val >= 0 else "↓"
#                 return f"<span style='color: {color}; font-weight: 700;'>{arrow} {abs(val):.1f}%</span>"

#             comparison_html = f"""
#             <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'}; margin-bottom: 20px;">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px;">Trend vs Last Month</p>
#                 <div style="color: {t_primary}; font-size: 14px; font-weight: 600;">
#                     Focus: {get_change_ui(summary['total_focus'], last_summary['total_focus'])} | 
#                     Fatigue: {get_change_ui(summary['avg_fatigue'], last_summary['avg_fatigue'])}
#                 </div>
#             </div>
#             """

#         # ADDED: padding-bottom: 40px to the main div
#         return f"""
#         <div style="font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.2; padding-bottom: 40px;">
#             <p style="color: {accent}; font-weight: 800; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">
#                 Monthly Report
#             </p>

#             <h1 style="color: {t_primary}; font-size: 32px; font-weight: 800; margin: 0 0 25px 0; letter-spacing: -1px;">
#                 Monthly Progress
#             </h1>

#             <div style="margin-bottom: 30px;">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Total Monthly Focus</p>
#                 <div style="color: {accent}; font-size: 64px; font-weight: 800; line-height: 1;">
#                     {total_focus} <span style="font-size: 20px; font-weight: 400; color: {t_secondary};">mins</span>
#                 </div>
#             </div>

#             <div style="display: flex; gap: 30px; margin-bottom: 30px;">
#                 <div>
#                     <p style="color: {t_secondary}; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 2px;">Avg Fatigue</p>
#                     <p style="color: {t_primary}; font-size: 22px; font-weight: 700; margin: 0;">{fatigue}%</p>
#                 </div>
#                 <div>
#                     <p style="color: {t_secondary}; font-size: 10px; font-weight: 700; text-transform: uppercase; margin-bottom: 2px;">Breaks</p>
#                     <p style="color: {t_primary}; font-size: 22px; font-weight: 700; margin: 0;">{summary.get('breaks', 0)}</p>
#                 </div>
#             </div>

#             <div style="border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'}; padding-top: 20px; margin-bottom: 10px;">
#                 <h3 style="color: {t_primary}; font-size: 15px; font-weight: 700; margin-bottom: 10px;">Executive Insights</h3>
#                 <ul style="color: {t_secondary}; font-size: 14px; line-height: 1.5; margin: 0; padding-left: 18px;">
#                     {"".join(f"<li style='margin-bottom: 6px;'>{i}</li>" for i in summary.get('insights', []))}
#                 </ul>
#             </div>

#             {comparison_html}
#         </div>
#         """














# class MonthlyReportGenerator:
#     def generate(self, summary, last_summary=None, is_dark_mode=True):
#         if summary is None:
#             return "No activity data available for this month."

#         # Colors - Consistent with Weekly
#         t_primary = "#E4E7F2" if is_dark_mode else "#1A1A1A"
#         t_secondary = "rgba(228, 231, 242, 0.5)" if is_dark_mode else "#64748B"
#         accent = "#4DA3FF" if is_dark_mode else "#0057D9"
        
#         # Formatting
#         total_focus = f"{int(summary.get('total_focus', 0)):,}"
#         fatigue = f"{float(summary.get('avg_fatigue', 0)):.1f}"
        
#         # Trend Logic
#         comparison_html = ""
#         if last_summary:
#             def get_change_ui(curr, prev):
#                 if prev == 0: return "—"
#                 val = ((curr - prev) / prev) * 100
#                 color = "#2ECC71" if val >= 0 else "#E74C3C"
#                 arrow = "↑" if val >= 0 else "↓"
#                 return f"<span style='color: {color}; font-weight: 700;'>{arrow} {abs(val):.1f}%</span>"

#             comparison_html = f"""
#             <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'};">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px;">Trend vs Last Month</p>
#                 <div style="color: {t_primary}; font-size: 13px; font-weight: 600;">
#                     Focus: {get_change_ui(summary.get('total_focus', 0), last_summary.get('total_focus', 0))} 
#                     <span style="color: {t_secondary}; margin: 0 10px;">|</span> 
#                     Fatigue: {get_change_ui(summary.get('avg_fatigue', 0), last_summary.get('avg_fatigue', 0))}
#                 </div>
#             </div>
#             """

#         return f"""
#         <div style="font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.2; padding-bottom: 40px;">
#             <p style="color: {accent}; font-weight: 800; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">
#                 Monthly Report
#             </p>

#             <h1 style="color: {t_primary}; font-size: 32px; font-weight: 800; margin: 0 0 25px 0; letter-spacing: -1px;">
#                 Monthly Progress
#             </h1>

#             <div style="margin-bottom: 30px;">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Total Monthly Focus</p>
#                 <div style="color: {accent}; font-size: 64px; font-weight: 800; line-height: 1;">
#                     {total_focus} <span style="font-size: 20px; font-weight: 400; color: {t_secondary};">mins</span>
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
#                 <h3 style="color: {t_primary}; font-size: 15px; font-weight: 700; margin-bottom: 10px;">Executive Insights</h3>
#                 <ul style="color: {t_secondary}; font-size: 14px; line-height: 1.5; margin: 0; padding-left: 18px;">
#                     {"".join(f"<li style='margin-bottom: 6px;'>{i}</li>" for i in summary.get('insights', []))}
#                 </ul>
#             </div>

#             {comparison_html}
#         </div>
#         """












# # Changed the title color
# class MonthlyReportGenerator:
#     # Added title_color argument to match the Page's refresh call
#     def generate(self, summary, last_summary=None, is_dark_mode=True, title_color="#1A1A1A"):
#         if summary is None:
#             return "No activity data available for this month."

#         # 1. LINKED: t_primary now pulls directly from the QSS Title Color
#         t_primary = title_color
        
#         # 2. CONSTANT: These stay as the standard theme colors for readability
#         t_secondary = "rgba(228, 231, 242, 0.5)" if is_dark_mode else "#64748B"
#         accent = "#4DA3FF" if is_dark_mode else "#0057D9"
        
#         # Formatting
#         total_focus = f"{int(summary.get('total_focus', 0)):,}"
#         fatigue = f"{float(summary.get('avg_fatigue', 0)):.1f}"
        
#         # Trend Logic
#         comparison_html = ""
#         if last_summary:
#             def get_change_ui(curr, prev):
#                 if prev == 0: return "—"
#                 val = ((curr - prev) / prev) * 100
#                 color = "#2ECC71" if val >= 0 else "#E74C3C"
#                 arrow = "↑" if val >= 0 else "↓"
#                 return f"<span style='color: {color}; font-weight: 700;'>{arrow} {abs(val):.1f}%</span>"

#             comparison_html = f"""
#             <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid {'rgba(255,255,255,0.1)' if is_dark_mode else '#E2E8F0'};">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 8px; letter-spacing: 1px;">Trend vs Last Month</p>
#                 <div style="color: {t_primary}; font-size: 13px; font-weight: 600;">
#                     Focus: {get_change_ui(summary.get('total_focus', 0), last_summary.get('total_focus', 0))} 
#                     <span style="color: {t_secondary}; margin: 0 10px;">|</span> 
#                     Fatigue: {get_change_ui(summary.get('avg_fatigue', 0), last_summary.get('avg_fatigue', 0))}
#                 </div>
#             </div>
#             """

#         return f"""
#         <div style="font-family: 'Segoe UI', system-ui, sans-serif; line-height: 1.2; padding-bottom: 40px;">
#             <p style="color: {accent}; font-weight: 800; font-size: 11px; letter-spacing: 1.5px; text-transform: uppercase; margin-bottom: 8px;">
#                 Monthly Report
#             </p>

#             <h1 style="color: {t_primary}; font-size: 32px; font-weight: 800; margin: 0 0 25px 0; letter-spacing: -1px;">
#                 Monthly Progress
#             </h1>

#             <div style="margin-bottom: 30px;">
#                 <p style="color: {t_secondary}; font-size: 11px; font-weight: 700; text-transform: uppercase; margin-bottom: 4px;">Total Monthly Focus</p>
#                 <div style="color: {accent}; font-size: 64px; font-weight: 800; line-height: 1;">
#                     {total_focus} <span style="font-size: 20px; font-weight: 400; color: {t_secondary};">mins</span>
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
#                 <h3 style="color: {t_primary}; font-size: 15px; font-weight: 700; margin-bottom: 10px;">Executive Insights</h3>
#                 <ul style="color: {t_secondary}; font-size: 14px; line-height: 1.5; margin: 0; padding-left: 18px;">
#                     {"".join(f"<li style='margin-bottom: 6px;'>{i}</li>" for i in summary.get('insights', []))}
#                 </ul>
#             </div>

#             {comparison_html}
#         </div>
#         """








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