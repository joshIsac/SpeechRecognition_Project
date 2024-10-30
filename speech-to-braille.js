document.getElementById('speech-to-braille-btn').addEventListener('click', () => {
    // Functionality for Speech-to-Braille
    fetch('/speech-to-braille')
        .then(response => response.text())
        .then(data => {
            document.getElementById('braille-output').innerText = `Braille: ${data}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
});

document.getElementById('braille-to-speech-btn').addEventListener('click', () => {
    const brailleInput = document.getElementById('braille-input').value;
    fetch('/braille-to-speech', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ braille: brailleInput }),
    })
    .then(response => response.blob())
    .then(data => {
        const audioUrl = URL.createObjectURL(data);
        const audio = new Audio(audioUrl);
        audio.play();
    })
    .catch(error => {
        console.error('Error:', error);
    });
});
