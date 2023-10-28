const menuBtn = document.getElementById("mobile-menu");
const navMenu = document.getElementById("menu-nav");

menuBtn.addEventListener('click', () => {
    if (navMenu.classList.contains('showing')) {
        hideMobileMenu()
    } else  {
        showMobileMenu()
    }
});

function showMobileMenu() {
    navMenu.classList.add('showing')
    navMenu.animate(
        [
            { transform: 'translateX(50%)', opacity: '0' },
            { transform: 'translateX(0%)', opacity: '1' }
        ],
        {
            duration: 300, iterations: 1
        }
    );
}

function hideMobileMenu() {
    navMenu.classList.remove('showing')
    navMenu.animate(
        [
            { transform: 'translateX(0%)', opacity: '1' },
            { transform: 'translateX(50%)', opacity: '0' }
        ],
        {
            duration: 300, iterations: 1
        }
    );
}