TINYMCE_DEFAULT_CONFIG = {
    'height': 500,
    'width': 800,
    'plugins': (
        'advlist autolink lists link image charmap print preview hr anchor '
        'pagebreak searchreplace wordcount visualblocks visualchars code fullscreen '
        'insertdatetime media nonbreaking save table contextmenu directionality '
        'emoticons template paste textcolor colorpicker textpattern',
        'advlist autolink lists link image charmap print preview hr anchor pagebreak',
    ),
    'toolbar': (
        'undo redo | styleselect | bold italic underline | '
        'forecolor backcolor | alignleft aligncenter alignright alignjustify | '
        'bullist numlist outdent indent | link image | '
        'ltr rtl | code'
    ),
    'directionality': 'rtl',  # Set default direction to RTL
    'language': 'ar',  # Set the language to Arabic
    'menubar': True,  # Show the menu bar
    'toolbar_mode': 'floating',  # Optionally make the toolbar float

    'selector': 'textarea',  
    
}
