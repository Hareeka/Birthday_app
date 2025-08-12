const threshold = 0.15;
const duration = 3000;

let context = new AudioContext();
navigator.mediaDevices.getUserMedia({ audio: true })
    .then(stream => {
        let mic = context.createMediaStreamSource(stream);
        let analyser = context.createAnalyser();
        mic.connect(analyser);
        analyser.fftSize = 512;

        const data = new Uint8Array(analyser.frequencyBinCount);

        const detect = () => {
            analyser.getByteFrequencyData(data);
            let volume = data.reduce((a, b) => a + b) / data.length;
            if (volume > threshold * 100) {
                document.getElementById("blowResult").innerText = "Candles blown!";
                const img = document.getElementById("cakeImage");
                img.src = "assets/cake_blown.gif";
            } else {
                setTimeout(detect, 200);
            }
        };

        detect();
    });