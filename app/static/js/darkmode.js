/**
 * @function setDarkmode
 * @description Sets the dark mode based on the user's preference
 */
export function setDarkmode() {
    const darkModeSwitcher = document.getElementById('dark-mode-switcher');
    const isDarkModeEnabled = localStorage.getItem('darkModeEnabled') === 'true';

    // Get the elements that need to be styled
    const bottom = document.querySelector('.bottom');
    const bottomComponents = document.querySelectorAll('.bottom-component');
    const languageSwitcher = document.getElementById('languageSwitcher');
    const top = document.querySelector('.top');
    const topButtons = document.querySelectorAll('.top-button');
    const topTitle = document.querySelector('.top-title');

    // Set the initial state of the dark mode
    if (isDarkModeEnabled) {
        darkModeSwitcher.querySelector('input').checked = true;

        bottom.classList.add('dark');
        bottomComponents.forEach(component => {
            component.classList.add('dark')
        });
        languageSwitcher.classList.add('dark');
        top.classList.add('dark');
        topButtons.forEach(button => {
            button.classList.add('dark')
        });
        topTitle.classList.add('dark');
    };

    darkModeSwitcher.addEventListener('change', function () {
        const isChecked = darkModeSwitcher.querySelector('input').checked;

        bottom.classList.toggle('dark', isChecked);
        bottomComponents.forEach(component => {
            component.classList.toggle('dark', isChecked)
        });
        languageSwitcher.classList.toggle('dark', isChecked);
        top.classList.toggle('dark', isChecked);
        topButtons.forEach(button => {
            button.classList.toggle('dark', isChecked)
        });
        topTitle.classList.toggle('dark', isChecked);
  
        // Store the state of the dark mode in the localStorage object
        localStorage.setItem('darkModeEnabled', isChecked);
    });
};