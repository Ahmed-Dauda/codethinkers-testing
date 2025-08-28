            #python code working fine
            # for line in lines:
            #     stripped = line.strip()

            #     # Detect code block markers (```python or ```)
            #     if stripped.startswith("```") and not in_code_block:
            #         in_code_block = True
            #         formatted_lines.append('<pre><code class="language-python" style="white-space: pre;">')
            #         continue
            #     elif stripped.startswith("```") and in_code_block:
            #         in_code_block = False
            #         formatted_lines.append("</code></pre>")
            #         continue

            #     # Inside code block: escape HTML but preserve indentation
            #     if in_code_block:
            #         escaped_line = (
            #             line.replace("&", "&amp;")
            #                 .replace("<", "&lt;")
            #                 .replace(">", "&gt;")
            #         )
            #         formatted_lines.append(escaped_line)

            #     # Headings outside code block
            #     elif any(keyword.lower() in line.lower() for keyword in heading_keywords):
            #         formatted_lines.append(f"<h3>{line}</h3>")
            #     else:
            #         # Normal text
            #         formatted_lines.append(f"<p>{line}</p>")

            # formatted_desc = "\n".join(formatted_lines)
