from aqt import mw
from aqt.qt import QAction, QFileDialog
from aqt.utils import showInfo
from anki.notes import Note
from anki.decks import DeckManager

from .llm import call_llm
from .pdf_parser import extract_text_from_pdf

import os

def generate_flashcards():
    # Choose PDF file
    file_path, _ = QFileDialog.getOpenFileName(mw, "Select PDF", "", "PDF Files (*.pdf)")
    if not file_path:
        return

    # Extract text
    text = extract_text_from_pdf(file_path)
    
    # Call LLM to generate flashcards
    flashcards = call_llm(text)

    # Parse and create cards
    deck_id = mw.col.decks.id("LLM Flashcards")
    model = mw.col.models.by_name("Basic")

    for line in flashcards.strip().split("\n"):
        if "::" in line:
            front, back = map(str.strip, line.split("::", 1))
            note = Note(mw.col, model)
            note.model()['did'] = deck_id
            note.fields[0] = front
            note.fields[1] = back
            mw.col.add_note(note)

    mw.col.autosave()
    showInfo("Flashcards generated successfully!")

action = QAction("Generate LLM Flashcards", mw)
action.triggered.connect(generate_flashcards)
mw.form.menuTools.addAction(action)
