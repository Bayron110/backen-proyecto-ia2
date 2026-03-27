from openai import OpenAI
from openai.types.shared.reasoning import Reasoning
from typing import Optional, List, Dict, Any

from config import OPENAI_API_KEY
from schemas import VanillaComponentSpec

client = OpenAI(api_key=OPENAI_API_KEY)

INSTRUCTIONS = """
You are an expert UI Engineer and Visual Layout Interpreter.
Your job is to transform a UI mockup image (or text instruction) into a fully functional web component using ONLY vanilla HTML, CSS, and JavaScript.

STRICT RULES — follow these without exception:

HTML:
- Write semantic, clean HTML5 only.
- NO Angular syntax: no *ngIf, *ngFor, [(ngModel)], [class.x], (click)="", {{ }}, @if, @for, or any directive.
- NO JSX, NO React, NO Vue, NO framework-specific attributes.
- Use standard onclick, onsubmit, onchange attributes OR leave events to the JS block.
- All interactive elements (modals, tabs, dropdowns, forms) must be fully present in the HTML — not conditionally rendered.
- Modals must exist in the DOM at all times, hidden via CSS (display:none or opacity:0), shown by JS.

CSS:
- Pure CSS only. No SCSS, no Less.
- NO :host selector. NO ::ng-deep. NO Angular encapsulation artifacts.
- Use class selectors and IDs. Use CSS variables for theming if needed.
- Modals hidden by default: .modal { display: none; } and .modal.active { display: flex; }

JavaScript (returned in the "ts" field):
- Vanilla JavaScript ONLY. Must execute directly in a browser <script> tag without any build step.
- NO import/export statements.
- NO TypeScript syntax: no type annotations, no interfaces, no enums, no generics.
- NO Angular: no Component, no NgModule, no signal(), no computed(), no inject().
- NO class-based components.
- Use addEventListener() for all events.
- For modals triggered by form submit: listen to the form's submit event, call e.preventDefault(), then show the modal by adding class 'active' or setting style.display = 'flex'.
- For closing modals: listen to close buttons and overlay clicks, remove class 'active' or set style.display = 'none'.
- Listen for keydown Escape to close any open modal.
- All logic must be wrapped in a DOMContentLoaded listener or an IIFE to avoid global scope pollution.

EXAMPLE of correct JS for a form + modal:
document.addEventListener('DOMContentLoaded', function() {
  var form = document.getElementById('myForm');
  var modal = document.getElementById('successModal');
  var closeBtn = document.getElementById('closeModal');

  form.addEventListener('submit', function(e) {
    e.preventDefault();
    modal.style.display = 'flex';
  });

  closeBtn.addEventListener('click', function() {
    modal.style.display = 'none';
  });

  document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') modal.style.display = 'none';
  });
});

If the user provides conversation context, use it to maintain continuity and build upon previous generations.
If no image is provided, generate the component from the text instruction alone.
Return only valid structured output matching the schema exactly.
"""


def generate_component(
    instruction: str,
    base64_image: Optional[str] = None,
    context: Optional[List[Dict[str, Any]]] = None
):
    if context is None:
        context = []

    context_text = ""
    if context:
        context_text = "\n\nConversation context (last 10 messages):\n"
        for msg in context[-10:]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            # Include previous HTML/CSS/JS for continuity but keep it brief
            html_snippet = msg.get("htmlContent", "")[:300]
            if html_snippet:
                context_text += f"{role}: {content}\n[previous html snippet]: {html_snippet}...\n"
            else:
                context_text += f"{role}: {content}\n"

    # Strip any Angular-related instructions the frontend may have injected
    # (the SYSTEM_INSTRUCTION prefix from home.ts) — it's redundant now but harmless
    clean_instruction = instruction.replace(
        "IMPORTANTE - REGLAS OBLIGATORIAS DE GENERACIÓN DE CÓDIGO:", ""
    ).strip()

    full_text = f"{clean_instruction}{context_text}"

    content: List[Dict] = [
        {"type": "input_text", "text": full_text}
    ]

    if base64_image:
        content.append({
            "type": "input_image",
            "image_url": f"data:image/jpeg;base64,{base64_image}"
        })

    user_input = [
        {
            "role": "user",
            "content": content
        }
    ]

    response = client.responses.parse(
        instructions=INSTRUCTIONS,
        model="gpt-5.2",
        reasoning=Reasoning(effort="low", summary="auto"),
        text_format=VanillaComponentSpec,
        input=user_input
    )

    return response.output_parsed.dict()