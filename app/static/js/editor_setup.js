window.onload = function () {

    toolbar = [
        'title',
        'bold',
        'italic',
        'underline',
        'strikethrough',
        'color',
        'ol',
        'ul',
        'blockquote',
        'code',
        'table',
        'link',
        'indent',
        'outdent',
        'alignment'
    ];

    var editor = new Simditor({
        textarea: $('#body'),
        placeholder: '内容不能为空',
        toolbar: toolbar
    });

}