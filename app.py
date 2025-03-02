# app.py
import os
import json
import logging
from model import model_initialized
from pdf_processor import to_pdf, to_markdown, file_to_pdf
from config import config
from tts import text_to_speech, generate_audio  # Import TTS module


# Set up logging with ANSI escape codes for colored output
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def log_info(message: str):
    logging.info(f"\033[92m{message}\033[0m")  # Green for info

def log_error(message: str):
    logging.error(f"\033[91m{message}\033[0m")  # Red for errors

# Load header HTML content
try:
    with open("header.html", "r") as file:
        header = file.read()
    log_info("Header loaded successfully.")
except Exception as e:
    log_error(f"Failed to load header.html. Error: {e}")
    header = "<h1>Header not found</h1>"

try:
    # Load the language options from the JSON file
    with open('language_options.json', 'r') as file:
        data = json.load(file)

    # Create the all_lang list by concatenating the different language lists
    all_lang = ['','auto'] + data["other_lang"] + data["latin_lang"] + data["arabic_lang"] + data["cyrillic_lang"] + data["devanagari_lang"]
except Exception as e:
    log_error(f"Filed to load file language_options.json. Error: {e}")
    all_lang = ['es', 'en']

with gr.Blocks() as demo:
    gr.HTML(header)
    with gr.Row():
        with gr.Column(variant='panel', scale=5):
            file_input = gr.File(
                label="Please upload a PDF or image",
                file_types=[".pdf", ".png", ".jpeg", ".jpg" ,"webp"])
            max_pages = gr.Slider(1, 20,config.get("max_pages_default", config.get("max_pages", 10)), step=1, label='Max convert pages')
            with gr.Row():
                layout_mode = gr.Dropdown(
                    ["layoutlmv3", "doclayout_yolo"],
                    label="Layout model",
                    value=config.get("layout_model_default", "layoutlmv3")
                )
                language = gr.Dropdown(
                    all_lang,
                    label="Language",
                    value=config.get("language_default", config.get("language", "auto"))
                )
            with gr.Row():
                formula_enable = gr.Checkbox(label="Enable formula recognition", value=True)
                is_ocr = gr.Checkbox(label="Force enable OCR", value=False)
                table_enable = gr.Checkbox(label="Enable table recognition", value=True)
            with gr.Row():
                convert_button = gr.Button("Convert")
                clear_button = gr.ClearButton(value="Clear")
            pdf_display = PDF(label='PDF preview', interactive=False, visible=True, height=800)
            with gr.Accordion("Examples:"):
                example_root = os.path.join(os.path.dirname(__file__), "examples")
                examples = [os.path.join(example_root, f) for f in os.listdir(example_root) if f.endswith("pdf")]
                gr.Examples(examples=examples, inputs=file_input)
        with gr.Column(variant='panel', scale=5):
            output_file = gr.File(label="Convert result", interactive=False)
            with gr.Tabs():
                with gr.Tab("Markdown rendering"):
                    md_render = gr.Markdown(label="Markdown rendering", height=1100, show_copy_button=True, line_breaks=True)
                with gr.Tab("Markdown text"):
                    md_text = gr.TextArea(lines=45, show_copy_button=True)
    
    file_input.change(fn=file_to_pdf, inputs=file_input, outputs=pdf_display)
    
    convert_button.click(
        fn=to_markdown,
        inputs=[file_input, max_pages, is_ocr, layout_mode, formula_enable, table_enable, language],
        outputs=[md_render, md_text, output_file, pdf_display]
    )

    
    clear_button.add([file_input, md_render, pdf_display, md_text, output_file, is_ocr])

if __name__ == "__main__":
    demo.launch(ssr_mode=True)
