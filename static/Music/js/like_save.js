function getCsrf() {
    let cookies = document.cookie.split(';')
    for(let i of cookies){
        let key = i.split('=')
        if(key[0] === 'csrftoken' ) {return key[1]}
    }
}

function  csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", getCsrf());
        }
    }
})

$(document).ready(function () {
    $('#add-favorite').click((e) => {
        e.preventDefault()
        $.post('{% url "music:like" %}', {
            id:$(this).data('id'),
            action:$(this).data('action'),
        },function (data) {
            if(data['status'] === 'add'){
                $('#add-favorite').css('color', 'red');
                $('#add-favorite').data('action', 'unlike');
            }else if(data['status'] === 'remove'){
                $('#add-favorite').css('color', 'none');
                $('#add-favorite').data('action', 'like');
            }else {

            }
        })
    })
})


/*
<script>
    let element = document.querySelector('#past-7')
    let csrf = Cookies.get('csrftoken')
    element.addEventListener('click', e => {
        e.preventDefault()
        let requestOptions = {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
                'title': 'pass7'
            },
        };
        fetch('{% url "account:profile" %}', requestOptions)
    })

</script>*/
