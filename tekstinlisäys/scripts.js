function lisaaTeksti() {
    var alue = document.getElementById('tekstialue');
    var uusiTeksti = document.createElement('p');
    uusiTeksti.textContent = 'Uusi kappale lisätty kello' + new Date().toLocaleTimeString();
    uusiTeksti.style.color = 'rgb('+ Math.floor(Math.random() * 256) + ','
        + Math.floor(Math.random() * 256) + ','
        + Math.floor(Math.random() * 256) + ')'; 
    uusiTeksti.style.fontSize = (Math.random() * 20 + 10) + 'px';
    alue.appendChild(uusiTeksti);
}