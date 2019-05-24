function submit_form() {
    document.querySelectorAll('form.delete').forEach((el) => {
        el.addEventListener('submit', (event) => {
            event.preventDefault();
            let form = event.target;
            let data = new FormData();
            data.append('csrfmiddlewaretoken', form.querySelector('input[name=csrfmiddlewaretoken]').value);
            data.append('substitute', form.querySelector('input[name=substitute]').value);
            data.append('substituted', form.querySelector('input[name=substituted]').value);
            let xhr = new XMLHttpRequest();
            xhr.open('POST', form.getAttribute('action'));
            xhr.addEventListener('load', () => {
                const answer = JSON.parse(xhr.responseText);
                if (xhr.status == 200) {
                    let status = answer.status;
                    if (status == 'success') {
                        alert('Favori supprimé !');
                        let favorite_div = form.closest('div.favorite');
                        favorite_div.remove();
                    }
                    else {
                        alert('Une erreur est survenue lors de la suppression');
                    }
                }
                else {
                    alert('Une erreur est survenue lors de la suppression');
                }
            });
            xhr.send(data);
        });
    });
}

window.onload = submit_form();
