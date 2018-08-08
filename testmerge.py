from mailmerge import MailMerge

import io

with MailMerge('template.travel-advance.docx') as document:
    print document.get_merge_fields()
    document.merge(full_name='Daniel Langer')
    
    output = io.BytesIO()
    document.write(output)

    with open('newfoo.docx', 'w') as f:
        f.write(output.getvalue()) 