function submit_form() {
    let forms = document.querySelectorAll('form.save');
    Array.from(forms).forEach(form => {
        form.addEventListener('submit', (event) => {
            event.preventDefault();
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
                        alert('Favori sauvegardé !');
                        let button = form.querySelector('input.btn');
                        button.disabled = true;
                        button.classList.add('btn-success');
                        button.value = 'Sauvegardé';
                    }
                    else {
                        alert('Une erreur est survenue lors de la sauvegarde');
                    }
                }
                else {
                    alert('Une erreur est survenue lors de la sauvegarde');
                }
            });
            xhr.send(data);
        });
    });
}
window.onload = submit_form();
