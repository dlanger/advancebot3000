import io
from mailmerge import MailMerge

WORD_TEMPLATE = 'template.travel-advance.docx' 

def render_advance_form(full_name):
    output_buffer = io.BytesIO()

    with MailMerge(WORD_TEMPLATE) as template:
        template.merge(
            full_name=full_name
        )

        template.write(output_buffer)
    
    output_buffer.seek(0)
    return output_buffer