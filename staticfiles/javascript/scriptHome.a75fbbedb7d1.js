const bubbles = document.querySelectorAll('.bubble');

bubbles.forEach((bubble) => { const animation = bubble.style.animation; const delay = animation.split(',')[1].split(' ')[1]; setTimeout(() => { bubble.style.animation = ''; }, parseInt(delay) * 1000); });