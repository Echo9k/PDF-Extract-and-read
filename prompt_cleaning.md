**Objective:**
You are given a raw text extracted from scanned PDFs in Markdown format. The text may contain artifacts such as random capitalizations, extra spaces, HTML tags, special characters, OCR misinterpretations, and misplaced line breaks. Your task is to clean the text while preserving meaningful content and structure.

---

### **Instructions:**
1. **Remove Noise & Artifacts**  
   - Eliminate random capitalizations and convert text to sentence case where necessary.  
   - Remove unnecessary spaces, duplicate spaces, and excessive line breaks.  
   - Strip out special characters and symbols that do not contribute to meaning (e.g., `\n`, `\t`, `?`, `&`, `_`, `|`, etc., unless they belong to words).  

2. **Fix OCR Mistakes**  
   - Correct common OCR misinterpretations, such as:  
     - `l` → `I` (if it appears incorrectly in context)  
     - `i:` → `I:`  
     - `1` mistaken for `I` or `l`  
     - `O` mistaken for `0`  
     - `S` mistaken for `5`  
   - Identify and fix gibberish words that result from misinterpretations.

3. **Preserve Meaningful Formatting**  
   - Keep Markdown format.
   - Retain **headings** (e.g., `#`, `##`, `###` ), **bold** (`**text**`) and *italic* (`*text*`) formatting where applicable.
   - Maintain numbered lists and bullet points properly formatted.

4. **Remove Unwanted HTML Tags**  
   - Extract the meaningful content from `<html>`, `<body>`, `<table>`, `<tr>`, `<td>` while removing unnecessary structural tags.

5. **Correct Grammar & Structure**  
   - Fix broken sentences and misplaced words.  
   - Reformat fragmented text into readable paragraphs.

6. **Special Handling for Dates, Names, & Numbers**  
   - Ensure that dates are formatted correctly (e.g., `JAN 2` → `January 2`).  
   - Normalize place names and proper nouns (e.g., `RHoDE ISLaND` → `Rhode Island`).  
   - Ensure numbers and symbols are correctly spaced from text.

7. **Output:**  
   - Provide the cleaned text in a structured and readable Markdown format.  
   - Ensure that headings, paragraphs, and lists are appropriately formatted.
   - Add no notes, conclusions or starting analisis. Just keep the cleaned text.
---
