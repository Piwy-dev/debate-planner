/**
 * @function setLanguage
 * @description Sets the language based on the user's preference
 */
export function setLanguage() {
    const selectedLanguage = localStorage.getItem('language');

    if (selectedLanguage) {
        const languageSwitcher = document.getElementById('languageSwitcher');
        languageSwitcher.value = selectedLanguage;
    }

    const languageSwitcher = document.getElementById('languageSwitcher');

    languageSwitcher.addEventListener('change', function() {
        const newLanguage = this.value;
        const currentPath = window.location.pathname;
        const newPath = currentPath.replace(/^\/[a-z]{2}\//, '/' + newLanguage + '/');
        window.location.href = newPath;
    });
};