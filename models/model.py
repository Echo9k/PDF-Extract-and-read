# model.py
import logging
from magic_pdf.model.doc_analyze_by_custom_model import ModelSingleton

def init_model():
    """
    Initialize the document analysis models.
    """
    try:
        model_manager = ModelSingleton()
        _ = model_manager.get_model(False, False)
        logging.info("Text model initialized successfully")
        _ = model_manager.get_model(True, False)
        logging.info("OCR model initialized successfully")
        return True
    except Exception as e:
        logging.exception("Model initialization failed: %s", e)
        return False

model_initialized = init_model()
