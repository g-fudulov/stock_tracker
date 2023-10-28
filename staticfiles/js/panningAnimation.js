const sectionElement = document.querySelector('section.middle-hero.wrapper');
const imageTrack = document.getElementById('image-track')

if (sectionElement !== null || imageTrack !== null) {

    sectionElement.onmousedown = e => {
        sectionElement.dataset.mouseDownAt = e.clientX;
    }

    sectionElement.onmousemove = e => {
        if (window.innerWidth < 1800) {return;}
        if (sectionElement.dataset.mouseDownAt === "0") {return}


        let mouseDelta = parseFloat(sectionElement.dataset.mouseDownAt) - e.clientX;
        const maxDelta = window.innerWidth / 2;
        const percentage = (mouseDelta / maxDelta) * -100;
        let nextPercentage = parseFloat(sectionElement.dataset.prevPercentage) + percentage;
        nextPercentage = Math.min(nextPercentage, 1);

        let maxValue = -300
        if (window.innerWidth <=1900) {
            let diff = 1900 - window.innerWidth;
            let toSub = (diff / 300) * 35
            maxValue -= toSub
        }

        nextPercentage = Math.max(nextPercentage, maxValue);

        sectionElement.dataset.percentage = nextPercentage;
        imageTrack.animate(
            {transform: `translate(${nextPercentage}%, 0%)`},
            {duration: 1200, fill: "forwards"}
        );
    }

    sectionElement.onmouseup = e => {
        sectionElement.dataset.mouseDownAt = "0";
        sectionElement.dataset.prevPercentage = sectionElement.dataset.percentage;
    }
}
